from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QComboBox, QPushButton, QRadioButton, QButtonGroup, QHBoxLayout
from PyQt6.QtCore import Qt
import sys

from slap2_utils.datafile import DataFile
from slap2_utils.functions import stim

from plotWindows.roiTracePlot import  roiPlot
from plotWindows.allROITraces import  roiTraces

class roiSelector(QMainWindow):
    def __init__(self, file_paths):
        super().__init__()

        self.setWindowTitle("ROI Trace Plot")
        self.hDataFile = DataFile(file_paths[0])
        if file_paths[1] is not None:
            self.stimTimes = stim.returnStimTime(file_paths[1]) 
        else:
            self.stimTimes = None

        layout = QVBoxLayout()
        
        # Create dropdown selector
        self.dropdown = QComboBox()
        roiIndices = [str(i) for i in range(len(self.hDataFile.metaData.AcquisitionContainer.ROIs))]
        self.dropdown.addItems(roiIndices)

        # Create radio buttons for available channels
        num_channels = int(self.hDataFile.header['numChannels'])
        self.button_group = QButtonGroup()

        radio_layout = QHBoxLayout()

        for i in range(num_channels):
            radio_button = QRadioButton(f"Channel {i + 1}")
            if i == 0:
                radio_button.setChecked(True)  # Default selection
            self.button_group.addButton(radio_button, i + 1)
            radio_layout.addWidget(radio_button)

        layout.addLayout(radio_layout)
        
        layout.addWidget(QLabel("Select a ROI:"))
        layout.addWidget(self.dropdown)

        # Add a button to open the PlotWindow
        self.plot_button = QPushButton("Plot ROI Data")
        self.plot_button.clicked.connect(self.open_plot_window)
        layout.addWidget(self.plot_button)

        # Add a button to plot all traces
        self.plot_all_button = QPushButton("Plot All Traces")
        self.plot_all_button.clicked.connect(self.plot_all_traces)
        layout.addWidget(self.plot_all_button)


        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.setStyleSheet("QPushButton { color: black; }")

    def open_plot_window(self):
        selected_roi = int(self.dropdown.currentText())
        selected_channel = self.button_group.checkedId() 
        self.plot_window = roiPlot(selected_roi, selected_channel, self.hDataFile, self.stimTimes)
        self.plot_window.show()

    def plot_all_traces(self):
        selected_channel = self.button_group.checkedId()
        self.plot_all_window = roiTraces(selected_channel, self.hDataFile, self.stimTimes)
        self.plot_all_window.show()