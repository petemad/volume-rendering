
#
# This example demonstrates how to read a series of dicom images
# and how to scroll with the mousewheel or the up/down keys
# through all slices
#
# some standard vtk headers
from PyQt5 import QtWidgets 
import vtk
import sys 
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWidgets import QFileDialog
from iso import Ui_MainWindow
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
class ApplicationWindow(QtWidgets.QMainWindow):
 
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Load.clicked.connect(self.Browse_clicked)
        self.ui.render.clicked.connect(self.main)
        self.ui.slider.valueChanged.connect(self.slider_SLOT)
        self.show() 


    def slider_SLOT(self,val):
        surfaceExtractor.SetValue(0, val)
        iren.update()

    def Browse_clicked (self) :
        fileName = QFileDialog.getExistingDirectory(self)
        global folder 
        folder = fileName
        global surfaceExtractor
        surfaceExtractor = vtk.vtkContourFilter()

        

    def main(self):
        global iren
        iren = QVTKRenderWindowInteractor()
        renWin = iren.GetRenderWindow()
        aRenderer = vtk.vtkRenderer()
        renWin.AddRenderer(aRenderer)
 
        # Read all the DICOM files in the specified directory.
        reader = vtk.vtkDICOMImageReader()
        reader.SetDirectoryName(folder)
        reader.Update()
        
        # An isosurface, or contour value of 500 is known to correspond to the
        surfaceExtractor.SetInputConnection(reader.GetOutputPort())
        surfaceExtractor.SetValue(0, 500)
        surfaceNormals = vtk.vtkPolyDataNormals()
        surfaceNormals.SetInputConnection(surfaceExtractor.GetOutputPort())
        surfaceNormals.SetFeatureAngle(60.0)
        surfaceMapper = vtk.vtkPolyDataMapper()
        surfaceMapper.SetInputConnection(surfaceNormals.GetOutputPort())
        surfaceMapper.ScalarVisibilityOff()
        surface = vtk.vtkActor()
        surface.SetMapper(surfaceMapper)

        aCamera = vtk.vtkCamera()
        aCamera.SetViewUp(0, 0, -1)
        aCamera.SetPosition(0, 1, 0)
        aCamera.SetFocalPoint(0, 0, 0)
        aCamera.ComputeViewPlaneNormal()
        
        aRenderer.AddActor(surface)
        aRenderer.SetActiveCamera(aCamera)
        aRenderer.ResetCamera()
        
        aRenderer.SetBackground(0, 0, 0)
        
        aRenderer.ResetCameraClippingRange()

        # Interact with the data.

        iren.Initialize()
        renWin.Render()
        iren.Start()
        iren.show()



def init():
    app = QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()

if __name__ == "__main__":
    init()