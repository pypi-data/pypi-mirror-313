import sys
import apoc
import os
import time

import numpy as np
import pyclesperanto_prototype as cle
import napari
import random

from skimage.io import imread
from skimage.morphology import skeletonize,binary_closing, skeletonize_3d,dilation, erosion, remove_small_objects, disk, square
from skimage import filters

from scipy.io import savemat
from skimage.measure import label, regionprops
from scipy import ndimage
from scipy.ndimage import center_of_mass

from segment_anything import sam_model_registry, SamPredictor



def masked_sliding_window_inference(image, mask, segmenter, window_size=(256, 256), stride=128, ):
    """Perform masked sliding window inference on an image.

    This function applies a sliding window over the image, using the given mask to limit the
    area of inference and a segmenter model to predict within each window.

    Parameters
    ----------
    image : array
        The input image array with shape (z, y, x).
    mask : array
        A binary mask indicating the regions to include in the inference.
    segmenter : object
        The segmentation model to apply on each patch.
    window_size : tuple of int, optional
        The size of the sliding window (default is (256, 256)).
    stride : int, optional
        The stride of the sliding window (default is 128).

    Returns
    -------
    output : array
        The segmented output image.
    """
    
    h, w = image.shape[1:]
    output = np.zeros((image.shape[0], image.shape[1], image.shape[2]))
    for y in range(0, h-window_size[1]+1, stride):
        for x in range(0, w-window_size[0]+1, stride):
            if np.max(mask[y:y+window_size[1], x:x+window_size[0]]) == True:
                for z in range(0, output.shape[0]-1, 1):

                    patch = image[z, y:y+window_size[1], x:x+window_size[0]]
                    patch_output = segmenter.predict(patch)

                    # Handle overlap by averaging or other strategies
                    output[z, y:y+window_size[1], x:x+window_size[0]] = patch_output
    return output

def find_skeleton_3Dpoints(skelly_image):
    """Identify end points and junction points in a 3D skeleton image.

    This function finds end points and junction points in a binary skeletonized image.

    Parameters
    ----------
    skelly_image : array
        A 3D binary skeleton image.

    Returns
    -------
    end_points : list of tuple
        List of coordinates for end points.
    y_points : list of tuple
        List of coordinates for junction points.
    """

    # Force binary image
    skelly_image[skelly_image>0]=1

    points = np.where(skelly_image==1)
    end_points = []
    y_points = []

    for point in range(len(points[0])):
        z = points[0][point]
        x = points[1][point]
        y = points[2][point]

        window=skelly_image[z-1:z+2, x-1:x+2, y-1:y+2]
        if np.sum(window)<=2:
            end_points.append((z,x,y))
        if np.sum(window)>=4:
            y_points.append((z,x,y))
    return end_points, y_points


def find_bounding_box(data, label):
    """Find the bounding box of a specific label in a 2D array.

    This function calculates the bounding box coordinates of a given label in a 2D array.

    Parameters
    ----------
    data : array
        The input 2D array.
    label : int
        The label for which to find the bounding box.

    Returns
    -------
    min_y : int
        Minimum y-coordinate of the bounding box.
    min_x : int
        Minimum x-coordinate of the bounding box.
    max_y : int
        Maximum y-coordinate of the bounding box.
    max_x : int
        Maximum x-coordinate of the bounding box.
    """
    rows, cols = np.where(data == label)

    if rows.size == 0 or cols.size == 0:
        return None, None, None, None
    
    min_y, max_y = np.min(rows), np.max(rows)
    min_x, max_x = np.min(cols), np.max(cols)

    return min_y, min_x, max_y, max_x

def cutlabel(array, label):
    """Recursively split labels in an array based on certain conditions.

    This function modifies the input array by splitting the regions of a given label.

    Parameters
    ----------
    array : array
        The input 2D array with labels.
    label : int
        The label to be split.

    Returns
    -------
    array : array
        The modified array with split labels.
    """
    labelMod = random.randint(3, 10)
    
    min_y, min_x, max_y, max_x = find_bounding_box(array, label)
    if min_y == None:
        return 
    elif ((max_y-min_y) <= 30) or ((max_x - min_x) >= 2*(max_y-min_y)):
        return 
    elif (max_x - min_x) < 2*(max_y-min_y):
        halfway = int((max_y - min_y)/2 + min_y)
        mask = (array == label)
        array[:halfway, :][mask[:halfway, :]] = label + labelMod
    else:
        return

    array1 = cutlabel(array, label+labelMod)
    array2 = cutlabel(array, label)

    if array1 is not None:
        array[:halfway, :][mask[:halfway, :]] = array1[:halfway, :][mask[:halfway, :]]
    
    if array2 is not None:
        array[halfway:, :][mask[halfway:, :]]= array2[halfway:, :][mask[halfway:, :]]
    
    return array

def returnSomaRoi(maskSAM, RFPix):
    """Extract the region of interest (ROI) for the soma based on SAM and RFPix masks.

    This function calculates the center of mass of the ROI and extracts the corresponding region.

    Parameters
    ----------
    maskSAM : array
        Binary mask from SAM.
    RFPix : array
        The mask representing the region of interest in RFPix.

    Returns
    -------
    somaLabel : array
        The binary mask of the extracted soma ROI.
    """
    RFPix = RFPix.copy()
    RFPix[RFPix > 0] = 1
    maskSAM[maskSAM > 0] = 1
    for z in range(RFPix.shape[0]):
        RFPix[z,:,:] = RFPix[z,:,:] * maskSAM
    _com = center_of_mass(RFPix)
    somaLabel = np.zeros_like(RFPix)
    somaLabel[int(_com[0]), :, : ] = RFPix[int(_com[0]), :, : ]
    return somaLabel.astype(int)

def genDendriticRoi(imagepath):
    """Generate dendritic ROIs using a segmentation pipeline.

    This function performs segmentation on a reference stack image to identify and label dendritic ROIs.

    Parameters
    ----------
    imagepath : str
        Path to the input image file.

    Returns
    -------
    None
    """
    cl_filename = "test_object_segmenter_from_folders.cl"

    # Load Reference Stack to segment
    data1 = imread(imagepath)
    img_slice= data1[0,:,:,:]

    # Load Random Forest Pixel Classifier
    segmenter = apoc.PixelClassifier(opencl_filename=cl_filename)

    # Load up SAM to help select only neuron of interest
    sam_checkpoint = "checkpoints/sam_vit_l_0b3195.pth"
    model_type = "vit_l"
    device = "cuda"

    sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
    sam.to(device=device)
    predictor = SamPredictor(sam)

    # Make 2D projection for SAM has to be RGB image
    projection = np.max(img_slice.astype('uint8'), axis=0)

    projectionRGB = np.array([projection.astype('uint8'), projection.astype('uint8'), projection.astype('uint8')])
    projectionRGB = np.moveaxis(projectionRGB, 0, 2)
    predictor.set_image(projectionRGB)

    # provide box for SAM
    with napari.gui_qt():
        boxSelector = napari.Viewer()
        boxSelector.add_image(projection, gamma=.35)
        boxSelector.add_shapes()


    neuron_box = boxSelector.layers[1].data[0].astype(int)
    neuron_box = [np.min(neuron_box[:, 1]),np.min(neuron_box[:, 0]),  np.max(neuron_box[:, 1]), np.max(neuron_box[:, 0])] #np.concatenate([input_box[0, :], input_box[2, :]])
    neuron_box = np.array(neuron_box)


    soma_box = boxSelector.layers[1].data[1].astype(int)
    soma_box = [np.min(soma_box[:, 1]),np.min(soma_box[:, 0]),  np.max(soma_box[:, 1]), np.max(soma_box[:, 0])] #np.concatenate([input_box[0, :], input_box[2, :]])
    soma_box = np.array(soma_box)


    # Generate neuron mask with SAM
    masks, _, _ = predictor.predict(
                                    point_coords=None,
                                    point_labels=None,
                                    box=neuron_box,
                                    multimask_output=False)
    


 

    # Use the Random Forest
    labels = masked_sliding_window_inference(img_slice, masks[0], segmenter)
    labels[:, masks[0]==False] = 0

    soma_masks, _, _ = predictor.predict(
            point_coords=None,
            point_labels=None,
            box=soma_box,
            multimask_output=False,
        )
    


    soma = returnSomaRoi(soma_masks[0], labels)

    # Prepare the neuron labels for ROI creation
    neuron = labels.copy()
    neuron[neuron!=2] = 0
    neuron[neuron==2] = 1
    neuron = ndimage.binary_fill_holes(neuron)
    neuron = remove_small_objects(neuron, 500, connectivity=10)
    neuron = filters.gaussian(neuron, .5)
    neuron[neuron >0] = 1
    neuron = neuron.astype(int)
    footprint = disk(3)

    # Preslice errosion to tighten things up
    for i in range(neuron.shape[0]):
        neuron[i, :,:] = erosion(neuron[i,:,:],footprint)
    skel=0
    skel = skeletonize_3d(neuron)
    
    # Find Junctions
    ends, junctions = find_skeleton_3Dpoints(skel)

    # Use the branch nodes to break up the skeleton into branches
    for _branchNode in junctions:
        skel[_branchNode[0], _branchNode[1], _branchNode[2]] = 0

    line_fragments = label(skel)
    lineInts = list(np.unique(line_fragments))
    lineInts.pop(0)
    SLAP2ROIs = np.zeros_like(neuron)
    SLAP2ROIs2 = np.zeros_like(neuron)

    roi=1
    footprint = square(15)

    for z in range(skel.shape[0]):
        line_fragments = label(skel[z, :, :])
        roiData = dilation(line_fragments, footprint)
        roiData = roiData * neuron[z, :, : ]
        SLAP2ROIs[z, :, :], _ = ndimage.label(roiData)
        
        for _label in list(np.unique(SLAP2ROIs[z, :, : ]))[1:]:
            modified_slice = cutlabel(SLAP2ROIs[z, :, :].astype(int), _label)
            if modified_slice is not None:
                SLAP2ROIs2[z, :, : ] += modified_slice.astype(int)

    SLAP2ROIs2[soma==1]=1

    #abeled_array, num_features = ndimage.label(SLAP2ROIs)
    # Specify full connectivity for 3D (26-connectivity)
    #structure = np.zeros((3, 3, 3), dtype=int)
    #structure[1, :, :] = 1

    # Apply connected component labeling with the specified structure
    #labeled_array, num_features = ndimage.label(SLAP2ROIs, structure=structure)

    newFilePath = os.path.join(os.path.split(imagepath)[0], '_autoROI_'+os.path.basename(imagepath))
    np.save(newFilePath[:-4]+'.npy', SLAP2ROIs2)
    savemat(newFilePath[:-4]+'.mat', {'roi':SLAP2ROIs2})



def main():
    # Loading bunch of stuff

    _imgpath = sys.argv[1]

    
    genDendriticRoi(_imgpath)

if __name__ == "__main__":
    main()