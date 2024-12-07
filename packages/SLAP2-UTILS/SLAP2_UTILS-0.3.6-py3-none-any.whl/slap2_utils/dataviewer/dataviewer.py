from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import QCoreApplication
from skimage.draw import polygon_perimeter

import fastplotlib as fpl
import numpy as np

from ..datafile import DataFile
from ..utils.trace import Trace
import copy




def viewROItraces(ch=1, zIdz=1, windowWidth_lines=10, expectedWindowWidth_lines = 100):
    # Values or trace
    mask = np.full((800, 1280), True, dtype=bool)
    rasterPixels = mask
    integrationPixels = mask
    
    # QT file picker    
    """app = QtWidgets.QApplication([])
    fileName = QtWidgets.QFileDialog.getOpenFileName(None,
        QCoreApplication.translate("MainWindow", "Open Data File"),
        QCoreApplication.translate("MainWindow", "Data Files (*.dat)"))[0]"""
    
    fileName = 'D:\\Simulated_1_ROI_Scan\\acquisition_20240205_105010_DMD1.dat'
    # Load Data
    experiment = DataFile(fileName)
    rois2D = return2Droi(experiment)

    plot = fpl.Plot(canvas="qt")
    plot.add_image(rois2D)
    plot.camera.local.scale *= -1
    plot.show()
    plot.canvas.resize(*rois2D.shape[:2])


    def autoscale(ev):
        if ev.key == "r":
            plot.auto_scale()


    # useful if you pan/zoom away from the image
    plot.renderer.add_event_handler(autoscale, "key_down")

    # execute Qt app
    app.exec()



def return2Droi(datafile):
    img = np.zeros((800, 1280), dtype=np.uint8)

    for _roi in range(len(datafile.metaData.AcquisitionContainer.ROIs)):
        roi_shape = datafile.metaData.AcquisitionContainer.ROIs[_roi].shapeData
        
        rr, cc = polygon_perimeter(roi_shape[0,:],
                                    roi_shape[1,:],
                                    shape=img.shape, clip=True)

        img[rr, cc] = _roi+1

    return(img)

def returnTraces(datafile):
    zIdx = 1
    chIdx = 1
    hTrace = Trace(hDataFile,zIdx,chIdx)


    from skimage.draw import polygon_perimeter

    roi_shape = hDataFile.metaData.AcquisitionContainer.ROIs[0].shapeData

    img = np.zeros((800, 1280), dtype=np.uint8)

    rr, cc = polygon_perimeter(roi_shape[0,:], roi_shape[1,:],

                            shape=img.shape, clip=True)

    img[rr, cc] = 1

    plt.imshow(img)

    #rasterPixels = pixelMask;
    #integrationPixels = pixelMask;

    pixelMask=np.full((800, 1280), False)
    pixelMask[img==1] = True

    rasterPixels = np.full((800, 1280), False)
    integrationPixels = pixelMask;

    hTrace.setPixelIdxs(rasterPixels, integrationPixels);
    #windowWidth_lines = 10;
    #expectedWindowWidth_lines = 100;
    #trace = hTrace.process(windowWidth_lines,expectedWindowWidth_lines);
    _trace, _, _, _ = hTrace.process(10, 100)
    print(_trace)
    plt.plot(_trace)


    viewROItraces()




# Qt app MUST be instantiated before creating any fpl objects, or any other Qt objects
app = QtWidgets.QApplication([])

# QT file picker    
fileName = QtWidgets.QFileDialog.getOpenFileName(None,
    QCoreApplication.translate("MainWindow", "Open Data File"),
    QCoreApplication.translate("MainWindow", "Data Files (.dat)"))[0]

exp1 = DataFile(fileName)
traceObjs = []
lineData = []
for idx, _ROI in enumerate(exp1.metaData.AcquisitionContainer.ROIs):
    zIdx = exp1.fastZs.index(_ROI.z)
    chIdx = 1 
    hTrace = Trace(exp1,zIdx,chIdx)

    windowWidth_lines = 5
    expectedWindowWidth_lines = 100
    roi_shape = _ROI.shapeData
    img = np.zeros((800, 1280), dtype=np.uint8)
    if roi_shape.shape[1] > 2:
        rr, cc = polygon_perimeter(roi_shape[0,:],
                                roi_shape[1,:],

                                shape=img.shape, clip=True)
    else:
        rr, cc = roi_shape[0, :].astype(int), roi_shape[1, :].astype(int)
    lineData.append((rr, cc))
    img[rr, cc] = 1
    mask = np.full((800, 1280), False, dtype=bool)
    mask[img==1]=True
    rasterPixels = np.full((800, 1280), False, dtype=bool)
    integrationPixels = mask

    hTrace.setPixelIdxs(rasterPixels,integrationPixels)
    traceObjs.append(hTrace)
    _trace, _, _, _ = hTrace.process(windowWidth_lines, expectedWindowWidth_lines)

# force qt canvas, wgpu will sometimes pick glfw by default even if Qt is present
plot = fpl.Plot(canvas="qt")
dmdCanvas = np.zeros((800, 1280))
plot.add_image(np.zeros((800, 1280)), name="ROI_1")
#plot.camera.local.scale *= -1


def update_frame(ix):
    ix = frame_slider.value()
    img = np.zeros((800, 1280), dtype=np.uint8)
    for idx, _ROI in enumerate(exp1.metaData.AcquisitionContainer.ROIs):
        if _ROI.z ==  exp1.fastZs[(z_slider.value())]:
            _traceData = traceObjs[idx]
            _rr, _cc = lineData[idx][0], lineData[idx][1]
            for _line , col in enumerate(list(np.unique(_cc))):
                if len(_traceData.TracePixels) > 1:
                    try:
                        _superPixVal = _traceData.TracePixels[_line-1].data[0][int(ix)]
                    
                        for _row in list(np.where(_cc==col)[0]):
                            img[_rr[_row], col] = _superPixVal
                    except:
                        print('Error')
                else:
                    print( len(_traceData.TracePixels))

    plot["ROI_1"].data = img


# create a QMainWindow, set the plot canvas as the main widget
# The canvas does not have to be in a QMainWindow and it does
# not have to be the central widget, it will work like any QWidget
main_window = QtWidgets.QMainWindow()
#main_window.setCentralWidget(plot.canvas)

# Create a QSlider for updating frames
frame_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
#print(hTrace.TracePixels[0].data[0][:].shape[0]-1)
frame_slider.setMaximum(344)#hTrace.TracePixels[0].data[0][:].shape[0]-1)
frame_slider.setMinimum(0)
frame_slider.valueChanged.connect(update_frame)
Z_Mask_GLOBAL = exp1.fastZs[0]

def Z_Mask(zIdxCallBack, zz=Z_Mask_GLOBAL):
    print(zz)
    print(z_slider.value())
    zz = exp1.fastZs[(z_slider.value())]
    print(zz)
    return zz

z_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
z_slider.setMaximum(len(exp1.fastZs)-1)
z_slider.setMinimum(0)

z_slider.valueChanged.connect(update_frame)
# put frame_slider in a dock
dock = QtWidgets.QDockWidget()
dock.setWidget(frame_slider)
dock2 = QtWidgets.QDockWidget()
dock2.setWidget(z_slider)

# put the dock in the main window
main_window.addDockWidget(
    QtCore.Qt.DockWidgetArea.BottomDockWidgetArea,
    dock
)
main_window.addDockWidget(
    QtCore.Qt.DockWidgetArea.BottomDockWidgetArea,
    dock2
)
# calling plot.show() is required to start the rendering loop
plot.show()

# set window size from width and height of video
main_window.resize(dmdCanvas.shape[0], dmdCanvas.shape[1])

# show the main window
main_window.show()

# execute Qt app
app.exec()