# -*- coding: utf-8 -*- 
from doc import Doc 
from triangulation import Triangulation
import shapefile
import copy
import os

class shp_reader:
    def __init__(self, shp_name):
        self.rf = shapefile.Reader(shp_name)
        self.shapes = self.rf.shapes()

    def fields(self):
        return self.rf.fields

    def records(self):
        return self.rf.records()
        
class Reader:
	""" Cette class est pour lire la carte """
	def __init__(self, document_full_path = None ):
		self.r2 = shp_reader(document_full_path)
		self.shapes = self.r2.shapes
		self.a = self.get_doc()
		self.a_copy = copy.deepcopy(self.a)
		
	def get_doc(self):
		a = Doc()
		for obj in range(0, len(self.shapes)):
			for pt in range(0, len(self.shapes[obj].points)):
				a.ajoute_sommet(self.shapes[obj].points[pt], obj, pt, self.shapes[obj].shapeType)
		return a
		

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
    i = 0
    sz = len(sites_tatoue)
    if sz:
        curr = sites_tatoue[i]
        for obj in range(0, len(cdoc)):
            if sz <= i: break
            s = cdoc.get(obj)
            if s[1] == curr[0][1] and s[2] == curr[0][2]:
                cdoc[obj] = tuple(curr[0][0])
                i = i + 1
    return cdoc
    

def save_result_on_shp(cdoc, arg):
    w = shapefile.Writer(shapefile.POLYGON)
    w.fields = arg.r2.fields()
    w.records = arg.r2.records()
    shapes = arg.shapes
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
