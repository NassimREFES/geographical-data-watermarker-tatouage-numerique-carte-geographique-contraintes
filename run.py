from doc import Doc
from triangulation import Triangulation
from site_ import Site
from codage_site import Codage_site
from general import *
import math
import copy
# 1: 34077294
"""
a.ajoute_sommet([675, 340], 1, 50) # c
a.ajoute_sommet([715, 0], 2, 22)   # m7
a.ajoute_sommet([425, 240], 2, 20) # n1
a.ajoute_sommet([715, 241], 2, 21) # n7
a.ajoute_sommet([890, 189], 1, 52) # m6
a.ajoute_sommet([802, 290], 1, 51) # n6
a.ajoute_sommet([980, 381], 3, 32) # m4, m5



a.ajoute_sommet([797, 380], 3, 31) # n5
a.ajoute_sommet([797, 515], 3, 30) # n4
a.ajoute_sommet([540, 522], 3, 29) # n3
a.ajoute_sommet([520, 450], 1, 49) # n2
a.ajoute_sommet([540, 705], 3, 28) # m3
a.ajoute_sommet([435, 670], 1, 48) # m1, m2
"""
"""
a.ajoute_sommet([715, 0], 2, 22)   # m7
a.ajoute_sommet([425, 240], 2, 20) # n1
a.ajoute_sommet([775, 341], 2, 21) # n7
a.ajoute_sommet([675, 340], 1, 50) # c

#a.ajoute_sommet([890, 189], 1, 52) # m6
#a.ajoute_sommet([802, 290], 1, 51) # n6
a.ajoute_sommet([580, 551], 3, 35) # m4, m5
a.ajoute_sommet([980, 681], 3, 32) # m4, m5
"""
""""


#print (angle([890, 189], [900, 189], [715,0 ], no_inv=False))
"""
"""
import sys
sys.exit()


a.ajoute_sommet([291, 24], 1, 50)   # m7
a.ajoute_sommet([447, 18], 1, 51) # n1
a.ajoute_sommet([378.5, 81], 1, 52) # n7
a.ajoute_sommet([282, 108], 1, 53) # m6
a.ajoute_sommet([235, 142.5], 1, 54) # n6
a.ajoute_sommet([451, 101], 2, 32) # m4, m5

a.ajoute_sommet([376, 145], 2, 33) # c

a.ajoute_sommet([289, 170], 2, 34) # n5
a.ajoute_sommet([222, 253], 3, 20) # n4
a.ajoute_sommet([357, 212], 3, 21) # n3
a.ajoute_sommet([399, 253], 3, 22) # n2
a.ajoute_sommet([442, 210], 3, 23) # m3
a.ajoute_sommet([543, 124], 3, 24) # m1, m2


a.ajoute_sommet([715, 0], 22, 22)   # m7
a.ajoute_sommet([425, 240], 22, 20) # n1
a.ajoute_sommet([715, 241], 22, 21) # n7
a.ajoute_sommet([890, 189], 11, 52) # m6
a.ajoute_sommet([802, 290], 11, 51) # n6
a.ajoute_sommet([980, 381], 33, 32) # m4, m5

a.ajoute_sommet([675, 340], 11, 50) # c

a.ajoute_sommet([797, 380], 33, 31) # n5
a.ajoute_sommet([797, 515], 33, 30) # n4
a.ajoute_sommet([540, 522], 33, 29) # n3
a.ajoute_sommet([520, 450], 11, 49) # n2
a.ajoute_sommet([540, 705], 33, 28) # m3
a.ajoute_sommet([435, 670], 11, 48) # m1, m2
"""

#tri = Triangulation(a)
#print(tri.triangles.values())

"""s = Site(tri, ([797, 380], 3, 31))
print('\n')
print(s.sommet_centrale)
print('\n')
print(s.voisins)
print('\n')
print(s.miroires)
print('\n')

print('2 = {}'.format(a))


del s

ss = Site(tri, ([797, 515], 3, 30))
print('\n')
print(ss.sommet_centrale)
print('\n')
print(ss.voisins)
print('\n')
print(ss.miroires)
print('\n')"""

"""ss = Site(tri, ([435, 670], 1, 48))
print('\n')
print(s.sommet_centrale)
print('\n')
print(s.voisins)
print('\n')
print(s.miroires)
print('\n')"""

"""print(s.voisins)

print('\n')

print(s.miroires)

print('\n')

print(s.sommet_centrale)

print('\n')

c = Codage_site(s)

print(c.M)

print(c.Mp)

print('\n')

print(c.checksum_site())

print(selection_site(c.checksum_site(), "NASSIM", 6))

print(barycentre(s))

print(distance(s.sommet_centrale, barycentre(s)))

print('\n')

#cercle = Cercle([425, 240], [715, 241], [715, 0])
cercle = Cercle([715, 241], 300)
print(cercle.apartient_au_cercle([675, 340]))

print('\n')

test = test_preservation(s,  ([700, 400], 1, 50), 100)
print(test)"""
""""
sites = []

for i in range(len(a)):
    print ("Start running ", i+1 , " ... ")
    s = Site(tri, a.get(i))
    sites.append(s)
    s.print_voisins(s.voisins)
    print('\n')
    print("Mirroires : ", s.miroires)
    print('\n')
"""

"""print(angle([715, 241], [425, 240], [675, 340]))
print(a[6])
bg = bouger(a.get(6), [715, 241], 10, distance(a.get(6), [715, 241]), -1)
print(bg)
print(angle([715, 241], [425, 240], bg[0]))"""

"""
#--------- Error ici (24/02) ---------------
print ("=========== Modification =======")
for site in sites :
    print("\n-------------------------------")
    print('sommet_centrale = {}'.format(site.sommet_centrale))
    res = forcer_a_ne_pas_satisfait(site, 10)
    print('sommet_bouger = {}'.format(res.sommet_centrale[0]))
    print('distance = {}'.format(distance(res.sommet_centrale, site.sommet_centrale[0])))

    res = forcer_a_satisfait(site, 10)
    print('sommet_bouger = {}'.format(res.sommet_centrale[0]))
    print('distance = {}'.format(distance(res.sommet_centrale, site.sommet_centrale[0])))
"""
# ---------------------------------------------------------------
import shapefile
from tatouage import *

a = Doc()

"""a.ajoute_sommet([7, 0], 1, 50) # c
a.ajoute_sommet([715, 0], 2, 22)   # m7
a.ajoute_sommet([425, 240], 2, 20) # n1
a.ajoute_sommet([715, 241], 2, 21) # n7
a.ajoute_sommet([890, 189], 1, 52) # m6
a.ajoute_sommet([802, 290], 1, 51) # n6
a.ajoute_sommet([980, 381], 3, 32) # m4, m5

a.ajoute_sommet([797, 380], 3, 31) # n5
a.ajoute_sommet([797, 515], 3, 30) # n4
a.ajoute_sommet([540, 522], 3, 29) # n3
a.ajoute_sommet([520, 450], 1, 49) # n2
a.ajoute_sommet([540, 705], 3, 28) # m3
a.ajoute_sommet([435, 670], 1, 48) # m1, m2"""

class shp_reader:
    def __init__(self, shp_name):
        self.rf = shapefile.Reader(shp_name)
        self.shapes = self.rf.shapes()

    def fields(self):
        return self.rf.fields

    def records(self):
        return self.rf.records()

r2 = shp_reader("../../map_douglas_peucker_80p/map")
shapes = r2.shapes

for obj in range(0, len(shapes)):
    for pt in range(0, len(shapes[obj].points)):
        print(shapes[obj].points[pt])
        a.ajoute_sommet(shapes[obj].points[pt], obj, pt, shapes[obj].shapeType)

a_copy = copy.deepcopy(a)

aa = copy.deepcopy(a)

def sous_doc(cdoc, point_from, point_to):
    from scipy.spatial import ConvexHull
    pf1 = [point_to[0], point_from[1]]
    pf2 = [point_from[0], point_to[1]]
    points = [point_from, pf1, point_to, pf2]
    copie = cdoc[0]
    enfin_darha = True
    while enfin_darha:
        enfin_darha = False
        for obj in range(0, len(cdoc)):
            if obj < len(cdoc):
                points.append(copy.deepcopy(cdoc[obj])) # 5eme element: indice = 4
                print(points)
                ch = ConvexHull(points)
                ch = list(ch.vertices)
                if  4 in ch:
                    enfin_darha = True
                    copie = cdoc.get(obj)
                    cdoc.supprimer_sommet(obj)#cdoc.index_of(cdoc.get(obj))
                del points[4]
    cdoc.calcule_max_min_pos()

    return cdoc

def apre_tatouage(cdoc, sites_tatoue):
    global shapes

    for i in range(0, len(sites_tatoue)):
        curr = sites_tatoue[i]
        j = sum([len(shapes[ii].points[:]) for ii in range(0, curr[0][1])]) + curr[0][2] + 1
        t = cdoc.get_objet_type(j)
        cdoc.supprimer_sommet(j)
        cdoc.ajoute_sommet_at(curr[0][0], curr[0][1], curr[0][2], t, j)

    return cdoc

def save_result_on_shp(cdoc, original_fields, original_records):
    global shapes

    w = shapefile.Writer(shapefile.POLYGON)

    w.fields = original_fields
    w.records = original_records

    obj = 0
    part = []
    parts = []
    sz = len(cdoc)
    i = 0
    while i < sz and obj < len(shapes):
        s = cdoc.get(i)
        if len(shapes[obj].points): # objet contient des points
            if len(shapes[obj].parts) == 1: # un objet contient une seul partie
                while s[1] == obj and i < sz:
                    part.append(copy.deepcopy(list(s[0])))
                    i = i + 1
                    if i < sz:
                        s = cdoc.get(i)
                obj = obj + 1 # objet suivant

                if len(part):
                    parts.append(copy.deepcopy(part))
                    w.poly(parts=parts, shapeType=cdoc.get_objet_type(i-1)) # ajout de l'objet
                    del part[:]
                    del parts[:]

            else: # un objet contient plusieur partie
                start_part = shapes[obj].parts
                start_part.append(len(shapes[obj].points)) # contient les positions de debut de chaque forme
                for ii in range(0, len(start_part)-1):
                    begin = start_part[ii] # debut d'une forme
                    end = start_part[ii+1] # fin d'une forme
                    for coords in shapes[obj].points[begin:end]: # tout les coords entre debut et fin
                        part.append(copy.deepcopy([float(coords[0]), float(coords[1])]))

                    if len(part):
                        parts.append(copy.deepcopy(part))
                        i = i + (start_part[ii+1]-start_part[ii])
                        del part[:]

                w.poly(parts=parts, shapeType=cdoc.get_objet_type(i-1)) # ajout de l'objet
                del parts[:]
                obj = obj + 1
        else: # objet vide
            obj = obj + 1    

    return w

def save_on_shp_file(w, filename):
	w.save(target=filename)

def new_delta(delta, echelle, tmp):
    # mm - cm - m - km 
    res = [0.1, 1, 100, 100000]
    return (delta*res[tmp])/echelle

#n = (113.40209592971893, -23.194633732173276)
#n1 = (115.5999716844713, -21.300274153077172)

#n = (140.65638072685584, -12.657679817780421)
#n1 = (144.58891727961117, -5.8910552245796239)

#n = (110.70430593611576, -28.582585152482217)
#n1 = (123.2928591090355, -20.624304410981217)

#n = (144.40693653978533, -42.632340818011926)
#n1 = (148.93859583710727, -40.189252387312848)

#n = (140.65638072685584, -14.657679817780421)
#n1 = (145.58891727961117, -4.8910552245796239)

#n = (144.52954603562608, -42.11000652975325)
#n1 = (147.23723815545446, -40.327632165160324)

n = (140.511684713374, -17.440992114380816) 
n1 = (149.84457758295247, -8.7592313054706423)

aa = sous_doc(aa, n, n1)

aa_copy = copy.deepcopy(aa)

cle = "Mohamed12345"
cle1 = "Mohamed12345"

delta = 1
echelle = 34077294 #10
delta = new_delta(delta, echelle, 2)

print("len doc origin: ", len(a))
print("max = ", a.max_pos)
print("min = ", a.min_pos)
print("len sous doc: ", len(aa))
print("max = ", aa.max_pos)
print("min = ", aa.min_pos)
print("echelle = ", echelle)
print("delta = ", delta)

aaa = tatouage(aa, delta, cle, 2)

print("temp de tatouage: ", temp_de_tatouage)

res_a = apre_tatouage(a_copy, sites_bouger)

#res_save = save_result_on_shp(res_a, r2.fields(), r2.records())

#save_on_shp_file(res_save, "../../map_douglas_peucker_50p/map_tatoue2014722224")

print("----------------------")
print(sites_bouger)
print("----------------------")
print("--> ", len(res_a))

def unique_sites_bouger(sites_bouger):
    usb = {}
    for sb in sites_bouger:
        print("===> ", sb)
        s = complex(sb[0][0][0], sb[0][0][1])
        try:
            if usb[s]:
                usb[s][2] = usb[s][2] + 1    
        except KeyError:
            usb[s] = []
            usb[s].append(tuple(sb[0][0]))
            usb[s].append(sb[1][0])
            usb[s].append(1)
            usb[s].append(0)
    
    return usb

def original_per_sites_bouger(cdoc, usb):
    for i in range(0, len(cdoc)):
        for value in usb.values():
            if cdoc[i] == value[1]:
                value[3] = value[3] + 1

    return usb

print('nombre de site bouger = {}'.format(len(nombre_de_site_bouger)))

from detection import *

seuil = 0.1

res = detection(aaa, cle1, seuil, delta, 2)

print("detecte = ", res)

usb = unique_sites_bouger(sites_bouger)

usb1 = original_per_sites_bouger(aa_copy, usb)

print("len usb = ", len(usb))

print(usb1)

print("----------------------")
print(sites_bouger)
print("----------------------")

print("temp de tatouage: ", temp_de_tatouage)

print("seuil = ", seuil)

print("temp de detection: ", temp_de_detection)

print("taux de detection: ", taux_de_detection)


print("detecte = ", res)


print('nombre de site bouger = {}'.format(len(nombre_de_site_bouger)))

print("len doc origin: ", len(a_copy))
print("max = ", a_copy.max_pos)
print("min = ", a_copy.min_pos)
print("len sous doc: ", len(aa_copy))
print("max = ", aa_copy.max_pos)
print("min = ", aa_copy.min_pos)
print("echelle = ", echelle)
print("delta = ", delta)

print("clÃ© tatouage = ", cle)
print("cle detection = ", cle1)

#with open("test_algo_parallel_300sommets.txt", "a") as myfile:
#    myfile.write("{} = {}".format("temp de tatouage", temp_de_tatouage))
#    myfile.write("\n{} = {}".format("temp de detection", temp_de_detection))
#    myfile.write("\n\n{} = {}".format("seuil", seuil))
#    myfile.write("\n{} = {}".format("taux de detection", taux_de_detection))
#    myfile.write("\n{} = {}".format("detecte", res))
#    myfile.write("\n\n{} = {}".format("nombre de site bouger", len(nombre_de_site_bouger)))
#    myfile.write("\n\n{} = {}".format("len doc origin", len(a_copy)))
#    myfile.write("\n{} = {}".format("max", a_copy.max_pos))
#    myfile.write("\n{} = {}".format("min", a_copy.min_pos))
#    myfile.write("\n\n{} = {}".format("len sous doc", len(aa_copy)))
#    myfile.write("\n{} = {}".format("max", aa_copy.max_pos))
#    myfile.write("\n{} = {}".format("min", aa_copy.min_pos))
#    myfile.write("\n\n{} = {}".format("echelle", echelle))
#    myfile.write("\n{} = {}".format("delta", delta))
#    myfile.write("\n\n{} = {}".format("clÃ© tatouage", cle))
#    myfile.write("\n{} = {}\n\n----------------------------------------------\n\n".format("cle detection", cle1))
