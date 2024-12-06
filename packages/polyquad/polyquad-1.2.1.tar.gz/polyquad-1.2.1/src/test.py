import numpy as np

import polyquad

if __name__=='__main__':
    #pentagon
    verts = np.array(((1,-1), (-1,0), (0,3), (2,3), (3,0)))
    face = np.arange(5)

    k=4
    # points, weights = polyquad.get_quadrature_2d(k, verts, face)
    
    # #P2 fron antonietti's paper
    # x = 0.666666666666667,0.555555555555556,1.000000000000000, - 0.555555555555556,- 1.0000
    # y = - 0.789473684210526,- 1.000000000000000,- 0.052631578947368,1.000000000000000,- 0.157894736842105
    
    # pts = np.vstack((x,y)).T
    # face = np.arange(pts.shape[0])
    # k=20
    # # points, weights, r = polyquad.get_quadrature_2d(k, verts, face, get_residual = True)
