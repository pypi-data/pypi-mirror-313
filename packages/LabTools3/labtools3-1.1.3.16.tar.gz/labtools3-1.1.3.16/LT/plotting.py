"""

The plotting module contains functions based on :mod:`matplotlib` and
:class:`~LT.datafile`.

They provide shortcuts to perform typical plotting tasks in experimental physics.

**NOTE:** when you use these functions, enter the show() command to see the result interactively.

Example::
   >>> import LT.plotting as P
   >>> import numpy as np
   >>> x = np.array([1.,2.,3.,4.,5])
   >>> y = x**2
   >>> P.plot_line(x, y)
   >>> P.pl.show() # or just show() if you used: ipython -pylab

__________________________________________________________

"""
#---------------------------------------------------------------------- 
# plotting functions
#---------------------------------------------------------------------- 

import numpy as np
import matplotlib.pyplot as pl
# for interpolation
from scipy.interpolate import splrep, splev 

#---------------------------------------------------------------------- 
# simple plotting of array's of data, x, y and two sets of errors
#---------------------------------------------------------------------- 
def plot_exp(x,\
                 y, \
                 dy=[], \
                 dyt=[], \
                 marker='.',\
                 linestyle='None',\
                 label='_nolegend_',\
                 # color of total error bar
                 ecolor_1 = 'black', \
                 # set the errobar line width
                 elinewidth=2,\
                 # set the size of the bar at the end of the error bar
                 capsize = 4, \
                 # set the linewidth of the bar at the end of the errorbar
                 mew = 2, \
                 # set general line width
                 linewidth=2,\
                 logy = False,\
                 logx = False, \
                 min_val = None,\
                 scale = 1.,\
                 # labelling
                 x_label = None, \
                 y_label = None, \
                 plot_title = None, \
                 skip_labels = False, \
                 axes = None, \
                 **kwargs):
    """
        
    Plot experimental data using a linear scale by default. Below are a few
    examples 

    (it is assumed that the module as been imported as ``import
    LT.plotting as P``::
    
        >>> P.plot_exp(x, y)             # plot data points only, no errobars
        >>> P.plot_exp(x, y, sig_y)      # plot data points including errors stored in sig_y
        >>> P.plot_exp(x, y, dy=sig_y)   # alternatively using key word dy
        >>> P.plot_exp(x, y, dy=sig_y, dyt = sig_y_tot) # plot two errorbars, sig_y_tot = total error
        >>> P.plot_exp(x, y, dy=sig_y, xerr = sig_x) # plot also x errorbars, values stored in sig_x
        
    
    Important keywords:
    
    ============   =====================================================
    Keyword        Meaning
    ============   ===================================================== 
    dy             array with errors
    dyt            array with additional error values (e.g. total errors)
    marker         marker type (see :func:`~matplotlib.pyplot.plot`)
    linestyle      line style (see :func:`~matplotlib.pyplot.plot`)
    logy           use log y-scale (True/False)
    logx           use log x-scale (True/False)
    label          label for data (used in :func:`~matplotlib.pyplot.legend` )  
    min_val        min. values to be plotted
    scale          scale ally-values (including errrors ) by this factor
    x_label        label for x-axis
    y_label        label for y-axis
    plot_title     plot title
    skip_labels    do no put any labels (True/False)
    ============   =====================================================
        
    There are more key words, but ususally you do not need to change them
    and you should be familiar with matplotlib before you do so.  Keywords
    which are not listed here are passed along on to :func:`~matplotlib.pyplot.plot`, or :func:`~matplotlib.pyplot.errorbar` 
    routines. 

    """
    xx = np.array(x)
    yy = np.array(y)*scale
    dyy = np.array(dy)*scale
    dyyt = np.array(dyt)*scale
    if (axes == None):
        axes = pl.gca()
    if logy:
        axes.set_yscale("log", nonpositive='clip')
    if logx:
        axes.set_xscale("log", nonpositive='clip')
    if len(dy) == 0:
        # no error bars
        e=axes.plot(xx, yy,\
                   linestyle=linestyle,\
                   marker=marker, \
                   label=label,\
                   linewidth=linewidth,\
                   **kwargs)
        if skip_labels:
            return e
        else:
            axes.set_xlabel(x_label)
            axes.set_ylabel(y_label)
            axes.set_title(plot_title)
        return e
    # plot second (total) error bar behind first (statistical) one
    if len(dyt) != 0:
        # in case ther are several different errors
        et=axes.errorbar(xx, \
                        yy, \
                        yerr = dyyt, \
                        linestyle='None',\
                        color = ecolor_1, \
                        marker=marker,\
                        label=label, \
                        elinewidth=elinewidth,\
                        capsize = capsize, \
                        mew = mew, \
                        linewidth=linewidth,\
                        **kwargs)
    # pass all the explicit keyword arguments
    e=axes.errorbar(xx, yy, yerr = dyy,\
                   linestyle=linestyle,\
                   marker=marker, \
                   label=label,\
                   elinewidth=elinewidth,\
                   capsize = capsize, \
                   mew = mew, \
                   linewidth=linewidth,\
                   **kwargs)
    # negative error bars
    diff = yy - dyy
    if (diff.min() <= 0.) :
        if logy:
            print('---> errorbars go negative !')
            in_pos = np.where(diff > 0.)[0]
            l_min_val = yy[in_pos].min()
            # where is the min.value
            ii = list(yy).index(l_min_val)
            l_min_val -= dyy[ii]
            if min_val == None:
                    min_val = l_min_val
    if min_val != None:
        axes.set_ylim(ymin = min_val)
    if skip_labels:
        return e
    else:
        axes.set_xlabel(x_label)
        axes.set_ylabel(y_label)
        axes.set_title(plot_title)
    return e


#---------------------------------------------------------------------- 
# plot a line given by array x and y
#---------------------------------------------------------------------- 
def plot_line(x,\
             y, \
             label='_nolegend_',\
             logy = False, \
             logx = False, \
             convx = 1., \
             convy = 1., \
              axes = None, \
             **kwargs):
    """
    Plot a line through a set of data point using a linear scale by default. Below are a few
    examples. This is mostly used to plot a calculated curve.

    (it is assumed that the module as been imported as ``import
    LT.plotting as P``::

            >>> P.plot_line(x, y)             # x and y are :func:`numpy.array`
    
    Important keywords:
    
    ============   =====================================================
    Keyword        Meaning
    ============   ===================================================== 
    label          label for curve (used in :func:`~matplotlib.pyplot.legend` ) 
    logy           use log y-scale (True/False) 
    logx           use log x-scale (True/False) 
    convx          scale all x-values by this factor 
    convy          scale all y-values by this factor 
    ============   =====================================================
    
    Additional keywords are passed along to the :func:`~matplotlib.pyplot.plot` command.

    """
    if (axes == None):
        axes = pl.gca()
    xx = np.array(x) * convx
    yy = np.array(y) * convy
    s=axes.plot(xx, yy, marker='None',label=label,**kwargs)
    if logy:
        axes.set_yscale("log", nonpositive='clip')
    if logx:
        axes.set_xscale("log", nonpositive='clip')
    return s

#---------------------------------------------------------------------- 
# plot spline lines only, this has to be used carefully
#---------------------------------------------------------------------- 
def plot_spline(x, \
                y, \
                marker = 'None', \
                min_val=5.e-12,\
                label='_nolegend_',\
                nstep = 5,\
                conv = 1., \
                convx = 1., \
                convy = 1., \
                logy = False,\
                logx = False, \
                axes = None, \
                **kwargs):
    """
    Plot a line through a set of data point using a linear scale by default. Below are a few
    examples. This is mostly used to plot a calculated curve.
    
    (it is assumed that the module as been imported as ``import
    LT.plotting as P``::
    
        >>> P.plot_line(x, y)             # x and y are numpy arrays
    
    Important keywords:
    
    ============   =====================================================
    Keyword        Meaning
    ============   ===================================================== 
    label          label for curve (used in :func:`~matplotlib.pyplot.legend` ) 
    logy           use log y-scale (True/False)
    logx           use log x-scale (True/False)
    nstep          factor by which the number of interpolated data points is increased 
    convx          scale all x-values by this factor 
    convy          scale all y-values by this factor 
    ============   =====================================================
    
    Additional keywords are passed along to the :func:`~matplotlib.pyplot.plot` command.

    """
    if (axes == None):
        axes = pl.gca()
    xvar = np.array(x)*convx
    yvar = np.array(y)*conv*convy
    # number of interpolation steps
    new_xvar = np.linspace(xvar[0], xvar[-1:], int(nstep*len(xvar))) # create a new range with more points
    # need a loop to handle the error
    # for i in range(len(xvar)):
    #        if yvar[i] < 0. :
    #            yvar[i] =  -yvar[i]
    #        if yvar[i] == 0.:
    #            yvar[i] = min_val
    # now get interpolation coefficients
    yvar_cj = splrep(xvar,yvar)
    new_yvar = splev(new_xvar, yvar_cj)
    s=axes.plot(new_xvar, new_yvar, marker=marker,\
               label=label,\
               **kwargs)
    if logy:
        axes.set_yscale("log", nonpositive='clip')
    if logx:
        axes.set_xscale("log", nonpositive='clip')
    return s

#---------------------------------------------------------------------- 
#---------------------------------------------------------------------- 
# plot spline lines only, this has to be used carefully
#---------------------------------------------------------------------- 
def log_plot_spline(x, \
                y, \
                    marker = 'None', \
                    min_val=5.e-12,\
                    label='_nolegend_',\
                    nstep = 5,\
                    conv = 1., \
                    axes = None, \
                    logx = False, \
                    **kwargs):
    if (axes == None):
        axes = pl.gca()
    xvar = x*1.
    yvar = y*conv
    # number of interpolation steps
    new_xvar = np.linspace(xvar[0], xvar[-1:], int(nstep*len(xvar))) # create a new range with more points
    # need a loop to handle the error
    # for i in range(len(xvar)):
    #        if yvar[i] < 0. :
    #            yvar[i] =  -yvar[i]
    #        if yvar[i] == 0.:
    #            yvar[i] = min_val
    # now get interpolation coefficients
    yvar_cj = splrep(xvar,yvar)
    new_yvar = splev(new_xvar, yvar_cj)
    s=axes.semilogy(new_xvar, new_yvar, marker=marker,\
               label=label,\
               **kwargs)
    if logx:
        axes.set_xscale("log", nonpositive='clip')
    return s
#---------------------------------------------------------------------- 
# plot data read using data file
#---------------------------------------------------------------------- 
#---------------------------------------------------------------------- 
# simple plotting of array's of data, x, y and two sets of errors
#---------------------------------------------------------------------- 
def datafile_plot_exp(set,\
                 x='x', \
                 y='y', \
                 dy=None, \
                 dyt=None, \
                 linestyle='None',\
                 marker='.',\
                 label='_nolegend_',\
                 ecolor_1 = 'black', \
                 # set the errobar line width
                 elinewidth=2,\
                 # set the size of the bar at the end of the error bar
                 capsize = 4, \
                 # set the linewidth of the bar at the end of the errorbar
                 mew = 2, \
                 # set general line width
                 linewidth=2,\
                 # set for semilog plot
                 logy = False,\
                 logx = False, \
                 # minimum value for semilog plot
                 min_val = None,\
                 scale = 1.,\
                 # labelling
                 x_label = None, \
                 y_label = None, \
                 plot_title = None, \
                 skip_labels = False, \
                 axes = None, \
                 **kwargs):
    """
    Plot experimental data from a datafile using the variable names
    defined there.
    
    (it is assumed that the module as been imported as ``import
    LT.plotting as P``::
    
        >>> P.datafile_plot_exp(df, x='xv', y='yv') 
        >>> P.datafile_plot_exp(df, x='xv', y='yv', dy = 'sigy')          
        >>> P.datafile_plot_exp(df, x='xv', y='yv' ,dy='sigy', dyt = 'sigyt') 

    *df* is the datafile object, opened with :func:`~LT.datafile.dfile` or :func:`LT.get_data`
    
    **NOTE:** errors in x-axis are not implemented here.
    
    Important keywords:
    
    ============   =====================================================
    Keyword        Meaning
    ============   ===================================================== 
    x              variable name for x-axis data
    y              variable name for y-axis data
    dy             variable name for errors
    dyt            variable name  with additional error values (e.g. total errors)
    marker         marker type (see :func:`~matplotlib.pyplot.plot`)
    linestyle      line style (see :func:`~matplotlib.pyplot.plot`)
    label          label for data (used in :func:`~matplotlib.pyplot.legend` )  
    logy           use log y-scale (True/False)
    logx           use log x-scale (True/False)
    min_val        min. values to be plotted
    scale          scale all y-values (including errrors ) by this factor 
    x_label        label for x-axis
    y_label        label for y-axis
    plot_title     plot title
    skip_labels    do no put any labels (True/False)
    ============   =====================================================
    
    There are more key words, but ususally you do not need to change them
    and you should be familiar with matplotlib before you do so.  Keywords
    which are not listed here are passed along on to :func:`~matplotlib.pyplot.plot`,
    or :func:`~matplotlib.pyplot.errorbar`
    routines. 
    
    """


    if (axes == None):
        axes = pl.gca()
    xx = np.array(set.get_data(x) )
    yy = np.array(set.get_data(y))*scale
    if logy:
        axes.set_yscale("log", nonpositive='clip')
    if logx:
        axes.set_xscale("log", nonpositive='clip')
    if dy != None:
        dyy = np.array(set.get_data(dy))*scale
    dyyt = []
    if dyt != None:
        dyyt = np.array(set.get_data(dyt))*scale
    # plot without errorbars
    if (dy == None) & (dyt == None):
        plot_exp= axes.plot(xx, \
                        yy, \
                        linestyle=linestyle,\
                        marker=marker,\
                        label=label, \
                        **kwargs)
    # plot second (total) error bar behind first (statistical) one
    elif len(dyyt) != 0:
        # in case ther are several different errors
        et=axes.errorbar(xx, \
                        yy, \
                        yerr = dyyt, \
                        linestyle=linestyle,\
                        color = ecolor_1, \
                        marker=marker,\
                        label=label, \
                        elinewidth=elinewidth,\
                        capsize = capsize, \
                        mew = mew, \
                        linewidth=linewidth,\
                        **kwargs)
         # pass all the explicit keyword arguments
    else:
        e=axes.errorbar(xx, yy, yerr = dyy,\
                   linestyle=linestyle,\
                   marker=marker, \
                   label=label,\
                   elinewidth=elinewidth,\
                   capsize = capsize, \
                   mew = mew, \
                   linewidth=linewidth,\
                   **kwargs)
        # negative error bars
        diff = yy - dyy
        if (diff.min() <= 0.) :
            if logy:
                print('---> errorbars go negative !')
                in_pos = np.where(diff > 0.)[0]
                l_min_val = yy[in_pos].min()
            # where is the min.value
                ii = list(yy).index(l_min_val)
                l_min_val -= dyy[ii]
                if min_val == None:
                    min_val = l_min_val
                if min_val != None:
                    axes.set_ylim(ymin = min_val)
    # continue with general plotting
    if x_label == None:
        x_label = x
    if y_label == None:
        y_label = y
    if plot_title == None:
        plot_title = set.filename
    if skip_labels:
        return
    else:
        axes.set_xlabel(x_label)
        axes.set_ylabel(y_label)
        axes.set_title(plot_title)
    return 

#---------------------------------------------------------------------- 
#---------------------------------------------------------------------- 
#plot lines only
def datafile_plot_theory(set,\
                         x = 'x', \
                         y = 'y', \
                         marker = 'None', \
                         min_val=5.e-12,\
                         color='b',\
                         label='_nolegend_',\
                         convx = 1.,\
                         convy = 1.,\
                         logy = False,\
                         logx = False, \
                         axes = None, \
                         **kwargs):
    """
    
    Plot a line through data using the variable names and datafile object directly. 
    Keywords similar to :meth:`~LT.plotting.plot_line`

    """
    if (axes == None):
        axes = pl.gca()
    xvar = np.array(set.get_data(x) )*convx
    yvar = np.array(set.get_data(y))*convy

    s=axes.plot(xvar, yvar, marker=marker,color=color, \
               label=label,\
               **kwargs)

    if logy:
        axes.set_yscale("log", nonpositive='clip')
    if logx:
        axes.set_xscale("log", nonpositive='clip')
    return s


#---------------------------------------------------------------------- 
#plot spline lines only, this has to be used carefully
def datafile_spline_plot_theory(set,\
                                x = 'x', \
                                y = 'y', \
                                marker = 'None', \
                                min_val=5.e-12,\
                                color='b',\
                                label='_nolegend_',\
                                nstep = 5,\
                                convx = 1.,\
                                convy = 1.,\
                                logy = False,\
                                logx = False, \
                                axes = None, \
                                **kwargs):
    """
    
    Plot a spline through data using the variable names and datafile object directly.
    Keywords similar to :meth:`~LT.plotting.plot_spline`

    """
    if (axes == None):
        axes = pl.gca()
    xvar = np.array(set.get_data(x) )*convx
    yvar = np.array(set.get_data(y))*convy
    # number of interpolation steps
    new_xvar = np.linspace(xvar[0], xvar[-1:], int(nstep*len(xvar)) ) # create a new range with more points
    # handle 0 and neg values for log scale
    # now get interpolation coefficients
    yvar_cj = splrep(xvar,yvar)
    new_yvar = splev(new_xvar, yvar_cj)
    s=axes.plot(new_xvar, new_yvar, marker=marker,\
               color=color,\
               label=label,\
               **kwargs)
    if logy:
        axes.set_yscale("log", nonpositive='clip')
    if logx:
        axes.set_xscale("log", nonpositive='clip')

    return s

#----------------------------------------------------------------------
# shortcut, interface  names:

def dplot_exp(*args, **kwargs):
    """
    see :func:`LT.plotting.datafile_plot_exp`

    """
    return datafile_plot_exp(*args,**kwargs)

def dplot_line(*args, **kwargs):
    """
    see :func:`LT.plotting.datafile_plot_theory`

    """
    return datafile_plot_theory(*args,**kwargs)

def dplot_spline(*args, **kwargs):
    """
    see :func:`LT.plotting.datafile_spline_plot_theory`

    """
    return datafile_spline_plot_theory(*args,**kwargs)

#---------------------------------------------------------------------- 
