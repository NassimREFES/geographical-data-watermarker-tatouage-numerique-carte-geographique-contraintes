import copy, math
import pprint
from collections import OrderedDict 
from angle import *

class Site:
    def __init__(self, *arg):
        if len(arg) == 2:
            tri, c = arg[0], arg[1]
            self.voisins = []
            self.miroires = []
            print('\nSommet centrale')
            print(c)
            self.sommet_centrale = c
            tri1 = copy.deepcopy(tri.triangles)
            tri2 = copy.deepcopy(tri.triangles)

            for j, i in tri2.items():
                if c in i:
                    self.voisins.append(i)
                    del self.voisins[-1][self.voisins[-1].index(c)] 
                    del tri1[j] 

            for i in self.voisins :
                for j in tri1.values():
                    if i[0] in j and i[1] in j :
                        j.remove(i[0])
                        j.remove(i[1])
                        self.miroires.append(j[0])
            
            l = []
            # append les voisins(sommet par sommet)
            l = [j for i in self.voisins for j in i if j not in l]

            self.voisins = self.__sens_trigonomitrique(l) # Avoir le sens trigonomitrique des voisins
            self.miroires = self.__sens_trigonomitrique(self.miroires)

            print("\nVoisins : ", self.voisins)
            print("\nMirroires : ", self.miroires)
   
        elif len(arg) == 3:
            self.sommet_centrale = arg[0]
            self.voisins = arg[1]
            self.miroires = arg[2]
        
    def __sens_trigonomitrique(self, l):
        angles = []
        c = self.sommet_centrale
        for v in l:
            if v[0][1] < c[0][1]:
                angles.append(angle(c[0], [c[0][0] + 100, c[0][1]], v[0], False))
            else :
                angles.append(angle(c[0], [c[0][0] + 100, c[0][1]], v[0]))   

        temp_voisins = {angles[i]: l[i] for i in range(len(l))}
      
        d = OrderedDict(sorted(temp_voisins.items(), key=lambda t: t[0]))
        return list(d.values()) 
