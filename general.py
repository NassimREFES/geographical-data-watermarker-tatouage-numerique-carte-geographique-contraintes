import math
from scipy.spatial import ConvexHull
from site_ import Site
from shapely.geometry import Polygon, Point
from sympy.geometry import Circle
from angle import *
import hashlib
import copy

nombre_de_site_bouger = []

def normalize_doc(ni, ci, doc):
    """
        ni[0] = [x_min, x_max]
        ni[1] = [y_min, y_max]
        ----------------------
        ci[0] = [x_min, y_min] --> Doc.min_pos 
        ci[1] = [x_max, y_max] --> Doc.max_pos 
    """
    doc = copy.deepcopy(doc)
    for i in range(0, len(doc)):
        np = normalize_point(ni, ci, doc[i])
        doc.set(i, tuple([np, doc.get(i)[1], doc.get(i)[2]]))

    return doc

def normalize_point(ni, ci, point):
    x = normalize_valeur(ni[0], [ ci[0][0], ci[1][0] ], point[0])
    y = normalize_valeur(ni[1], [ ci[0][1], ci[1][1] ], point[1])
    return (x, y)

def normalize_valeur(ni, ci, valeur):
    """ ni = [minp, maxp] = nouvelle intervale
        ci = [min, max] = intervale ou est contenu la valeur
        valeur = la valeur a normalize dans l'intervale [minp, maxp]
    """
    return (ni[1]-ni[0])/(ci[1]-ci[0])*(valeur-ci[1])+ni[1]

def selection_site(codage_site, cle, p=2):
    cs = codage_site
    hl = hashlib.md5()
    for i in cs:
        hl.update(i.encode('utf-8'))
    hl.update(str(cle).encode('utf-8'))
    myhash = hl.hexdigest()
    hl = hashlib.md5()

    return int(myhash, 16) % p

def barycentre(s):
    N = len(s.voisins)
    if N == 0: return (0, 0)
    x_sum, y_sum = 0, 0
    for i in range(N):
	    x_sum, y_sum = x_sum + s.voisins[:][i][0][0], y_sum + s.voisins[:][i][0][1]
    return (x_sum/N, y_sum/N)

def distance(sommet_centrale, barycentre):
    b = barycentre
    c = sommet_centrale
    return math.sqrt( (b[0]-c[0][0])**2 + (b[1]-c[0][1])**2 )

class Cercle:
    def __init__(self, *arg):
        self.__centre = [0, 0]
        self.__rayon = 0.0
        if len(arg) == 0:
            self.__centre([0, 0])
            self.__rayon = 0.0
        elif len(arg) == 2:
            centre, rayon = arg[0], arg[1]
            self.__centre = centre
            self.__rayon = rayon
        elif len(arg) == 3:
            p1, p2, p3 = arg[0], arg[1], arg[2]
            c = Circle(p1, p2, p3)
            self.__centre = [ float(c.center[0]), float(c.center[1]) ]
            self.__rayon = float(c.radius)
        else:
            raise Exception("Cercle : nombre d'argument invalid")

    def centre(self):
        return self.__centre

    def set_centre(self, c):
        self.__centre = c

    def rayon(self):
        return self.__rayon

    def set_rayon(self, r):
        self.__rayon = r

    def apartient_au_cercle(self, x):
        dist = math.pow(x[0] - self.__centre[0], 2) + math.pow(x[1] - self.__centre[1], 2)
        if dist <= math.pow(self.__rayon, 2):
            return True
        return False

def rotation(centre, p, degree):
    x = math.cos(degree_to_radian(degree))*(p[0]-centre[0]) - \
        math.sin(degree_to_radian(degree))*(p[1]-centre[1]) + centre[0]
    y = math.sin(degree_to_radian(degree))*(p[0]-centre[0]) + \
        math.cos(degree_to_radian(degree))*(p[1]-centre[1]) + centre[1]
    return [x, y]

def bouger(c, b, delta, distance_cb, satisfait):
    cc = c[0][:]
    if b[0] == c[0][0]:
        cc[1] = c[0][1] + delta*satisfait
    elif b[1] == c[0][1]:
        cc[0] = c[0][0] + delta*satisfait
    elif b[0] == c[0][0]:
        cc[1] = c[0][1] + delta*satisfait
    else:
        cc = [b[0], b[1] + distance_cb]
        d = angle(b, cc, c[0], False)
        cc[1] = cc[1] + delta*satisfait
        cc = rotation(b, cc, -d)
    return (cc, c[1], c[2])

def forcer_a_satisfait(site, delta):
    b = barycentre(site)
    d = distance(site.sommet_centrale, b)
    v = math.floor(d/delta) % 2
    if v == 1:
        return site
    return Site(bouger(site.sommet_centrale, b, delta, d, -1),\
                site.voisins, site.miroires)

def forcer_a_ne_pas_satisfait(site, delta):
    b = barycentre(site)
    d = distance(site.sommet_centrale, b)
    v = math.floor(d/delta) % 2
    if v == 0:
        return site
    return Site(bouger(site.sommet_centrale, b, delta, d, 1),\
                site.voisins, site.miroires)

def test_preservation(site_original, sommet_modifie, delta):
    global nombre_de_site_bouger
    
    print(distance(site_original.sommet_centrale, sommet_modifie[0]))
    if distance(site_original.sommet_centrale, sommet_modifie[0]) > delta:
        return False

    param = [x[0] for x in site_original.voisins]
    N = len(site_original.voisins)
    print(N)
    if N < 3:
        return False
    t = Polygon(param)
    if not t.contains(Point(sommet_modifie[0])):
        return False

    if N == site_original.miroires:
        for i in range(N):
            j = (i+1) % N
            k = (i+2) % N

            cercle = Cercle(site_original.voisins[i][0], site_original.voisins[j][0], site_original.miroires[i][0])
            if cercle.apartient_au_cercle(sommet_modifie[0]):
                return False
            cercle = Cercle(site_original.voisins[i][0], site_original.voisins[j][0], site_original.voisins[k][0])
            if cercle.apartient_au_cercle(site_original.sommet_centrale[0]):
                if not cercle.apartient_au_cercle(sommet_modifie[0]):
                    return False

    nombre_de_site_bouger.append(1)

    return True
