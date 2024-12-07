import dask
import os
import numpy as np 
import cupy as cu
import dask.array as da
import  slap2_utils.datafile as slap2
import zarr
import dask_image.imread
from slap2_utils.subclasses.metadata import MetaData
import tifffile 
from ScanImageTiffReader import ScanImageTiffReader
from cellpose import models
import torch
print(torch.__version__)
def genSomaROI(path):
    path = path[0]
    print(f"Processing Image: {path}")

    metadata = MetaData(path[:-4]+'.meta')
    duration = metadata.acqDuration_s
    xdim, ydim = metadata.AcquisitionContainer.ParsePlan['rasterSizeXY'][0][0], metadata.AcquisitionContainer.ParsePlan['rasterSizeXY'][1][0]
    linesPerFrame = metadata.AcquisitionContainer.ParsePlan['linesPerFrame']
    lineRate = metadata.AcquisitionContainer.ParsePlan['lineRateHz']
    linesPerCycle = metadata.AcquisitionContainer.ParsePlan['linesPerCycle']
    frameRate = (lineRate[0]/ydim)[0]
    frameNumber = int(frameRate*duration)
    cyclePeriod_s = linesPerCycle / lineRate


    store = tifffile.imread(path, aszarr=True)
    imagedata = da.from_zarr(store)
    imagedata = imagedata.rechunk((frameNumber, ydim, xdim))
    avgStack = np.zeros((1, int(imagedata.shape[0]/frameNumber), imagedata.shape[1], imagedata.shape[2]))

    @dask.delayed
    def returnSlice(_block):
        return cu.mean(_block, axis=0)
    results = []
    for _block in imagedata.blocks:
        results.append(returnSlice(_block))



    avgStack = np.array(dask.compute(results))
    
    tifffile.imwrite(os.path.split(path)[0] +'/averageGPU_' + os.path.basename(path), avgStack)
    print('Stack Average Complete... Saved to '+ os.path.split(path)[0])
    
    model = models.Cellpose(model_type='cyto')
    channels = [[0,0]]
    masks, flows, styles, diams = model.eval(data[0,0,:,:], diameter=None, channels=channels)


    
    return mask

if __name__ == "__main__":
    pass
