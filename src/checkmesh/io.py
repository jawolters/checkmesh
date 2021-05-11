import numpy as np
import meshio

def load(filename):
    file = meshio.read(filename)
    file.cells = np.asarray(file.get_cells_type('tetra'), dtype=np.int32)
    file.points = np.asarray(file.points, dtype=np.float64)
    return file

def save(filename, mesh, data, format="vtk"):
    #if isinstance(data, dict):
    #    raise TypeError('Invalid dataype: %s'%(isinstance(data)))    
    output = meshio.Mesh(points=mesh.points, cells={'tetra':mesh.cells}, cell_data=data)
    output.write(filename, file_format=format)