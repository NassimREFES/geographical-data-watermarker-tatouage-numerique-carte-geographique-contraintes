# -*- coding: utf-8 -*- 

from reglage_panel import *
from test_tatouage import *
from tatouage import Tatouage
from lancer_detection import detection

def new_delta(delta, echelle, tmp):
    # mm - cm - m - km 
    res = [0.1, 1, 100, 100000]
    return (delta*res[tmp])/echelle
    
def unique_sites_bouger(sites_bouger):
    usb = {}
    for sb in sites_bouger:
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

class LeftPanel(ScrolledPanel):
	""" Cette class contient les widgets dans le pannau gauche """
	detect_opened = 0
	tatou_opened = 0
	sous_doc = []
	f1, t1 = 0, 0 
	f2, t2 = 0, 0
	def __init__(self, parent):
		ScrolledPanel.__init__(self, parent, style = wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
		self.parent = parent
		
		self.tatouage_done = False
		self.detection_done = False
		self.reglage_done = False
		
		self.new = Reglage(parent = self.GetTopLevelParent(), title = "Réglages")
		self.stat1 = None
		self.stat2 = None
		
		self.SetBackgroundColour("white")
		self.SetAutoLayout(1)
		self.SetupScrolling()
		
		
		msizer = wx.GridBagSizer(0,0)
		
		font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
		self.sb = wx.StaticBox(self, label=" Informations : ")
		self.sb.SetFont(font)
		self.sb.SetBackgroundColour("grey")
	
		
		boxsizer = wx.StaticBoxSizer(self.sb, wx.VERTICAL)
		sizer = wx.GridBagSizer(0,0) 
		
		nom_carte_label = wx.StaticText(self, -1, "Nom de la carte  : ")
		sizer.Add(nom_carte_label,pos= (0,0), flag = wx.ALL, border=5)
		font = wx.Font(12, wx.DEFAULT, wx.ITALIC, wx.NORMAL)
		
	
		self.nom_carte = wx.TextCtrl(self, -1,wx.EmptyString, style = wx.TE_READONLY)
		self.nom_carte.SetFont(font)
		sizer.Add(self.nom_carte,pos= (1,0), flag = wx.ALL|wx.EXPAND, border=5)
		
		self.a = wx.StaticText(self, -1, "Réglages : ")
		
		self.echelle_label = wx.StaticText(self, -1)
		self.echelle_label.SetLabel("	Echelle ="+ str(Reglage.echelle))
		sizer.Add(self.a,pos= (2,0), flag = wx.ALL, border=5)
		sizer.Add(self.echelle_label,pos= (3,0), flag = wx.ALL, border=5)
		
		self.perte_precision_label = wx.StaticText(self, -1, "	Perte de Précision = "+ str(Reglage.perte_precision))
		sizer.Add(self.perte_precision_label,pos= (4,0), flag = wx.ALL, border=5)
		self.nbre_partie_label = wx.StaticText(self, -1, "	Nombre de parties = "+ str(Reglage.nbre_partie))
		sizer.Add(self.nbre_partie_label,pos= (5,0), flag = wx.ALL, border=5)
		
		self.a = wx.StaticText(self, -1, "	Clé de tatouage : ")
		sizer.Add(self.a,pos= (6,0), flag = wx.ALL, border=5)
		self.cle_label = wx.TextCtrl(self, size=(270,100), style=wx.TE_MULTILINE)
		self.cle_label.SetEditable(False)
		
		sizer.Add(self.cle_label,pos= (7,0), flag = wx.ALL, border=5)
	

		boxsizer.Add(sizer,flag=wx.LEFT, border=5)
		
		self.reglage_btn = wx.Button(self,1, label='Réglages')
		self.lancer_tatouage_btn = wx.Button(self,2, label='Lancer le tatouage')
		self.lancer_detection_btn = wx.Button(self,3, label='Lancer la detection')
		
		
		self.Bind (wx.EVT_BUTTON, self.OnReglage, id=1)
		self.Bind (wx.EVT_BUTTON, self.OnTatouage, id=2)
		self.Bind (wx.EVT_BUTTON, self.OnDetection, id=3)
		
		msizer.Add(boxsizer,pos= (0,0), flag = wx.ALL|wx.EXPAND, border=5)
		msizer.Add(self.reglage_btn,pos= (2,0), flag = wx.ALL|wx.EXPAND, border=5)
		msizer.Add(self.lancer_tatouage_btn,pos= (4,0), flag = wx.ALL|wx.EXPAND, border=5)
		msizer.Add(self.lancer_detection_btn,pos= (6,0), flag = wx.ALL|wx.EXPAND, border=5)
		self.reglage_btn.Disable()
		self.lancer_tatouage_btn.Disable()
		self.lancer_detection_btn.Disable()
		
		
		self.SetSizer(msizer)
		
		
		
	def OnReglage(self, event): 
		if Reglage.reglage_done : # re_initialiser le réglage
			echelle, delta, cle, nbre_partie, perte_precision_unite, tatouer = get_parameters()
			self.new = Reglage(parent = self.GetParent().GetParent(), title = "Réglage")
			self.new.echelle.SetValue(echelle)
			self.new.perte_precision.SetValue(delta)
			self.new.nbre_partie.SetValue(nbre_partie)
			self.new.rbox.SetStringSelection(perte_precision_unite)
			self.new.cle.SetValue(cle)
			self.new.tatouer.SetStringSelection(tatouer)
			self.new.Show()
		else :
			self.new.Show()
			
	
	def Re_Init_Reglage(self): # initialiser au valeur à l'etat initiale
		self.new = Reglage(parent = self.GetParent().GetParent(), title = "Réglages")
		Reglage.reglage_done = False
		
			
		
	def OnDetection(self, e):
		self.dt = Detection(self.parent, "Seuil de détection ")

		a = self.GetTopLevelParent().t.get_doc()
		aa = copy.deepcopy(a)
		a_copy = copy.deepcopy(a)
	
		echelle, delta, cle, nbre_partie , unite = get_parameters()[0:5]
		tmp = ["mm","cm","m","km"]
		delta = new_delta(delta, echelle, tmp.index(unite))
		ss = False 
		if len(LeftPanel.sous_doc) != 0:
			ss = True 
		if Detection.flag :
			if  Reglage.reglage_done :
				if self.GetTopLevelParent().rightpanel.page1.t.draw_selection  :
					from_ , to_ = self.GetTopLevelParent().rightpanel.page1.t.selection_coords[0], self.GetTopLevelParent().rightpanel.page1.t.selection_coords[1]
					if get_parameters()[5] == "Un morceau de la carte"  :
						if ss :
							aa = LeftPanel.sous_doc
						else :
							aa = sous_doc(aa, from_, to_) # [96, -10]  To : [157, -43] self.GetTopLevelParent().t.shapes
						
						aa_copy = copy.deepcopy(aa)
						if len(aa) >= 3: # ici , il demande de detecter un morceu et le morceu séléctioné est valide
							d = detection(aa_copy, cle, self.dt.seuil, delta, nbre_partie)
							
							if d[0] == 22 :
								dial = wx.MessageDialog(None, "Le morceu séléctionné ne satisfait pas les conditions pour créé une triangulation ", 'Error',wx.ICON_ERROR)
								ret = dial.ShowModal()
								if ret == wx.ID_YES:
									self.Destroy()	
								
								return 
							""" Cette partie est pour affichage les résultats dans un tableu """
							tmp = [len(a), len(aa_copy), d[0], d[1], d[2]]
							self.stat2 = StatFrame(self.GetTopLevelParent(), [], tmp, 2 )
							LeftPanel.detect_opened = 1
							"""----------------------------------------------------------------"""
							self.detection_done = True 	
							self.GetTopLevelParent().toolbar.EnableTool(3, True)
							self.GetTopLevelParent().toolbar.EnableTool(4, True)
						else : # ici , il demande de tatouer un morceu mais la selection est vide 
							dial = wx.MessageDialog(None, "La detection non realisable, le nombre de sommets est inférieur à 3", 'Error',wx.ICON_ERROR)
							ret = dial.ShowModal()
							if ret == wx.ID_YES:
								self.Destroy()	
							
					else : # # ici , il a séléctioné un morceu mais il veut tatouer toute la carte
						dial = wx.MessageDialog(None, "T'as sélécetioné un morceau mais tu veux detecter dans toute la carte, tu doit modifier le réglage", 'Error',wx.ICON_ERROR)
						ret = dial.ShowModal()
						if ret == wx.ID_YES:
							self.Destroy()
							
				elif get_parameters()[5] == u"Carte Complète":
					d = detection(a_copy, cle, self.dt.seuil, delta, nbre_partie)
					if d[0] == 22 :
						dial = wx.MessageDialog(None, "Le morceu séléctionné ne satisfait pas les conditions pour créé une triangulation ", 'Error',wx.ICON_ERROR)
						ret = dial.ShowModal()
						if ret == wx.ID_YES:
							self.Destroy()	
							return 						
					""" Cette partie est pour affichage les résultats dans un tableu """
					self.stat2 = StatFrame(self.GetTopLevelParent(), data)
					LeftPanel.detect_opened = 1
							
					"""----------------------------------------------------------------"""
						
					self.detection_done = True 					
					self.GetTopLevelParent().toolbar.EnableTool(3, True)
					self.GetTopLevelParent().toolbar.EnableTool(4, True)
				
				else : # ici , il demande de tatouer un morceu mais il n'y a pas de selection
					dial = wx.MessageDialog(None, "Detection non realisable, veuillez sélectionner un morceu", 'Error',wx.ICON_ERROR)
					ret = dial.ShowModal()
					if ret == wx.ID_YES:
						self.Destroy()	
			else :
				dial = wx.MessageDialog(None, "Detection non realisable, veuillez saisir un réglage", 'Error',wx.ICON_ERROR)
				ret = dial.ShowModal()
				if ret == wx.ID_YES:
					self.Destroy()	
					
		
	def OnTatouage(self, e):
		LeftPanel.sous_doc = []
		shapes = self.GetTopLevelParent().t.shapes 
		shapes2 = copy.deepcopy(shapes)
		a = self.GetTopLevelParent().t.a
		a_copy = self.GetTopLevelParent().t.a_copy
		aa = copy.deepcopy(self.GetTopLevelParent().t.a_copy)
		echelle, delta, cle, nbre_partie , unite = get_parameters()[0:5]
		tmp = ["mm","cm","m","km"]
		delta = new_delta(delta, echelle, tmp.index(unite))
		
		if  Reglage.reglage_done :
			if self.GetTopLevelParent().rightpanel.page1.t.draw_selection:
				from_ , to_ = self.GetTopLevelParent().rightpanel.page1.t.selection_coords[0], self.GetTopLevelParent().rightpanel.page1.t.selection_coords[1]
				if get_parameters()[5] == "Un morceau de la carte":
					
					aa = sous_doc(aa, from_, to_) # [96, -10]  To : [157, -43] self.GetTopLevelParent().t.shapes
					aa_copy = copy.deepcopy(aa)
					
					if len(aa) >= 3: # ici , il demande de tatouer un morceu et le morceu séléctioné est valide
						self.GetTopLevelParent().rightpanel.page2.flag = 1
						aaa, sites_bouger, temptatouage  = Tatouage(aa, delta, cle, nbre_partie)[:]
						if aaa == False :
							dial = wx.MessageDialog(None, "Le morceu séléctionné ne satisfait pas les conditions pour créé une triangulation", 'Error',wx.ICON_ERROR)
							ret = dial.ShowModal()
							if ret == wx.ID_YES:
								self.Destroy()	
							
							return 
						usb = unique_sites_bouger(sites_bouger)
						usb1 = original_per_sites_bouger(aa_copy, usb)
						self.GetTopLevelParent().rightpanel.set_original_per_sites_bouger(usb1)
						LeftPanel.sous_doc = copy.deepcopy(aaa)
						
						""" Cette partie est pour affichage les résultats dans un tableu """
						id_ = 1
						data = []
						for i in range(len(aaa)) :
							data.append([])
							if aaa.get(i) != aa_copy.get(i):
								data[i].append([str(id_) , str(aa_copy[i][0])+" , "+str(aa_copy[i][1]), 
											str(aaa.get(i)[1]), str(aaa.get(i)[2]), 
											str(aaa[i][0]) + " , "+str(aaa[i][1]) ])
											
							else :
								data[i].append([str(id_) , str(aa_copy[i][0])+" , "+str(aa_copy[i][1]), 
											str(aaa.get(i)[1]), str(aaa.get(i)[2]), "/"])
								
							id_ += 1
						tmp = [len(a), len(aa_copy), len(sites_bouger), temptatouage] # ces donnés vont etre afficher comme resultat de tatouage
						self.stat1 = StatFrame(self.GetTopLevelParent(), data, tmp ,1)
						LeftPanel.tatou_opened = 1
						
						"""----------------------------------------------------------------"""
						self.GetTopLevelParent().rightpanel.nb.SetSelection(1)
						self.GetTopLevelParent().rightpanel.page3.flag = 1
						self.GetTopLevelParent().rightpanel.page3.drawn = 0
					
						for v in sites_bouger :
							shapes2[v[0][1]].points[v[0][2]] = v[0][0]	
						
						
							
									
						self.GetTopLevelParent().rightpanel.set_shapes(shapes2) #ici que les shapes pas besoin des records et fields prcq sont les memes
						self.GetTopLevelParent().rightpanel.set_sites_bouger(sites_bouger)
						
						
						self.doc_tatouer = apre_tatouage(copy.deepcopy(a),sites_bouger)
						self.tatouage_done = True 
						
						self.GetTopLevelParent().toolbar.EnableTool(3, True)
						self.GetTopLevelParent().toolbar.EnableTool(4, True)
						
						
						
					else : # ici , il demande de tatouer un morceu mais la selection est vide 
						dial = wx.MessageDialog(None, "Le tatouage non realisable, le nombre de sommets est inférieur à 3", 'Error',wx.ICON_ERROR)
						ret = dial.ShowModal()
						if ret == wx.ID_YES:
							self.Destroy()	
						
				else : # # ici , il a séléctioné un morceu mais il veut tatouer toute la carte
					dial = wx.MessageDialog(None, "T'as sélécetioné un morceau mais tu veux tatouer toute la carte, tu doit modifier le réglage", 'Error',wx.ICON_ERROR)
					ret = dial.ShowModal()
					if ret == wx.ID_YES:
						self.Destroy()
					
				
				
			elif get_parameters()[5] == u"Carte Complète":
				self.GetTopLevelParent().rightpanel.page2.flag = 1
				aaa, sites_bouger, temptatouage = tatouage(aa, delta, cle, nbre_partie)[:]
				LeftPanel.sous_doc = copy.deepcopy(aaa)
				
				usb = unique_sites_bouger(sites_bouger)
				usb1 = original_per_sites_bouger(a_copy, usb)
				self.GetTopLevelParent().rightpanel.set_original_per_sites_bouger(usb1)
						
				self.GetTopLevelParent().rightpanel.nb.SetSelection(1)
				self.GetTopLevelParent().rightpanel.page3.flag = 1
				self.GetTopLevelParent().rightpanel.page3.drawn = 0
				
				for v in sites_bouger :
					shapes2[v[0][1]].points[v[0][2]] = v[0][0]
				self.GetTopLevelParent().rightpanel.set_shapes(shapes2) #ici que les shapes pas besoin des records et fields prcq sont les memes
				self.GetTopLevelParent().rightpanel.set_sites_bouger(sites_bouger)
				self.doc_tatouer = apre_tatouage(copy.deepcopy(a), sites_bouger)
				
				tmp = [len(a), len(a), len(sites_bouger), temptatouage] # ces donnés vont etre afficher comme resultat de tatouage
				self.stat1 = StatFrame(self.GetTopLevelParent(), data, tmp, 1 )
				LeftPanel.tatou_opened = 1
				
				self.tatouage_done = True 
				
				self.GetTopLevelParent().toolbar.EnableTool(3, True)
				self.GetTopLevelParent().toolbar.EnableTool(4, True)
			
			else : # ici , il demande de tatouer un morceu mais il n'y a pas de selection
				dial = wx.MessageDialog(None, "Tatouage non realisable, veuillez sélectionner un morceu", 'Error',wx.ICON_ERROR)
				ret = dial.ShowModal()
				if ret == wx.ID_YES:
					self.Destroy()	
		else :
			dial = wx.MessageDialog(None, "Tatouage non realisable, veuillez saisir un réglage", 'Error',wx.ICON_ERROR)
			ret = dial.ShowModal()
			if ret == wx.ID_YES:
				self.Destroy()	
			
				
	def res_save(self, dirname , filename = "resultat"):	
		w = save_result_on_shp(self.doc_tatouer, self.GetTopLevelParent().t)
		save_on_shp_file(w,dirname + os.sep+filename)
		
		
		
		
