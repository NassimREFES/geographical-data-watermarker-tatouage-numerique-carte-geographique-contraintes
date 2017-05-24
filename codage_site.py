# -*- coding: utf-8 -*- 
from site_ import Site
import math

class Codage_site:
    def __init__(self, lsite):
        # matrice
        self.M = [[0 for i in range(len(lsite.voisins))]\
                    for i in range(len(lsite.voisins))]
        # matrice permutÃ©
        self.Mp = [[0 for i in range(len(lsite.voisins))]\
                    for i in range(len(lsite.voisins))]

        N = len(lsite.voisins)
        for i in range(N):
            for j in range(N):
                if j == 0: # arrete entre ni et Ec
                    # si ils sont dans la meme shape
                    if lsite.voisins[i][1] == lsite.sommet_centrale[1]:
                        # si ils se suive
                        if math.fabs(lsite.voisins[i][2] - lsite.sommet_centrale[2]) == 1.0:
                            self.M[i][j] = 1
                else: # arrete entre ni et n(i+j-1)%N
                    if lsite.voisins[i][1] == lsite.voisins[(i+j)%N][1]:
                        if math.fabs(lsite.voisins[i][2] - lsite.voisins[(i+j)%N][2]) == 1.0:
                            self.M[i][j] = 1

        self.__permutation(lsite) # permutation maximale de la matrice


    def __permutation(self, lsite):
        N = len(lsite.voisins) + 1
        for i in range(1, N):
            self.Mp[i-1] = self.M[i%(N-1)]

    def id_site(self):
        if len(self.Mp):
            N = len(self.Mp[0])
        else:
            N = 0
        cs = []
        for i in range(N):
            line_str = [str(x) for x in self.Mp[i]]
            line_str = ''.join(line_str)
            cs.append(line_str)

        return cs
