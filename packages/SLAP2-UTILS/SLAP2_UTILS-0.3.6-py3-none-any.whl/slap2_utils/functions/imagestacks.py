import sys
import dask
import os
import numpy as np 
import cupy as cu
import dask.array as da
import numpy as np
import matplotlib.pyplot as plt
import zarr
import tifffile 
import json




# Functions for generating an image stack from slice data without loading the tiff file into memory
def averageStack(path):
    """Compute the average stack of a TIFF file using CPU.

    This function reads a multi-frame TIFF file, computes the average of each slice, 
    and saves the resulting average stack as a new TIFF file.

    Parameters
    ----------
    path : str
        Path to the input TIFF file.

    Returns
    -------
    newFilePath : str
        Path to the saved average stack TIFF file.
    """
    _data = tifffile.tiffcomment(path)
    _stackInfo = json.loads(_data)
    store = tifffile.imread(path, aszarr=True)
    frameNumber = _stackInfo['numZs']
    
    imagedata = da.from_zarr(store)
    imagedata = imagedata.rechunk((frameNumber, imagedata.shape[1], imagedata.shape[2]))
    avgStack = np.zeros((1, int(imagedata.shape[0]/frameNumber), imagedata.shape[1], imagedata.shape[2]))


    store = tifffile.imread(path, aszarr=True)
    imagedata = da.from_zarr(store)
    framePerSlice = int(imagedata.shape[0]/frameNumber)

    imagedata = imagedata.rechunk((framePerSlice, imagedata.shape[1], imagedata.shape[2]))
    avgStack = np.zeros((1, frameNumber, imagedata.shape[1], imagedata.shape[2]))

    @dask.delayed
    def returnSlice(_block):
        return np.mean(_block, axis=0)
    results = []
    for _block in imagedata.blocks:
        results.append(returnSlice(_block))

    avgStack = np.array(dask.compute(results))
    newFilePath = os.path.join(os.path.split(path)[0], 'averageCPU_'+os.path.basename(path))
    tifffile.imwrite(newFilePath, avgStack, metadata=_stackInfo)

def averageStackGPU(path):
    """Compute the average stack of a TIFF file using GPU.

    This function reads a multi-frame TIFF file, computes the average of each slice using GPU, 
    and saves the resulting average stack as a new TIFF file.

    Parameters
    ----------
    path : str
        Path to the input TIFF file.

    Returns
    -------
    newFilePath : str
        Path to the saved average stack TIFF file.
    """
    _data = tifffile.tiffcomment(path)
    _stackInfo = json.loads(_data)
    store = tifffile.imread(path, aszarr=True)
    frameNumber = _stackInfo['numZs']
    
    imagedata = da.from_zarr(store)
    framePerSlice = int(imagedata.shape[0]/frameNumber)

    imagedata = imagedata.rechunk((framePerSlice, imagedata.shape[1], imagedata.shape[2]))
    avgStack = np.zeros((1, frameNumber, imagedata.shape[1], imagedata.shape[2]))


    @dask.delayed
    def returnSlice(_block):
        return cu.mean(_block, axis=0)
    results = []
    for _block in imagedata.blocks:
        results.append(returnSlice(_block))

    avgStack = np.array(dask.compute(results))
    newFilePath = os.path.join(os.path.split(path)[0], 'averageGPU_'+os.path.basename(path))
    tifffile.imwrite(newFilePath, avgStack, metadata=_stackInfo)
    return newFilePath

def main():
    if len(sys.argv)<2:
        print('No path to tif file given')
        sys.exit(1)
    tifPath = sys.argv[1]
    averageStackGPU(tifPath)

if __name__ == "__main__":
    main()