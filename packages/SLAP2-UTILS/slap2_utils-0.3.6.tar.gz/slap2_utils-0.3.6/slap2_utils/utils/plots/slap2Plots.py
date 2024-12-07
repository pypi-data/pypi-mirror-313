import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm
from ..roi_utils import roiImg

def roiOverlay(datafile, refimg, roiIdx, display=True):
    """Plot contours of an SLAP2 ROI over a reference image with color-coded super pixels.

    This function plots the contours of specified ROIs over a reference image. The super pixels are color-coded.

    Parameters
    ----------
    datafile : SLAP2_Utils Datafile Object
        The datafile containing metadata and header information.
    refimg : array
        Reference image, can be 3D (t, x, y) or 2D (x, y).
    roiIdx : int or list
        Integer or list of integers for the ROI indices.
    display : bool, optional
        If True, display the plot. Default is True.

    Returns
    -------
    ax : matplotlib.axes.Axes
        Matplotlib axes object with the plotted contours.
    """
    assert type(roiIdx) == int or type(roiIdx) == list
    if type(roiIdx) == int:
        roiIdx = [roiIdx]
    
    if len(refimg.shape) == 3:
        refimg = np.mean(refimg, axis=0)
    
    fig, ax = plt.subplots(1,figsize=(24,16), dpi=100)
    ax.imshow(refimg, cmap='Greys_r', vmax=np.max(refimg)*.45)
    
    for _roiIdx in roiIdx:
        img = roiImg(datafile, _roiIdx)
        _roiColor = mpl.colors.rgb2hex(cm.Spectral(_roiIdx/len(datafile.metaData.AcquisitionContainer.ROIs)))
        ax.contour(img, colors=_roiColor)
        
    ax.set_xticks([],[])
    ax.set_yticks([],[])
    if display:
        plt.show()
    return ax 

def roiOverlaySuperPix(datafile, refimg, roiIdx, display=True):
    """Plot pixel-wise traces of fluorescence changes over time.

    This function plots the traces of fluorescence changes for each super pixel over a specified time period.

    Parameters
    ----------
    dffData : array
        The delta F/F data of super pixels.
    hz : float
        Sampling rate in Hertz.
    start : int
        Start frame index.
    end : int
        End frame index.

    Returns
    -------
    ax : matplotlib.axes.Axes
        Matplotlib axes object with the plotted contours
    """
    assert type(roiIdx) == int
    if type(roiIdx) == int:
        roiIdx = [roiIdx]
    
    if len(refimg.shape) == 3:
        refimg = np.mean(refimg, axis=0)
    
    fig, ax = plt.subplots(1,figsize=(24,16), dpi=100)
    
    ax.imshow(refimg, cmap='Greys_r', vmax=np.max(refimg)*.45)
    
    for _roiIdx in roiIdx:
        img = roiImg(datafile, _roiIdx)
        _roiColor = mpl.colors.rgb2hex(cm.Spectral(_roiIdx/len(datafile.metaData.AcquisitionContainer.ROIs)))
        ax.contour(img, colors=_roiColor)

    yIndex = list(np.unique(np.where(img==1)[1]))
    xIndex = list(np.unique(np.where(img==1)[0]))
    barRow = (np.max(xIndex)+5, np.max(xIndex)+15)

    superPixBar = np.zeros((img.shape[0], img.shape[1], 3))
    for i, col in enumerate( range(4, len(yIndex)-4, 1)):
        superPixBar[barRow[0]:barRow[1], yIndex[col], :] = cm.Spectral(i/(len(yIndex)-10))[:3]
        
    all_channels_zero = np.all(superPixBar == 0, axis=-1)
    mask_rgb = np.repeat(all_channels_zero[:, :, np.newaxis], 3, axis=2)
    _maskedBar = np.ma.masked_where(mask_rgb, superPixBar)
    _maskedBar = superPixBar.copy()
    _maskedBar[all_channels_zero, :] = [0, 0, 0]  # Set to black or make transparent

   
    alpha = np.ones((800, 1280, 4))  # Create an RGBA for alpha
    alpha[all_channels_zero] = [0, 0, 0, 0]  # Make masked areas fully transparent
    _maskedBar = np.concatenate((_maskedBar, alpha[:, :, 3:]), axis=-1)                
    ax.imshow(_maskedBar)
    ax.set_xticks([],[])
    ax.set_yticks([],[])
    if display:
        plt.show()
    return ax

def plotPixTrace(dffData, hz, start, end):
    """Plot pixel-wise traces of fluorescence changes over time.

    This function plots the traces of fluorescence changes for each super pixel over a specified time period.

    Parameters
    ----------
    dffData : array
        The delta F/F data of super pixels.
    hz : float
        Sampling rate in Hertz.
    start : int
        Start frame index.
    end : int
        End frame index.

    Returns
    -------
    None
    """
    plt.figure(figsize=(24, 16))
    time = np.arange(0, int(end-start)/hz, 1/hz)
    for j in range(dffSuperPix.shape[0]):
        _traceColor = mpl.colors.rgb2hex(cm.Spectral(j/dffSuperPix.shape[0]))
        plt.plot(time, dffSuperPix[j, start:end]+(.15*j), color=_traceColor, alpha=.8, zorder=dffSuperPix.shape[0]-j+5)
    plt.show()