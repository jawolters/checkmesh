import checkmesh

#load mesh file
mesh = checkmesh.load('cube.vtk')

#compute metrics and store results in a dict
edge_ratio = checkmesh.edge_ratio(mesh.cells, mesh.points)
data = {'edge_ratio': [edge_ratio]}

#save results to vtk file
checkmesh.save('mesh_analysis.vtk', mesh, data)

#visualize
checkmesh.show_scalar_field('mesh_analysis.vtk', 'edge_ratio')