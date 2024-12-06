import vtk


def convertRectilinear2PolyData(input):

    reader = vtk.vtkXMLRectilinearGridReader()
    reader.ReadFromInputStringOn()
    reader.SetInputString(input)
    reader.Update()

    surfaceF = vtk.vtkDataSetSurfaceFilter()
    surfaceF.SetInputConnection(reader.GetOutputPort())
    surfaceF.Update()

    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetInputData(surfaceF.GetOutput())
    writer.WriteToOutputStringOn()
    writer.Update()
    return writer.GetOutputString()


def convertStructuredGrid2PolyData(input):

    reader = vtk.vtkXMLStructuredGridReader()
    reader.ReadFromInputStringOn()
    reader.SetInputString(input)
    reader.Update()

    surfaceF = vtk.vtkDataSetSurfaceFilter()
    surfaceF.SetInputConnection(reader.GetOutputPort())
    surfaceF.Update()

    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetInputData(surfaceF.GetOutput())
    writer.WriteToOutputStringOn()
    writer.Update()
    return writer.GetOutputString()
