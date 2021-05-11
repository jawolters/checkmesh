# checkmesh 

checkmesh is a simple mesh quality analysis tool written in Python3.

The tool is build around [meshio](https://github.com/nschloe/meshio) and thus supports a great variety of meshes types. Furthermore, [VTK](https://vtk.org) is used as a basic for porting quality metrics to Python and for rudimentary quality visualization. Finally,  [numba](https://github.com/numba/numba) is used to parallize and speed up the analysis in order to cope with large meshes.

Currently supported quality checks:
 - edge ratio
 - aspect frobenius

---

Minimal `edge_ratios.py` example 
```
import checkmesh

mesh = checkmesh.load('some/file/name')
edge_ratios = checkmesh.edge_ratio(mesh.cells, mesh.points)
data = {'edge_ratio': [edge_ratios]}
checkmesh.save('mesh_analysis.vtk', mesh, data)
checkmesh.show_scalar_field('mesh_analysis.vtk', 'edge_ratio')
```
