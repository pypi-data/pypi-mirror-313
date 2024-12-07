import numpy as np

import polyquad

from polyquad._antonietti import evaluateMonomials, integrateMonomialsFace

def I_ref(x1,x2,y1,y2,ii,jj):
    i = ii+1
    j = jj+1
    ref = ((x2**i)/i - (x1**i)/i) * ((y2**j)/j - (y1**j)/j) 
    return ref

if __name__=='__main__':
    # check implementation on a parallelepipedic box
    x1,x2 =  -1,2
    y1,y2 =  -30,-10
    x = [x1,x2,x2,x1]
    y = [y1,y1,y2,y2]
    pts = np.vstack((x,y)).T

    face = np.arange(4)

    order = 4
    vertices = pts

    p,w = polyquad.get_quadrature_2d(order, pts, face, mapping = True)
    
    # # verts = tmp
    # # vertexMonomials = evaluateMonomials(2, order, verts)
    # # integral, _ = integrateMonomialsFace(2, order, face, verts, vertexMonomials)

    x= p[:,0]
    y= p[:,1]
    for i in range(5):
        for j in range(5):
            if i+j<order:
                I = sum((x**i * y**j )*w)
                ref = I_ref(x1,x2,y1,y2,i,j)
                print(I - ref)




 
    order = 4
    vertices = pts
    # perform matrix transfomation to fit in the local bounding box = [-1, 1]^2
    verts, jacobian, transfo = polyquad.map_to_local_bb_2d(vertices)
    verts = np.pad(verts,((0,0),(0,1)))
    monos= evaluateMonomials(2, order, verts)
    integral, _ = integrateMonomialsFace(2, order, face, verts, monos)
    # # call antonietti's algorithm
    # integrated_monomials = polyquad.integrateMonomialsPolygon(order, face, verts)
