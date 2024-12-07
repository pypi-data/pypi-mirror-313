import numpy as np
import matplotlib.pyplot as plt
from skimage.draw import polygon_perimeter
 
from ..utils import trace
from ..utils import roi_utils


def returnAllTrace(datafile, chIdx=1,  zIdx=1, window=10, expectedWindowWidth=100):
    """Return a dictionary of traces for all ROIs in the datafile.

    This function iterates through all ROIs in the datafile metadata and processes traces for each ROI.

    Parameters
    ----------
    datafile : SLAP2_Utils Datafile Object
        The datafile containing metadata and header information.
    chIdx : int, optional
        Channel index (default is 1).
    zIdx : int, optional
        Z index (default is 1).
    window : int, optional
        Window size for processing the trace (default is 10).
    expectedWindowWidth : int, optional
        Expected window width for processing the trace (default is 100).

    Returns
    -------
    traces : dict
        Dictionary of traces where the key is the ROI index.
    """

    # Returns dictionary of traces. Key is ROI index.
    traces  = {}
    hTrace = trace.Trace(datafile, zIdx, chIdx)

    # Iterate through all ROIs in the datafile metadata
    for _roi in range(len(datafile.metaData.AcquisitionContainer.ROIs)):
 
        rasterPixels = np.full((int(datafile.header['dmdPixelsPerColumn']),
                                int(datafile.header['dmdPixelsPerRow'])),
                                False)
        integrationPixels = roi_utils.roiBoolean(datafile, _roi)

        # Set the pixels for the trace object
        hTrace.setPixelIdxs(rasterPixels, integrationPixels)
        
        # Process the trace and adjust the order
        _trace, _, _, _ = hTrace.process(window, expectedWindowWidth)
        hTrace.orderadjust()
        
        # Store the trace in the dictionary with the ROI index as the key
        traces[_roi] = _trace
    
    return traces

def cleanVolumeTrace(datafile, zId, rawTrace):
    """Clean the raw trace data by averaging over slices.

    This function extracts the slice index information and averages the raw trace data for the given zId.

    Parameters
    ----------
    datafile : SLAP2_Utils Datafile Object
        The datafile containing metadata and header information.
    zId : int
        Z index to be cleaned.
    rawTrace : array
        The raw trace data.

    Returns
    -------
    cleanTrace : array
        The cleaned trace data.
    """

    # Extract the slice index information from the datafile metadata
    sliceIdx = datafile.metaData.AcquisitionContainer.ParsePlan['acqParsePlan']['sliceIdx']
    dataIndex = []
    
    # Adjust zId for Python's 0-based indexing
    zId -= 1
    
    # Find the indices of slices that match the given zId
    for _idx, _sliceIdx in enumerate(sliceIdx):
        if _sliceIdx.shape[0] == 1:
            if zId in _sliceIdx:
                dataIndex.append(_idx)

    cleanTrace = []

    # Iterate through the raw trace in steps of the number of slices
    for x in range(0, rawTrace.shape[0], len(sliceIdx)):
        traceIdx = np.array(dataIndex) + x
        # Calculate the mean of the raw trace at the relevant indices
        cleanTrace.append(np.mean(rawTrace[np.array(dataIndex) + x]))
    
    return np.array(cleanTrace)

def returnVolumeTrace(datafile, roiIndex, chIdx=1):
    """Return volume traces for a given ROI.

    This function processes and cleans the volume trace data for a specified ROI.

    Parameters
    ----------
    datafile : SLAP2_Utils Datafile Object
        The datafile containing metadata and header information.
    roiIndex : int
        Index of the ROI.
    chIdx : int, optional
        Channel index (default is 1).

    Returns
    -------
    _trace1 : array
        The raw trace data.
    _trace : array
        The cleaned trace data.
    """

    # Get the ROI from the datafile metadata
    ROI = datafile.metaData.AcquisitionContainer.ROIs[roiIndex]
    
    # Find the z index corresponding to the ROI
    zIdx = datafile.fastZs.index(ROI.z)
       
    # Create boolean arrays of raster and  integration pixels
    rasterPixels = None
    integrationPixels = roi_utils.roiBoolean(datafile, roiIndex)
    
    # Initialize the trace object
    hTrace = trace.Trace(datafile, zIdx, chIdx)
    
    # Set the pixels for the trace object
    hTrace.setPixelIdxs(rasterPixels, integrationPixels)
    
    # Process the trace
    _rawTrace, _, _, _ = hTrace.process(1, 1)
   
    
    # Clean the volume trace
    _cleanTrace = cleanVolumeTrace(datafile, zIdx, _rawTrace)
    
    return _rawTrace, _cleanTrace



def superPixelTraces(datafile, roiIdx, zIdx=1, chIdx=1):
    """

    Args:
        datafile: SLAP2_Utils Datafile Object

        roiIdx: int 
            index value of roi in the roi list

        zIdx: Z-Plane Index

        chIdx: int
            Index of the channel being recorded

    Returns:
        _pixSignal: array
            An array of floats of a raw signal for each super pixel
    """

    traceObject = trace.Trace(datafile,zIdx,chIdx)
 
    integrationPixels = roi_utils.roiBoolean(datafile, roiIdx)
    rasterPixels      = np.full(integrationPixels.shape, False)

    traceObject.setPixelIdxs(rasterPixels, integrationPixels)
    for pix in traceObject.TracePixels:
        pix.load()

    traceObject.orderadjust()

    _pixSignal = np.zeros((traceObject.TracePixels[0].data[0].shape[0]*len(traceObject.TracePixels[0].data), len(traceObject.TracePixels)))
    for colIdx, pix in enumerate(traceObject.TracePixels):
        _pixSignal[:, colIdx] = np.array(pix.data).flatten('F')
    
    return _pixSignal