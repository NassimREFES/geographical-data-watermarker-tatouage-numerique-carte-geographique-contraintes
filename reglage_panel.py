# -*- coding: utf-8 -*- 

import wx
from lancer_detection import Detection
from wx.lib.scrolledpanel import ScrolledPanel
from wx.lib.agw.floatspin import FloatSpin
from tatouage import *

def __champ_valide__(arg):
		if arg.isdigit():
			try :
				int(arg)
				return True 
			except :
				return False 
		return False	
def get_parameters():
		return (Reglage.echelle, 
				Reglage.perte_precision,
				Reglage.cle, 
				Reglage.nbre_partie, 
				Reglage.perte_precision_unite,
				Reglage.tatouer )
 		
class Reglage(wx.Dialog):
	""" Cette class pour la fenetre de réglage """
	echelle, perte_precision, perte_precision_unite, nbre_partie, cle , tatouer= "", "", "", "", "", ""
	reglage_done = False
	def __init__(self, parent, title):
		super(Reglage, self).__init__(parent, title = "Réglages", size =(360,450), style =wx.CLOSE_BOX|wx.SYSTEM_MENU|wx.CAPTION | wx.CLOSE_BOX)
		
		self.InitUi()
		self.Center()
    	   
	def InitUi(self):
		panel = wx.Panel(self)
		vbox = wx.BoxSizer(wx.VERTICAL)

		hbox1 =	wx.BoxSizer(wx.HORIZONTAL)
		echelle_label = wx.StaticText(panel, -1, "Echelle : 1/")
		hbox1.Add(echelle_label, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,9)
		
		self.echelle = FloatSpin(panel, value=1 , min_val=1.0, 
									increment=1.0, digits=8, size=(100,-1))
		hbox1.Add(self.echelle, 2, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,4)
		vbox.Add(hbox1, 1, wx.EXPAND|wx.ALL, 1)
		#-------------------------------------------
		sb = wx.StaticBox(panel, label=" Perte de précision autorisé :")
		boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
		self.perte_precision = wx.SpinCtrl(panel, value="1")
		self.perte_precision.SetRange(1, 8)
		self.perte_precision.SetValue(2)
		boxsizer.Add(self.perte_precision, 1, wx.ALL|wx.EXPAND, 1)
		#-------------------------------------------
		tmp = ["mm","cm","m","km"]
		self.rbox = wx.RadioBox(panel, label='', choices = tmp, majorDimension=1, style=wx.RA_SPECIFY_ROWS)
		boxsizer.Add(self.rbox, flag=wx.ALL|wx.ALIGN_CENTER, border=1)
		vbox.Add(boxsizer, 1, wx.EXPAND, 5)
		#------------------------------------------
		hbox2 =	wx.BoxSizer(wx.HORIZONTAL)
		partie_label = wx.StaticText(panel, -1, "Nombre de partie : ")
		hbox2.Add(partie_label, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,9)
		self.nbre_partie = wx.TextCtrl(panel)
		self.nbre_partie.SetValue("")
		hbox2.Add(self.nbre_partie, 1, wx.EXPAND|wx.ALIGN_RIGHT|wx.ALL,4)
		vbox.Add(hbox2, 1, wx.EXPAND|wx.ALL, 1)
		#-------------------------------------------
		sb2 = wx.StaticBox(panel, label=" Clé de tatouage :")
		boxsizer = wx.StaticBoxSizer(sb2, wx.VERTICAL)
		self.cle = wx.TextCtrl(panel, size=(270,100), style=wx.TE_MULTILINE)
		self.cle.SetValue("")
		boxsizer.Add(self.cle, 22, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,4)
		vbox.Add(boxsizer, 1, wx.EXPAND|wx.ALL, 1)
		#----------------------------------------		
		sb3 = wx.StaticBox(panel, label=" Appliquer sur :")
		boxsizer = wx.StaticBoxSizer(sb3, wx.VERTICAL)
		tmp = ["Un morceau de la carte", "Carte Complète"]
		self.tatouer = wx.RadioBox(panel, label='', choices = tmp, majorDimension=1, style=wx.RA_SPECIFY_ROWS)
		boxsizer.Add(self.tatouer,flag=wx.RIGHT, border=5)
		vbox.Add(boxsizer, 1, wx.EXPAND|wx.ALL, 1)
		#-----------------------------------------------
		
		
		hbox4 =	wx.BoxSizer(wx.HORIZONTAL)
		help_btn = wx.Button(panel,1, label='Help')
		ok_btn = wx.Button(panel, 2,label = "Ok")
		cancel_btn= wx.Button(panel,3, label="Cancel")
		
		
		self.Bind (wx.EVT_BUTTON, self.OnHelp, id=1)
		self.Bind (wx.EVT_BUTTON, self.OnOk, id=2)
		self.Bind (wx.EVT_BUTTON, self.OnCancel, id=3)
		
		
		hbox4.Add(help_btn, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL, 9)
		hbox4.Add(cancel_btn, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL, 9)
		hbox4.Add(ok_btn, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL, 9)
		
		vbox.Add(hbox4, 1, wx.EXPAND|wx.ALL, 1)
 	
		panel.SetSizer(vbox)
		
 
		
	def OnOk(self, event): 
					
		if not __champ_valide__(self.nbre_partie.GetValue()): 
			dial = wx.MessageDialog(None,"Nombre de parties doit etre un Entier positif", 'Error',wx.ICON_ERROR)
			ret = dial.ShowModal()
			if ret == wx.ID_YES:
				self.Destroy()
			return 
				 
		if self.cle.GetValue() == "":
			dial = wx.MessageDialog(None, "Valeur de Cle abscente ", 'Error',wx.ICON_ERROR)
			ret = dial.ShowModal()
			if ret == wx.ID_YES:
				self.Destroy()
			return 
		
		
		self.GetParent().leftpanel.echelle_label.SetLabelText("	Echelle = 1/"+str(self.echelle.GetValue()))
		self.GetParent().leftpanel.perte_precision_label.SetLabelText("	Delta = "+str(self.perte_precision.GetValue()))
		self.GetParent().leftpanel.nbre_partie_label.SetLabelText("	Nombre de parties = "+str(self.nbre_partie.GetValue()))
		self.GetParent().leftpanel.cle_label.SetValue(str(self.cle.GetValue()))
		self.GetParent().leftpanel.cle_label.SetEditable(False)
		
		self.GetParent().leftpanel.lancer_tatouage_btn.Enable()
		self.GetParent().leftpanel.lancer_detection_btn.Enable()  # ici, ca dépent il veut vérifier si la carte est tatoué ou non sans faire passé par un tatouage
		
		
		Reglage.echelle = self.echelle.GetValue()
		Reglage.perte_precision = self.perte_precision.GetValue()
		Reglage.perte_precision_unite = self.rbox.GetStringSelection()
		Reglage.nbre_partie = self.nbre_partie.GetValue()
		Reglage.cle = self.cle.GetValue()
		Reglage.tatouer = self.tatouer.GetStringSelection()
		Reglage.reglage_done = True
		
		self.Close()
				

	def OnHelp(self, event):
		try :
			import webbrowser
			webbrowser.open_new_tab('aide.html')
		except :
			pass
	
	def OnCancel(self, event):
		self.Close()
		

 

fichier_demo = [(" Ouvrir", " Ctrl + O"), (" Enregistrer", " Ctrl + S"), (" Enregistrer Sous", " Shift+Ctrl + S"), (" Réglage", " Ctrl + R") , (" Quitter", " Ctrl + Q")]
help_demo = [(" Aide", "F1"), ("Reccourcis", "F2"), ("A propos", "F3")]
view_demo = [(" Voir La barre d'outil","Shift+Ctrl+T"), ("Voir La barre de status","Shift+Ctrl+S")]

import sys

class ShortCutFrame(wx.Frame):
	""" Cette class est pour afficher les raccourcis du clavier """
	
	def __init__(self, parent):	
		stl =  wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN | wx.FRAME_NO_TASKBAR
		
		wx.Frame.__init__(self, parent, title = "Raccourcis", size = (400, 630), style = stl) # (400, 450)
		panel = wx.Panel(self)
		
		sizer = wx.GridBagSizer(0,0) 
		font = wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD)
		tmp = wx.StaticText(panel, -1, "   Les Raccourcis suivants sont configurés : ")
		tmp.SetFont(font)
		sizer.Add(tmp, pos = (0,0), flag = wx.ALL|wx.EXPAND)
		
		#----------------------------------------
		hbox = wx.GridBagSizer(0,0) 
		self.list = wx.ListCtrl(panel, -1, style = wx.LC_REPORT)
		self.list.InsertColumn(0, 'Fichier', width = 200)
		self.list.InsertColumn(1, '			', width = 160)
		for v in fichier_demo :
			index  = self.list.InsertStringItem(sys.maxint, v[0])
			self.list.SetStringItem(index, 1, v[1])
		hbox.Add(self.list, pos = (0,1))

		#----------------------------------------
		self.list = wx.ListCtrl(panel, -1, style = wx.LC_REPORT)
		self.list.InsertColumn(0, 'Aide', width = 200)
		self.list.InsertColumn(1, '			', width = 160)
		for v in help_demo :
			index  = self.list.InsertStringItem(sys.maxint, v[0])
			self.list.SetStringItem(index, 1, v[1])
		hbox.Add(self.list, pos = (1,1))
		
		
		#----------------------------------------
		
		self.list = wx.ListCtrl(panel, -1, style = wx.LC_REPORT)
		self.list.InsertColumn(0, 'View', width = 200)
		self.list.InsertColumn(1, '			', width = 160)
		for v in view_demo :
			index  = self.list.InsertStringItem(sys.maxint, v[0])
			self.list.SetStringItem(index, 1, v[1])
			
		hbox.Add(self.list, pos = (2,1))
		sizer.Add(hbox, pos= (2,0),  flag = wx.ALL|wx.EXPAND, border=5)
		
		
		ok_btn = wx.Button(panel, 2, label = "Ok")
		self.Bind (wx.EVT_BUTTON, self.OnOk, id=2)
		sizer.Add(ok_btn, pos= (4,0),  flag = wx.ALL|wx.EXPAND, border=4)
		
		panel.SetSizer(sizer)
		panel.Fit()
		self.Centre()
		
		self.Show(True)
		
	def OnOk(self, event) :
		self.Close()
		



class StatFrame(wx.Frame):
	""" Cette class pour affichage des résultats """
	opened = 0
	def __init__(self, parent, data = [], tmp = [""]*4 , kind = 0):	# kind : 1 == Affichage pour tatouage , 2 == Affichage pour detection
		stl =  wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN | wx.FRAME_NO_TASKBAR
		
		wx.Frame.__init__(self, parent, title = "Résultats", size = (900, 600), style = wx.DEFAULT_FRAME_STYLE) # (400, 450)
		panel = wx.Panel(self)
		StatFrame.opened = 1
		
		sizer = wx.GridBagSizer(0,0) 
		widths = [100, 300, 100, 200, 350]
		if kind == 1: # affichage pour tatouage
		
			#---------------------------------------- 
			hbox = wx.BoxSizer(wx.HORIZONTAL)
			self.list = wx.ListCtrl(panel, -1, style = wx.LC_REPORT)
			self.list.InsertColumn(0, 'ID', wx.LIST_FORMAT_CENTER, widths[0])
			self.list.InsertColumn(1, 'Position',wx.LIST_FORMAT_CENTER,  widths[1])
			self.list.InsertColumn(2, "ID Objet", wx.LIST_FORMAT_CENTER,  widths[2])
			self.list.InsertColumn(3, "Position dans L'objet", wx.LIST_FORMAT_CENTER, widths[3])
			self.list.InsertColumn(4, "Nouvelle Position", wx.LIST_FORMAT_CENTER, widths[4])
			
			
			
			for i  in range(len(data)) :
				v  = data[i][0]
				index  = self.list.InsertStringItem(sys.maxint, v[0])
				self.list.SetStringItem(index, 1, v[1])
				self.list.SetStringItem(index, 2, v[2])
				self.list.SetStringItem(index, 3, v[3])
				self.list.SetStringItem(index, 4, v[4])
				if v[4] != "/" :
					self.list.SetItemBackgroundColour(index, wx.Colour(0, 255, 0))
					
			
				
			hbox.Add(self.list, 1, wx.EXPAND|wx.ALL, 5)
			sizer.Add(hbox, pos= (1,0),  flag = wx.ALL|wx.EXPAND, border=5)
			self.SetSize((sum(widths)+20, 500))
			vbox = wx.BoxSizer(wx.VERTICAL)
			hbox1 =	wx.BoxSizer(wx.HORIZONTAL)
			font = wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD)
			info_label = wx.StaticText(panel, -1, "Informations du tataouge :")
			info_label.SetFont(font)
			hbox1.Add(info_label, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,9)
			vbox.Add(hbox1, 1, wx.EXPAND|wx.ALL, 1)
			
			
			hbox1 =	wx.BoxSizer(wx.HORIZONTAL)
			info_label = wx.StaticText(panel, -1, "   Nombre Sommets du document : " + str(tmp[0]))
			hbox1.Add(info_label, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,9)
			vbox.Add(hbox1, 1, wx.EXPAND|wx.ALL, 1)
			
			hbox1 =	wx.BoxSizer(wx.HORIZONTAL)
			info_label = wx.StaticText(panel, -1, "   Nombre Sommets du morceu selectionné : " + str(tmp[1]))
			hbox1.Add(info_label, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,9)
			vbox.Add(hbox1, 1, wx.EXPAND|wx.ALL, 1)
			
			hbox1 =	wx.BoxSizer(wx.HORIZONTAL)
			info_label = wx.StaticText(panel, -1, "   Nombre de sites bougé : " + str(tmp[2]))
			hbox1.Add(info_label, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,9)
			vbox.Add(hbox1, 1, wx.EXPAND|wx.ALL, 1)
			
			hbox1 =	wx.BoxSizer(wx.HORIZONTAL)
			info_label = wx.StaticText(panel, -1, "   Temps de tatouage : " + str(tmp[3][0]) + " (s)")
			hbox1.Add(info_label, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,9)
			vbox.Add(hbox1, 1, wx.EXPAND|wx.ALL, 1)
			sizer.Add(vbox, pos= (2,0),  flag = wx.ALL|wx.EXPAND, border=5)
		
		
		
		elif kind == 2:
			self.SetSize((400, 350))
			vbox = wx.BoxSizer(wx.VERTICAL)
			hbox1 =	wx.BoxSizer(wx.HORIZONTAL)
			font = wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD)
			info_label = wx.StaticText(panel, -1, "Informations du détection :")
			info_label.SetFont(font)
			hbox1.Add(info_label, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,9)
			vbox.Add(hbox1, 1, wx.EXPAND|wx.ALL, 1)
			
			
			hbox1 =	wx.BoxSizer(wx.HORIZONTAL)
			info_label = wx.StaticText(panel, -1, "   Nombre Sommets du document : " + str(tmp[0]))
			hbox1.Add(info_label, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,9)
			vbox.Add(hbox1, 1, wx.EXPAND|wx.ALL, 1)
			
			hbox1 =	wx.BoxSizer(wx.HORIZONTAL)
			info_label = wx.StaticText(panel, -1, "   Nombre Sommets du morceu selectionné : " + str(tmp[1]))
			hbox1.Add(info_label, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,9)
			vbox.Add(hbox1, 1, wx.EXPAND|wx.ALL, 1)
			
			
			hbox1 =	wx.BoxSizer(wx.HORIZONTAL)
			info_label = wx.StaticText(panel, -1, "   Résultat de détection : " + str(tmp[2]))
			hbox1.Add(info_label, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,9)
			vbox.Add(hbox1, 1, wx.EXPAND|wx.ALL, 1)
			
			
			hbox1 =	wx.BoxSizer(wx.HORIZONTAL)
			info_label = wx.StaticText(panel, -1, "   Taux de détection : " + str(tmp[3][0]))
			hbox1.Add(info_label, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,9)
			vbox.Add(hbox1, 1, wx.EXPAND|wx.ALL, 1)
			
			
			hbox1 =	wx.BoxSizer(wx.HORIZONTAL)
			info_label = wx.StaticText(panel, -1, "   Temps de détection : " + str(tmp[4][0]) +" (s)")
			hbox1.Add(info_label, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,9)
			vbox.Add(hbox1, 1, wx.EXPAND|wx.ALL, 1)
			sizer.Add(vbox, pos= (2,0),  flag = wx.ALL|wx.EXPAND, border=5) 
	
        	ok_btn = wx.Button(panel, 2, label = "Ok")
        	self.Bind (wx.EVT_BUTTON, self.OnOk, id=2)
		#tmp = wx.StaticText(panel, -1, " ")
		#sizer.Add(tmp, pos= (3,0),  flag = wx.ALL|wx.EXPAND, border=5)
       		sizer.Add(ok_btn, pos= (3,0),  flag = wx.ALL|wx.ALIGN_CENTER, border=9)
        	panel.SetSizer(sizer)
        	panel.Fit()
        	self.Centre()
        	self.Show(True)
		
	def OnOk(self, event) :
		self.Close()
		
	def Closing(self):
		self.Close()
		
