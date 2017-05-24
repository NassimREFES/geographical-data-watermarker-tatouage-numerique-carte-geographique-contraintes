from tatouage import get_sites
from tatouage import get_codages
from tatouage import pretraitement
from triangulation import Triangulation
from site_ import Site
from codage_site import Codage_site
from general import *
import copy

def detection(document, cle, seuil, delta, proportion_site):
    u = 0.5
    n0, n1, m0, m1 = 0, 0, 0, 0
    
    pt = pretraitement(document)
    w, tri, sites, codage_site = pt[0], pt[1], pt[2], pt[3]

    for i in range(len(w)):
        d = distance(sites[i].sommet_centrale, barycentre(sites[i]))
        j = selection_site(codage_site[i].id_site(), cle, proportion_site)
        if j == 0:
            n0 = n0 + 1
            if math.floor(d/delta) % 2 == 0:
                m0 = m0 + 1
        elif j == 1:
            n1 = n1 + 1
            if math.floor(d/delta) % 2 == 1:
                m1 = m1 + 1

    res = 4*math.exp(-2*n0*(m0/n0 - (1-u))**2) * math.exp(-2*n1*(m1/n1 - u)**2)
    print("res = ", res)
    return res < seuil


