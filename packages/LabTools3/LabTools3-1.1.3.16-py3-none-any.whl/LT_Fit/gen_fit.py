"""

Tool for general non-linear fitting based on the Marquardt algorithm. To setup a fit you need to::

   1. define parameters and assign them reasonable initial values
   2. define a fitting function in terms of the parameters
   3. define the fit and carry it out

Depending on the outcome, one might need to change the initial values of the parameters or
decide to change which parameters are fixed and which are to be fitted.

1. Setting up the parameters::
    
    >>> import numpy as np
    >>> import LT_Fit.parameters as P  # get the parameter module
    >>> import LT_Fit.gen_fit as G     # load the genfit module
    >>> a = P.Parameter(1., 'amp')     # parameter a, called 'amp', initialized to 1. 
    >>> b = P.Parameter(3., 'omega')   # parameter b, called 'omega', intialized to 3.
    >>> c = P.Parameter(1.5, 'phase')  # parameter c, called 'phase', initialize to 1.5


    

2. Define the fitting function::

    >>> def f(x):
    ....    return a()*np.sin(b() * x + c() )
    

3. Setup pseudo data::
    
    >>> xval = np.linspace(0,2,20)        # generate pseudo data
    >>> y = f(xval)
    >>> y_exp = y + np.random.normal(loc = 0, scale = 0.05, size = len(y))
    >>> sig_y = np.ones_like(y)*0.05
    

4. Now do the fit::

    >>> F = G.genfit( f, [a, b, c], x = xval, y = y_exp) #  the list [a,b,c] defines which parameters are fitted
    >>> F = G.genfit( f, [a], x = xval, y = y_exp, y_err = sig_y) #  only a is fitted, but take the exp. error into account
    >>> F = G.genfit( f, [a, c], x = xval, y = y_exp, y_err = sig_y) #  a and c are fitted b is kept constant
    
To change the initial values and repeat the fit::

    >>> a.set(1.5)
    >>> b.set(3.2)
    >>> c.set(2.0)
    >>> F = G.genfit( f, [a, b, c], x = xval, y = y_exp)
    
Calculate parameter derivatives analytically::
    
    >>> dfda = lambda x : np.sin(b() * x + c() )       # derivative wrsp a
    >>> dfdb = lambda x : a()*np.cos(b() * x + c() )*x # derivative wrsp b
    >>> dfdc = lambda x : a()*np.cos(b() * x + c() )   # derivative wrsp c
    >>> deriv_list = [dfda, dfdb, dfdc]                # list of derivative functions
    >>> # do the fit using analytically calculated derivatives
    >>> F = G.genfit( f, [a, b, c], x = x, y = y_exp, y_err = sig_y, func_deriv=deriv_list) 


Finally plot the data and the fit::

    >>> import LT.box as B
    >>> B.plot_exp(xval, y_exp, sig_y)   # plot the data with errorbars
    >>> F.plot()                        # plot the fitted function as a line    
    >>> B.plot_line(F.xpl, F.ypl)       # old version of plotting the fitted function as a line
    >>> F(x)                            # evaluate the fitted function at x
    >>> show()                          # show the new plot


----------------------------------------------------------


"""
#
from scipy import optimize
# for chi2 probability
import scipy.stats as SS
import matplotlib.pyplot as pl

import copy as C
# from LT_Fit.parameters import *
import numpy as np
# import pdb


class  genfit:
    """

    general non-linear fit  based on the Marquardt algorithm

    Important keywords:
    
    ==========   ===================================================================
    Keyword      Meaning
    ==========   ===================================================================
    y            (:func:`numpy.array`) array of experimental values (mandatory)
    x            (:func:`numpy.array`) array of independent variables 
    y_err        (:func:`numpy.array`) array of errors
    nplot        number of points to be used for plotting the fit
    ftol         minimal change in chi square to determine if the fit has converged
    diff_step    step size used to the numerical calculation of derivetives with respect to the
                 fit parameters (default = 0.001), h = diff_step * par
    kwargs       additional keywords are passes to scipy.optimize.least_squares, examples below
    bounds       an array for upper and lower bounds for the parameter
    loss         alternative loss function to handle outliers e.g. 'huber'
    f_scale      outliers with a residual more the f_scale should be not affect the result
    plot_fit     (default True) plot the fitted function automatically
    func_deriv   list of functions corresponding to the fit parameter list (parameters)
                 that calculate the derivative of the fit function with respect to each 
                 of the fit parameters. (default = None)
    ==========   ===================================================================

    Additional keyword arguments are passed on to :func:`scipy.optimize.leastsq`

    """
    def __init__(self, function, parameters, \
                 x = None, \
                 y = None, \
                 y_err = None, \
                 nplot = 100, \
                 full_output = 1, \
                 ftol = 0.001, \
                 diff_step = 0.001, \
                 print_results = True, \
                 plot_fit = True, \
                 func_deriv = None, \
                 **kwargs):
        print('gen_fit kwargs = ', kwargs)
        self.plot_fit = plot_fit
        self.print_results = print_results
        self.y = y
        if x is None:
            if y is not None:
                self.x = np.arange(y.shape[0])
            else:
                self.x = x
        else:
            self.x = x
        self.y_err = y_err
        self.nplot = nplot
        self.parameters = parameters # the array stores the addresses of the parameter objects
        self.func = function
        self.func_deriv = func_deriv
        # carry out the fit
        if y is None:
            print('No values to fit, use set_yval to set them before fitting !')
            return
        return self.fit(full_output = full_output, \
                 ftol = ftol, \
                 diff_step = diff_step, \
                 **kwargs)

    def f(self, params):
        # define minimzation function for least square
        for i,p in enumerate(self.parameters):
            # store the current values in the array p back into the parameter
            # classes to be used by the user defined function
            # check if there is only 1 parameter
            ps = params.shape
            if len(ps) > 0:
                p.set(params[i])
            else:
                p.set(params)
        # now calculate the difference between data and fit function
        # and return it to the optimization routine
        if self.y_err is None:
            return self.y - self.func(self.x)
        else:
            return (self.y - self.func(self.x))/self.y_err
    # end of the minimization function
    
    def f_jac(self, params):
        # calculate the jacobian analytically for a list of derivative functions if available
        # define minimzation function for least square        i = 0
        for i,p in enumerate(self.parameters):
            # store the current values in the array p back into the parameter
            # classes to be used by the user defined function
            # check if there is only 1 parameter
            ps = params.shape
            if len(ps) > 0:
                p.set(params[i])
            else:
                p.set(params)
        if self.y_err is None:        
            jac = np.array([-f(self.x) for f in self.func_deriv]).T
        else:
            jac = np.array([-f(self.x)/self.y_err for f in self.func_deriv]).T
        return jac
    
    def plot(self, xv = None, **kwargs):
        """
        Plot the fitting function 

        Parameters
        ----------
        xv : TYPE, optional
            x-values for which the fitting function should be plotted. The default is None i.e. using the standard xpl and ypl values.

        **kwargs : TYPE
            keyword aguments passed to matplotlib plot function

        Returns
        -------
        None.

        """
        if (xv is None):
            pl.plot(self.xpl, self.ypl, **kwargs)
        else:
            pl.plot(xv, self.func(xv), **kwargs)    

    def fit(self, full_output = 1, ftol = 0.001, diff_step = 0.001, **kwargs):
        # this is the minimzation routine
        # store the current parameter values in a list to be passed to the fitting function 
        # this is an implicit loop, it is equivalent to
        # p =[]
        # for param in parameters:
        #     p.append(param())
        # clear the parameter errors:
        print('gen_fit.fit kwargs = ', kwargs)
        for p in self.parameters:
            p.err = 0.
        p = [param() for param in self.parameters]
#        old version
#        self.fit_result = optimize.leastsq( self.f, p,\
#                                            full_output = full_output, \
#                                            ftol = ftol, \
#                                            **kwargs)
        if self.func_deriv is None:
            print(f'Calculate numerical parameter derivatives with diff_step = {diff_step}')
            self.fit_result = optimize.least_squares( self.f, p,\
                                                ftol = ftol, \
                                                diff_step = diff_step, \
                                                **kwargs)
        else:
            print('Calculate analytical parameter derivatives ')
            self.fit_result = optimize.least_squares( self.f, p,\
                                                ftol = ftol, \
                                                jac = self.f_jac, \
                                                **kwargs)
            
            
        # estimate covariance matrix
        J = self.fit_result.jac 
        try:
            self.covar = np.linalg.inv(J.T.dot(J))
        except Exception as err:
            print(f'Cannot calculate covariance matrix, reason: {err}')
            print(f'jacobian = {J}')
            self.stat = {}
            self.covar = [] 
            self.xpl = []
            self.ypl = []
            self.chi2 = -1.
            self.chi2_red = -1.
            self.CL = -1.
            return    
        # now calculate the fitted values
        fit_func = self.func(self.x)
        # final total chi square
        p_fin = self.fit_result.x
        # number of degrees of freedom
        ps = p_fin.shape
        if len(ps) > 0:
            # if there was only 1 data point
            self.n_dof = len(self.y) - len(p_fin)
        else:
            self.n_dof = len(self.y)
        self.chi2 = np.sum( np.power( self.f( self.fit_result.x) , 2) )
        self.chi2_red = self.chi2/self.n_dof
        # calculate confidence level = prob to get a chi2 larger that the one obtained
        self.CL = 1. - SS.chi2.cdf(self.chi2, self.n_dof)
        #
        self.xpl = []
        self.ypl = []
        self.stat = {'fitted values':fit_func, \
                     'parameters':self.fit_result.x, \
                     'leastsq output':dict(self.fit_result)}
        if (self.nplot > 0):
            self.xpl = np.linspace(self.x.min(), self.x.max(), self.nplot+1)
            self.ypl = self.func(self.xpl)
        # set the parameter errors
        try:
            if self.y_err is None:
                # res-scale covariance matrix by chi2_red to get the correct values
                self.covar *= self.chi2_red
                self.common_error = np.sqrt(self.chi2_red)
            for i,p in enumerate(self.parameters):
                p.err = np.sqrt( self.covar[i,i] )
        except:
            print("gen_fit : problem with fit, parameter errors,  check initial parameters !")
            print('covariance matrix : ', self.covar)
            print('current parameter values : ')
            self.show_parameters()
        #
        if self.print_results:
            print('----------------------------------------------------------------------')
            print('fit results : ')
            print('----------------------------------------------------------------------')
            print('chisquare = ',self.chi2)
            print('red. chisquare = ',self.chi2_red)
            print('parameters: ')
            self.show_parameters()
        if self.plot_fit:
            self.plot()

    def set_yval(self, y, y_err = None):
        """
        
        set the array of values to be fitted

        """
        self.y = y
        self.y_err = y_err

    def set_xval(self, x):
        """
        
        set the array of values x

        """
        self.x = x

    def show_parameters(self):
        """

        show the fitted parameters


        """
        for i,p in enumerate(self.parameters):
            print('parameter ', i, ' : ', p)

    def save_parameters(self):
        """

        make a deep copy of the current parameters to be saved


        """
        self.parameters_sav = C.deepcopy(self.parameters)

    def get_parameters(self):
        """

        use the saved parameters

        """
        for i,p in enumerate(self.parameters_sav):
            self.parameters[i].value = p.value
            self.parameters[i].err = p.err
            
    def __call__(self, x):
        """
        Evaluate fitting function at x

        Parameters
        ----------
        x : float
            values of independent variable 

        Returns
        -------
        self.func: float 
            value of fitting function at x .

        """
        return self.func(x)

        




