import sys
from PyQt6.QtWidgets import QApplication
from slap2_utils.dataviewer.mainWindow import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()