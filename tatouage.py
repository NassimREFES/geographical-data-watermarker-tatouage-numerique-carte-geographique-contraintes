from triangulation import Triangulation
from site_ import Site
from codage_site import Codage_site
from general import *
import copy
import time
import threading
from multiprocessing import Process, Lock, Queue

sites_bouger = [] # contient une suits de tuple (site_bouger, site_original)
temp_de_tatouage = [] # contient le temp de tatouage en second

gms = []

def create_site(a, tri, i, gsites):
    """
    creation de site avec leur codage
    a = Doc ( carte )
    tri = triangulation du Doc
    i = position on Doc
    gsites = la queue qui gerer les processus
    """
    curr_site = Site(tri, a.get(i))
    gsites.put([curr_site, Codage_site(curr_site), i])
    
def get_sites(a, tri):
    """
    creation de tout les sites du Document a avec la triangulation tri qui correspond
    a = Document ( carte )
    tri = triangulation du Doc
    """
    global gms

    gsites = Queue()

    i = 0
    my_process = []
    while i < len(a):
        j = i + 16 # crée 16 processus en meme temp
        if j < len(a):
            while i < j:
                my_process.append(Process(target=create_site, args=(a, tri, i, gsites)))
                i = i + 1
            for p in my_process:
                p.start()
            for p in my_process:
                p.join()
            for p in my_process:
                gms.append(gsites.get())
            del my_process[:]
        else:
            my_process.append(Process(target=create_site, args=(a, tri, i, gsites)))
            i = i + 1
    for p in my_process:
        p.start()
    for p in my_process:
        p.join()
    for p in my_process:
        gms.append(gsites.get())

def pretraitement(document):
    """
    pretraitement necessaire avant le tatouage ou la detection
    document = Doc ( carte )
    """
    global gms
    w = document
    tri = Triangulation(w) # crée une triangulation du Doc
    get_sites(w, tri) # crée les sites du Doc
    return (w, tri)

def tatouage(document, delta, cle, proportion_site):
    """ 
    recuperer un document tatoué avec une clé donnée
    document        = Doc ( carte ) c'est le morceau à tatouer 
    delta           = perte de precision autorisé
    clé             = la clé choisi pour le tatouage
    proportion_site = pour maximisé ou minimisé le nombre de site tatoué
    """
    global sites_bouger
    global temp_de_tatouage
    global gms
    
    t_begin = time.time() # debut de tatouage

    pt = pretraitement(document)
    w, tri = pt[0], pt[1]

    for site in gms:
        d = distance(site[0].sommet_centrale, barycentre(site[0]))
        j = selection_site(site[1].id_site(), cle, proportion_site)
        if j == 0:
            if math.floor(d/delta) % 2 == 1:
                ss = forcer_a_ne_pas_satisfait(site[0], delta)
                if test_preservation(site[0], ss.sommet_centrale, delta) :
                    sites_bouger.append([ss.sommet_centrale, site[0].sommet_centrale])
                    old_site = [w.get(site[2]), w.get_objet_type(site[2])]
                    w.supprimer_sommet(site[2])
                    w.ajoute_sommet_at(tuple(ss.sommet_centrale[0]), old_site[0][1], old_site[0][2], old_site[1], site[2])
                    #w.set(i, ss.sommet_centrale)
        elif j == 1:
            if math.floor(d/delta) % 2 == 0:
                ss = forcer_a_satisfait(site[0], delta)
                if test_preservation(site[0], ss.sommet_centrale, delta) :
                    sites_bouger.append([ss.sommet_centrale, site[0].sommet_centrale])
                    old_site = [w.get(site[2]), w.get_objet_type(site[2])]
                    w.supprimer_sommet(site[2])
                    w.ajoute_sommet_at(tuple(ss.sommet_centrale[0]), old_site[0][1], old_site[0][2], old_site[1], site[2])

    t_end = time.time() # fin de tatouage
    temp_de_tatouage.append(t_end - t_begin)

    del gms[:]

    return w # document tatoué
