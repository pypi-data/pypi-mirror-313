"""
The LT box contains an assortment of plotting, histogramming and fitting routines
used for data analysis. The plotting routines have been imported from the :ref:`plotting`
module and the fitting routines have been imported from the :ref:`LT_Fit`. For detailed
information about these functions check the :ref:`plotting` and the the :ref:`LT_Fit` documentation.

Normally all you should need to do is import the `box`_ and you have a *box of tools*.

Example::

    >>> import LT.box as B

-------------------------------------------

Imported functions:

   From LT.plotting:
        * :meth:`~LT.plotting.plot_exp`: plot experimental data points with or without error bar
        * :meth:`~LT.plotting.plot_line`: plot a line through a set of data points
        * :meth:`~LT.plotting.plot_spline`: plot a spline curve through a set of data points

        * dplot_exp: (:meth:`~LT.plotting.datafile_plot_exp`) is like plot_exp but accesses the datafile variables directly via their names
        * dplot_line: (:meth:`~LT.plotting.datafile_plot_theory`) like plot_line for datafile variables
        * dplot_spline: (:meth:`~LT.plotting.datafile_spline_plot_theory`) like plot_spline for datafiles variables

   From LT_Fit:
        * :class:`~LT_Fit.linear_fit.linefit`: fit a straight line through a set of data points
        * :class:`~LT_Fit.linear_fit.polyfit`: fit a polynomial
        * :class:`~LT_Fit.linear_fit.gen_linfit`: general linear fit
        * :class:`~LT_Fit.gen_fit.genfit`: general, non-linear fit

-------------------------------------------

"""

import numpy as np
import matplotlib.pyplot as pl
from matplotlib.colors import LogNorm
from matplotlib import ticker
import copy

import LT

# include the version with parameters
from .pdatafile import pdfile

from .plotting import plot_exp
from .plotting import plot_line
from .plotting import plot_spline

from .plotting import datafile_plot_exp as dplot_exp

from .plotting import datafile_plot_theory as dplot_line
from .plotting import datafile_spline_plot_theory as dplot_spline

from LT_Fit.linear_fit import linefit
from LT_Fit.linear_fit import polyfit
from LT_Fit.linear_fit import gen_linfit

from LT_Fit.parameters import *

# general fitting
from LT_Fit.gen_fit import genfit

# this is done for general linear fitting

# for MCA spectra
from . import MCA as mcsp

def get_file(file, **kwargs):
    """
    Assume that  B is  the name of LT.box.

    Open and read the file::

    >>> md = B.get_file( 'file.data' )

    """
    return pdfile(file, **kwargs)

def get_data(D, var):
    """

    Assume that  B is  the name of LT.box.

    Get all the values of variable 'my_var' as a :func:`numpy.array`::

    >>> mv = B.get_data(md, 'my_var')
    
    This is an old method, better use:
        
    >>> mv = md['my_var']

    """
    return np.array(D.get_data(var))

# window cuts
def in_between(xmin, xmax, val):
    """

    return a selection of the values in val
    that satisfy:

    xmin <= val <= xmax

    Returns
    -------
    numpy array of True and False

    """
    return (xmin <= val) & (val <= xmax)

# select data within a window
def select_data(xmin, a, xmax):
    """

    Assume that  B is  the name of LT.box.

    Find which values of an array A lie between 0.8 and 1.2

    >>> iw = B.select_data( 0.8, A, 1.2)

    iw now is an array of indices, A[iw] is an array with values
    between 0.8 and 1.2

    in general: B.select_data(xmin, a, xmax)

    """
    return np.where( in_between(xmin, xmax, a) )

# Determine if a point is inside a given polygon or not
# Polygon is a list of (x,y) pairs. This function
# returns True or False.  The algorithm is called
# the "Ray Casting Method".
#
# here the rays are cast horizontally to the right (toward positive x)

def point_in_poly(x,y,poly):
    """
    x, y coordinates of a point to test if it lies inside a polygon
         given by a list of (xv, yv) vertices
    returns True if inside
    """
    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n] # cycles to all possible values

        # is y larger than any of the two min. y-values ?
        if y > min(p1y,p2y):
            # if so is y smaller than any of the two max. y-values
            if y <= max(p1y,p2y):
                # there is a potential that the point is inside
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        # point not on a vertex calculate intersection with a horizontal line at y
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        # print ' i, p1x, p1y, p2x, p2y, x, y ', i, p1x, p1y, p2x, p2y, x, y, inside
        p1x,p1y = p2x,p2y

    return inside


def array_point_in_poly(r,poly):
    """
    r arrays of  points; array with shape (N,s), where N is the number of points
    poly  an array of vertices for the polygon with the shape (M,2), M number of polygon vertices

    return a list of logical values indicating if the point is inside or outside the poly.
    """
    inside = []
    for rr in r:
        inside.append( point_in_poly(rr[0], rr[1], poly) )
    return np.array(inside)



## Test


# polygon = [(-5,5),(5,5),(5,-5),(-5,-5)]

# point_x = -4
# point_y = -3

## Call the function with the points and the polygon
# print point_in_poly(point_x,point_y,polygon)



# histogram class exception
class histoError(Exception):
    def __init__(self, comment, value):
        self.comment = comment
        self.value = value
    def __str__(self):
        return self.comment + repr(self.value)

# 1d -histogram class
#
# fitting of a gaussian on a quadratic back ground is built in
#
class histo:
    """

    Define a histogram based on the np.histogram class.

    The various ways of defining one are:

       *  If *a* is a 1D ( :func:`numpy.array`) containing the data to be histogrammed

          >>> h = histo( a )

       *  If *his* is the output of the :func:`numpy.histogram` function

          >>> h = histo(histogram = his)

       *  If ``bc`` is a 1D array with bin center values, and ``bcont``
          contains bin content values then:

          >>> h = histo(bin_center = bc, bin_content = bcont)

       *  A filename for a stored histogram is given

          >>> h = histo(filename), where filename contains the pdatafile

          Usually the result of a histo.save operation

    Important keywords:

    ============   =====================================================
    Keyword        Meaning
    ============   =====================================================
    values         Array of values to be histogrammed (:func:`numpy.array`)
    range          Lower and upper limits  of binning ( e.g. ``range = (10.,20.)`` )
    bins           Number of bins
    histogram      Result of :func:`numpy.histogram` function
    bin_error      Array of errors for each bin content (:func:`numpy.array`)
    bin_center     Array of bin-center values (:func:`numpy.array`)
    bin_content    Array of bin-content values (:func:`numpy.array`)
    file           Load data from file
    window         Set a window (a zoom window)
    title          Set the title
    xlabel         Set the x-label
    ylabel         Set the y-label
    calc_w2        If True calccultae the sum of the square of the weights for each bin to calculate the final bin error
    weights        Array of weight to increment the histogram with
    ============   =====================================================

    Additional keyword arguments are passed to the :func:`numpy.histogram` function

    """
    def __init__(self,\
                 values = None, \
                 range = None, \
                 bins = None, \
                 histogram = None, \
                 bin_error = None, \
                 bin_center = None, \
                 bin_content = None, \
                 file = None, \
                 window = None, \
                 title = 'my histogram', \
                 xlabel = 'x-bin', \
                 ylabel = 'content', \
                 calc_w2 = False, \
                 **kwargs):
        self.res = None
        self.has_weights = 'weights' in kwargs
        self.calc_w2 = calc_w2
        self.fit_dict = {}
        # initialize fitting
        self.b0 = Parameter(0., 'b0')
        self.b1 = Parameter(0., 'b1')
        self.b2 = Parameter(0., 'b2')
        self.mean =  Parameter(1.,'mean')
        self.sigma =  Parameter(1., 'sigma')
        self.A = Parameter(1., 'A')
        # create a dictionary for vairable fitting
        self.fit_par = {
        "b0" : self.b0, \
        "b1" : self.b1, \
        "b2" : self.b2, \
        "mean" :  self.mean, \
        "sigma":  self.sigma, \
        "A" : self.A}
        # setup fitting list
        self.set_fit_list()
        self.window_set = False
        self.ignore_zeros = True
        if values is not None:
            # values have been given for filling
            if (range is None) and (bins is None):
                self.fill(values, **kwargs)
            elif (range is not None) and (bins is None):
                self.fill(values, range = range, **kwargs)
            elif (range is None) and (bins is not None):
                self.fill(values, bins = bins, **kwargs)
            else:
                self.fill(values, bins = bins, range = range, **kwargs)
        elif file is not None:
            # create from file
            self.load(file)
            return
        elif histogram is not None:
            # the output of the numpy histogram function has been given
            self.res = histogram
        elif (bin_center is not None) and (bin_content is not None):
            # the histogram content is given direectly
            self.bin_center = np.copy(bin_center)
            self.bin_content = np.copy(bin_content)
            self.bin_width = np.diff(self.bin_center)[0]
            self.__get_histogram()
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.__setup_bins(error = bin_error)
        self.nbins = self.bin_center.shape[0]
        self.fit_index_min = 0
        self.fit_index_max = len(self.bin_content)-1
        if window is None:
            self.clear_window()
        else:
            self.set_window( xmin = window[0], xmax = window[1])

    def save_index(self, i):
        # make sure i is always within the allowed range
        return min(len(self.bin_content)-1, i)

    def fill(self, y, add = False, **kwargs):
        """

        Fill the histogram with the values stored in the :func:`numpy.array` y.

        ============   =====================================================
        Keyword        Meaning
        ============   =====================================================
        add            if True add the results to the existing content
        ============   =====================================================

        Additional keyword arguments are passed to the :func:`numpy.histogram` function

        """
        if not add:
            # a new filling
            self.res = np.histogram(y,  **kwargs)
            if self.calc_w2 and self.has_weights:
                w_loc = kwargs['weights']**2
                # histogram with weights squared
                kwargs1 = copy.copy(kwargs)
                kwargs1['weights'] = w_loc
                self.w2 = np.histogram(y, **kwargs1)[0] # save only the bin content
            self.__setup_bins(error = None)
        else:
            # the bins have already been defined continue
            # to accumulate statistics
            if self.res is None:
                print("no binning information: try fill with add = False ")
                return

            res = np.histogram(y, bins = self.res[1], **kwargs)
            if self.calc_w2 and self.has_weights:
                w2 = kwargs['weights']**2
                # histogram with weights squared
                kwargs1 = copy.copy(kwargs)
                kwargs1['weights'] = w2
                w2 = np.histogram(y, **kwargs1)[0] # save only the bin content
            # add the new bin content to the old one
            self.res = (self.res[0] + res[0], self.res[1])
            if self.calc_w2 and self.has_weights:
                self.w2 += w2
            # update the histogram information
            self.__setup_bins(error = None)
        # end of fill

    def clear(self):
        """

        Set the content and errors to 0.

        """
        self.bin_content = np.zeros_like(self.bin_content)
        self.bin_error = np.zeros_like(self.bin_content)
        self.res = (np.zeros_like(self.res[0]), self.res[1])
        self.__prepare_histo_plot()

    def sum(self, xmin = None, xmax = None):
        """

        Return the sum of all bins. If the limits are given, calculate the sum of all bins between the bins that contain
        the values xmin and xmax. If a window is set only the sum within the window is returned when no limits are specified.

        Example::

           >>> s0 = h.sum() # add all bins
           >>> s1 = h.sum(0.5, 1.1) # add the bins between 0.5 and 1.1
           >>> s2 = h.sum(xmin = 0.5, xmax = 1.1) # add the bins between 0.5 and 1.1

        ============   =====================================================
        Keyword        Meaning
        ============   =====================================================
        xmin           lower limit of sum of bin content
        xmax           upper limit of sum
        ============   =====================================================

        The errors are also calculated.

        """
        if (xmin is None) and (xmax is None):
            if self.window_set:
                sel = self.window_sel
                sum_v = self.bin_content[sel].sum()
                sum_err = np.sqrt( (self.bin_error[sel]**2).sum())
            else:                
                sum_v = self.bin_content.sum()
                sum_err = np.sqrt( (self.bin_error**2).sum())
        elif (xmin is None):
            sel = (self.bin_center <= xmax)
            sum_v = self.bin_content[sel].sum()
            sum_err = np.sqrt( (self.bin_error[sel]**2).sum())
        elif (xmax is None):
            sel = (xmin <= self.bin_center)
            sum_v = (self.bin_content[sel]).sum()
            sum_err = np.sqrt( (self.bin_error[sel]**2).sum())
        else:
            sel = (xmin <= self.bin_center) & (self.bin_center <= xmax)
            sum_v = (self.bin_content[sel]).sum()
            sum_err = np.sqrt( (self.bin_error[sel]**2).sum())
        return (sum_v, sum_err)

    def copy(self):
        """

        Create a copy of the histogram::

           >>>hc = h.copy()

        Only the histogram values are copied, no lables and titles etc.
        """
        res = (np.copy(self.res[0]), np.copy(self.res[1]) )
        err = np.copy( self.bin_error )
        return histo(histogram = res, bin_error = err)

    def rebin(self, n, scale = False, use_mean = False, replace = False):
        """

        rebin the histogram by a factor n::

           >>>hc = h.rebin(2)

        ============   =====================================================
        Keyword        Meaning
        ============   =====================================================
        scale          True: the original bin number is not a multiple of n
                             and the last bin content will be scaled accordingly
                             
        use_mean       True: the new bin content is the mean of the bin_content 
                             of n bins

        replace        True: replace the current histogram with the
                             rebinned version
        ============   =====================================================


        """
        n_bins = self.bin_center.shape[0]
        divisible = (np.mod(n_bins, n) != 0)
        # change bin content
        bco_sl, bco_mean_sl, sl, fact_sl =  self._rebin_array(self.bin_content, n)
        be2_sl, mean_sl, sl, fact_sl =  self._rebin_array(self.bin_error**2, n)
        sum_sl, bc_sl, sl, fact_sl =  self._rebin_array(self.bin_center, n)
        # adjust the bin center of last bin if necessary
        if not divisible:
            bc_sl[-1] = bc_sl[-2]+ np.diff(bc_sl)[0]
        if scale:
            bco_sl *= fact_sl
        # store new histogram parameters and update histogram
        if not use_mean:
            bin_content = bco_sl
            bin_error = np.sqrt(be2_sl)
        else:
            bin_content = bco_mean_sl
            s_i, n_p = self._sl_indices(sl, n_bins)  # n_p number of points per slice
            b_e = np.sqrt(be2_sl)/np.array(n_p)
            bin_error = b_e
        bin_center = bc_sl
        if replace:
            self.bin_content = np.copy(bin_content)
            self.bin_error = np.copy(bin_error)
            self.bin_center = np.copy(bin_center)
            self.__get_histogram()
            # prepare for plotting
            self.__prepare_histo_plot()
        else:
            # return a new histogram
            hn =  self.__new_histogram(bin_content, bin_center, bin_error)
            hn.xlabel = self.xlabel
            hn.ylabel = self.ylabel
            hn.title = self.title
            return hn
        


    def plot(self,filled = 'True', ymin = 0.,  axes = None, ignore_zeros = False,  **kwargs):
        """

        Plot the histogram content:

        ============   =====================================================
        Keyword        Meaning
        ============   =====================================================
        filled         if True draw a filled histogram
        ymin           lower limit where fill starts (horizontal line)
        ignore_zeros   do not plot channels with  bin content 0 (default = False)
        ============   =====================================================

        """
        if axes is None:
            axes = pl.gca()
        if ymin is None:
            ymin = self.cont_min
        # prepare histo plot if axes have changed
        self.__prepare_histo_plot()
        if filled :
            xx = self.xpl
            yy = self.ypl
            if ignore_zeros:
                sel = yy != 0.
            else:
                sel = np.ones_like(yy).astype('bool')
            axes.fill_between( xx[sel], yy[sel], y2=ymin, **kwargs)
        else:
            xx = np.concatenate([self.xpl[:1], self.xpl, self.xpl[-1:]])
            yy = np.concatenate([np.array([ymin]), self.ypl, np.array([ymin])])
            if ignore_zeros:
                sel = yy != 0.
            else:
                sel = np.ones_like(yy).astype('bool')
            axes.plot(xx[sel],yy[sel], **kwargs)
        if self.window_set:
            axes.set_xlim( (self.win_min, self.win_max) )
            # prepare y scale
            sel = (self.win_min <= self.xpl) & (self.xpl <= self.win_max)
            ymin = self.ypl[sel].min()
            ymax = self.ypl[sel].max()
            axes.set_ylim( (ymin, ymax) )
        axes.set_xlabel(self.xlabel)
        axes.set_ylabel(self.ylabel)
        axes.set_title(self.title)

    def set_window(self, xmin =  None, xmax = None):
        """

        Define a window into the histogram. This is similar to a zoom or a
        region of interest (ROI)

        ============   =====================================================
        Keyword        Meaning
        ============   =====================================================
        xmin           lower limit for plotting or fitting
        xmax           upper limit
        ============   =====================================================

        """
        # a call to __setup_bins MUST preced usage of this call
        self.window_set = True
        if xmin is None:
            self.win_min = self.xpl.min()
        else:
            self.win_min = xmin
        if xmax is None:
            self.win_max = self.xpl.max()
        else:
            self.win_max = xmax
        self.window_sel = (self.win_min <= self.bin_center) & (self.bin_center <= self.win_max)

    def set_window_view(self):
        """

        Like set_windows but uses the current display limits. This is only
        useful if the histogram has been plotted.

        """
        xmin,xmax = pl.xlim()
        self.set_window(xmin,xmax)

    def clear_window(self):
        """

        Reset (Clear) the defined window

        """
        # a call to __setup_bins MUST precede usage of this call
        self.window_set = False
        self.win_min = self.xpl.min()
        self.win_max = self.xpl.max()

    def plot_exp(self, ignore_zeros = False, axes = None, **kwargs):
        """

        Plot histogram content and errors like experimental data.

        ============   =====================================================
        Keyword        Meaning
        ============   =====================================================
        ignore_zeros   do not plot channels with  bin content 0 (default = False)
        ============   =====================================================


        """
        if axes is None:
            axes = pl.gca()
        xx = self.bin_center
        yy = self.bin_content
        dyy = self.bin_error
        if ignore_zeros:
            sel = yy != 0.
        else:
            sel = np.ones_like(yy).astype('bool')

        plot_exp(xx[sel], yy[sel], dyy[sel],\
                 x_label = self.xlabel, \
                 y_label = self.ylabel, \
                 plot_title = self.title, \
                 **kwargs)

        if self.window_set:
            axes.set_xlim( (self.win_min, self.win_max) )
            # prepare y scale
            sel = (self.win_min <= self.xpl) & (self.xpl <= self.win_max)
            ymin = self.ypl[sel].min()
            ymax = self.ypl[sel].max()
            axes.set_ylim( (ymin, ymax) )

    def save(self, filename = 'histo.data'):
        """

        Save the histogram in :mod:`~LT.pdatafile` format

        """
        of = open(filename, 'w')
        of.write('#\ title = %s\n'%(self.title))
        of.write('#\ xlabel = %s\n'%(self.xlabel))
        of.write('#\ ylabel = %s\n'%(self.ylabel))
        # fir limits used when the last fit was made
        of.write('#\ fit_index_min = %d\n'%(self.fit_index_min))
        of.write('#\ fit_index_max = %d\n'%(self.fit_index_max))
        # now write the current fit parameters
        for key in self.fit_par:
            name = key + ' = %r'
            err_name = '; d_'+name
            fmt = '#\ '+name+err_name+'\n'
            l =  fmt%( self.fit_par[key].value, self.fit_par[key].err)
            of.write(l)
        of.write('# \n')
        of.write('#! bin_center[f, 0]/ bin_content[f,1]/ bin_error[f, 2]/ \n')
        for i,bc in enumerate(self.bin_center):
            of.write ("%r %r %r \n"%( bc, self.bin_content[i], self.bin_error[i])  )
        of.close()

    def load(self, file='histo.data'):
        """

        read the histogram data from :mod:`~LT.pdatafile`

        If the file does not result from a save function make sure that
        all the necessary data are present.

        """
        data = get_file(file)
        # first the data
        self.bin_center = np.array(data.get_data('bin_center') )
        self.bin_content = np.array(data.get_data('bin_content') )
        self.bin_error =  np.array(data.get_data('bin_error') )
        # now the parameters
        self.title = data.par.get_value('title', str)
        self.xlabel = data.par.get_value('xlabel', str)
        self.ylabel = data.par.get_value('ylabel', str)
        # now the fit limits (if they exist)
        try:
            fi_min = data.par.get_value('fit_index_min')
            fi_max = data.par.get_value('fit_index_max')
            self.fit_index_min = int(fi_min)
            self.fit_index_max = int(fi_max)
        except:
            self.fit_index_min = 0
            self.fit_index_max = len(self.bin_content) - 1
        
        # now the fit parameters
        for key in self.fit_par:
            name = key
            dname = 'd_'+key
            self.fit_par[key].set(data.par.get_value(name, float), \
                                      err = data.par.get_value(dname, float))
        self.bin_width = np.diff(self.bin_center)[0]
        self.__get_histogram()
        self.bins = self.res[1]
        self.__prepare_histo_plot()
        self.clear_window()
        # plot the fit
        x = np.linspace(self.bins[0], self.bins[-1:][0], 100)
        self.fit_dict['xpl'] = x
        self.fit_dict['ypl'] = self.fit_func(x)


    def find_bin(self, x):
        """

        Find the bin that would contain the value x

        """
        # self.bins contains the bin edged
        if (x < self.bins[0]):
            print('searched value {0} < lowest bin = {1} '.format(x, self.bins[0]))
            return 0
        elif (x > self.bins[-1:][0]):
            print('searched value {0} > highest bin = {1} '.format(x, self.bins[-1:][0]))
            return len(self.bins) - 1
        elif (x == self.bins[0]):
            return 0
        else:
            return (np.searchsorted(self.bins, x) - 1 )

    def set_fit_list(self, fit = [ 'A', 'mean', 'sigma'] ):
        """

        Define which parameters are to be fitted.

        The default list is ::

           fit = [ 'A', 'mean', 'sigma']

        to use all parameters::

           h.set_fit_list( fit = [ 'A', 'mean', 'sigma', 'b0', 'b1', 'b2'])

        """
        if fit==[]:
            # empty list show possibilities
            print('possible fit parameters:')
            print(list(self.fit_par.keys()))
            return
        self.fit_names = fit
        self.fit_list = []
        for key in self.fit_names:
            try:
                curr_par_name = self.fit_par[key]
            except:
                print('cannot use parameter :', key, ' (does not exist ?!)')
                continue
            self.fit_list.append(curr_par_name)
        # end of fitting list

    def show_fit_list(self):
        """
        Show the current fit list

        Returns
        -------
        None.

        """
        print("\nCurrent fit list : ", [k.name for k in self.fit_list])
        print("\nAvailable parameters: [ 'A', 'mean', 'sigma', 'b0', 'b1', 'b2']")


    def fit(self, xmin = None, xmax = None, init = True, ignore_zeros = True, **kwargs):
        """

        Fit a gaussian on a quadratic background. You can also just
        fit a background or just a gaussian. All this is controlled by which
        parameters you want to fit. Another important part of non-linear
        fitting is that you need to provide reasonable guesses for the fit
        parameters. The parameters in :class:`~LT.box.histo` are not just
        numbers but objects with their own properties and functions (see
        :class:`~LT_Fit.parameters.Parameter` ).  The full fit function is as
        follows:

        :math:`$ f(x) = b_0 + b_1x + b_2x^2  + A exp(-(x - \mu)^2/\sigma^2)$`

        The (:class:`LT.box.histo`) parameters are:

        =================== ================================================
        Parameter           Histo Class Member
        =================== ================================================
        :math:`$b_o $`      b0
        :math:`$b_1 $`      b1
        :math:`$b_2 $`      b2
        :math:`$A $`        A
        :math:`$\mu  $`     mean
        :math:`$\sigma  $`  sigma
        =================== ================================================

        Which parameters are fitted is defined in :meth:`~LT.box.histo.set_fit_list`

        Keyword arguments are:

        ============   =====================================================
        Keyword        Meaning
        ============   =====================================================
        xmin           lower fit limit
        xmax           upper fit limit
        init           True/False (default = True) estimate initial fit parameters automatically
        ignore_zeros   True/False (default = True) ignore channels with bin content zero
        kwargs         additional keywords are passed to gen_fit (use only if you know what you are doing!)
        ============   =====================================================



        """
        self.ignore_zeros = ignore_zeros
        # is there a range given, or is a window set
        sel_all = np.ones_like(self.bin_center, dtype = 'bool')
        if init:
            self.init_gauss(xmin, xmax, ignore_zeros)
        if (xmin is None) and (xmax is None):
            # check if a window is set
            if self.window_set:
                # if so use the set window limits
                sel = (self.win_min <= self.bin_center) & (self.bin_center <= self.win_max)
                self.fit_indx, = np.where ( sel )
            else:
                # if not use all data
                self.fit_indx, = np.where(sel_all)
        elif (xmin is None):
            sel = (self.bin_center <= xmax)
            if self.window_set:
                # if so check which is smaller
                sel_w = (self.bin_center <= self.win_max) & sel
                self.fit_indx, = np.where(sel_w)
            else:
                self.fit_indx, = np.where(sel)
        elif (xmax is None):
            sel = (xmin <= self.bin_center)
            if self.window_set:
                # if so check which is larger
                sel_w = (self.win_min <= self.bin_center) & sel
                self.fit_indx, = np.where(sel_w)
            else:
                self.fit_indx, = np.where(sel)
        else:
            sel = (xmin <= self.bin_center) & ( self.bin_center <= xmax)
            if self.window_set:
                # if so check the set window limits
                sel_w = (self.win_min <= self.bin_center) & ( self.bin_center <= self.win_max) & sel
                # use the tighter limits
                self.fit_indx, = np.where(sel_w)
            else:
                self.fit_indx, = np.where(sel)
        if not ignore_zeros:
            # set minimal error to 1
            is_zero = np.where(self.bin_error == 0.)
            self.bin_error[is_zero] = 1.
        # store the limits of fit_indx
        self.fit_index_min = self.fit_indx.min()
        self.fit_index_max = self.fit_indx.max()
        # do the fit
        if ignore_zeros:
            # ignore bins with content of 0
            sel = self.bin_content[self.fit_indx] != 0.
            bin_content = self.bin_content[self.fit_indx][sel]
            bin_center = self.bin_center[self.fit_indx][sel]
            bin_error = self.bin_error[self.fit_indx][sel]
        else:
            bin_content = self.bin_content[self.fit_indx]
            bin_center = self.bin_center[self.fit_indx]
            bin_error = self.bin_error[self.fit_indx]

        # do the fit using the new version
        self.F = genfit( self.fit_func, self.fit_list, \
                                   x = bin_center, \
                                   y = bin_content, \
                                   y_err = bin_error, \
                                   full_output=1, \
                                   ftol = 0.001, \
                                   print_results = False, **kwargs)
        self.fit_dict = self.F.stat
        self.fit_dict['xpl'] = self.F.xpl
        self.fit_dict['ypl'] = self.F.ypl
        # get the covariance matrix
        if self.fit_dict == {}:
            print("Problem with fit: no result, check parameters !")
            return
        self.cov = self.F.covar
        self.chi2_red = self.F.chi2_red
        self.chi2 = self.F.chi2
        self.CL = self.F.CL
        # print the result
        print('----------------------------------------------------------------------')
        print('Fit results:')
        for key in self.fit_names:
            print(key, ' = ', self.fit_par[key].value,' +/- ', self.fit_par[key].err)
        print('Chi square = ', self.F.chi2)
        print('Chi sq./DoF = ', self.F.chi2_red)
        print('----------------------------------------------------------------------')
        self.calc_fit_plot()

    def fit_view(self, init = True):
        """

        Fit histogram using the current display limits as fit range. This is only
        useful if the histogram has been plotted.

        """
        xmin,xmax = pl.xlim()
        self.fit(xmin,xmax, init = init)

    def init_parameters(self):
        """

        Reset fit parameters to their default values

        Returns
        -------
        None.

        """
        self.b0.set(0.)
        self.b1.set(0.)
        self.b2.set(0.)
        self.mean.set(0.)
        self.sigma.set(1.)
        self.A.set(1.)

    def init_gauss(self, xmin = None, xmax = None, ignore_zeros = True):
        """

        Calculate the initial parameter guess for a gaussian. These parameters
        can them be used in the call to :class:`~LT.box.histo.fit`

        """
        # is there a range given, or is a window set
        sel_all = np.ones_like(self.bin_center, dtype = 'bool')
        if (xmin is None) and (xmax is None):
            # check if a window is set
            if self.window_set:
                # if so use the set window limits
                sel = (self.win_min <= self.bin_center) & (self.bin_center <= self.win_max)
                self.fit_indx, = np.where ( sel )
            else:
                # if not use all data
                self.fit_indx, = np.where(sel_all)
        elif (xmin is None):
            sel = (self.bin_center <= xmax)
            if self.window_set:
                # if so check which is smaller
                sel_w = (self.bin_center <= self.win_max) & sel
                self.fit_indx, = np.where(sel_w)
            else:
                self.fit_indx, = np.where(sel)
        elif (xmax is None):
            sel = (xmin <= self.bin_center)
            if self.window_set:
                # if so check which is larger
                sel_w = (self.win_min <= self.bin_center) & sel
                self.fit_indx, = np.where(sel_w)
            else:
                self.fit_indx, = np.where(sel)
        else:
            sel = (xmin <= self.bin_center) & ( self.bin_center <= xmax)
            if self.window_set:
                # if so check the set window limits
                sel_w = (self.win_min <= self.bin_center) & ( self.bin_center <= self.win_max) & sel
                # use the tighter limits
                self.fit_indx, = np.where(sel_w)
            else:
                self.fit_indx, = np.where(sel)
        if not ignore_zeros:
            # set minimal error to 1
            s_zero = np.where(self.bin_error == 0.)
            self.bin_error[is_zero] = 1.
        # do the fit
        bin_content = self.bin_content[self.fit_indx]
        bin_center = self.bin_center[self.fit_indx]
        # bin_error = self.bin_error[self.fit_indx]
        # calculate initial parameters
        mean = np.sum(bin_center*bin_content)/bin_content.sum()
        sigma = np.sqrt( np.sum(bin_content*(bin_center - mean)**2)/bin_content.sum())
        A = bin_content.max()
        # store the parameters
        self.A.set(A)
        self.mean.set(mean)
        self.sigma.set(sigma)

    def calc_fit_plot(self):
        # plot the fit
        imax = min(len(self.bins)-1, self.fit_indx[-1:][0] + 1)
        xmin = self.bins[self.fit_indx][0]
        xmax = self.bins[imax]
        x = np.linspace(xmin, xmax, 100)
        self.fit_dict['xpl'] = x
        self.fit_dict['ypl'] = self.fit_func(x)

    def plot_fit(self, color = 'r', axes = None, **kwargs):
        """

        Plot the fitted curve

        ============   =====================================================
        Keyword        Meaning
        ============   =====================================================
        color          color of the fitted line
        ============   =====================================================

        """
        if axes is None:
            axes = pl.gca()
        if self.fit_dict == {}:
            print('no fit, nothing to plot !')
        else:
            plot_line(self.fit_dict['xpl'], self.fit_dict['ypl'], color = color, axes = axes, **kwargs)
            if self.window_set:
                axes.set_xlim( (self.win_min, self.win_max) )


    def fit_func(self, x):
        """

        The function fitted to the histogram data

        """
        fit_val = (self.b2()*x + self.b1())*x + self.b0() + \
            self.A()*np.exp(-0.5*((x-self.mean())/self.sigma() )**2)
        return fit_val
    
    def gauss(self, x):
        """
        
        Return the value of the gauss function using the fitted parameters at x
        

        Parameters
        ----------
        x : float

        Returns
        -------
        gauss(x) : float
            fitted gaussian at x.

        """
        g_val = self.A()*np.exp(-0.5*((x-self.mean())/self.sigma() )**2)
        return g_val
    
    def bkg(self, x):
        """
        
        Return the value of the fitted background at x

        Parameters
        ----------
        x : float

        Returns
        -------
        b_val(x) : float
            fitted backgound at x.

        """
        b_val = (self.b2()*x + self.b1())*x + self.b0()
        return b_val
        
    def apply_calibration(self, cal):
        """

        apply x-axis calibration, new axis values are cal(xaxis)

        """
        self.bin_center = cal(self.bin_center)
        self.bin_width = np.diff(self.bin_center)[0]
        self.bins = cal(self.bins)
        # prepare histo plot if axes have changed
        self.__prepare_histo_plot()

# private functions

    def __setup_bins(self, error = None ):
        self.bin_width = np.diff(self.res[1])[0]
        self.bin_center = self.res[1][:-1] + self.bin_width/2.
        self.bin_content = self.res[0]
        self.bins = self.res[1]
        if error is None:
            if not self.has_weights:  # no weights specified
                self.bin_error = np.sqrt(self.bin_content)
            elif self.calc_w2:   # weights given and sum(weights**2) calculated for each bin
                self.bin_error = np.sqrt(self.w2)
        else:
            self.bin_error = error
        self.__prepare_histo_plot()

    def __get_histogram(self):
        # create the histogram arrays from bin_width, bin_center, bin_content and bin_error
        res1 = np.concatenate( [self.bin_center - self.bin_width/2., self.bin_center[-1:] + self.bin_width/2.])
        res0 = self.bin_content
        self.res = ([res0,res1])

    def __new_histogram(self, b_content, b_center, b_error):
        # setup new np historam parameters using content, center abd error arrays
        # same as get_histogram
        # return a new histogram with these parameters
        b_width = np.diff(b_center)[0]
        res1 = np.concatenate( [b_center - b_width/2., b_center[-1:] + b_width/2.])
        res0 = b_content
        res = ([res0,res1])
        return histo(histogram = res, bin_error = b_error, window = (self.win_min, self.win_max))


    def __prepare_histo_plot(self):
        # prepare data for plotting as steps
        self.cont_min = self.res[0].min()
        iv = self.bin_width / 2.
        self.xpl = np.array(list(zip( self.bin_center - iv, self.bin_center + iv))).ravel()
        self.ypl = np.array(list(zip( self.bin_content, self.bin_content))).ravel()

    def _sl_indices(self, sla, Ni):
        # sla arrayt of slices
        # Ni length of array that the slices are applied to
        # get indices for slices and number of elements   per slice
        si = [sll.indices(Ni) for sll in sla]
        np = [x[1] - x[0] for x in si]
        # list of index tuples : start,stop, step
        # number of corresonding elements
        return si, np

    def _rebin_array(self, x, n):
        # rebin 1d  array, useful for histograms
        # start array for slices
        i_s = np.arange(0, x.shape[0]+n, n, dtype=int)
        # end array for slices
        # i_e = np.roll(i_s, -1)
        i_e = np.arange(n, x.shape[0]+2*n, n, dtype=int)
        # create the slices
        slices = [ slice(s, e) for s, e in zip(i_s,i_e)]
        # sum over the slices
        sum_sl = np.array([np.sum(x[sl]) for sl in slices[:-1]])
        # mean value of the slices
        mean_sl = np.array([np.mean(x[sl]) for sl in slices[:-1]])
        # factor to correct the sum for slices that are shorter than n
        fact = np.array([float(n)/len(x[sl]) for sl in slices[:-1]])
        # return the values
        return sum_sl, mean_sl, slices[:-1], fact


    def __add__(self, v):
        if np.isscalar(v):
            res0 = self.bin_content + v
            err = self.bin_error
            res1 = np.copy(self.res[1])
            res = ([res0, res1 ])
            return histo(histogram = res, bin_error = err, window = (self.win_min, self.win_max))
         # add 2 histograms and take care of the errors
        elif np.array_equal(self.bin_center.shape, v.bin_center.shape):
            # this is the content
            res0 = self.res[0] + v.res[0]
            err = np.sqrt( self.bin_error**2 + v.bin_error**2)
            res1 = np.copy(v.res[1])
            res = ([res0, res1 ])
            return histo(histogram = res, bin_error = err, window = (self.win_min, self.win_max))
        else:
            print('bin centers do not match-> cannot add, sorry !')
            return None

    def __sub__(self, v):
        # subtract 2 histograms and take care of the errors
        if np.isscalar(v):
            res0 = self.bin_content - v
            err = self.bin_error
            res1 = np.copy(self.res[1])
            res = ([res0, res1 ])
            return histo(histogram = res, bin_error = err, window = (self.win_min, self.win_max))
        elif np.array_equal(self.bin_center.shape, v.bin_center.shape):
            res0 = self.res[0] - v.res[0]
            err = np.sqrt( self.bin_error**2 + v.bin_error**2)
            res1 = np.copy(v.res[1])
            res = ([res0, res1 ])
            return histo(histogram = res, bin_error = err, window = (self.win_min, self.win_max))
        else:
            print('bin centers do not match-> cannot subtract, sorry !')
            return None

    def __mul__(self, v):
        # scale a histogram multiply from left
        if np.isscalar(v):
            res0 = v*self.bin_content
            err = v*self.bin_error
            res1 = np.copy(self.res[1])
            res = ([res0, res1 ])
            return histo(histogram = res, bin_error = err, window = (self.win_min, self.win_max))
        elif np.array_equal(self.bin_center.shape, v.bin_center.shape):
            res0 = self.res[0] * v.res[0]
            err = np.sqrt(self.bin_error**2 + v.bin_error**2)
            res1 = np.copy(self.res[1])
            res = ([res0, res1 ])
            return histo(histogram = res, bin_error = err, window = (self.win_min, self.win_max))
        else:
            print('bin centers do not match-> cannot multiply, sorry !')
            return None


    def __truediv__(self, v):
        # divide 2 histograms and take care of the errors
        # check the shapes
        if np.isscalar(v):
            res0 = self.res[0]/v
            err = self.bin_error/v
            res1 = np.copy(self.res[1])
            res = ([res0, res1])
            return histo(histogram = res, bin_error = err, window = (self.win_min, self.win_max))
        elif np.array_equal(self.bin_content.shape, v.bin_content.shape):
            # this is the content
            res0 = self.bin_content / v.bin_content
            f1 = 1./v.bin_content
            f2 = res0/v.bin_content
            err = np.sqrt( (f1*self.bin_error)**2 + (f2*v.bin_error)**2)
            res1 = np.copy(v.res[1])
            res = ([res0, res1])
            return histo(histogram = res, bin_error = err, window = (self.win_min, self.win_max))
        else:
            print('bin centers do not match-> cannot divide, sorry !')
            return None


    def __rmul__(self, c):
        # scale a histogram multiply from right
        res0 = c*self.res[0]
        err = c*self.bin_error
        res1 = np.copy(self.res[1])
        res = ([res0, res1 ])
        return histo(histogram = res, bin_error = err, window = (self.win_min, self.win_max))



# end of 1d-histo class

# 2d histogram class


class histo2d:
    """

    Define a 2d histogram based on the np.histogram2d class.

    The various ways of defining one are:

       *  If *xv* is a 1D ( :func:`numpy.array`) containing the x-value data to be histogrammed
          and *yx* is a 1D array containing the y-value data :

          >>> h2 = histo2d( xv, yv )

       *  If *his2* is the output of the :func:`numpy.histogram2d` function

          >>> h2 = histo2d(histogram = his2)

       *  If ``xbc`` is an array with x-bin center values, ``ybc`` is an array with y-bin center values
          and ``bcont`` contains bin content values then use:

          >>> h2 = histo2d(x_bin_center = xbc, y_bin_center = ybc, bin_content = bcont)

       *  A filename for a stored histogram is given

          >>> h2 = histo2d(filename), where filename contains the pdatafile

          Usually the result of a histo2d.save operation

    Important keywords:

    ============   =====================================================
    Keyword        Meaning
    ============   =====================================================
    xvalues        Array of x-values to be histogrammed (1d-:func:`numpy.array`)
    yvalues        Array of y-values to be histogrammed (1d-:func:`numpy.array`)
    range          Lower and upper limits  of binning ( e.g. ``range = (10.,20.)`` )
    bins           Number of bins, or [binsx, binsy]
    histogram      Result of :func:`numpy.histogram2d` function
    x_bin_center   1d-Array of x - bin-center values (:func:`numpy.array`)
    y_bin_center   1d-Array of y - bin-center values (:func:`numpy.array`)
    bin_content    2d-Array of bin-content values (:func:`numpy.array`)
    bin_error      2d-Array of errors for each bin content (:func:`numpy.array`)
    file           Load data from file
    title          Set the title
    xlabel         Set the x-label
    ylabel         Set the y-label
    zlabel         Set the z-label
    calc_w2        If True calccultae the sum of the square of the weights for each bin to calculate the final bin error
    weights        Array of weight to increment the histogram with
    colorbar       if True, plot a colorbar
    bad_color      Set the color for plot for bins below zmin (default: w)
    logz           if True plot content on log scale
    ============   =====================================================

    Additional keyword arguments are passed to the :func:`numpy.histogram2d` function

    """
    def __init__(self,\
                 x_values = None, \
                 y_values = None, \
                 range = None, \
                 bins = None, \
                 histogram = None, \
                 bin_error = None, \
                 bin_content = None, \
                 x_bin_center = None, \
                 y_bin_center = None, \
                 file = None, \
                 title = 'my histogram', \
                 xlabel = 'x-bin', \
                 ylabel = 'y-bin', \
                 zlabel = 'content',\
                 bad_color = 'w',\
                 colorbar = True, \
                 logz = False,\
                 calc_w2 = False,\
                 **kwargs):
        self.has_weights = 'weights' in kwargs
        self.bad_color = bad_color # color for bad pixels
        self.colorbar = colorbar
        self.logz = logz
        self.calc_w2 = calc_w2
        # initialize fitting
        if (x_values is not None) and (y_values is not None):
            # values have been given for filling
            if (range is None) and (bins is None):
                self.fill(x_values, y_values, **kwargs)
            elif (range is not None) and (bins is None):
                self.fill(x_values, y_values, range = range, **kwargs)
            elif (range is None) and (bins is not None):
                self.fill(x_values, y_values, bins = bins, **kwargs)
            else:
                self.fill(x_values, y_values, bins = bins, range = range, **kwargs)
        elif file is not None:
            # create from file
            self.load(file)
            return
        elif histogram is not None:
            # the output of the numpy histogram function has been given
            self.res = histogram
        elif (x_bin_center is not None) and (y_bin_center is not None) and (bin_content is not None):
            # the histogram content is given direectly
            self.x_bin_center = np.copy(x_bin_center)
            self.y_bin_center = np.copy(y_bin_center)
            self.bin_content = np.copy(bin_content)
            if(bin_error is not None):
                self.bin_error = bin_error
            self.__setup_histogram()
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.zlabel = zlabel
        self.__setup_bins(error = bin_error)
        self.nbins_x = self.x_bin_center.shape[0]
        self.nbins_y = self.y_bin_center.shape[0]


    def set_nans(self, value = 0., err_value = 1.):
        """

        replace nans by specified values

        ============   =====================================================
        Keyword        Meaning
        ============   =====================================================
        value          replaces the nan in bin_content (default 0)
        err_value      replaces the corresponding bin_error (default 1)
        ============   =====================================================


        Returns
        -------
        None.

        """
        sel = np.isnan(self.bin_content)
        self.bin_content[sel] = value
        self.bin_error[sel] = err_value

    def fill(self, x, y, add = False, **kwargs):
        """

        Fill the histogram with the values stored in the :func:`numpy.array` y.

        ============   =====================================================
        Keyword        Meaning
        ============   =====================================================
        add            if True add the results to the existing content
        ============   =====================================================

        Additional keyword arguments are passed to the :func:`numpy.histogram` function

        """
        if not add:
            # a new filling
            self.res = np.histogram2d(x, y, **kwargs)
            if self.calc_w2 and self.has_weights:
                w_loc = kwargs['weights']**2
                # histogram with weights squared
                kwargs1 = copy.copy(kwargs)
                kwargs1['weights'] = w_loc
                self.w2 = np.histogram2d(x,y, **kwargs1)[0] # save only the bin content
            self.__setup_bins(error = None)
        else:
            # the bins have already been defined continue
            # to accumulate statistics
            if self.res is None:
                print("no binning information: try fill with add = False ")
                return
            res = np.histogram2d(x, y, bins = [self.x_bins,self.y_bins], **kwargs)
            if self.calc_w2 and self.has_weights:
                w_loc = kwargs['weights']**2
                # histogram with weights squared
                kwargs1 = copy.copy(kwargs)
                kwargs1['weights'] = w_loc
                w2 = np.histogram2d(x,y, bins = [self.x_bins,self.y_bins], **kwargs1)[0] # save only the bin content            
            # add the new bin content to the old one
            self.res = (self.res[0] + res[0], self.res[1], self.res[2])
            self.w2 += w2
            # update the histogram information
            self.__setup_bins(error = None)
        # end of fill

    def clear(self):
        """

        Set the content and errors to 0.

        """
        self.bin_content = np.zeros_like(self.bin_content)
        self.bin_error = np.zeros_like(self.bin_content)
        self.res = (np.zeros_like(self.res[0]), self.res[1], self.res[2])
        self.x_bin_width = np.zeros_like(self.x_bin_width)
        self.y_bin_width = np.zeros_like(self.y_bin_width)
        self.x_bin_center = np.zeros_like(self.x_bin_center)
        self.y_bin_center = np.zeros_like(self.y_bin_center)
        self.x_bins = np.zeros_like(self.x_bins)
        self.y_bins = np.zeros_like(self.y_bins)
        self.__prepare_histo_plot()

    def sum(self, rect_cut = None, poly_cut = None, draw = False):
        """

        Return the sum of all bins. If the limits are of a rectangle  are given,
        calculate the sum of all bins inside it or inside a polygon poly

        Example::

           >>> s0 = h.sum() # add all bins
           >>> s1 = h.sum(rect = [x1,x2, y1, y2])
           >>> s2 = h.sum(poly = ([x1, x2, ...], [y1, y2, ...])) # add the bins inside the polygon

        ============   =====================================================
        Keyword        Meaning
        ============   =====================================================
        xmin           lower limit of sum of bin content
        xmax           upper limit of sum
        ============   =====================================================

        The errors are also calculated.

        """
        if (rect_cut is None) and (poly_cut is None):
            h_sum = self.bin_content.sum()
            h_sum_err = np.sqrt( (self.bin_error**2).sum() )
        elif (poly_cut is None):
            h_sum = self.bin_content[rect_cut].sum()
            h_sum_err = np.sqrt( (self.bin_error[rect_cut]**2).sum())
            if draw:
                self.draw_polygon(self.rect)
        else:
            h_sum = self.bin_content[poly_cut].sum()
            h_sum_err = np.sqrt( (self.bin_error[poly_cut]**2).sum())
            self.poly_cut = poly_cut
            if draw:
                self.draw_polygon(self.poly)
        return (h_sum, h_sum_err)



    def plot(self,  axes = None, graph = 'patch', clevel = 10, colormap = pl.cm.CMRmap, logz = False,
             skip_x_label = False, skip_ylabel = False, skip_title = False, 
             **kwargs):
        """

        Plot the 2d histogram content:

        ============   =====================================================
        Keyword        Meaning
        ============   =====================================================
        graph          type of plot: patch, contour, surface, lego
        clevel         number of contour levels (default 10)
        colormap       colormap to be used (default CMRmap)
        logz           if True use a logarithmic scale for content (patch and contour only)
        skip_x_label   if True do not plot x-label
        skip_y_label   if True do not plot y-label
        skip_title     if True do not plot title
        kwargs         additional kwargs are possed to the plotting routines
        ============   =====================================================

        """
        nz = self.bin_content>0.
        self.logz = logz
        self.zmin = self.bin_content[nz].min()
        colormap_l = copy.copy(colormap)
        colormap_l.set_bad(color = self.bad_color)
        # create a masked z-array, suppress 0 etc.
        Zm = np.ma.masked_less(self.bin_content, self.zmin)
        if graph == 'patch':
            if axes is None:
                axes = pl.gca()
            # color mesh
            if not self.logz:
                pcm = axes.pcolormesh(self.x_bins, self.y_bins, Zm.T, cmap=colormap_l, **kwargs)
            else:
                pcm = axes.pcolormesh(self.x_bins, self.y_bins, Zm.T, cmap=colormap_l, norm = LogNorm(),  **kwargs)
            if self.colorbar:
                cbar = pl.colorbar(pcm,ax=axes)
                cbar.minorticks_on()
        elif graph == 'contour':
            if axes is None:
                axes = pl.gca()
                # color mesh
            YY,XX = np.meshgrid(self.y_bin_center, self.x_bin_center)
            if not self.logz:
                ctf = pl.contourf(XX,YY, Zm, cmap=colormap_l, **kwargs)        # contour
                if self.colorbar:
                    cbar = pl.colorbar(ctf,ax=axes)
                    cbar.minorticks_on()
            else:
                Zml = np.log10(Zm)
                # setup the ticks
                # z-limits
                zmin = np.floor(Zml.min())
                zmax = np.ceil(Zml.max())
                # tick values
                llev = np.log10((ticker.LogLocator(subs = [1.])).tick_values(10**zmin, 10**zmax))
                # print("llev = ", llev)
                ctf = pl.contourf(XX,YY, Zml, levels = clevel)
                # setup the tick labels
                ctkls = [r"$10^{" +f"{int(v):d}" +r"}$" for v in llev]
                if self.colorbar:
                    cbar = pl.colorbar(ctf,ax=axes)
                    cbar.set_ticks(llev)
                    cbar.set_ticklabels(ctkls)
        elif graph == 'surface':      
            if logz:
                print('log scale not yet implemented!')
            if axes is None:
                axes = pl.gca(projection='3d')
            YY,XX = np.meshgrid(self.y_bin_center, self.x_bin_center)
            axes.plot_surface(XX,YY, self.bin_content, cmap=colormap_l, **kwargs)
            axes.set_zlabel(self.zlabel)
        elif graph == 'lego':
            if self.logz:
                print('log scale not yet implemented!')
            if axes is None:
                axes = pl.gca(projection='3d')
            YY,XX = np.meshgrid(self.y_bin_center, self.x_bin_center)
            xposf = XX.flatten()
            yposf = YY.flatten()
            zposf = np.ones_like(xposf)*self.zmin
            dx = self.x_bin_width
            dy = self.y_bin_width
            dz = self.bin_content.flatten()
            # select color
            rgba = [colormap((k-dz.min())/dz.max()) for k in dz]
            axes.bar3d(xposf, yposf, zposf, dx, dy, dz, color = rgba, zsort = 'max')
            axes.set_zlabel(self.zlabel)
        else:
            print('Unknown graph type:', graph, ' possible values: patch, contour, surface ')
            return
        if not skip_x_label:
            axes.set_xlabel(self.xlabel)
        if not skip_ylabel:
            axes.set_ylabel(self.ylabel)
        if not skip_title:
            axes.set_title(self.title)

    def save(self, filename = 'histo2d.data', ignore_zeros = True):
        """

        Save the histogram in :mod:`~LT.pdatafile` format

        ============   =====================================================
        Keyword        Meaning
        ============   =====================================================
        filename:      filename to be used
        ignore_zeros   if True, write only bins with non-zero content (default True)
        ============   =====================================================


        """
        of = open(filename, 'w')
        of.write(f'#\ title = {self.title}\n'   )
        of.write(f'#\ xlabel = {self.xlabel}\n' )
        of.write(f'#\ ylabel = {self.ylabel}\n' )
        of.write(f'#\ zlabel = {self.zlabel}\n' )
        of.write(f'#\ nbins_x = {self.nbins_x}\n')
        of.write(f'#\ nbins_y = {self.nbins_y}\n')
        of.write(f'#\ x_edge_min = {self.x_bins[0]}\n')
        of.write(f'#\ y_edge_min = {self.y_bins[0]}\n')
        of.write(f'#\ x_bin_width  = {self.x_bin_width}\n')
        of.write(f'#\ y_bin_width  = {self.y_bin_width}\n')
        of.write('#! x_bin_center[f,0]/ y_bin_center[f,1]/ bin_content[f,2]/ bin_error[f,3]/ i_x[i,4]/ i_y[i,5]/  \n')
        for i,xbc in enumerate(self.x_bin_center):
            for j,ybc in enumerate(self.y_bin_center):
                if ignore_zeros :
                    if self.bin_content[i,j] != 0.:
                        of.write (f" {xbc} {ybc} {self.bin_content[i,j]} {self.bin_error[i,j]}  {i} {j} \n ")
                else:
                    of.write (f" {xbc} {ybc} {self.bin_content[i,j]} {self.bin_error[i,j]}  {i} {j} \n ")
        of.close()

    def load(self, file):
        data = get_file(file)
        #x_bin_center = np.array(data.get_data('x_bin_center') )
        #y_bin_center = np.array(data.get_data('y_bin_center') )
        bin_content = np.array(data.get_data('bin_content') )
        bin_error =  np.array(data.get_data('bin_error') )
        x_edge_min = data.par.get_value('x_edge_min')
        y_edge_min = data.par.get_value('y_edge_min')
        ix = np.array(data.get_data('i_x') )
        iy = np.array(data.get_data('i_y') )
        # now the parameters
        self.title = data.par.get_value('title', str)
        self.xlabel = data.par.get_value('xlabel', str)
        self.ylabel = data.par.get_value('ylabel', str)
        self.zlabel = data.par.get_value('zlabel', str)
        self.nbins_x = data.par.get_value('nbins_x', int)
        self.nbins_y = data.par.get_value('nbins_y', int)
        self.x_bin_width = data.par.get_value('x_bin_width')
        self.y_bin_width = data.par.get_value('y_bin_width')
        self.bin_content = np.zeros((self.nbins_x, self.nbins_y))
        self.bin_error = np.zeros_like(self.bin_content)
        for n, i_x in enumerate(ix):
            # set the bins that are not zero
            i_y = iy[n]
            self.bin_content[i_x, i_y] = bin_content[n]
            self.bin_error[i_x, i_y] = bin_error[n]
        self.x_bins = np.array([x_edge_min + xx*self.x_bin_width for xx in np.arange(self.nbins_x + 1)])
        self.y_bins = np.array([y_edge_min + yy*self.y_bin_width for yy in np.arange(self.nbins_y + 1)])
        self.x_bin_center = self.x_bins[:-1] + self.x_bin_width/2.
        self.y_bin_center = self.y_bins[:-1] + self.y_bin_width/2.
        self.res = [self.bin_content, self.x_bins, self.y_bins ]


    def rect_cut(self, x1, x2, y1, y2):
        """
        Setup a rectangle cut

        ============   =====================================================
        Keyword        Meaning
        ============   =====================================================
        x1             lower x limit
        x2             upper x limit
        y1             lower y limit
        y2             upper y limit
        ============   =====================================================

        Returns
        -------
        sel : masked array for the bin_content

        """
        self.rect = np.array([[x1, y1], [x2, y1], [x2, y2], [x1, y2]])
        XX,YY = np.meshgrid(self.x_bin_center, self.y_bin_center)
        selx = (x1 <= XX) & (XX <= x2)
        sely = (y1 <= YY) & (YY <= y2)
        sel = selx.T & sely.T
        self.r_cut = sel
        return sel


    def poly_cut(self, p):
        """

        Setup a polygon cut :

        ============   =====================================================
        Keyword        Meaning
        ============   =====================================================
        p              array of coordinate pairs determining the corners of the polygon
        ============   =====================================================

        example for a triangle cut :
            p = np.array( [[1,2], [2,4], [0.5,3]  ])

        Returns
        -------
        Masked array to be applied to the bin_content and bin_error

        """
        self.poly = p
        XX,YY = np.meshgrid(self.x_bin_center, self.y_bin_center)
        ra = np.array([XX.flatten(), YY.flatten()])
        sel = array_point_in_poly(ra.T, p)
        sel_r = sel.reshape(self.nbins_y,self.nbins_x).T
        self.p_cut = sel_r
        return sel_r

    def draw_polygon(self, p, **kwargs):
        """
        draw a polygon used as cut

        ============   =====================================================
        Keyword        Meaning
        ============   =====================================================
        p               array of coordinate pairs determining the corners of the polygon
        ============   =====================================================

        Returns
        -------
        None.

        """
        px = list(p[:,0]) + [p[0,0]]
        py = list(p[:,1]) + [p[0,1]]
        pl.plot(px, py, **kwargs)


    def find_bin(self, x, y):
        """

        Find the bin value pair for that would contain
        the value pair x, y

        """
        ix = self.__find_bin(self.x_bins, x)
        iy = self.__find_bin(self.y_bins, y)
        return ix,iy

    def project_x(self, range = None, bins = None):
        """

        project a range of y-bins onto the x-axis

        ============   =====================================================
        Keyword        Meaning
        ============   =====================================================
        range          the range in y included in the projection
        bins           an array of bins or a slice selecting the y-bins to be
                       included in the projection
        both None      Project all the y-bins
        ============   =====================================================

        Returns
        -------
        1d - histogram

        """
        if range is None and bins is None:
            sel_y = slice(0,-1)
        elif range is not None:
            sel_y =  (range[0] <= self.y_bin_center) & (self.y_bin_center <= range[1])
        else:
            sel_y = bins
        # get the slice pf bin_content
        # get the slice pf bin_content
        y1 = self.y_bin_center[sel_y][0]
        y2 = self.y_bin_center[sel_y][-1]
        cont = self.bin_content[:,sel_y]
        d_cont = self.bin_error[:,sel_y]
        # sum allong y
        c = np.apply_along_axis(np.sum, 1, cont)
        dc = np.sqrt(np.apply_along_axis(np.sum, 1, d_cont**2))
        h = histo(bin_center = self.x_bin_center, bin_content = c, bin_error = dc)
        h.title = f"{self.title} x-projection for y between ({y1:.2e},{y2:.2e})"
        h.xlabel=self.xlabel
        h.ylabel="content"
        return h

    def project_y(self, range = None, bins = None):
        """

        project a range of x-bins onto the y-axis

        ============   =====================================================
        Keyword        Meaning
        ============   =====================================================
        range          the range in x included in the projection
        bins           an array of bins or a slice selecting the x-bins to be
                       included in the projection
        both None      Project all the x-bins
        ============   =====================================================

        Returns
        -------
        1d - histogram

        """
        if range is None and bins is None:
            sel_x = slice(0,-1)
        elif range is not None:
            sel_x =  (range[0] <= self.x_bin_center) & (self.x_bin_center <= range[1])
        else:
            sel_x = bins
        # get the slice pf bin_content
        x1 = self.x_bin_center[sel_x][0]
        x2 = self.x_bin_center[sel_x][-1]
        cont = self.bin_content[sel_x,:]
        d_cont = self.bin_error[sel_x,:]
        # sum allong y
        c = np.apply_along_axis(np.sum, 0, cont)
        dc = np.sqrt(np.apply_along_axis(np.sum, 0, d_cont**2))
        h = histo(bin_center = self.y_bin_center, bin_content = c, bin_error = dc)
        h.title = f"{self.title} y-projection for x between ({x1:.2e},{x2:.2e})"
        h.xlabel=self.ylabel
        h.ylabel="content"
        return h

    def apply_calibration(self, cal_x, cal_y):
        """

        apply x and y-axis calibration, new axis values are cal(xaxis) cal(yaxis)

        ============   =====================================================
        Keyword        Meaning
        ============   =====================================================
        cal_x          x-axis calibration function
        cal_y          y-axis calibration function
        ============   =====================================================

        Returns
        -------
        None., calculates new bin vakues

        """
        # x-axis
        self.x_bin_center = cal_x(self.x_bin_center)
        self.x_bin_width = np.diff(self.x_bin_center)[0]
        self.x_bins = cal_x(self.x_bins)
        # y -axis
        self.y_bin_center = cal_y(self.y_bin_center)
        self.y_bin_width = np.diff(self.y_bin_center)[0]
        self.y_bins = cal_y(self.y_bins)
        # prepare histo plot if axes have changed
        self.__prepare_histo_plot()

# private functions

    def __setup_bins(self, error = None ):
        self.x_bin_width = np.diff(self.res[1])[0]
        self.y_bin_width = np.diff(self.res[2])[0]
        self.x_bin_center = self.res[1][:-1] + self.x_bin_width/2.
        self.y_bin_center = self.res[2][:-1] + self.y_bin_width/2.
        self.bin_content = self.res[0]
        self.x_bins = self.res[1]
        self.y_bins = self.res[2]
        if error is None:
            if not self.has_weights:  # no weights specified
                self.bin_error = np.sqrt(self.bin_content)
            elif self.calc_w2:   # weights given and sum(weights**2) calculated for each bin
                self.bin_error = np.sqrt(self.w2)
            else:
                self.bin_error = np.sqrt(self.bin_content)
        else:
            self.bin_error = error
        self.__prepare_histo_plot()

    def __setup_histogram(self):
        # create the histogram arrays from bin_width, bin_center, bin_content and bin_error
        self.x_bin_width = np.diff(self.x_bin_center)[0]
        self.y_bin_width = np.diff(self.y_bin_center)[0]
        res1 = np.concatenate( [self.x_bin_center - self.x_bin_width/2., self.x_bin_center[-1:] + self.x_bin_width/2.])
        res2 = np.concatenate( [self.y_bin_center - self.y_bin_width/2., self.y_bin_center[-1:] + self.y_bin_width/2.])
        res0 = self.bin_content
        self.res = ([res0,res1,res2])

    def __prepare_histo_plot(self):
        # prepare data for plotting as steps
        self.__setup_histogram()


    def __find_bin(self,bins, x):
        # self.bins contains the bin edged
        if (x < bins[0]):
            print('searched value {0} < lowest bin = {1} '.format(x, bins[0]))
            return 0
        elif (x > bins[-1:][0]):
            print('searched value {0} > highest bin = {1} '.format(x, bins[-1:][0]))
            return len(bins) - 1
        elif (x == bins[0]):
            return 0
        else:
            return (np.searchsorted(bins, x) - 1 )

    def __add__(self, v):
        # add 2 histograms and take care of the errors
        # check the shapes
        if np.isscalar(v):
            res0 = self.bin_content+ v
            err = self.bin_error
            res1 = np.copy(self.res[1])
            res2 = np.copy(self.res[2])
            res = ([res0, res1, res2 ])
            return histo2d(histogram = res, bin_error = err)
        elif np.array_equal(self.bin_content.shape, v.bin_content.shape):
            # this is the content
            res0 = self.bin_content + v.bin_content
            err = np.sqrt( self.bin_error**2 + v.bin_error**2)
            res1 = np.copy(v.res[1])
            res2 = np.copy(v.res[2])
            res = ([res0, res1, res2 ])
            return histo2d(histogram = res, bin_error = err)
        else:
            print('shapes do not match-> cannot add, sorry !')
            return None

    def __sub__(self, v):
        # subtract 2 histograms and take care of the errors
        # check the shapes
        if np.isscalar(v):
            res0 = self.bin_content - v
            err = self.bin_error
            res1 = np.copy(self.res[1])
            res2 = np.copy(self.res[2])
            res = ([res0, res1, res2 ])
            return histo2d(histogram = res, bin_error = err)
        elif np.array_equal(self.bin_content.shape, v.bin_content.shape):
            # this is the content
            res0 = self.bin_content - v.bin_content
            err = np.sqrt( self.bin_error**2 + v.bin_error**2)
            res1 = np.copy(v.res[1])
            res2 = np.copy(v.res[2])
            res = ([res0, res1, res2 ])
            return histo2d(histogram = res, bin_error = err)
        else:
            print('shapes do not match-> cannot subtract, sorry !')
            return None

    def __mul__(self, v):
        # histogram multiply from left
        if np.isscalar(v):
            res0 = v*self.res[0]
            err = v*self.bin_error
            res1 = np.copy(self.res[1])
            res2 = np.copy(self.res[1])
            res = ([res0, res1, res2 ])
            return histo2d(histogram = res, bin_error = err)
        elif np.array_equal(self.bin_content.shape, v.bin_content.shape):
            # this is the content
            res0 = self.bin_content * v.bin_content
            f1 = v.bin_content
            f2 = self.bin_content
            err = np.sqrt( (f1*self.bin_error)**2 + (f2*v.bin_error)**2)
            res1 = np.copy(v.res[1])
            res2 = np.copy(v.res[2])
            res = ([res0, res1, res2 ])
            return histo2d(histogram = res, bin_error = err)
        else:
            print('shapes do not match-> cannot add, sorry !')
            return None

    def __truediv__(self, v):
        # divide 2 histograms and take care of the errors
        # check the shapes
        if np.isscalar(v):
            res0 = self.res[0]/v
            err = self.bin_error/v
            res1 = np.copy(self.res[1])
            res2 = np.copy(self.res[1])
            res = ([res0, res1, res2 ])
            return histo2d(histogram = res, bin_error = err)
        elif np.array_equal(self.bin_content.shape, v.bin_content.shape):
            # this is the content
            res0 = self.bin_content / v.bin_content
            f1 = 1./v.bin_content
            f2 = res0/v.bin_content
            err = np.sqrt( (f1*self.bin_error)**2 + (f2*v.bin_error)**2)
            res1 = np.copy(v.res[1])
            res2 = np.copy(v.res[2])
            res = ([res0, res1, res2 ])
            return histo2d(histogram = res, bin_error = err)
        else:
            print('shapes do not match-> cannot add, sorry !')
            return None



    def __radd__(self, v):
        # add 2 histograms and take care of the errors
        # check the shapes
        if np.isscalar(v):
            res0 = self.bin_content+ v
            err = self.bin_error
            res1 = np.copy(self.res[1])
            res2 = np.copy(self.res[2])
            res = ([res0, res1, res2 ])
            return histo2d(histogram = res, bin_error = err)
        elif np.array_equal(self.bin_content.shape, v.bin_content.shape):
            # this is the content
            res0 = self.bin_content + v.bin_content
            err = np.sqrt( self.bin_error**2 + v.bin_error**2)
            res1 = np.copy(v.res[1])
            res2 = np.copy(v.res[2])
            res = ([res0, res1, res2 ])
            return histo2d(histogram = res, bin_error = err)
        else:
            print('shapes do not match-> cannot add, sorry !')
            return None

    def __rsub__(self, v):
        # subtract 2 histograms and take care of the errors
        # check the shapes
        if np.isscalar(v):
            res0 = self.bin_content - v
            err = self.bin_error
            res1 = np.copy(self.res[1])
            res2 = np.copy(self.res[2])
            res = ([res0, res1, res2 ])
            return histo2d(histogram = res, bin_error = err)
        elif np.array_equal(self.bin_content.shape, v.bin_content.shape):
            # this is the content
            res0 = self.bin_content - v.bin_content
            err = np.sqrt( self.bin_error**2 + v.bin_error**2)
            res1 = np.copy(v.res[1])
            res2 = np.copy(v.res[2])
            res = ([res0, res1, res2 ])
            return histo2d(histogram = res, bin_error = err)
        else:
            print('shapes do not match-> cannot subtract, sorry !')
            return None

    def __rmul__(self, v):
        # histogram multiply from left
        if np.isscalar(v):
            res0 = v*self.res[0]
            err = v*self.bin_error
            res1 = np.copy(self.res[1])
            res2 = np.copy(self.res[1])
            res = ([res0, res1, res2 ])
            return histo2d(histogram = res, bin_error = err)
        elif np.array_equal(self.bin_content.shape, v.bin_content.shape):
            # this is the content
            res0 = self.bin_content * v.bin_content
            f1 = v.bin_content
            f2 = self.bin_content
            err = np.sqrt( (f1*self.bin_error)**2 + (f2*v.bin_error)**2)
            res1 = np.copy(v.res[1])
            res2 = np.copy(v.res[2])
            res = ([res0, res1, res2 ])
            return histo2d(histogram = res, bin_error = err)
        else:
            print('shapes do not match-> cannot add, sorry !')
            return None


    def __rtruediv__(self, v):
        # divide 2 histograms and take care of the errors
        # check the shapes
        if np.isscalar(v):
            res0 = v/self.res[0]
            err = v/self.res[0]**2*self.bin_error
            res1 = np.copy(self.res[1])
            res2 = np.copy(self.res[1])
            res = ([res0, res1, res2 ])
            return histo2d(histogram = res, bin_error = err)
        elif np.array_equal(self.bin_content.shape, v.bin_content.shape):
            # this is the content
            res0 =  v.bin_content/self.bin_content
            f1 = 1./self.bin_content
            f2 = res0/self.bin_content
            err = np.sqrt( (f1*v.bin_error)**2 + (f2*self.bin_error)**2)
            res1 = np.copy(v.res[1])
            res2 = np.copy(v.res[2])
            res = ([res0, res1, res2 ])
            return histo2d(histogram = res, bin_error = err)
        else:
            print('shapes do not match-> cannot add, sorry !')
            return None

# end of histo class




# get an MCA spectrum as histogram
def get_spectrum(file, calibration = None):
    """

    Read an MCA spectrum and convert it to a histogram.

    Example::

       >>> h = B.get_spectrum('co60.spe')  # read the spectrum
       >>> h.plot()                        # plot the spectrum

    """
    sp = mcsp.MCA(file)
    sp_title = sp.spectrum['$DATE_MEA'] + \
        " live time = %6.1f s, total time = %6.1f s"%(sp.spectrum['$MEAS_TIM'][0],\
                                                           sp.spectrum['$MEAS_TIM'][1])
    # create histogram
    if calibration is None:
        h = histo(bin_center=sp.chn, bin_content = sp.cont, title = sp_title)
        h.xlabel = 'Channels'
    elif calibration == 'internal':
        h = histo(bin_center=sp.energy, bin_content = sp.cont, title = sp_title)
        h.xlabel = 'Energy'
    else:
        chan_values = calibration( sp.chn )
        h = histo(bin_center=chan_values, bin_content = sp.cont, title = sp_title)
        h.xlabel = 'User Calibration'
    # set the titles
    h.ylabel = 'Counts'
    return(h)
