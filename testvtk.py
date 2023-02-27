import sys
from PyQt5 import QtWidgets, QtGui

import vtk
class MedicalImageViewer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.reader = vtk.vtkImageReader()
        self.reader.SetFileName("lung_002.nii")
        self.reader.Update()

        self.viewer = vtk.vtkImageViewer()
        self.viewer.SetInputConnection(self.reader.GetOutputPort())

        self.renderWindow = self.viewer.GetRenderWindow()
        self.renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        self.renderWindowInteractor.SetRenderWindow(self.renderWindow)

        self.imageLabel = QtWidgets.QLabel(self)
        self.imageLabel.setGeometry(0, 0, self.renderWindow.GetSize()[0], self.renderWindow.GetSize()[1])
        self.imageLabel.setScaledContents(True)

        self.image = QtGui.QImage(self.renderWindow.GetPixelData(), self.renderWindow.GetSize()[0], self.renderWindow.GetSize()[1], QtGui.QImage.Format_RGB888)
        self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(self.image))

        self.renderWindowInteractor.Initialize()
        self.renderWindowInteractor.Start()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MedicalImageViewer()
    window.show()
    sys.exit(app.exec_())
