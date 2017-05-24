from scipy.spatial import Delaunay
import numpy
import matplotlib.pyplot as plt
import copy

class Triangulation:
    triangles = {}

    def __init__(self, doc):
        cdoc = copy.deepcopy(doc[:])
        points = numpy.array(cdoc) 
        _triangulation = Delaunay(points)

        #for i in range(4, len(doc)):
        #    _triangulation.add_points(numpy.array([doc[i]]))

        _triangulation = _triangulation.simplices

        count = 0
        for ii in _triangulation:
            a = doc.get_by_coord(tuple(points[ii[0]]))
            b = doc.get_by_coord(tuple(points[ii[1]]))
            c = doc.get_by_coord(tuple(points[ii[2]]))

            for i in a:
                for j in b:
                    for k in c:
                        self.triangles[count] = [i, j, k]
                        count += 1 

        #plt.triplot(points[:,0], points[:, 1], _triangulation.copy())
        #plt.plot(points[:,0], points[:, 1], '.')
        #for j, p in enumerate(points):
        #    plt.text(p[0]-0.03, p[1]+0.03, (p[0], p[1]), ha='right')
        #plt.show()
            
        



    

    

