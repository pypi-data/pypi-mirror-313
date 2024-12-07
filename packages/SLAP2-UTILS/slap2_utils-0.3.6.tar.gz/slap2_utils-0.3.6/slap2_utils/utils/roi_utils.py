import numpy as np
import tifffile
import json

def roiImg(datafile, idx):
    """Return ROI coordinates as a 2D array.

    The function returns a 2D array where pixels belonging to the ROI are marked with 1, 
    and all other pixels are marked with 0.

    Parameters
    ----------
    datafile : SLAP2_Utils Datafile Object
        The datafile containing metadata and header information.
    idx : int
        Index value of the ROI in the ROI list.

    Returns
    -------
    img : array
        A 2D array with integers 0 or 1 indicating pixels belonging to the ROI.
    """


    roi_shape = datafile.metaData.AcquisitionContainer.ROIs[idx].shapeData
    img = np.zeros((int(datafile.header['dmdPixelsPerColumn']),
                     int(datafile.header['dmdPixelsPerRow'])), dtype=np.uint32)
    img[roi_shape[0].astype('int')-1,roi_shape[1].astype('int')-1] = 1
    return img



def roiBoolean(datafile, idx):
    """Return ROI coordinates as a 2D array of booleans.

    The function returns a 2D array where pixels belonging to the ROI are marked with True,
    and all other pixels are marked with False. This format is used in the trace function.

    Parameters
    ----------
    datafile : SLAP2_Utils Datafile Object
        The datafile containing metadata and header information.
    idx : int
        Index value of the ROI in the ROI list.

    Returns
    -------
    booleanPixels : array
        A 2D array with booleans indicating pixels belonging to the ROI.
    """
    roi_shape = datafile.metaData.AcquisitionContainer.ROIs[idx].shapeData
    booleanPixels=np.full((int(datafile.header['dmdPixelsPerColumn']),
                                int(datafile.header['dmdPixelsPerRow'])),
                                False)
    booleanPixels[roi_shape[0].astype('int')-1,roi_shape[1].astype('int')-1] = True   
    
    return booleanPixels

def roiLabels(datafile, refStackPath=None):
    """Return ROI labels as a 3D array with each plane representing a Z-stack.

    The function returns a 3D array where each plane represents a slice in a Z-stack, and labels indicate different ROIs. 
    If a reference stack is provided, the function can use it for generating ROI labels.

    Parameters
    ----------
    datafile : SLAP2_Utils Datafile Object
        The datafile containing metadata and ROI information.
    refstack : optional
        Reference stack to use for generating ROI labels. Default is None.

    Returns
    -------
    roiLabels : array
        A 3D array with each plane representing a Z-stack and labels indicating different ROIs.
    """
    if type(refStackPath)==type(None):
        roiLabels = np.zeros((len(datafile.fastZs),
                            int(datafile.header['dmdPixelsPerColumn']),
                            int(datafile.header['dmdPixelsPerRow'])))

        for lbl, roi in enumerate(datafile.metaData.AcquisitionContainer.ROIs):
            roi_shape = roi.shapeData
            z = roi.z
            plane = datafile.fastZs.index(roi.z)
            roiLabels[plane, :, :][roi_shape[0].astype('int')-1,roi_shape[1].astype('int')-1]= lbl+1
        roiLabels = roiLabels.astype(int)
        return  roiLabels
    else:
        try:
            _stackData = tifffile.tiffcomment(refStackPath)
            _stackInfo = json.loads(_stackData)
            zPosition = _stackInfo['zsAbsolute']
            
        except:
            print('Not a SLAP2 Ref Stack')
            return None
        roiLabels = np.zeros(_stackInfo['shape'][1:])
        for lbl, roi in enumerate(datafile.metaData.AcquisitionContainer.ROIs):
            roi_shape = roi.shapeData
            z = roi.z
            plane = zPosition.index(roi.z)
            roiLabels[plane, :, :][roi_shape[0].astype('int')-1,roi_shape[1].astype('int')-1]= lbl+1
            roiLabels = roiLabels.astype(int)
        return roiLabels

