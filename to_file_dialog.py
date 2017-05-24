# -*- coding: utf-8 -*- 
import wx
import os 
import sys
from test_tatouage import *
from leftpanel import LeftPanel
from reglage_panel import Reglage , ShortCutFrame,  StatFrame
from rightpanel import *
import os
# 1: 34077294

cursors = [wx.CURSOR_ARROW, wx.CURSOR_HAND, wx.CURSOR_WATCH, wx.CURSOR_SPRAYCAN, 
			wx.CURSOR_PENCIL, wx.CURSOR_CROSS, wx.CURSOR_QUESTION_ARROW, wx.CURSOR_POINT_LEFT, wx.CURSOR_SIZING]
app_name = "GDW v1.0"

class MainWindow( wx.Frame ):
	doc_loaded = False 
	def __init__( self, parent ):
		#stl = (wx.DEFAULT_FRAME_STYLE|wx.MAXIMIZE) & ~( wx.RESIZE_BORDER|wx.RESIZE_BOX|wx.MAXIMIZE_BOX)
		stl = wx.DEFAULT_FRAME_STYLE
		wx.Frame.__init__ ( self, parent, -1, title = app_name, pos = wx.DefaultPosition, size = wx.Size( 900,500 ), style = stl)
		wx.Frame.CenterOnScreen(self)
		#self.SetSize((wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X),wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y) -70 ))
		#self.ShowFullScreen(True)
		#self.SetMinSize(self.GetSize())
		
		self.fileName , self.dirName  = "", ""
		self.doc_name = ""
		self.t = None # ultilisé pour le lecture des shapes
		self.doc_loaded = False
		self.use_grid = False
		self.current_tab = 0
		self.outil_active = ["", "", ""] # pour l'affichage de l'outil active dans la barre de status
		self.stb_spacing = 0
		self.reglage = Reglage(parent = self, title = "Réglages")
		
	
		self.menubar1 = wx.MenuBar()
		self.menu1 = wx.Menu()
		self.menubar1.Append( self.menu1, u"Fichier" )
		
		self.ouvrir_item = wx.MenuItem( self.menu1, 1, u"Ouvrir\tCtrl+O", wx.EmptyString, wx.ITEM_NORMAL )
		
			
		self.menu1.AppendItem( self.ouvrir_item )
		self.Bind(wx.EVT_MENU, self.OnFileOpen, self.ouvrir_item) 		

		self.menu1.AppendSeparator()
		
		self.enregistrer_item = wx.MenuItem( self.menu1, 2, u"Enregistrer\tCtrl+S", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu1.AppendItem( self.enregistrer_item )
		self.enregistrer_item.Enable(False)
		self.Bind(wx.EVT_MENU,self.OnSave, self.enregistrer_item)
		
		self.enregistrer_sous_item = wx.MenuItem( self.menu1, 3, u"Enregistrer Sous\tShift+Ctrl+S", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu1.AppendItem( self.enregistrer_sous_item )
		self.enregistrer_sous_item.Enable(False)
		self.Bind(wx.EVT_MENU, self.OnSaveAs, self.enregistrer_sous_item) 
		
		self.reglage_item = wx.MenuItem( self.menu1, 4, u"Réglages\tCtrl+R", wx.EmptyString, wx.ITEM_NORMAL )
		self.menu1.AppendItem( self.reglage_item )
		self.reglage_item.Enable(False)
		self.Bind(wx.EVT_MENU, self.OnReglage, self.reglage_item) 
		
		self.menu1.AppendSeparator()
		
		self.quitter_item = wx.MenuItem( self.menu1, 5, u"Quitter\tCtrl+Q")
		self.quitter_item.SetBitmap(wx.Bitmap('exit2.png'))
		self.menu1.AppendItem( self.quitter_item )
		
		self.Bind(wx.EVT_MENU, self.OnQuit, self.quitter_item) 
		
		# 2eme menu : view menu
		view_menu = wx.Menu()
		self.menubar1.Append( view_menu, u"Affichage" )
		self.voir_tbar = wx.MenuItem( view_menu, wx.ID_ANY, u"Voir La barre d'outil\tShift+Ctrl+T", wx.EmptyString, wx.ITEM_CHECK )
		self.voir_stbar = wx.MenuItem( view_menu, wx.ID_ANY, u"Voir La barre de status\tShift+Ctrl+S", wx.EmptyString, wx.ITEM_CHECK )
		
		view_menu.AppendItem( self.voir_tbar )
		view_menu.AppendItem( self.voir_stbar )
		
		view_menu.Check(self.voir_tbar.GetId(), True)
		view_menu.Check(self.voir_stbar.GetId(), True)
		
		self.Bind(wx.EVT_MENU, self.ApparenceToolBar, self.voir_tbar)
		self.Bind(wx.EVT_MENU, self.ApparenceStatusBar, self.voir_stbar)
		
		"""
		self.outils_menu = wx.Menu()
		self.menubar1.Append( self.outils_menu, u"Outils" )
		self.vue_initiale_item = wx.MenuItem( self.outils_menu, wx.ID_ANY, u"Vue Initiale",wx.EmptyString)
		self.outils_menu.AppendItem(self.vue_initiale_item)
		self.Bind(wx.EVT_MENU,self.OnHome, self.vue_initiale_item)
		"""
		
		#self.grid_item = wx.MenuItem( self.option_menu, wx.ID_ANY, u"Show Grid",wx.EmptyString, wx.ITEM_CHECK)
		#self.option_menu.AppendItem(self.grid_item)
		#self.Bind(wx.EVT_MENU,self.OnShowGrid, self.grid_item)
		
		
        
		self.aide_menu = wx.Menu()
		self.menubar1.Append(self.aide_menu, u"Aide")
		self.aide_item = wx.MenuItem( self.aide_menu, wx.ID_ANY, u"Aide\tF1")
		self.aide_menu.AppendItem(self.aide_item)
		self.Bind(wx.EVT_MENU,self.OnAide, self.aide_item)
		
		self.short_cut_item = wx.MenuItem( self.aide_menu, wx.ID_ANY, u"Raccourcis Clavier\tF2")
		self.aide_menu.AppendItem(self.short_cut_item)
		self.Bind(wx.EVT_MENU,self.OnShowShortCut, self.short_cut_item)
		
		self.aide_menu.AppendSeparator()
		
		self.about_item = wx.MenuItem( self.aide_menu, wx.ID_ANY, u"À propos\tF3")
		self.aide_menu.AppendItem(self.about_item)
		self.Bind(wx.EVT_MENU,self.OnAbout, self.about_item)
		self.SetMenuBar(self.menubar1)
		self.toolbar = self.CreateToolBar(style = wx.BORDER|wx.TB_HORIZONTAL|wx.TB_FLAT)#|wx.TB_TEXT)
		self.toolbar.SetBackgroundColour("white")#wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENUBAR))
		self.toolbar.SetToolBitmapSize((32,32))
		
		ouvrir_tool = self.toolbar.AddLabelTool(2,'Ouvrir', wx.Bitmap('document_open.png'), shortHelp="Ouvrir")
		self.toolbar.AddSeparator()
		enreg_tool = self.toolbar.AddLabelTool(3,'Enregistrer', wx.Bitmap('save.png'), shortHelp="Enregistrer")
		enreg_sous_tool = self.toolbar.AddLabelTool(4,'Enregistrer Sous', wx.Bitmap('save_as5.png'), shortHelp="Enregistrer Sous")
		reglage_tool = self.toolbar.AddLabelTool(77,u'Réglages', wx.Bitmap('reglage2.png'), shortHelp=u"Réglages")
		self.toolbar.AddSeparator()
		quit_tool = self.toolbar.AddLabelTool(1,'Quitter', wx.Bitmap('exit.png'), shortHelp="Quitter")
		
		self.toolbar.AddSeparator()
		
		home_tool = self.toolbar.AddLabelTool(5,'Home', wx.Bitmap('home.png'), shortHelp="Vue Initial : Annuler toutes les actions appliqué sur la figure")
		export_image_tool = self.toolbar.AddLabelTool(10,'Export', wx.Bitmap('Image.png'),shortHelp="Exporter :\nExporter la figure sous forme d'image" ) #'export_as_image2.png' , 'childish_Image.png'
		undo_tool = self.toolbar.AddLabelTool(6,'Undo', wx.Bitmap('prev.png'),shortHelp="Annuler :\nAnnuler une à une vos actions")
		redo_tool = self.toolbar.AddLabelTool(7,'Redo', wx.Bitmap('next.png'), shortHelp="Rétablir :\nRefaire une à une vos actions annulées")
		self.toolbar.AddSeparator()
		pan_tool = self.toolbar.AddLabelTool(9,'Pan', wx.Bitmap('hand_tool.png'), shortHelp="Déplacer :\nFaire déplacer la figure présente dans le canevas de dessin ")
		zoom_tool = self.toolbar.AddLabelTool(8,'Zoom', wx.Bitmap('zoom_in3.png'), shortHelp="Zoomer :\nCréer un rectangle de zoom en cliquant droit sur une place de la vue Graphique et tirant la souris jusqu’au sommet opposé du rectangle désiré")
		
		#self.rect_selection_tool = self.toolbar.AddLabelTool(11,'Rectangle_Selection', wx.Bitmap('selection-resize.png'), shortHelp="Selection")
		self.rect_selection_tool = self.toolbar.AddLabelTool(11,'Rectangle_Selection', wx.Bitmap('selection-resize.png'), shortHelp="Sélectionner :\nPour selectionner un morceu de la carte, en maintenant le bouton gauche de la souris enfoncé, déplacez le curseur jusqu’au coin opposé ")
		
		
		
		
		self.toolbar.EnableTool(3, False)
		self.toolbar.EnableTool(4, False)
		self.toolbar.EnableTool(5, False)
		self.toolbar.EnableTool(6, False)
		self.toolbar.EnableTool(7, False)
		self.toolbar.EnableTool(8, False)
		self.toolbar.EnableTool(9, False)
		self.toolbar.EnableTool(10, False)
		self.toolbar.EnableTool(11, False)
		self.toolbar.EnableTool(77, False)
		
		self.toolbar.Realize()
		self.toolbar.Bind(wx.EVT_TOOL, self.OnQuit, quit_tool)
		self.toolbar.Bind(wx.EVT_TOOL, self.OnFileOpen, ouvrir_tool)
		self.toolbar.Bind(wx.EVT_TOOL, self.OnSave, enreg_tool)
		self.toolbar.Bind(wx.EVT_TOOL, self.OnSaveAs, enreg_sous_tool)
		self.toolbar.Bind(wx.EVT_TOOL, self.OnReglage, reglage_tool)
		self.toolbar.Bind(wx.EVT_TOOL, self.OnUndo, undo_tool)
		self.toolbar.Bind(wx.EVT_TOOL, self.OnRedo, redo_tool)
		self.toolbar.Bind(wx.EVT_TOOL, self.OnPan, pan_tool)
		self.toolbar.Bind(wx.EVT_TOOL, self.OnZoom, zoom_tool)
		self.toolbar.Bind(wx.EVT_TOOL, self.OnHome, home_tool)
		self.toolbar.Bind(wx.EVT_TOOL, self.OnExportImage, export_image_tool)
		self.toolbar.Bind(wx.EVT_TOOL, self.OnRectangleSelection, self.rect_selection_tool)
		
		
		
		self.st = wx.StatusBar(self)
		self.SetStatusBar(self.st)
		self.StatusBarUpdater("")
		
	
		self.splitter = wx.SplitterWindow(self, -1, style = wx.SP_3DSASH|wx.SP_LIVE_UPDATE)#|wx.SP_PERMIT_UNSPLIT)
		self.leftpanel = LeftPanel(self.splitter)
		self.rightpanel = RightPanel(self.splitter)
		
		
		
		
		
		
		self.splitter.SplitVertically(self.leftpanel, self.rightpanel)
		self.splitter.SetMinimumPaneSize(self.leftpanel.sb.GetSize()[0]+15)
		
		self.Bind(wx.EVT_SIZE, self.OnResize)		
		
		sizer = wx.BoxSizer(wx.HORIZONTAL)	
		sizer.Add(self.splitter, 1, wx.EXPAND)
		self.SetSizer(sizer)		
		
		self.Show(True)
		#self.SetMinSize(self.GetSize())
		self.Maximize(True)
		self.Centre( wx.BOTH )
		
		
	
	def OnShowGrid(self, event):
		if self.grid_item.IsChecked():
			self.GetTopLevelParent().rightpanel.page1.draw(use_grid = True)
		else :
			self.GetTopLevelParent().rightpanel.page1.draw(use_grid = False)
		
	def OnResize(self, e):
		CanvasPanel.w = self.GetTopLevelParent().rightpanel.GetClientSize()[0]
		self.stb_spacing  = self.splitter.GetSashPosition()
		e.Skip()
		pass
		
	def StatusBarUpdater(self, msg):
		if self.outil_active[self.current_tab]  != "":
			w = "<  "+self.outil_active[self.current_tab] +"  >"
			self.st.SetStatusText(app_name + self.stb_spacing/5 * "  "+ w + "        " +msg)
		else :
			#print "normally empty but look ", self.outil_active[self.current_tab]
			self.st.SetStatusText(app_name + self.stb_spacing/5 * "  "+ self.outil_active[self.current_tab] + " " +msg)
			
		
	def OnHome(self, event):
		if self.current_tab == 0:
			#if self.outil_active[0] == "" :
			#self.outil_active[0] = "Vue Initiale"
			self.GetTopLevelParent().rightpanel.page1.t.toolbar.home('on')
			
		elif self.current_tab == 1 and self.GetTopLevelParent().rightpanel.page2.flag :
			#self.outil_active[1] = "Vue Initiale"
			self.GetTopLevelParent().rightpanel.page2.t.toolbar.home('on')
			
		elif  self.current_tab == 2 and self.GetTopLevelParent().rightpanel.page3.flag :
			#self.outil_active[2] = "Vue Initiale"
			self.GetTopLevelParent().rightpanel.page3.t.toolbar.home('on')		
	
			
	def OnExportImage(self, event):
		if self.current_tab == 0:
			#if self.outil_active[0]  == "":
			#self.outil_active[0]  = "Exporter"
			self.GetTopLevelParent().rightpanel.page1.t.toolbar.save_figure('on')
		elif self.current_tab == 1 and self.GetTopLevelParent().rightpanel.page2.flag :
			#self.outil_active[1]  = "Exporter"
			self.GetTopLevelParent().rightpanel.page2.t.toolbar.save_figure('on')
		elif  self.current_tab == 2 and self.GetTopLevelParent().rightpanel.page3.flag :
			#self.outil_active[2]  = "Exporter"
			self.GetTopLevelParent().rightpanel.page3.t.toolbar.save_figure('on')
		
	def OnUndo(self, event):
		if self.current_tab == 0:
			#if self.outil_active[0]  == "":
			#self.outil_active[0] = "Annuler"
			self.GetTopLevelParent().rightpanel.page1.t.toolbar.back('on')
		elif self.current_tab == 1 and self.GetTopLevelParent().rightpanel.page2.flag :
			#self.outil_active[1] = "Annuler"
			self.GetTopLevelParent().rightpanel.page2.t.toolbar.back('on')
		elif  self.current_tab == 2 and self.GetTopLevelParent().rightpanel.page3.flag :
			#self.outil_active[2] = "Annuler"
			self.GetTopLevelParent().rightpanel.page3.t.toolbar.back('on')

		
	def OnRedo(self, event):
		if self.current_tab == 0:
			#if self.outil_active[0]  == "":
			#self.outil_active[0] = "Rétablir"
			self.GetTopLevelParent().rightpanel.page1.t.toolbar.forward('on')
		elif self.current_tab == 1 and self.GetTopLevelParent().rightpanel.page2.flag :
			#self.outil_active[1] = "Rétablir"
			self.GetTopLevelParent().rightpanel.page2.t.toolbar.forward('on')
		elif  self.current_tab == 2 and self.GetTopLevelParent().rightpanel.page3.flag :
			#self.outil_active = "Rétablir"
			self.GetTopLevelParent().rightpanel.page3.t.toolbar.forward('on')

		
		
	def OnPan(self, event):
		if self.current_tab == 0:
			if self.outil_active[0] != "Déplacer":
				self.outil_active[0] = "Déplacer"
			else :
				self.outil_active[0] = ""
				
			self.GetTopLevelParent().rightpanel.page1.t.toolbar.pan('on')
		elif self.current_tab == 1 and self.GetTopLevelParent().rightpanel.page2.flag :
			if self.outil_active[1] != "Déplacer":
				self.outil_active[1] = "Déplacer"
			else :
				self.outil_active[1] = ""
			self.GetTopLevelParent().rightpanel.page2.t.toolbar.pan('on')
		elif  self.current_tab == 2 and self.GetTopLevelParent().rightpanel.page3.flag :
			if self.outil_active[1] != "Déplacer":
				self.outil_active[1] = "Déplacer"
			else :
				self.outil_active[1] = ""
			self.GetTopLevelParent().rightpanel.page3.t.toolbar.pan('on')
		
	
	def OnZoom(self, event):
		if self.current_tab == 0:
			if self.outil_active[0] != "Zoomer":
				self.outil_active[0] = "Zoomer"
			else :
				self.outil_active[0] = ""
			self.GetTopLevelParent().rightpanel.page1.t.toolbar.zoom('on')
		elif self.current_tab == 1 and self.GetTopLevelParent().rightpanel.page2.flag :
			if self.outil_active[1] != "Zoomer":
				self.outil_active[1] = "Zoomer"
			else :
				self.outil_active[1] = ""
			self.GetTopLevelParent().rightpanel.page2.t.toolbar.zoom('on')
		elif  self.current_tab == 2 and self.GetTopLevelParent().rightpanel.page3.flag :
			if self.outil_active[2] != "Zoomer":
				self.outil_active[2] = "Zoomer"
			else :
				self.outil_active[2] = ""
			self.GetTopLevelParent().rightpanel.page3.t.toolbar.zoom('on')
			
			
			
	def OnRectangleSelection(self, event):
		
		if self.current_tab == 0:
			if toggle_selector.RS.active :
				toggle_selector.RS.set_active(False)
				if self.outil_active[0] == "Sélectionner":
					self.outil_active[0] = "" 
			else :
				if self.outil_active[0] == "" :
					self.outil_active[0] = "Sélectionner"
				toggle_selector.RS.set_active(True)
			
	def OnFileOpen(self, event):
		"""
		if LeftPanel.tatou_opened :
			self.leftpanel.stat1.Closing()
			LeftPanel.tatou_opened = 0
		elif LeftPanel.detect_opened :
			self.leftpanel.stat2.Closing()
			LeftPanel.detect_opened = 0
		"""
		"""
		if LeftPanel.tatou_opened :
			self.GetChildren()[-1].Close()
			LeftPanel.tatou_opened = 0
		"""
			
		text = "Shape File (*.shp)|*.shp"
		dlg = wx.FileDialog(self, "Ouvrir Fichier", os.getcwd(), "", text ,wx.OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			try :
				f = open(dlg.GetPath(), 'r')
				self.leftpanel.nom_carte.SetValue(f.name.split(os.sep)[-1])
				self.leftpanel.nom_carte.SetEditable(False)
				self.enregistrer_item.Enable(True)
				self.enregistrer_sous_item.Enable(True)
				self.reglage_item.Enable(True)
				
				self.leftpanel.reglage_btn.Enable()
				self.doc_name = f.name
				self.fileName = f.name.split(os.sep)[-1] # os separator
				self.SetTitle(self.fileName+" - "+ app_name)
				with f:
					self.doc_loaded = True
					self.t = Reader(str(self.doc_name))  #  ici, la partie ou on va Lire les donnés de la carte
					self.rightpanel.set_r2(self.t.r2)    #  charger les donnés dans un variable
					
					self.rightpanel.page1.flag = 1       # donner la permission pour dessiner le doc originale
					self.rightpanel.page1.Refresh()
					#self.rightpanel.page2.drawn = 0

					self.toolbar.EnableTool(3, True)
					self.toolbar.EnableTool(4, True)
					self.toolbar.EnableTool(5, True)
					self.toolbar.EnableTool(6, True)
					self.toolbar.EnableTool(7, True)
					self.toolbar.EnableTool(8, True)
					self.toolbar.EnableTool(9, True)
					self.toolbar.EnableTool(10, True)
					self.toolbar.EnableTool(11, True)
					self.toolbar.EnableTool(77, True)
				self.rightpanel.page1.InitDessin()
				self.Refresh()
				
			
				self.rightpanel.page1.Update()
				LeftPanel.sous_doc = []
				
				
					
				
				if self.GetTopLevelParent().rightpanel.page2.flag == 1: # si il y avait un tatouage avant on clean les autres panels, pour accepter un nouveu traitement
					self.GetTopLevelParent().rightpanel.page2.flag = False
					self.GetTopLevelParent().rightpanel.page2.draw()
					self.GetTopLevelParent().rightpanel.page2.t.Refresh()
					
				if self.GetTopLevelParent().rightpanel.page3.flag == 1: 
					self.GetTopLevelParent().rightpanel.page3.flag = False
					self.GetTopLevelParent().rightpanel.page3.draw()
					self.GetTopLevelParent().rightpanel.page3.t.Refresh()
					
					
					
				
			except IOError :
				dial = wx.MessageDialog(None,"Ne peut pas ouvrir le fichier", 'Error',wx.ICON_ERROR)
				ret = dial.ShowModal()
				if ret == wx.ID_YES:
					self.Destroy()
		dlg.Destroy()
		self.leftpanel.echelle_label.SetLabelText("	Echelle =")
		self.leftpanel.perte_precision_label.SetLabelText("	Perte de Précision =")
		self.leftpanel.nbre_partie_label.SetLabelText("	Nombre de parties = ")
		self.leftpanel.cle_label.SetValue("")
		if Reglage.reglage_done :
			self.GetTopLevelParent().leftpanel.Re_Init_Reglage()
			
		

	def OnSave(self, event):
		if (self.fileName != "") and (self.dirName != ""):
			if self.GetTopLevelParent().leftpanel.tatouage_done :
				self.GetTopLevelParent().leftpanel.res_save(self.dirName , self.fileName)
		else :
			self.OnSaveAs(event)
	

	def OnSaveAs(self, event):
		self.dirName = self.dirName[0 : self.dirName.rfind(os.sep, 0, len(self.dirName))+1]
		dlg = wx.FileDialog(self, "Enregistrer Sous", self.dirName, self.fileName,"Shape File (*.shp)|*.shp|All Files|*.*", wx.SAVE)
		
		if dlg.ShowModal() == wx.ID_OK:
			self.fileName = dlg.GetFilename()
			self.dirName = dlg.GetDirectory()
			if self.GetTopLevelParent().leftpanel.tatouage_done :
				self.GetTopLevelParent().leftpanel.res_save(self.dirName , self.fileName)

		dlg.Destroy()
	
		
	
	def ApparenceToolBar(self, e):
		if self.voir_tbar.IsChecked():
			self.toolbar.Show()
		else :
			self.toolbar.Show()
			
		
	def ApparenceStatusBar(self, e):
		if self.voir_stbar.IsChecked():
			self.st.Show()
		else :
			self.st.Show()
		
	def OnAide(self, e):
		try :
			import webbrowser
			webbrowser.open_new_tab('aide.html')
		except :
			pass
		
	
	def OnShowShortCut(self, e):
		ShortCutFrame(self)
		

	
	def OnAbout(self, e):
		#AproposFrame(self)
		description = """  est une application libre destiné à protéger les cartes géographique de type vectorielle par tatouage numérique. Il se base sur l'algorithme qui a été élaboré dans le cadre du projet Tadorne de l’ACI Sécurité et Informatique auquel participaient les laboratoires du GREYC, du Cédric CNAM, du Lamsade (Paris-Dauphine), du Le2i (Université de Bourgogne) et enfin le laboratoire Cogit de l’IGN (Institut National Géographique).
		"""
		licence = app_name + " est une application libre, vous pouvez la diffuser et/ou la modifier suivant les termes\nde la licence de la bibliotheque wxWindows telle que publiée par la Free Software Foundation,\nsoit la version 3 de cette licence soit (à votre convenance) une version ultérieure.\nPour plus d'information sur la licence visitez http://www.wxwidgets.org/about/licence/ \n"
		info = wx.AboutDialogInfo()
		info.SetIcon(wx.Icon('home.png', wx.BITMAP_TYPE_PNG))
		info.SetName('GDW')
		info.SetVersion('1.0')
		info.SetDescription(app_name + description)
		info.SetCopyright('(C) 2017 - 2016')
		#info.SetWebSite('http://www.zetcode.com')
		info.SetLicence(licence)
		info.AddDeveloper('Ould Miloud Mohamed\n <moh2012peace@hotmail.fr>')
		info.AddDeveloper('Refes Nassim\n <refes.nassim@gmail.com>')
		wx.AboutBox(info)
	

	def OnReglage(self, event): 
		self.leftpanel.new.Show()
		
		 
		
	def OnQuit(self, event):
		self.Close()		
	
	def __del__( self ):
		pass
	
if __name__ == "__main__":
	app = wx.App(False)
	frame = MainWindow(None)
	app.MainLoop()
	app.ExitMainLoop() 

