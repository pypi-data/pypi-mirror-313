import numpy as np
import polyquad

from polyquad import _utils

def I_ref(x1,x2,y1,y2,z1,z2,ii,jj,kk):
    i = ii+1
    j = jj+1
    k = kk+1
    ref = ((x2**i)/i - (x1**i)/i) * ((y2**j)/j - (y1**j)/j) * ((z2**k)/k - (z1**k)/k)
    return ref
if __name__=='__main__':

    # check implementation on a parallelepipedic box
    x1,x2 =  2,3
    y1,y2 = -12,-4.3
    z1,z2 = -1,1
    x = [x1,x2,x2,x1,x1,x2,x2,x1]
    y = [y1,y1,y1,y1,y2,y2,y2,y2]
    z = [z1,z1,z2,z2,z1,z1,z2,z2]
    pts = np.vstack((x,y,z)).T
    
    faces = [[0,1,2,3],#bottom
             [7,6,5,4],
             [0,4,5,1],
             [1,5,6,2],
             [2,6,7,3],
             [3,7,4,0]]

    
    order = 4
    
    faces = np.array(faces)
    p,w,r = polyquad.get_quadrature_3d(order, pts, faces, get_residual = True)
    xp = p[:,0]
    yp = p[:,1]
    zp = p[:,2]

    xpow,ypow,zpow = _utils.trios(order)
    monos = polyquad.integrateMonomialsPolyhedron(order, faces, pts)
    max_dif = -1
    for ii,mono in enumerate(monos):
        d =abs( mono - I_ref(x1,x2,y1,y2,z1,z2, xpow[ii], ypow[ii], zpow[ii]))
        if d>max_dif:
            max_dif = d
            
    print(max_dif)

    max_dif = -1
    for ii,mono in enumerate(monos):
        I = sum((xp**xpow[ii] * yp**ypow[ii] * zp**zpow[ii])*w)
        ref = I_ref(x1,x2,y1,y2,z1,z2, xpow[ii], ypow[ii], zpow[ii])
        d =abs( I - ref)
        print(d)
        if d>max_dif:
            max_dif = d
            
    print(max_dif)



        
