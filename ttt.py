"""
import wx

class View(wx.Panel):
    def __init__(self, parent):
        super(View, self).__init__(parent)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_PAINT, self.on_paint)
    def on_size(self, event):
        event.Skip()
        self.Refresh()
    def on_paint(self, event):
        w, h = self.GetClientSize()
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        dc.DrawLine(0, 0, w, h)
        dc.SetPen(wx.Pen(wx.BLACK, 5))
        dc.DrawCircle(w / 2, h / 2, 100)

class Frame(wx.Frame):
    def __init__(self):
        super(Frame, self).__init__(None)
        self.SetTitle('My Title')
        self.SetClientSize((500, 500))
        self.Center()
        self.view = View(self)

def main():
    app = wx.App(False)
    frame = Frame()
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
	
"""
"""
This demo demonstrates how to embed a matplotlib (mpl) plot 
into a wxPython GUI application, including:
* Using the navigation toolbar
* Adding data to the plot
* Dynamically modifying the plot's properties
* Processing mpl events
* Saving the plot to a file from a menu
The main goal is to serve as a basis for developing rich wx GUI
applications featuring mpl plots (using the mpl OO API).
Eli Bendersky (eliben@gmail.com)
License: this code is in the public domain
Last modified: 30.07.2008
"""

"""
import os
import pprint
import random
import wx

# The recommended way to use wx with mpl is with the WXAgg
# backend. 
#
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar


class BarsFrame(wx.Frame):
   
    title = 'Demo: wxPython with matplotlib'
    
    def __init__(self):
        wx.Frame.__init__(self, None, -1, self.title)
        
        self.data = [5, 6, 9, 14]
        
        self.create_menu()
        self.create_status_bar()
        self.create_main_panel()
        
        self.textbox.SetValue(' '.join(map(str, self.data)))
        self.draw_figure()

    def create_menu(self):
        self.menubar = wx.MenuBar()
        
        menu_file = wx.Menu()
        m_expt = menu_file.Append(-1, "&Save plot\tCtrl-S", "Save plot to file")
        self.Bind(wx.EVT_MENU, self.on_save_plot, m_expt)
        menu_file.AppendSeparator()
        m_exit = menu_file.Append(-1, "E&xit\tCtrl-X", "Exit")
        self.Bind(wx.EVT_MENU, self.on_exit, m_exit)
        
        menu_help = wx.Menu()
        m_about = menu_help.Append(-1, "&About\tF1", "About the demo")
        self.Bind(wx.EVT_MENU, self.on_about, m_about)
        
        self.menubar.Append(menu_file, "&File")
        self.menubar.Append(menu_help, "&Help")
        self.SetMenuBar(self.menubar)

    def create_main_panel(self):
       
        self.panel = wx.Panel(self)
        
        # Create the mpl Figure and FigCanvas objects. 
        # 5x4 inches, 100 dots-per-inch
        #
        self.dpi = 100
        self.fig = Figure((5.0, 4.0), dpi=self.dpi)
        self.canvas = FigCanvas(self.panel, -1, self.fig)
        
        # Since we have only one plot, we can use add_axes 
        # instead of add_subplot, but then the subplot
        # configuration tool in the navigation toolbar wouldn't
        # work.
        #
        self.axes = self.fig.add_subplot(111)
        
        # Bind the 'pick' event for clicking on one of the bars
        #
        self.canvas.mpl_connect('pick_event', self.on_pick)
        
        self.textbox = wx.TextCtrl(
            self.panel, 
            size=(200,-1),
            style=wx.TE_PROCESS_ENTER)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_text_enter, self.textbox)
        
        self.drawbutton = wx.Button(self.panel, -1, "Draw!")
        self.Bind(wx.EVT_BUTTON, self.on_draw_button, self.drawbutton)

        self.cb_grid = wx.CheckBox(self.panel, -1, 
            "Show Grid",
            style=wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_CHECKBOX, self.on_cb_grid, self.cb_grid)

        self.slider_label = wx.StaticText(self.panel, -1, 
            "Bar width (%): ")
        self.slider_width = wx.Slider(self.panel, -1, 
            value=20, 
            minValue=1,
            maxValue=100,
            style=wx.SL_AUTOTICKS | wx.SL_LABELS)
        self.slider_width.SetTickFreq(10, 1)
        self.Bind(wx.EVT_COMMAND_SCROLL_THUMBTRACK, self.on_slider_width, self.slider_width)

        # Create the navigation toolbar, tied to the canvas
        #
        self.toolbar = NavigationToolbar(self.canvas)
        
        #
        # Layout with box sizers
        #
        
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.vbox.Add(self.toolbar, 0, wx.EXPAND)
        self.vbox.AddSpacer(10)
        
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        flags = wx.ALIGN_LEFT | wx.ALL | wx.ALIGN_CENTER_VERTICAL
        self.hbox.Add(self.textbox, 0, border=3, flag=flags)
        self.hbox.Add(self.drawbutton, 0, border=3, flag=flags)
        self.hbox.Add(self.cb_grid, 0, border=3, flag=flags)
        self.hbox.AddSpacer(30)
        self.hbox.Add(self.slider_label, 0, flag=flags)
        self.hbox.Add(self.slider_width, 0, border=3, flag=flags)
        
        self.vbox.Add(self.hbox, 0, flag = wx.ALIGN_LEFT | wx.TOP)
        
        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)
    
    def create_status_bar(self):
        self.statusbar = self.CreateStatusBar()

    def draw_figure(self):
       
        str = self.textbox.GetValue()
        self.data = map(int, str.split())
        x = range(len(self.data))

        # clear the axes and redraw the plot anew
        #
        self.axes.clear()        
        self.axes.grid(self.cb_grid.IsChecked())
        
        self.axes.bar(
            left=x, 
            height=self.data, 
            width=self.slider_width.GetValue() / 100.0, 
            align='center', 
            alpha=0.44,
            picker=5)
        
        self.canvas.draw()
    
    def on_cb_grid(self, event):
        self.draw_figure()
    
    def on_slider_width(self, event):
        self.draw_figure()
    
    def on_draw_button(self, event):
        self.draw_figure()
    
    def on_pick(self, event):
        # The event received here is of the type
        # matplotlib.backend_bases.PickEvent
        #
        # It carries lots of information, of which we're using
        # only a small amount here.
        # 
        box_points = event.artist.get_bbox().get_points()
        msg = "You've clicked on a bar with coords:\n %s" % box_points
        
        dlg = wx.MessageDialog(
            self, 
            msg, 
            "Click!",
            wx.OK | wx.ICON_INFORMATION)

        dlg.ShowModal() 
        dlg.Destroy()        
    
    def on_text_enter(self, event):
        self.draw_figure()

    def on_save_plot(self, event):
        file_choices = "PNG (*.png)|*.png"
        
        dlg = wx.FileDialog(
            self, 
            message="Save plot as...",
            defaultDir=os.getcwd(),
            defaultFile="plot.png",
            wildcard=file_choices,
            style=wx.SAVE)
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.canvas.print_figure(path, dpi=self.dpi)
            self.flash_status_message("Saved to %s" % path)
        
    def on_exit(self, event):
        self.Destroy()
        
    def on_about(self, event):
        
        dlg = wx.MessageDialog(self, msg, "About", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
    
    def flash_status_message(self, msg, flash_len_ms=1500):
        self.statusbar.SetStatusText(msg)
        self.timeroff = wx.Timer(self)
        self.Bind(
            wx.EVT_TIMER, 
            self.on_flash_status_off, 
            self.timeroff)
        self.timeroff.Start(flash_len_ms, oneShot=True)
    
    def on_flash_status_off(self, event):
        self.statusbar.SetStatusText('')


if __name__ == '__main__':
    app = wx.PySimpleApp()
    app.frame = BarsFrame()
    app.frame.Show()
    app.MainLoop()
"""

'''This example demonstrates how to:
* Modify the Toolbar
* Create tools
* Add tools
* Remove tools
Using `matplotlib.backend_managers.ToolManager`
'''

"""
Combines :class:`~lib.floatcanvas.FloatCanvas.FloatCanvas` with Navigation
controls onto a :class:`Panel`
In the following very simple sample ``self`` is a frame, but it could be another
container type control::
    from wx.lib.floatcanvas import NavCanvas, FloatCanvas
    #Add the Canvas
    self.Canvas = NavCanvas.NavCanvas(self, -1,
                                 size=(500, 500),
                                 ProjectionFun=None,
                                 Debug=0,
                                 BackgroundColor="White",
                                 ).Canvas
    # add a circle
    cir = FloatCanvas.Circle((10, 10), 100)
    self.Canvas.AddObject(cir)
    
    # add a rectangle
    rect = FloatCanvas.Rectangle((110, 10), (100, 100), FillColor='Red')
    self.Canvas.AddObject(rect)
    
    self.Canvas.Draw()
    
Many samples are available in the `wxPhoenix/samples/floatcanvas` folder.
        
"""
#!/usr/bin/env python
"""
An example of how to use wx or wxagg in an application with the new
toolbar - comment out the setA_toolbar line for no toolbar
"""
"""
import wx 
import time 
class Mywin(wx.Frame): 
            
   def __init__(self, parent, title): 
      super(Mywin, self).__init__(parent, title = title,size = (300,200))  
      self.InitUI() 
         
   def InitUI(self):    
      self.count = 0 
      pnl = wx.Panel(self) 
      vbox = wx.BoxSizer(wx.VERTICAL)
		
      hbox1 = wx.BoxSizer(wx.HORIZONTAL) 
      hbox2 = wx.BoxSizer(wx.HORIZONTAL)
		
      self.gauge = wx.Gauge(pnl, size = (250, 25), style =  wx.GA_HORIZONTAL) 
      self.gauge.SetRange(20)
      self.btn1 = wx.Button(pnl, label = "Start") 
      self.Bind(wx.EVT_BUTTON, self.OnStart, self.btn1) 
		
      hbox1.Add(self.gauge, proportion = 1, flag = wx.ALIGN_CENTRE) 
      hbox2.Add(self.btn1, proportion = 1, flag = wx.RIGHT, border = 10) 
         
      vbox.Add((0, 30)) 
      vbox.Add(hbox1, flag = wx.ALIGN_CENTRE) 
      vbox.Add((0, 20)) 
      vbox.Add(hbox2, proportion = 1, flag = wx.ALIGN_CENTRE) 
      pnl.SetSizer(vbox) 
         
      self.SetSize((300, 200)) 
      self.Centre() 
      self.Show(True)   
		
   def OnStart(self, e): 
      while True: 
         time.sleep(1); 
         self.count = self.count + 1 
         self.gauge.SetValue(int(self.count)) 
			
         if self.count >= 20: 
            print "end" 
            return 
				
ex = wx.App() 
Mywin(None,'wx.Gauge') 
ex.MainLoop()
"""
import wx
class MyApp(wx.App):
    def OnInit(self):
        frame = MainWindow("ST v2.0.0", (50, 60), (458, 332))
        frame.Show()
        self.SetTopWindow(frame)
        return True



class MainWindow(wx.Frame):
    def __init__(self, pos, size, title):
        wx.Frame.__init__(self, None, -1, pos, size, title)


        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetBackgroundColour('LIGHT GREY')
        toolbar = self.CreateToolBar()
        toolbar.Realize()
        menuFile = wx.Menu()
        menuFile.Append(1, "&About...")
        menuFile.AppendSeparator()
        menuFile.Append(2, "E&xit")
        menuBar = wx.MenuBar()
        menuBar.Append(menuFile, "&File")
        menu2 = wx.Menu()
        menu2.Append(wx.NewId(), "&Copy", "Copy in status bar")
        menu2.AppendSeparator()
        menu2.Append(wx.NewId(), "C&ut", "")
        menu2.AppendSeparator()
        menu2.Append(wx.NewId(), "Paste", "")
        menu2.AppendSeparator()
        menu2.Append(wx.NewId(), "&Options...", "Display Options")
        menuBar.Append(menu2, "&Edit")

        self.SetMenuBar(menuBar)
        self.CreateStatusBar()
        self.SetStatusText("Welcome to sQAST!")#can put connected here when logged in
        #self.Bind(wx.EVT_MENU, self.OnAbout, id=1)
        #self.Bind(wx.EVT_MENU, self.OnQuit, id=2)

        x = 100

        #Progress Gauge
        self.gauge = wx.Gauge(panel, -1, x ,pos=(180, 0), size=(-1, 20))



        #Close button
        self.button = wx.Button(panel, label="EXIT", pos=(229, 160), size=(229, 80))
        #self.Bind(wx.EVT_BUTTON, self.OnQuit, self.button)
        #self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        #Dispenser button
        self.button2 = wx.Button(panel, label="Serv 1", pos=(0, 160), size=(229, 80))
        self.Bind(wx.EVT_BUTTON, self.OnStartButton, self.button2)
        #Site Server
        self.button3 = wx.Button(panel, label="SERV 2", pos=(0, 80), size=(229, 80))
        self.Bind(wx.EVT_BUTTON, self.OnSiteservButton, self.button3)
        #Local Search
        self.button4 = wx.Button(panel, label="ABORT", pos=(229, 80), size=(229, 80))
        self.Bind(wx.EVT_BUTTON, self.OnAbortButton, self.button4)
        self.button4.Disable()
        self.shouldAbort = False 
x = wx.App() 
MyApp(None,'wx.Gauge') 
ex.MainLoop()
