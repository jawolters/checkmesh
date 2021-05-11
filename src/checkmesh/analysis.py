import numpy as np
import numba
from numba import prange

@numba.jit(nopython=True, parallel=True, nogil=True)
def edge_ratio(cells, points):
    edge_ids = np.asarray([[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]], dtype=np.int32)
    ncells = cells.shape[0]
    ratios = np.zeros((ncells,1), dtype=np.float64)
    for id in prange(ncells):
        vtx_coords = points[cells[id]]
        edge_lengths = np.sqrt(np.square(vtx_coords[edge_ids[:,0],:] - vtx_coords[edge_ids[:,1],:]).sum(axis=1))
        ratios[id] = np.amax(edge_lengths)/np.amin(edge_lengths)
    return ratios

@numba.jit(nopython=True, parallel=True, nogil=True)
def aspect_frobenius(cells, points):        
    VERDICT_DBL_MIN = 1.0E-30
    VERDICT_DBL_MAX = 1.0E+30
    normal_exp = 1. / 3.

    ncells = cells.shape[0]
    af = np.zeros((ncells,1))
    for id in prange(ncells):
        coordinates = points[cells[id]]
  
        u = np.array( [[coordinates[1][0] - coordinates[0][0]],
                       [coordinates[1][1] - coordinates[0][1]],
                       [coordinates[1][2] - coordinates[0][2]]] )

        v = np.array( [[coordinates[2][0] - coordinates[0][0]],
                       [coordinates[2][1] - coordinates[0][1]],
                       [coordinates[2][2] - coordinates[0][2]]] )

        w = np.array( [[coordinates[3][0] - coordinates[0][0]],
                       [coordinates[3][1] - coordinates[0][1]],
                       [coordinates[3][2] - coordinates[0][2]]] )

        denominator = 3. * (2. * (u % ( v * w ))**2)**normal_exp        

        if denominator < VERDICT_DBL_MIN:
            af[id] = VERDICT_DBL_MAX
            continue

        numerator = 1.5 * ( u[0] * u[0] + u[1] * u[1] + u[2] * u[2]
                          + v[0] * v[0] + v[1] * v[1] + v[2] * v[2]
                          + w[0] * w[0] + w[1] * w[1] + w[2] * w[2] ) \
                    - v[0] * u[0] + v[1] * u[1] + v[2] * u[2] \
                    - w[0] * u[0] + w[1] * u[1] + w[2] * u[2] \
                    - w[0] * v[0] + w[1] * v[1] + w[2] * v[2]

        aspect_frobenius = numerator / denominator

        if aspect_frobenius > 0: af[id] = np.minimum( aspect_frobenius, VERDICT_DBL_MAX )            
        else:                    af[id] = np.maximum( aspect_frobenius, -VERDICT_DBL_MAX )

    return af