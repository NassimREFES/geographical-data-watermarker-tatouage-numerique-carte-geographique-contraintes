# -*- coding: utf-8 -*-
import wx
from wx.lib.agw.floatspin import FloatSpin

from triangulation import Triangulation
from site_ import Site
from codage_site import Codage_site
from general import *
import copy
from tatouage import *
import time

def detection(document, cle, seuil, delta, proportion_site):
    temp_de_detection = []
    taux_de_detection = []
    global gms2
    t_begin = time.time()
    u = 0.5
    n0, n1, m0, m1 = 0., 0., 0., 0.
    pt = pretraitement(document, True)
    if Triangulation.tri_done == 0:
        return (22, [], []) # 22 ici est un code d'erreur
    else:# si la triangulation est faite en succée il continue la detection sinon il renvoie un code d'erreur, realisé dans la ligne au dessus
        w, tri = pt[0], pt[1]
        for site in gms2:
            d = distance(site[0].sommet_centrale, barycentre(site[0]))
            j = selection_site(site[1].id_site(), cle, proportion_site)
            if j == 0:
                n0 = n0 + 1
                if math.floor(d/delta) % 2 == 0:
                    m0 = m0 + 1
            elif j == 1:
                n1 = n1 + 1
                if math.floor(d/delta) % 2 == 1:
                    m1 = m1 + 1
        taux_de_detection.append(4*math.exp(-2*n0*(m0/n0 - (1-u))**2) * math.exp(-2*n1*(m1/n1 - u)**2))
        t_end = time.time()
        temp_de_detection.append(t_end - t_begin)
        del gms2[:]
        return (taux_de_detection[0] < seuil, taux_de_detection, temp_de_detection)


class Detection(wx.Dialog):
	flag = False
	def __init__(self, parent, title):
		wx.Dialog.__init__(self, parent, title = title, size =(400,150),
		style = wx.CLOSE_BOX|wx.SYSTEM_MENU | wx.CAPTION)

		self.InitUi()
		self.Center()

	def InitUi(self):
		self.seuil = 0
		panel = wx.Panel(self)
		msizer = wx.GridBagSizer(0,0)

		hbox1 =	wx.BoxSizer(wx.HORIZONTAL)
		seuil_label = wx.StaticText(panel, -1,"Veuillez entrer le seuil de détection  ")
		hbox1.Add(seuil_label, 1, flag = wx.ALL,border = 5)

		self.seuil_spin = FloatSpin(panel, value=0.0, min_val=0.0, max_val=1, increment=0.01, digits=3, size=(100,-1))
		"""
		self.seuil_spin= wx.SpinCtrl(panel, value="0")
		self.seuil_spin.SetRange(0, 1)
		self.seuil_spin.SetValue(0)
		"""

		hbox1.Add(self.seuil_spin, 0, flag = wx.ALL,border = 3)

		msizer.Add(hbox1,pos= (1,0), flag = wx.ALL, border=5)

		sizer = wx.GridBagSizer(0,0)
		valider_btn = wx.Button(panel,1, label="Valider")
		self.Bind (wx.EVT_BUTTON, self.OnValider, id=1)
		sizer.Add(valider_btn,pos= (0,15), flag =wx.ALL|wx.EXPAND, border=5)

		msizer.Add(sizer,pos= (2,0), flag = wx.ALL, border=5)
		panel.SetSizer(msizer)
		self.ShowModal()


	def OnValider(self, e):
		global flag
		self.seuil = self.seuil_spin.GetValue()
		Detection.flag = True
		self.Close()







