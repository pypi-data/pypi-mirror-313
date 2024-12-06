import matplotlib.pyplot as plt
import numpy as np
import ipywidgets as widgets
from matplotlib.lines import Line2D
import os
import base64
import pickle

objs = []
names = []

par_form="{:.6g}" # format for parameters in boxes.
datsize=4.5 # size of data points on both graphs
ptsize=2.5 # size of markers that shown line "end points"

def get_file_name(fname):
    # fname = "".join(i if i.isalnum() else "_" for i in fname)
    # create safe filename.
    fname = base64.urlsafe_b64encode(bytes(fname,'utf-8')).decode('utf-8')
    base, name = os.path.split(os.environ['JPY_SESSION_NAME'])

    if len(name)>6:
        if name[-6:] == '.ipynb':
            name = name[0:-6]
    name = '.' + name
    newname = name+'-'+fname
    newname = os.path.join(base,newname)
    return newname

class generic_fit_with_background:
    """Generic Class for creating fit objects

    Parameters:
    name: a unique name that is used as a plot title as well as for tagging the fit parameters
    xdata: x values of the data
    ydata: y values
    yerr: uncertainties in y values
    use_background: a boolean. If false we just do a linear fit, if true the function is
            np.log(np.exp(self.intercept)*np.exp(self.cxp*self.slope)+np.exp(self.yoff))
    input_boxes: a boolean. If True display boxes that allow manual setting of parameters
    """
    
    def update_displays(self): # update the graphs and other output
        # store graph limits so if the user set them they persist:
        xl = self.ax[1].get_xlim()
        yl = self.ax[1].get_ylim()
        self.line.set_data(self.cxp, self.cyp) 
        self.line2.set_data(self.xp, self.yp)
             
        self.ax[0].cla()
        self.ax[0].errorbar(self.xdata,self.residuals,self.yerr, fmt='bo',markersize=datsize)
        self.ax[0].plot((np.min(self.xdata),np.max(self.xdata)),(0,0),'k-')
        self.ax[0].plot(self.xp,(0,0), 'bo', markersize=ptsize)
        self.ax[0].title.set_text('Residuals')
        self.ax[1].set_xlim(xl)
        self.ax[1].set_ylim(yl)
        
        self.fig.canvas.draw_idle()
        
        self.out.clear_output()
        self.print_output("", self.chi2)
        # save state:
        try:
            ff = open(self.filename, 'wb') 
            pickle.dump((self.xp, self.yp, self.yoff), ff)
            ff.close()
            # with self.out:
            #    print("saving to:",self.filename)
        except:
           with self.out:
               print("Back-up file saving failed?")
    
    def calc_yp(self): # calculate the yp values
        self.yp = self.xp * self.slope + self.intercept
       
        
    def slope_changed(self, change):
        if self.no_recur:
            return
        #  check that its a valid number, if not reset:
        # with self.out:
        #     print("in slope_changed")
        try:
            new_val = float(change.new)
            self.slope = new_val
            self.no_recur = True
            self.slopewidget.value = par_form.format(self.slope)
            self.no_recur = False
        except:
            self.no_recur = True
            self.slopewidget.value = par_form.format(self.slope)
            self.no_recur = False
            return
        # set new yp values and update display
        self.calc_yp()
        self.calc_fit()
        self.update_displays()
        
    def int_changed(self, change):
        if self.no_recur:
            return
        try:
            new_val = float(change.new)
            self.intercept = new_val
            self.no_recur = True
            self.intwidget.value = par_form.format(self.intercept)
            self.no_recur = False
        except:
            self.no_recur = True
            self.intwidget.value = par_form.format(self.intercept)
            self.no_recur = False
            return
        self.calc_yp()
        self.calc_fit()
        self.update_displays()
        
    def offset_changed(self, change):
        if self.no_recur:
            return
        try:
            new_val = float(change.new)
            self.yoff = new_val
            self.no_recur = True
            self.offwidget.value = par_form.format(self.yoff)
            self.no_recur = False
        except:
            self.no_recur = True
            self.offwidget.value = par_form.format(self.yoff)
            self.no_recur = False
            return
        self.calc_yp()
        self.calc_fit()
        self.update_displays()
        
        
    def calc_fit(self):
        self.slope = (self.yp[1]-self.yp[0])/(self.xp[1]-self.xp[0])
        self.intercept = self.yp[1]-self.slope*self.xp[1]

        if self.use_background:
            self.residuals = self.ydata - np.log(np.exp(self.intercept)*np.exp(self.xdata*self.slope)+np.exp(self.yoff))
            self.cyp = np.log(np.exp(self.intercept)*np.exp(self.cxp*self.slope)+np.exp(self.yoff))
        else:
            self.residuals = self.ydata - self.intercept-self.xdata*self.slope
            self.cyp = self.intercept+self.cxp*self.slope
    
    def print_output(self, message, chi2):
        with self.out:
            if message != "":
                print(message)
            if self.use_background:
                if self.slope != 0:
                    print("R0: %.6g, Attenuation Coef: %.6g, Background: %.6g"%(np.exp(self.intercept), -self.slope, np.exp(self.yoff)))
            else:
                if self.input_boxes == False:
                    print("slope: %.6g, intercept: %.6g"%(self.slope, self.intercept))
            if chi2:
                chi2val = np.sum(self.residuals*self.residuals/self.yerr/self.yerr) 
                if self.use_background:
                    chi2val = chi2val/(len(self.residuals) - 3)
                else:
                    chi2val = chi2val/(len(self.residuals) - 2)
                print("Chi2: %.4g"%(chi2val))
        
    def __init__ (self, name, xdata, ydata, yerr, use_background, chi2, input_boxes):
        global objs, names

        if not isinstance(xdata,np.ndarray):
            print("xdata must be a numpy array")
            return
        if not isinstance(ydata,np.ndarray):
            print("ydata must be a numpy array")
            return
        if not isinstance(yerr,np.ndarray):
            print("yerr must be a numpy array")
            return
        if xdata.ndim != 1 or ydata.ndim != 1 or yerr.ndim !=1:
            print("Data arrays must be one-dimensional")
            return
        if (len(xdata) < 2):
            print("Must have at least 2 data points!")
            return
        if len(ydata) != len(xdata) or len(yerr) != len (xdata):
            print("xdata, ydata and yerr must all have the same number of elements:", len(xdata), len(ydata), len(yerr))
            return    
        if name == "":
            print("Name must not be empty!")
            return
            
        plt.ioff()
        
        # look for our object in the current module's list of objects:        
        found_old = False
        for i in range(len(objs)):
            if name == names[i]:
                self = objs[i]
                found_old = True
                message = "Used fit values from previous invocation"
 
        # even so, update with current data        
        self.xdata = xdata
        self.ydata = ydata
        self.yerr = yerr
        self.chi2 = chi2
        self.use_background = use_background
        self.input_boxes = input_boxes
        # self.no_recur=False
        if found_old == False:
            # we're creating a new object:
            self.filename = get_file_name(name)  
            # self.name = name # not needed
            self.no_recur = False
            objs.append(self)
            names.append(name)
            loaded = False
            # here we should see if there is a file that has it. If so,
            # load xp, yp and yoff from it
            message = "No previous fit parameters"
            try:
                ff = open(self.filename, 'rb')
                self.xp, self.yp, self.yoff = pickle.load(ff)
                if not isinstance(self.xp, np.ndarray):
                    self.xp = np.array(self.xp)
                    self.yp = np.array(self.yp)
                ff.close()
                loaded = True
                message = "Loaded fit values from file"
            except:
                pass
            if not loaded:
                self.xp=np.array([0.0,0.0]) # xp yp are end points of selected line.
                self.yp=np.array([0.0,0.0])
            
                self.yoff = -4e9
                self.yp[0] = np.average(ydata)
                self.yp[1] = self.yp[0]
                self.xp[0] = np.min(xdata)
                self.xp[1] = np.max(xdata)
                
        
        if self.use_background:
            self.cxp = np.linspace(np.min(xdata), np.max(xdata),100)
            self.cyp = np.zeros(100) # cxp, cyp are points for fitted curve
        else:
            self.cxp = np.array((np.min(xdata), np.max(xdata)))
            self.cyp = np.zeros(2)


        self.calc_fit()
        #fig = plt.figure("myfig2",figsize=(6,8))
        plt.close(name)
        self.fig = plt.figure(name)
        # make y axes about 30% bigger than default:
        self.fig.set_figheight(self.fig.get_figheight()*1.3)
        self.fig.tight_layout()
        self.fig.canvas.toolbar_visible = False
        self.fig.canvas.header_visible = False
        self.ax = self.fig.subplots(2, sharex=True, height_ratios=[1, 2])

        self.ax[0].errorbar(xdata,self.residuals,yerr, fmt='bo', markersize=datsize)
        self.ax[0].plot((np.min(xdata),np.max(xdata)),(0,0),'k-')
        self.ax[0].plot(self.xp,(0,0), "bo", markersize=ptsize)
        self.ax[0].title.set_text('Residuals')
        self.fig.canvas.mpl_connect("button_press_event", self.onclick) # could do motion_notify_event, on_move(onmove?)
        self.line = Line2D(self.cxp,self.cyp)
        self.line2 = Line2D(self.xp,self.yp,marker='o',linestyle='',markersize=ptsize)
        self.ax[1].title.set_text(name)
        self.ax[1].errorbar(xdata,ydata,yerr, fmt='ro', label = "Data",markersize=datsize)
        self.ax[1].add_line(self.line)
        self.ax[1].add_line(self.line2)
        self.line.set_label("Fit")
        self.out = widgets.Output()
        
        self.button = widgets.RadioButtons(options=["Linear Slope/Intercept","Floor"]) # we look up its value later even if it doesn't appear.

        # We use text widgets so we can format numbers reasonably. with FloatText there's no way to control the formatting.
        self.slopewidget=widgets.Text(value=par_form.format(self.slope), description='Slope:', continuous_update=False)
        self.intwidget=widgets.Text(value=par_form.format(self.intercept), description='Intercept:', disabled=False, continuous_update=False)
        self.offwidget=widgets.Text(value=par_form.format(self.yoff), description='Floor:', disabled=False, continuous_update=False)
        #self.slopewidget=widgets.FloatText(value=self.slope, description='Slope:')
        #self.intwidget=widgets.FloatText(value=self.intercept, description='Intercept:')
        #self.offwidget=widgets.FloatText(value=self.yoff, description='Y offset:')

        self.slopewidget.observe(self.slope_changed, names='value')
        self.intwidget.observe(self.int_changed,names='value')
        self.offwidget.observe(self.offset_changed,names='value')
        
        if self.use_background:
            if self.input_boxes:
                app = widgets.AppLayout(
                    header=self.fig.canvas,
                    left_sidebar=widgets.HBox([self.slopewidget,self.intwidget,self.offwidget]),
                    footer=widgets.HBox([self.button,self.out]),
                    pane_heights=[12, 1, 1],grid_gap="1px",align_items='center',
                    pane_widths=[1,0,20])
            else:
                app = widgets.AppLayout(
                    header=self.fig.canvas,
                    left_sidebar=self.button,            
                    right_sidebar=self.out,
                    pane_heights=[12, 1, 0],grid_gap="1px",align_items='center',
                    pane_widths=[1,0,20])
        else: # just a line, no background
            if self.input_boxes:
                app = widgets.AppLayout(
                    header=self.fig.canvas,
                    footer=self.out,
                    left_sidebar=widgets.HBox([self.slopewidget, self.intwidget]),
                    pane_heights=[12, 1, 1],grid_gap="1px",align_items='center',
                    pane_widths=[20,0,1])
            else:
                app = widgets.AppLayout(
                header=self.fig.canvas,
                left_sidebar=self.out,
                pane_heights=[12, 1, 0],grid_gap="1px",align_items='center',
                pane_widths=[20,0,1])
        
        display(app)
            
        self.print_output(message, self.chi2) 
        plt.sca(self.ax[1])

    def onclick(self, event):

        # print(os.environ['JPY_SESSION_NAME']) - this gets me my current file name.
        # save state in same path but .FILENAME-hashedPLOTNAME
            
        # button.index tells the state of the radio buttons.
        with self.out:
            # print(event.xdata,event.ydata)
            # print(event)
            if event.inaxes != self.ax[0] and event.inaxes != self.ax[1]:
                return
        
        if event.button != 1: # we only look at the left button.
            return
            
        # if you click outside the axes bad things happen Should never happen now?
        if not isinstance(event.xdata, float):
            return
        if not isinstance(event.ydata, float):
            return
           
        if self.button.index == 0 or self.use_background == False:  # doing a point on the line.
            # which point? Use the closer one. Need to scale distances by limits!
            if event.inaxes == self.ax[1]: # main plot            
                xl = self.ax[1].get_xlim()
                yl = self.ax[1].get_ylim()
                xs = abs(xl[1]-xl[0])
                ys = abs(yl[1]-yl[0])
                d0 = (event.xdata-self.xp[0])*(event.xdata-self.xp[0])/xs/xs +\
                            (event.ydata-self.yp[0])*(event.ydata-self.yp[0])/ys/ys
                d1 = (event.xdata-self.xp[1])*(event.xdata-self.xp[1])/xs/xs +\
                            (event.ydata-self.yp[1])*(event.ydata-self.yp[1])/ys/ys
                if (d0 < d1):
                    self.xp[0] = event.xdata
                    self.yp[0] = event.ydata
                else:
                    self.xp[1] = event.xdata
                    self.yp[1] = event.ydata
            elif event.inaxes == self.ax[0]: # in residuals
                if abs(event.xdata-self.xp[0]) < abs(event.xdata-self.xp[1]):
                    # modify xp0
                    self.xp[0] = event.xdata
                    self.yp[0] = event.ydata + self.slope * self.xp[0] + self.intercept
                else:
                    self.xp[1] = event.xdata
                    self.yp[1] = event.ydata + self.slope * self.xp[1] + self.intercept
        elif self.button.index == 1: # doing offset
            if event.inaxes == self.ax[1]: # main plot
                self.yoff = event.ydata
            elif event.inaxes == self.ax[0]: # clicked in residuals
                self.yoff = event.ydata + np.log(np.exp(self.intercept)*np.exp(event.xdata*self.slope)+np.exp(self.yoff))
        # common
        
        self.calc_fit()
        self.no_recur = True
        self.slopewidget.value=par_form.format(self.slope)
        self.intwidget.value=par_form.format(self.intercept)
        self.offwidget.value=par_form.format(self.yoff)
        # self.slopewidget.value=self.slope
        # self.intwidget.value=self.intercept
        # self.offwidget.value=self.yoff
        self.no_recur = False
        self.update_displays()
                
class line(generic_fit_with_background):
    """Class for creating fit objects for straight line fit.

    Parameters:
    name: a unique name that is used as a plot title as well as for tagging the fit parameters
    xdata: x values of the data
    ydata: y values
    yerr: uncertainties in y values
    use_background: a boolean. If false we just do a linear fit, if true the function is
            np.log(np.exp(self.intercept)*np.exp(self.cxp*self.slope)+np.exp(self.yoff))
    input_boxes: a boolean. If True display boxes that allow manual setting of parameters
    """
    def __init__(self, name, xdata, ydata, yerr, chi2=False, input_boxes=True):
        super().__init__(name, xdata, ydata, yerr, False, chi2, input_boxes)

class with_background(generic_fit_with_background):
    """Class for creating fit objects for radiation experiment with background

    Parameters:
    name: a unique name that is used as a plot title as well as for tagging the fit parameters
    xdata: x values of the data
    ydata: y values
    yerr: uncertainties in y values
    use_background: a boolean. If false we just do a linear fit, if true the function is
            np.log(np.exp(self.intercept)*np.exp(self.cxp*self.slope)+np.exp(self.yoff))
    input_boxes: a boolean. If True display boxes that allow manual setting of parameters
    """
    def __init__(self, name, xdata, ydata, yerr, chi2=False, input_boxes=True):
        super().__init__(name, xdata, ydata, yerr, True, chi2, input_boxes)
