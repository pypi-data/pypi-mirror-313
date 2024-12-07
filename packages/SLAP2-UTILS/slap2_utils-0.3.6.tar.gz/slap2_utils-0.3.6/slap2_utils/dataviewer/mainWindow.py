from vispy import app
app.use_app('pyqt6')
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QGroupBox, QWidget, QFileDialog, QLabel, QHBoxLayout, QLineEdit
from PyQt6.QtCore import Qt
import sys
import os

from pixelTraces import tracePixelSelector
from roiTraces import roiSelector
from roiPlot import roiInspector
 



class FileSelector(QWidget):
    def __init__(self, label_text, file_filter):
        super().__init__()
        self.layout = QHBoxLayout()
        self.label = QLabel(label_text)
        self.button = QPushButton("Browse")
        self.file_filter = file_filter
        self.button.clicked.connect(self.browse_file)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        self.filepath = 'No file selected'

    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select File", "",  self.file_filter)
        if file_name:
            self.label.setText(os.path.basename(file_name))
        self.filepath = file_name
    def get_selected_file(self):
        return self.filepath

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Slap2 Data Viewer")

        self.DataFilePath = FileSelector("No file selected (Binary)", "SLAP2 Binary (*.dat)")
        self.StackPath = FileSelector("No file selected (Stack)", "Stack (*.tif)")
        self.StimPath = FileSelector("No Stim Log", "Stimlog (*.h5)")

        # Create buttons
        self.superPixButton = QPushButton("Super Pixel Traces")
        self.superPixButton.clicked.connect(self.viewSuperPixelTraces)

        self.roiTraceButton = QPushButton("ROI Traces")
        self.roiTraceButton.clicked.connect(self.viewROITraces)

        self.plotROIButton = QPushButton("ROI Inspector")
        self.plotROIButton.clicked.connect(self.roiViewerWindow)



        # Organize buttons in a QVBoxLayout
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.superPixButton)
        button_layout.addWidget(self.roiTraceButton)
        button_layout.addWidget(self.plotROIButton)
        

        # Group buttons in a QGroupBox for neat organization
        button_group = QGroupBox("Actions")
        button_group.setLayout(button_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.DataFilePath)
        main_layout.addWidget(self.StackPath)
        main_layout.addWidget(self.StimPath)
        main_layout.addWidget(button_group)


        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        self.setStyleSheet("QPushButton { color: black; }")

    def viewSuperPixelTraces(self):
        datFile = self.DataFilePath.get_selected_file()
        stim = self.StimPath.get_selected_file()
        if datFile.startswith("No file selected"):
            print("Please select all files before launching the second window.")
            return
        print('Plotting data from acquisition', os.path.basename(datFile))

        if stim.startswith("No file selected"):
            stim = None
        
        # Launch the second window with the selected file paths
        self.superPixSel = tracePixelSelector([datFile, stim])
        self.superPixSel.show()

    def viewROITraces(self):
        datFile = self.DataFilePath.get_selected_file()
        stim = self.StimPath.get_selected_file()
        if datFile.startswith("No file selected"):
            print("Please select all files before launching the second window.")
            return
        if stim.startswith("No file selected"):
            stim = None
        
        print('Plotting data from acquisition', os.path.basename(datFile))
        # Launch the second window with the selected file paths
        self.superPixSel = roiSelector([datFile, stim])
        self.superPixSel.show()
    
    
    def roiViewerWindow(self):
        datFile = self.DataFilePath.get_selected_file()
        imgPath = self.StackPath.get_selected_file()
        if datFile.startswith("No file selected"):
            print("Please select all files before launching the second window.")
            return
        if imgPath.startswith("No file selected"):
            imgPath = None
        
        print('Viewing ROIs from acquisition', os.path.basename(datFile))
        # Launch the second window with the selected file paths
        self.superPixSel = roiInspector([datFile, imgPath])
        self.superPixSel.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())