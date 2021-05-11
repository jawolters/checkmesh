
from vtk import vtkUnstructuredGridReader, vtkScalarBarActor, vtkColorTransferFunction, vtkLookupTable, vtkDataSetMapper, vtkActor, vtkRenderer, vtkRenderWindow, vtkRenderWindowInteractor
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np

def beautify_string(s):
    s = s.capitalize()
    s = s.replace('_',' ')

def show_scalar_field(filename, scalarname, show_mesh=False):
    ncolors = 256

    reader = vtkUnstructuredGridReader()
    reader.SetFileName(filename)
    reader.ReadAllScalarsOn()
    reader.Update()
    output = reader.GetOutput()

    scalarname_found = False
    for i in range(output.GetCellData().GetNumberOfArrays()):
        if scalarname == output.GetCellData().GetArrayName(i):
            scalarname_found = True
    if not scalarname_found:
        raise dataError('Could not find scalar "%s" in the vtk file.'%scalarname)

    ctf = vtkColorTransferFunction()
    ctf.SetColorSpaceToRGB()
    cmap = cm.get_cmap('viridis', ncolors)
    ctf.AddRGBPoint(-1, 1, 0, 0)
    for i,rgb in enumerate(cmap.colors):        
        ctf.AddRGBPoint(float(i/ncolors),rgb[0],rgb[1],rgb[2])   

    lut = vtkLookupTable()
    lut.SetNumberOfTableValues(ncolors)
    lut.Build()
    for i in range(0,ncolors):
        rgb = list(ctf.GetColor(float(i)/ncolors))+[1]
        lut.SetTableValue(i,rgb)   

    output_port = reader.GetOutputPort()
    mapper = vtkDataSetMapper()    
    mapper.SetInputConnection(output_port)
    mapper.ScalarVisibilityOn()
    mapper.SetColorModeToMapScalars()
    mapper.SetLookupTable(lut)
    mapper.SetScalarModeToUseCellFieldData()
    mapper.SelectColorArray(scalarname)
    mapper.SetScalarRange(output.GetCellData().GetArray(scalarname).GetRange())    

    scalarBar = vtkScalarBarActor()
    scalarBar.SetLookupTable(mapper.GetLookupTable())
    scalarBar.SetTitle(scalarname)
    scalarBar.SetOrientationToHorizontal()
    scalarBar.SetPosition(0.1,-0.001)
    scalarBar.SetLabelFormat('%-#6.1e')
    scalarBar.SetWidth(0.8)
    scalarBar.SetHeight(0.1)
    scalarBar.SetNumberOfLabels(4)
    scalarBar.SetMaximumNumberOfColors(256)
    scalarBar.SetTitleRatio(0.6)
    titleprop = scalarBar.GetTitleTextProperty()
    titleprop.ShadowOff()
    titleprop.BoldOff()
    titleprop.SetColor(1,1,1)
    labelprop = scalarBar.GetLabelTextProperty()
    labelprop.ShadowOff()
    labelprop.BoldOff()
    labelprop.SetColor(1,1,1)
    scalarBar.SetLabelTextProperty(labelprop)

    actor = vtkActor()
    actor.SetMapper(mapper)
    if show_mesh:
        actor.GetProperty().EdgeVisibilityOn()
        actor.GetProperty().SetLineWidth(1.0)

    renderer = vtkRenderer()
    renderer.AddActor(actor)
    renderer.AddActor2D(scalarBar)
    renderer.SetBackground(0,0,0)

    renderer_window = vtkRenderWindow()
    renderer_window.AddRenderer(renderer)

    interactor = vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderer_window)
    interactor.Initialize()
    interactor.Start()

def plot_histogram(data, xlabel, filename=None):
    cut = [np.quantile(data, 0.25), np.quantile(data, 0.5), np.quantile(data, 0.75)]
    fig, ((ax1,ax2),(ax3,ax4)) = plt.subplots(nrows=2,ncols=2)
    frq, edges = np.histogram(data)
    ax1.bar(edges[:-1], frq, width = np.diff(edges), edgecolor = "black",
            align = "edge")
    ax1.set_title('%s '%xlabel)
    frq, edges = np.histogram(data[data>cut[0]])
    ax2.bar(edges[:-1], frq, width = np.diff(edges), edgecolor = "black",
            align = "edge")
    ax2.set_title('%s > %.2f'%(xlabel,cut[0]))
    frq, edges = np.histogram(data[data>cut[1]])
    ax3.bar(edges[:-1], frq, width = np.diff(edges), edgecolor = "black",
            align = "edge")
    ax3.set_title('%s > %.2f'%(xlabel,cut[1]))
    frq, edges = np.histogram(data[data>cut[2]])
    ax4.bar(edges[:-1], frq, width = np.diff(edges), edgecolor = "black",
            align = "edge")
    ax4.set_title('%s > %.2f'%(xlabel,cut[2]))
    ax3.set_xlabel('%s'%xlabel)
    ax1.set_ylabel('frequency')
    ax4.set_xlabel('%s'%xlabel)
    ax3.set_ylabel('frequency')
    fig.suptitle('Histogram of %s'%xlabel)
    fig.tight_layout()
    if filename: 
        if not filename.endswith('.pdf'): filename += '.pdf'
        plt.savefig(filename, dpi=150, format='pdf')
    plt.show()
