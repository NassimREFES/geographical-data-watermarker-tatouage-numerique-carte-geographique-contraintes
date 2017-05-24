# -*- coding: utf-8 -*-

from test_tatouage import *
from triangulation import Triangulation
from tatouage import *

import wx
from wx.lib.scrolledpanel import ScrolledPanel
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx, wxc
from matplotlib.figure import Figure
from numpy import *
import matplotlib as mpl
from matplotlib.widgets import RectangleSelector
import matplotlib.patches as patches
from matplotlib.patches import Polygon, Circle, RegularPolygon, Arrow
from matplotlib.collections import PatchCollection

import math

def toggle_selector(event):
	""" cette fonction est pour lancer le dessin du rectange de selection"""
	pass 			

class CustomNavToolbar(NavigationToolbar2Wx):
    def __init__(self, *args, **kwargs):
        NavigationToolbar2Wx.__init__(self, *args, **kwargs)
  
		
		


class CanvasPanel(wx.Panel): 
    w = 0
    draw_map = False
    def __init__(self, parent, sf, size, use_grid ):
        wx.Panel.__init__(self, parent, size=size)
        self.SetBackgroundColour(wxc.NamedColour("BLACK"))
        self.selection_coords = []
        self.draw_selection = False
	
        self.figure = Figure(figsize=(10, 12), dpi = 65) #figsize=(16,9))
        self.figure.set_size_inches(1,1, forward=True)
        
        
        #self.axes.xaxis.set_ticks_position('bottom')
        #self.axes.yaxis.set_ticks_position('left')
        self.axes = self.figure.add_subplot(111, frameon=False) 
        #self.axes.clear()
        #self.Refresh()
        
        user_grid = False 

        d = (0, 0, 0.999, 0.999)
        
        self.axes.get_xaxis().set_visible(False)
        self.axes.get_yaxis().set_visible(False)
    	
    	self.w, self.h = self.figure.get_size_inches()*self.figure.dpi
    	CanvasPanel.w = size[0]
    	self.axes.set_position(d) # x-top-left-corner, y-top-left-corner, x-width, y-width (in pixels)     
        self.canvas = FigureCanvas(self, -1, self.figure)
        
      
        recs    = sf.records()
        shapes  = sf.shapes
        Nshp    = len(shapes)	
        for nshp in xrange(Nshp):
			ptchs = []
			pts = array(shapes[nshp].points)
			if shapes[nshp].shapeType == 5:
				prt = shapes[nshp].parts
				par = list(prt) + [pts.shape[0]]
				for pij in xrange(len(prt)):
					ptchs.append(Polygon(pts[par[pij]:par[pij+1]]))
			else : 
				#print "type shape >> ",shapes[nshp].shapeType
				pass
			self.axes.add_collection(PatchCollection(ptchs,facecolor='none',edgecolor='black', linewidths=1.5))
        #self.axes.plot(146.661411968, -41.09612087949996, 'g+')
        #self.axes.plot(146.66141197230283, -41.096120875508596, 'r+')
        
        
        
		
        """
        circle = Circle((100, 100), 3)
        ptchs.append(circle)
        p = PatchCollection(ptchs)
        self.axes.add_collection(p)
		"""
        self.figure.canvas.mpl_connect('key_press_event', toggle_selector)
        self.figure.canvas.mpl_connect('motion_notify_event',self.StatusBarUpdate)
      
        
        
        #self.canvas.Refresh()
        CanvasPanel.draw_map  = True
        
        
        self.axes.axis('scaled') # si cet instruction n'est pas activé , il n'y aura pas d'affichage
        self.canvas.draw()
        
        
        #print self.figure.canvas.manager
        toggle_selector.RS = RectangleSelector(self.axes, self.line_select_callback,
                                       drawtype='box', useblit = False,
                                       button=[1],  # don't use middle button , button=[1, 3]
                                       minspanx=5, minspany=5,
                                       spancoords='pixels', interactive=True)
        
		
        toggle_selector.RS.set_active(False)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.toolbar = CustomNavToolbar(self.canvas)
        self.toolbar.DeleteToolByPos(6)
        
    
        
        self.sizer.Add(self.canvas, 1,wx.LEFT | wx.TOP | wx.GROW )
        self.SetSizer(self.sizer)
        self.Fit()

    def line_select_callback(self, eclick, erelease):
		x1, y1 = eclick.xdata, eclick.ydata
		x2, y2 = erelease.xdata, erelease.ydata
		self.draw_selection = True
		self.selection_coords  = [(x1, y1), (x2, y2)]
	
    def StatusBarUpdate(self, e):
		if e.inaxes:
			a,b = e.xdata, e.ydata
			#self.GetTopLevelParent().StatusBarUpdater(int(CanvasPanel.w - 10)/6  * " "+"x = "+str(a)+"  y = "+str(b)) 
			self.GetTopLevelParent().StatusBarUpdater("x = "+str(a)+",  y = "+str(b))		
		else :
			pass
			

class CarteOriginalPanel(ScrolledPanel):
	def __init__(self, parent):
		ScrolledPanel.__init__(self, parent, style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER|wx.FULL_REPAINT_ON_RESIZE)
		self.w, self.h = 500, 500
		self.t = None # pour la creation d'un canvas de dessin
		self.flag  = 0
		self.use_grid = False
		self.Bind(wx.EVT_SCROLLWIN, self.OnScroll)
		
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.SetupScrolling(1)
		
	
		self.SetScrollbars(1, 1, self.w * 2, self.h * 2, xPos = 5, yPos = 5 )
		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_SIZE, self.OnReSize)
		self.SetSizer(self.sizer)
	
	def OnScroll(self, e):
		#print e.GetPosition()
		e.Skip()
		pass
		
	def InitDessin(self):
		self.drawn = 0
		
	def OnReSize(self, e):
		self.w, self.h = self.GetClientSize()[0], self.GetClientSize()[1] -10
		#self.SetScrollbars(1, 1, self.w  + 50, self.h + 50, xPos = 10 , yPos = 100 )
		#self.Refresh()
		
			
	def OnPaint(self, e):
		self.w, self.h = self.GetClientSize()[0], self.GetClientSize()[1] -10
		self.SetBackgroundColour("WHITE")
		dc = wx.PaintDC(self)
		brush = wx.Brush("WHITE")
		dc.SetBackground(brush)
		if self.GetTopLevelParent().doc_loaded and not self.drawn : # self.flag and not self.drawn : 
			self.r2 = self.GetTopLevelParent().rightpanel.get_r2()   # avoir les shapes aprés lecture d'un shape_file
			self.draw()
		
	def draw(self, use_grid = False):
		self.use_grid = use_grid 
		self.t = CanvasPanel(self, self.r2 , (self.w , self.h ), self.use_grid)
		self.sizer.Add(self.t, 1, wx.EXPAND)
		self.drawn = 1
		
	

class CanvasPanel2(wx.Panel): 
    w = 0
    def __init__(self, parent, size, permission = False):
        wx.Panel.__init__(self, parent, size=size)
        self.SetBackgroundColour(wxc.NamedColour("BLACK"))
        self.permission = permission
    

        
	
        self.figure = Figure(dpi = 65) #figsize=(16,9))
        self.figure.set_size_inches(1,1, forward=True)
        
        
        #self.axes.xaxis.set_ticks_position('bottom')
        #self.axes.yaxis.set_ticks_position('left')
        
        self.axes = self.figure.add_subplot(111, frameon=False) #plt.subplot(111, projection="lambert")
        
       
        d = (0, 0, 0.999, 0.999)
        self.axes.get_xaxis().set_visible(False)
        self.axes.get_yaxis().set_visible(False)
    	
    	self.w, self.h = self.figure.get_size_inches()*self.figure.dpi
    	CanvasPanel2.w = size[0]
    	self.axes.set_position(d) # x-top-left-corner, y-top-left-corner, x-width, y-width (in pixels)
        
        
        
      
                                       
        self.canvas = FigureCanvas(self, -1, self.figure)
      
        if permission :
			self.axes.triplot(Triangulation.points[:,0], Triangulation.points[:, 1], Triangulation.triang)
			self.axes.plot(Triangulation.points[:,0], Triangulation.points[:, 1], 'r.')
			#Triangulation.points = []
			#Triangulation.triang = []
			
		
        
        self.figure.canvas.mpl_connect('motion_notify_event',self.StatusBarUpdate)
        
        self.canvas.draw()
       
        
        self.axes.axis('scaled') # si cet instruction n'est pas activé , il n'y aura pas d'affichage
        
       
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.toolbar = CustomNavToolbar(self.canvas)
        self.toolbar.DeleteToolByPos(6)
        
        #self.toolbar.AddLabelTool(12,'',wx.Bitmap('save_as2.png'))#wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, (16,16)))
        
        #self.toolbar.Realize()
        #self.toolbar.wx_ids['Selection'] = 500
        
        #self.sizer.Add(self.toolbar, 0,wx.LEFT | wx.TOP | wx.GROW)
        #self.toolbar.update()
        #print self.toolbar.wx_ids['Selection']
     
       
        #self.toolbar.ToggleTool(self.toolbar.wx_ids['Pan'], False)
        
       
        
        
        
        
        
        
        self.sizer.Add(self.canvas, 1,wx.LEFT | wx.TOP | wx.GROW )
        self.SetSizer(self.sizer)
        self.Fit()

		
		
	
    def StatusBarUpdate(self, e):
		if e.inaxes:
			if self.permission :
				a,b = e.xdata, e.ydata
				#self.GetTopLevelParent().StatusBarUpdater(int(CanvasPanel2.w - 10)/6  * " "+"x = "+str(a)+"  y = "+str(b)) 
				self.GetTopLevelParent().StatusBarUpdater("x = "+str(a)+",  y = "+str(b))
			#else :
			#	self.GetTopLevelParent().StatusBarUpdater("") 
		else :
			self.GetTopLevelParent().StatusBarUpdater("")
				

class TriangulationPanel(ScrolledPanel):
	def __init__(self, parent):
		ScrolledPanel.__init__(self, parent, style = wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
		self.w, self.h = 500, 500
		self.t = None # pour la creation d'un canvas de dessin
		self.flag  = 0
		self.drawn = 0
		
		
		
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.SetupScrolling(1)
	
		#self.SetScrollbars(1, 1, self.w * 2, self.h * 2, xPos = 0, yPos = 0 )
		self.Bind(wx.EVT_PAINT, self.OnPaint)
		#self.Bind(wx.EVT_SIZE, self.OnReSize)
		self.SetSizer(self.sizer)
	
		
	def OnReSize(self, e):
		self.w, self.h = self.GetClientSize()[0], self.GetClientSize()[1] -10
		#self.SetScrollbars(1, 1, self.w  + 50, self.h + 50, xPos = 10 , yPos = 100 )
		"""
		if CanvasPanel.draw_map :
			self.t.axes.clear()
			self.draw(self.use_grid)
			
		"""
		self.Refresh()
		
			
	def OnPaint(self, e):
		self.draw()
			
	def draw(self, color = "WHITE"):
		self.w, self.h = self.GetClientSize()[0], self.GetClientSize()[1] -10
		self.SetBackgroundColour(color)
		dc = wx.PaintDC(self)
		brush = wx.Brush(color)
		dc.SetBackground(brush)
		
		if self.flag and Triangulation.tri_done and not self.drawn :
			self.t = CanvasPanel2(self,  (self.w , self.h ), True)
			self.sizer.Add(self.t, 1, wx.EXPAND)
			self.drawn = 0
			
		elif not self.flag : # ici pour redémarrer un nouveu traitemnt , en cas il y avait un autre avant
			Triangulation.tri_done = False 
			self.t = CanvasPanel2(self,  (self.w , self.h ))
			self.sizer.Add(self.t, 1, wx.EXPAND)
			#self.drawn = 1
			
			
			
		


class CanvasPanel3(wx.Panel): 
    w = 0
    draw_map = False
    def __init__(self, parent, sf, shapes2, size, use_grid , permission = False, sites_bouger = []):
        wx.Panel.__init__(self, parent, size=size)
        self.SetBackgroundColour(wxc.NamedColour("BLACK"))
        self.permission = permission
      

        
	
        self.figure = Figure(dpi = 65) #figsize=(16,9))
        self.figure.set_size_inches(1,1, forward=True)
        
        
        #self.axes.xaxis.set_ticks_position('bottom')
        #self.axes.yaxis.set_ticks_position('left')
        self.axes = self.figure.add_subplot(111, frameon=False) #plt.subplot(111, projection="lambert")
        
        user_grid = False 
        if use_grid :
			
			
			d = (0, 0.01, 0.99, 0.99)
			self.axes.grid(use_grid)
		
			
        else :
			#self.axes = self.figure.add_subplot(111, frameon=False)
			d = (0, 0, 0.999, 0.999)
			self.axes.get_xaxis().set_visible(False)
			self.axes.get_yaxis().set_visible(False)
    	
    	self.w, self.h = self.figure.get_size_inches()*self.figure.dpi
    	CanvasPanel3.w = size[0]   
    	self.axes.set_position(d) # x-top-left-corner, y-top-left-corner, x-width, y-width (in pixels)
        
        self.canvas = FigureCanvas(self, -1, self.figure)
  
        if permission :
			self.axes.clear()
			self.canvas.Update()
			recs    = sf.records()
			
			shapes  = sf.shapes
			Nshp    = len(shapes)
			"""
			for nshp in xrange(Nshp):
				ptchs = []
				pts = array(shapes[nshp].points)
				if shapes[nshp].shapeType == 5:
					prt = shapes[nshp].parts
					par = list(prt) + [pts.shape[0]]
					for pij in xrange(len(prt)):
						ptchs.append(Polygon(pts[par[pij]:par[pij+1]]))
			
				self.axes.add_collection(PatchCollection(ptchs,facecolor='none',edgecolor='b', linewidths=2))
			"""
			
			"""
			data = [(50, 50), (70, 70)]
			pp = []
			for x, y in data :
				c = Circle((x,y), 0.5)
				pp.append(c)
			
			p = PatchCollection(pp, cmap=mpl.cm.jet, alpha=0.4)
			self.axes.add_collection(PatchCollection(p,facecolor='none',edgecolor='r', linewidths=2))
			"""
			#self.axes.scatter(50, 50, s=10, c='g', marker='^', label='Two Fires')
			#print "Len shapes :", len(shapes)
			
			
			"""
			for obj in range(0, len(shapes)):
						for pt in range(0, len(shapes[obj].points)):
							if shapes[obj].points[pt] != shapes2[obj].points[pt]:
								print "------------------------------------"
								print "Not equal !"
								print "Original :",shapes[obj].points[pt], obj, pt
								print "Modifie :",shapes2[obj].points[pt], obj, pt
			"""
			

			#t = [ [147.83058185027457, -42.27884684129017] ,[146.66141197230283, -41.096120875508596] ]
			
			self.axes.triplot(Triangulation.points[:,0], Triangulation.points[:, 1], Triangulation.triang)
			self.axes.plot(Triangulation.points[:,0], Triangulation.points[:, 1], 'r.')				
			
			

			
			
			shapes  = shapes2
			Nshp    = len(shapes)
			import random
			color = random.choice(["g", "r", "y" ])
			for nshp in xrange(Nshp):
				ptchs = []
				pts = array(shapes[nshp].points)
				if shapes[nshp].shapeType == 5:
					prt = shapes[nshp].parts
					par = list(prt) + [pts.shape[0]]
					for pij in xrange(len(prt)):
						ptchs.append(Polygon(pts[par[pij]:par[pij+1]]))
				self.axes.add_collection(PatchCollection(ptchs,facecolor='none',edgecolor="black", linewidths=1.5))
			"""
			pp = [
			      [146.661411968, -41.09612087949996] , [146.66141197230283, -41.096120875508596]

					#(142.89579288266205, -43.922664989702909), 
					#(142.89579288266205, -43.922664989702909)
				]
			"""
			#ptchs.append(Circle(pp[0], 0.001))
			
			
			
			
			#self.axes.add_collection(PatchCollection(ptchs,facecolor='r',edgecolor="r", linewidths= 5))
			#ptchs.append(Circle(pp[1], 0.001))
			#self.axes.add_collection(PatchCollection(ptchs,facecolor='g',edgecolor="g", linewidths= 0.1, alpha=0.9))
			original = {
					'family': 'Courier New',
					'color':  'green',
					'weight': 'bold',
					'size': 12,
					}
			modified = {
					'family': 'Courier New',
					'color':  'red',
					'weight': 'bold',
					'size': 12,
					}
			
			
			usb = self.GetTopLevelParent().rightpanel.get_original_per_sites_bouger()
			
			
			for pp in sites_bouger :
				self.axes.plot(pp[0][0][0], pp[0][0][1], 'r+') # modifie
				self.axes.plot(pp[1][0][0], pp[1][0][1], 'g+') # original
				#self.axes.text(pp[0][0][0], pp[0][0][1], "Modifie" , fontdict = modified, ha='left')
				#self.axes.text(pp[1][0][0], pp[1][0][1], "Original" , fontdict = original, ha='left')	
				for tt in usb:
					if tt == complex(pp[0][0][0],pp[0][0][1]) : 
						v = usb[tt]
						self.axes.text(pp[0][0][0], pp[0][0][1], u"Modifié ( " + str(v[2])+" )", fontdict = modified, ha='left')
						self.axes.text(pp[1][0][0], pp[1][0][1], "Original ( " + str(v[3])+" )", fontdict = original, ha='left')
        
        self.figure.canvas.mpl_connect('motion_notify_event',self.StatusBarUpdate)
        
        
        self.canvas.draw()
        CanvasPanel.draw_map  = True
        
        self.axes.axis('scaled') # si cet instruction n'est pas activé , il n'y aura pas d'affichage
        
       
        
		
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.toolbar = CustomNavToolbar(self.canvas)
        self.toolbar.DeleteToolByPos(6)
        
        self.sizer.Add(self.canvas, 1,wx.LEFT | wx.TOP | wx.GROW )
        self.SetSizer(self.sizer)
        self.Fit()

  

		
		
	
    def StatusBarUpdate(self, e):
		if e.inaxes:
			if self.permission :
				a,b = e.xdata, e.ydata
				self.GetTopLevelParent().StatusBarUpdater("x = "+str(a)+",  y = "+str(b))
				
		else :
			self.GetTopLevelParent().StatusBarUpdater("")
			

class TatouagePanel(ScrolledPanel):
	def __init__(self, parent):
		ScrolledPanel.__init__(self, parent, style = wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER)
		self.w, self.h = 500, 500
		self.t = None # pour la creation d'un canvas de dessin
		self.flag  = 0
		self.use_grid = False
		self.drawn = 0
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.SetupScrolling(1)
	
		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_SIZE, self.OnReSize)
		self.SetSizer(self.sizer)
		
		
	def OnReSize(self, e):
		self.w, self.h = self.GetClientSize()[0], self.GetClientSize()[1] -10
		self.Refresh()
		
			
	def OnPaint(self, e):
		self.w, self.h = self.GetClientSize()[0], self.GetClientSize()[1] -10
		self.SetBackgroundColour("WHITE")
		dc = wx.PaintDC(self)
		brush = wx.Brush("WHITE")
		dc.SetBackground(brush)
		self.draw()

			
	def draw(self, use_grid = False):
		if self.flag and not self.drawn :
			self.r2 = self.GetTopLevelParent().rightpanel.get_r2() # avoir les shapes aprés lecture d'un shape_file
			self.shapes2 = self.GetTopLevelParent().rightpanel.get_shapes() # avoir les shapes aprés lecture d'un shape_file
			self.use_grid = use_grid 
			self.t = CanvasPanel3(self, self.r2, self.shapes2, (self.w , self.h ), self.use_grid, True , self.GetTopLevelParent().rightpanel.get_sites_bouger())
			self.sizer.Add(self.t, 1, wx.EXPAND)
			self.drawn = 1
		
		elif not self.flag  :
			self.use_grid = use_grid 
			self.t = CanvasPanel3(parent = self, sf = None, shapes2 = None, size = (self.w , self.h ), use_grid = self.use_grid , permission =  False  )
			self.sizer.Add(self.t, 1, wx.EXPAND)
			self.drawn = 1



class RightPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, style = wx.BORDER_RAISED)# style=wx.SUNKEN_BORDER)
		self.nb = wx.Notebook(self)
		self.nb.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT,
                         wx.FONTWEIGHT_NORMAL, 
                         wx.FONTSTYLE_NORMAL))
		
		self.r2 = ''
		self.shapes2 = '' # shapes modifié aprés tatouage
		self.sites_bouger = []
		self.usb = {} # pour indice des objets bouger
		self.page1 = CarteOriginalPanel(self.nb) 
		self.page2 = TriangulationPanel(self.nb)
		self.page3 = TatouagePanel(self.nb)
		
		
		self.nb.AddPage(self.page1, "Carte Original")
		self.nb.AddPage(self.page2, "Carte Triangulé")
		self.nb.AddPage(self.page3, "Carte Tatoué ")
		self.nb.SetForegroundColour("black")
		
		self.page1.SetFocus()
		self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
	
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.nb, 2, wx.EXPAND|wx.ALL, 5)
		self.SetSizer(sizer)
		
	def OnPageChanged(self, e):
		self.GetTopLevelParent().current_tab = e.GetSelection()
		if e.GetSelection() in  [1, 2]:
			self.GetTopLevelParent().toolbar.EnableTool(11, False)
			
		else :
			if self.GetTopLevelParent().doc_loaded:
				self.GetTopLevelParent().toolbar.EnableTool(11, True)
			
		
			
		
	def set_r2(self, r2):
		self.r2 = r2
		
	def get_r2(self):
		return self.r2
		
	def set_shapes(self, shapes2):
		self.shapes2 = shapes2
		
	def get_shapes(self):
		return self.shapes2
		
	def set_sites_bouger(self, sb):
		self.sites_bouger = sb
	
	def get_sites_bouger(self):
		return self.sites_bouger
		
	def set_original_per_sites_bouger(self, arg):
		self.usb = arg
		
	def get_original_per_sites_bouger(self):
		return self.usb
	

		
		
		
		
		
