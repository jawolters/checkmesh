import numpy as np
import meshio

def load(filename):
    file = meshio.read(filename)
    file.cells = np.asarray(file.get_cells_type('tetra'))
    file.points = np.asarray(file.points)
    return file

def save(filename, mesh, data, format="vtk"):
    #if isinstance(data, dict):
    #    raise TypeError('Invalid dataype: %s'%(isinstance(data)))    
    output = meshio.Mesh(points=mesh.points, cells={'tetra':mesh.cells}, cell_data=data)
    output.write(filename, file_format=format)