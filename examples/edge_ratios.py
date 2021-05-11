import checkmesh

mesh = checkmesh.load('some/file/name')
edge_ratios = checkmesh.edge_ratio(mesh.cells, mesh.points)
data = {'edge_ratio': [edge_ratios]}
checkmesh.save('mesh_analysis.vtk', mesh, data)
checkmesh.show_scalar_field('mesh_analysis.vtk', 'edge_ratio')