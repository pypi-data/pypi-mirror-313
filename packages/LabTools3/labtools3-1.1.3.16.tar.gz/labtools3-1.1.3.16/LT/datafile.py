"""

Reads a file containing columns of data and creates a dictionary according to header information
using the following format:

1. comments start with ``#`` in the **first column** : ``# My Comment``

2. header information starts with ``#!``, where ``#`` is also in the **first column**. It must precede the data.

3. each columns is represented by ``name[dtype, col.nr.]/``,  *dtype* (optional) is the data type and *col.nr*
   (starting at 0) is the column number

4. data are separated by white space **NOT commas!**

5. data types:

      - s : string
      - f : float
      - i : integer

6. blank lines are ignored

 **NOTE**: if data formats are entered they should be specified for all columns

Example data::

   #! p_miss[0]/ siglt[2]/ s01[3]/ alt[4]/
   200. 1.35e-4 -1.e-3    0.1
   220. 2.56e-4 -2.e-4    -0.1
   230. 3.47e-6 -3.e-5    1.1

The header can also contain data type information::

   #! p_miss[f,0]/ siglt[f,2]/ s01[f,3]/ alt[f,4]/

   200. 1.35e-4 -1.e-3    0.1
   220. 2.56e-4 -2.e-4    -0.1
   230. 3.47e-6 -3.e-5    1.1


Example that opens a file and create a dfile object::

   >>> f0 = dfile('sig_LT.dat')

Loop over content::

   >>> for l in f0:
   >>> ...pm = l['p_miss']
   >>> ...sig_lt = l['siglt']*10000.
   >>> ...print pm, sig_lt, l['alt']
   >>> # end for l


Variables can also be accessed directly as numpy arrays (if installed):

   >>> pm = f0['p_miss']
   >>> sig_lt = f0['siglt']*10000.

They can also be converted to attributes:

   >>> f0.make_attr()
   >>> print f0.p_miss
   >>> print f0.sig_lt

Variable names are also called keys.

Save the data file as a csv file, this is useful for exporting and formatting for 
documents (other than latex)

   >>> f0.write_csv(filename)


---------------------------------------------------------

"""

import sys
import os
import string
import math
import re
import pdb

numpy_ok = True
try:
    import numpy as np
except:
    numpy_ok = False

# function to create a dictionary from 2 lists: key, values
format_dict = {'i':'{:d}', 'f':'{:f}', 's':'{:s}'}
# create a dictionary from  an array of keys and values
#----------------------------------------------------------------------
def find_duplicates(array):
    # array with no duplicates
    na = []
    # counter array
    count = []
    # arrays with duplucates
    da = []
    for a in array:
        try:
            na.index(a)
        except:
            na.append(a)
            count.append(0.)
    # na has no duplicates
    for i,a in enumerate(na):
        for aa in array:
            if aa == a:
                count[i]+= 1
    for i,c in enumerate(count):
        if c>1:
            da.append(na[i])
    return da
#----------------------------------------------------------------------


class dfile:
    """
    Open a file, read and interpret the contents and return a dfile object:

    >>> df = dfile('my_datafile')

    keywords:
        
        debug = False (default) : print additional iformation
        
        fast = False (default) : load data in a fast way (using np.loadtxt) this has
                                 some limits for string entries. Best used for large purely
                                 numerical data.
                                 
        use_numpy = True (if numpy is installed) : set automatically but can be overridden
                                                   some attributes of datafile are not availables when
                                                   numpy is not present
                                                   
        adata = my_lines (default = None) : use the data provided in a list of strings (my_lines) as data file content. 
                                            The content of my_lines must follow the datafile syntax.
        
    """
    def __init__(self, filename, debug = False, new=False, skip = True, use_numpy = numpy_ok, fast = False, adata = None):
        self.H=re.compile("^#\!") # pattern for header
        self.C=re.compile("^#")   # pattern for comment
        # pattern for splitting header
        # currently:
        # ^#\! : matches line beginning with #!
        # \[[0-9]+\]\/: matches [0]/ ... [8796]/
        # \[ *\w+ *, *\w *\]\/ : matches [   f  , blabla   ]/
        #
        self.S=re.compile("^#\!|\[[0-9]+\]\/|\[ *\w *, *\w+ *\]\/")
        # pattern to find format information in the header
        self.F=re.compile("\w+ *, *\w+")
        # pattern to find a character
        self.Fc=re.compile("[a-zA-Z]")
        # pattern to find a number
        self.Fn=re.compile("[0-9]+ *\]")
        # supported formats: the output format dictionary key must match the supported formats
        self.fmt_characters = ['f','i','s']
        self.dt_formats = {'f':'f8', 'i':'i4','s':'S32'}
        self.output_format= {'f':'%r ','i':'%d ','s':'%s '}
        # empty dictionary for the formats
        self.formats = {}
        self.formats_dt = {}
        self.cols = {}
        # flag for printing debugging information
        self.debug = debug
        # flat to ignore bad line in input
        self.skip = skip
        self.use_numpy = use_numpy
        if not self.use_numpy:
            print('numpy will not be used !')
        if fast and (not use_numpy):
            print ('fast mode not possible as numpy cannot be used!')
            fast = False
        self.fast = fast
        #
        self.header = None
        self.data = []
        self.adata = []
        self.adata_index = []
        self.adata_comment_index = []
        self.fdata=[]
        self.keys=[]
        self.new = False
        if new:
            new=True
            self.filename = filename
            self.keys.append('indx')
            self.headindex=0
            self.headerline = ('#! ')
            self.adata.append('#! ')
            return
        # pdb.set_trace()
        # open file
        self.filename = filename
        if adata is None:
            i=open(filename,"r")      # open file            
            # remove leading and trailing spaces
            self.adata=[ x.strip() for x in i.readlines()]   # read all data  
            i.close()
        else:
            self.adata = [ x.strip() for x in adata]
        if self.debug :
            print("datafile --> data read !")
        if self.debug :
            print("datafile --> spaces removed read !")
        self.remove_blanks()
        if self.debug :
            print("datafile --> blank lines removed read !")
        if (self.find_header() != 0): # find the header
            print("cannot interpret data, header probably missing or wrong")
            return
        if self.debug :
            print("datafile --> create arrays !")
        self.make_array()  # read data
        # remove the header line from the comment index list
        self.adata_comment_index.remove(self.headindex)
        if self.debug :
            print("datafile --> arrays created !")
    def __getitem__(self,i):
        # allows 'direct' access to the data
        if type(i) is int:
            # it'sm index
            return self.data[i]
        elif type(i) is str:
            # its a lkey return the list of data
            return self.get_data(i)
    def __len__(self):
        return len(self.data)
    def remove_blanks(self):
        # work through the list in reverse order
        indices = list(range( len( self.adata ))) # list of indices
        indices.reverse() # reverse order
        for i in indices: # loop through from the top
            if len(self.adata[i].strip()) == 0:
                del self.adata[i]
    def find_header(self):
        # find header information : look for a line starting with #!
        for i,l in enumerate(self.adata):
            if (self.H.match(l) != None):
                self.headindex=self.adata.index(l)
                self.headerline=l
                self.header=re.split(self.S,l)[1:-1] # remove first and last element
                self.keys=[ x.strip() for x in self.header]
                self.keys.append('indx') # store the index into the original
                # handle data format
                # check for duplicate keys
                duplicate_keys = find_duplicates(self.keys)
                if duplicate_keys != []:
                    print("duplicate keys found : ", duplicate_keys)
                    return -1
                # pdb.set_trace()
                fmt = re.findall(self.F,l)
                col_t = re.findall(self.Fn,l)
                col = [cc.replace(']','') for cc in col_t]
                # no format specification, set default format
                if fmt == []:
                    for i,k in enumerate(self.keys[:-1]) : # skip index
                        self.formats[k] = 'f'
                        self.formats_dt[k] = self.dt_formats['f']
                # use format specifications
                else:
                    for i,f in enumerate(fmt):
                        fc = re.findall(self.Fc,f)[0] # use 1st char. for format
                        self.formats[self.keys[i]] = fc
                        self.formats_dt[self.keys[i]] = self.dt_formats[fc]
                # addformat for the index
                self.formats['indx'] ='i'
                self.formats_dt['indx'] = self.dt_formats['i']
                # use format specifications
                for i,cc in enumerate(col):
                    f = self.formats[self.keys[i]]
                    if f == 's':
                        self.cols[self.keys[i]] = ''
                    else:
                        self.cols[self.keys[i]] = col[i]
                self.cols['indx'] ='-1'
                # addformat for the index
                # adata array
                # do some checks
                if (len(self.keys)  != len(self.formats)):
                    print(self.filename,": problem in data formats !")
                    print(self.adata)
                    return -1
                return 0
            elif(self.C.match(l) != None):
                # found a comment line that is not a header line
                self.adata_comment_index.append(i)
        print(self.filename,": no header information !")
        print('data dump : ')
        print(self.adata)
        return -1

    def parse_line(self, l):
        if (self.C.match(l) != None) : # not a comment
            return 'C'
        ll=l.split()
        # handle file format problems
        if len(ll) > (len(self.keys)-1) :
            n_data = (len(self.keys)-1)
            print(self.filename, ' error: more data than variable names !')
            print(' ---> check header : ', self.headerline)
            print('current line : ', self.line_n+1, ' ', ll)
            if self.skip:
                print('skipping !')
                return None
            else:
                sys.exit(-1)
        if len(ll) < (len(self.keys)-1) :
            print(self.filename, ' error: too few data values !')
            print(' ---> check header : ', self.headerline)
            print('current line : ', self.line_n+1, ' ', ll)
            if self.skip:
                print('skipping !')
                return None
            else:
                sys.exit(-1)
        f = []
        # now convert to values
        for i,k in enumerate(ll):
            # check if there are format specifications
            f_err = False
            try:
                fmt = self.formats[self.keys[i]]
                fc = fmt
                # check that the format is supported
                fi = self.fmt_characters.index(fmt)
            except:
                f_err = True
                print('unknown format : ', fc, ' set to f')
                fc = 'f'
                self.formats[self.keys[i]] = 'f'
            # now try to convert according to the format
            try:
                if fc == 'f':
                    f.append(float(k)) # create a float
                if fc == 'i':
                    f.append(int(k))   # create an integer
                if fc == 's':
                    f.append(k)        # leave as string
            except:
                f.append(k) # if not possible leave it,
                # but make a comment
                if len(self.formats) == 0 :
                    print('cannot convert : ', k, ' to float, line : ', self.line_n +1)
                else:
                    if (f_err ):
                        print('cannot convert : ', k, ' line : ', self.line_n+1,\
                            ', problem with unknown format : ', fmt)
                    else:
                        print('cannot convert : ', k, ' line : ', self.line_n+1,\
                            ', with format :', fmt)
        f.append(self.adata.index(l))
        # pdb.set_trace()
        return f

    def make_array(self):
        if self.fast:
            # use loadtxt to get the data
            data_types = [self.formats_dt[k] for k in self.keys[:-1]]
            self.data = np.loadtxt(self.filename, dtype = {'names':self.keys[:-1], 'formats':data_types})
        else:   
               # create an array of dictionaries
            self.data = []
            n_data = len(self.adata)
            for self.line_n, l in enumerate(self.adata):
                f = self.parse_line(l)
                # potential comment line was found
                if f == 'C':      
                    if self.line_n in self.adata_comment_index:  # has already been registered as comment line
                        continue
                    else:
                        self.adata_comment_index.append(self.line_n)  # add index to list of comment lines
                        continue
                elif f == None:
                    continue
                self.data.append(self.make_dict(self.keys,f) )
                self.adata_index.append(self.line_n)
                if self.debug:
                    print("processed data : ", self.line_n, " out of ", n_data)
            
    def make_dict(self,keys,values):
        # create a dictionary from a list of keys and values
        p = []
        for j,key in enumerate(keys): # loop over keys
            try:
                p.append( (key.strip(),values[j]) ) # an array of tuples
                d=dict(p) # create a dictionary
            except:
                print('problem in data : ', key, values, j)
            #
        return d

    def make_attr(self):
        # make attributes out of the keys
        for k in self.keys:
            ka = ''
            try:
                self.__dict__[k]
                # attrtibute exists append _d
                ka = k + '_d'
                print(("{:s} exists using : {:s}".format(k, ka)))
            except:
                ka = k
            # replace periods with underscores
            if self.use_numpy:
                setattr(self, ka.replace('.','_'), np.array(self[k]))
            else:
                setattr(self, ka.replace('.','_'), self[k])
                    

    def scale(self, key, factor):
        """
        multiply all values of key with a factor
        """
        for i, d in enumerate(self.data):
            self.data[i][key] = factor*d[key]
        #

    def sort(self, key, **kwargs):
        """
        sort the data according to the values in key
        """
        index_array = []
        for d in self.data:
            index_array.append((d[key], self.data.index(d))) # store index and values pair
        sorted_array = sorted(index_array,**kwargs) # create a sorted array
        temp = []
        for ip in sorted_array:
            temp.append(self.data[ip[1]])
        self.data = temp
        temp=[]

    def name(self):
        """
        print the filename associate with this instance

        """
        print("Input file name : ", self.filename)
    def show_keys(self):
        """
        print a list of variable names in the dictionary

        """
        print(self.keys)
    def get_keys(self):
        """

        return a list of keys

        """
        return self.keys
    def get_header(self):
        """

        return the header lines

        """
        return self.adata[self.headindex]

    def get_full_header(self):
        """

        return all line up to the header line

        """
        return self.adata[:self.headindex+1]

    def show_data(self,keylist):
        """

        print all the data corresponding to the key list::

           >>> df.show_data('key1:key2:key3')

        """
        akey=keylist.split(":")
        for l in self.data:
            ll=[]
            for i in akey:
                format = self.output_format[ self.formats[i] ]
                ll.append( format%( l[i] ) )
            print(ll)


    def check_data(self, func, data, key, *args):
        """

        function used to check if data fulfill a condition provided
        by the user. The function is assumed to return True of False.

        """
        return func( data, key, *args)

    def select_data(self, sel_func = None, sel_args = None):
        """
        returns an iterator for the data. As in get_data() a selector function and
        its arguments can be supplied:

        conditions can be applied:

        1) sel_func: a user provided function returning True or False

        2) sel_args: a list of arguments used in the sel_func function

        The iterator returned can be used as follows:

        >>> for d in df.select_data():
        >>> ...print d

        or the result can be converted to a list:

        >>> list(df.select_data())

        Using a selector function:

        Example: assume the data contain a variable (key) called 'name'
           you want to select only those data where name contains a certain substring 'sub'

        Define this function:

        >>> def myfind(data, key , what):
        >>> ...where = data[key]
        >>> ...return (str.find(where, what) >= 0)

        now you can select the data using:

        >>> list( df.select_data( myfind, 'name', 'sub') )

        """
        if sel_func == None:
            for i,data in enumerate(self.data):
                yield data
        else:
            for i,data in enumerate(self.data):
                if self.check_data(sel_func, data, *sel_args):
                    yield data
        # that's all

    def select_data_eval(self, eval_str):
        """
        returns an iterator for data selected with an *eval* expression
        stored in the string `eval_str` each dataset item is accessed using the name data::

        >>> df.select_data_eval("data['x'] >= 0.")

        returns only those data items where the value of the x-column in the file
        is larger than or equal to 0.

        """
        for i,data in enumerate(self.data):
            if eval( eval_str):
                yield data
        # that's all

    def eval_data(self, eval_str):
        """
        iterator over all data evaluating an expression contained in eval_str
        """
        for i,data in enumerate(self.data):
            yield eval(eval_str)
        # that's all

    def get_data(self,key, sel_func = None, sel_args = None):
        """

        return all data for `key` subject to the results of a selector function.

        one can define a selector function (`sel_func`) using the arguments stored in `sel_args`.
        This function is evaluated for each data record and only
        those data are returned for which the condition is fulfilled.

        1) sel_func: a user provided function returning True or False

        2) sel_args: a list of arguments used in the sel_func function

        Example::
           assume the data contain a variable (key) called 'name'
           you want to select only those data where name contains a certain substring 'Jo'

        Define this function::

        >>> def myfind(data, key , what):
        >>> ...where = data[key]
        >>> ...return (str.find(where, what) >= 0)

        now you can select the data using::

        >>> df.get_data('name',myfind, ['name','Jo'] )

        This should return a list of names containing the substring 'Jo'

        """
        array=[]
        for l in self.data:
            if sel_func == None:
                array.append(l[key])
            else :
                if self.check_data( sel_func, l, *sel_args):
                    array.append(l[key])
        if self.use_numpy:
            return np.array(array)
        else:
            return array

    def get_data_eval(self,key,eval_str): # return data for a  key
        """

        return all data for the `key` under the condition that the expression in `eval_str`
        is True.

        """
        array=[]
        for l in self.select_data_eval(eval_str):
            array.append(l[key])
        if self.use_numpy:
            return np.array(array)
        else:
            return array


    def get_data_list(self,keylist, sel_func = None, sel_args = None):

        """

        return all the data corresponding to the key list
        as follows::

           >>> a = df.get_data_list('key1:key2:key3')

           >>> a = df.get_data_list('key1:key2:key3', myfind, ['name','J'])

        return those data where the `name` values contain the character `J`

        *a* contains the list of data

        """

        akey=keylist.split(":")
        dd = []
        if sel_func == None:
            for l in self.data:
                ll=[]
                for i in akey:
                    ll.append( l[i] )
                dd.append(ll)
            if self.use_numpy:
                return np.array(dd)
            else:
                return dd
        else:
            for l in self.data:
                if self.check_data(sel_func, l, *sel_args):
                    ll=[]
                    for i in akey:
                        ll.append( l[i] )
                    dd.append(ll)
            if self.use_numpy:
                return np.array(dd)
            else:
                return dd

    def get_data_list_eval(self,keylist, eval_str):
        """

        similar function as select_data_eval but it only returns the
        values for the keys defined in `keylist`.

        """
        akey=keylist.split(":")
        dd = []

        for l in self.select_data_eval(eval_str):
            ll=[]
            for i in akey:
                ll.append( l[i] )
            dd.append(ll)
        if self.use_numpy:
            return np.array(dd)
        else:
            return dd

    def show_all_data(self):
        """

        print all data and keys stored

        """
        for l in self.data:
            print(l)
    def get_all_data(self):
        """

        return a list of all data stored

        """
        return self.data
    def write_complete_header(self,fp):
        """
        write entire header including comments and internal parameters to file with
        handle fp. Example:
            
        fp = open('mydile.data','w')
        
        datafile.write_comlete_header(fp)
        
        """
        for i,l in enumerate(self.adata[0:self.headindex]):
            fp.write(l+'\n')
        # write header line
        h = '#! '
        n = 0
        for k in self.keys[:-1]:
            h = h + k+'['+'%s,%d'%(self.formats[k],n)+']/ '
            n = n +1
        fp.write(h+'\n')
    def update_header(self):
        """
        update header line of this data file including format. This
        makes sure that the header line is in sync with the dictionary keys
        """
        # write header line
        h = '#! '
        n = 0
        for k in self.keys[:-1]:
            h = h + k+'['+'%s,%d'%(self.formats[k],n)+']/ '
            n = n +1
        # update data arrays
        self.adata[self.headindex]=h
        self.headerline = h
    def write_header(self,fp):
        """
        write only header line of this data file into file fp, including format
        """
        # write header line
        h = '#! '
        n = 0
        for k in self.keys[:-1]:
            h = h + k+'['+'%s,%d'%(self.formats[k],n)+']/ '
            n = n +1
        fp.write(h+'\n')
    def write_line(self,fp, i):
        """
        write data line i into file fp
        """
        l = ''
        # check array boundary
        ndata = len(self.data)
        if (i<0) :
            print('index below lower bound, set to 0')
            i = 0
        if (i>=ndata):
            print('index above upper bound, set to : ', ndata-1)
        for k in self.keys[:-1]:
            format = self.output_format[ self.formats[k] ]
            l = l + format%(self.data[i][k])
        fp.write(l+'\n')
    def write_all(self,fp, complete_header = False):
        """
        write all data to a file associated to fp

        if complete_header = True include the complete header including all comments
        """
        if complete_header:
            self.write_complete_header(fp)
        else:
            self.write_header(fp)
        for i in range(len(self.data)):
            self.write_line(fp, i)
        fp.close()
    #   new function to add a key
    def write_selected(self,fp,index_list, complete_header = False):
        """
        write a new datafile with an identical header but enter only
        those data with an index given in index_list. If the index does not
        exist print a message and skip it.

        if complete_header = True include the complete header including all comments

        """
        if complete_header:
            self.write_complete_header(fp)
        else:
            self.write_header(fp)
        for i in index_list:
            try:
                self.write_line(fp, i)
            except:
                print('cannot write index : ', i, ' does it exist ?')
        fp.close()

    def add_key(self,key,format='f'):
        """
        add a new key, this is useful if you want to add new data
        assign new values using a loop like::

        >>> df.add_key('newkey',format='i')

        The new data need to be stored as follows::

        >>> for d in df.data:
        >>>     d['newkey']= some_new_value

        where df is the datafile and 'newkey' the new key. The new data set
        can be saved using ``fp = open('new_file','w')`` and ``df.write_all(fp)``
        """
        # check if key already exists
        try:
            self.keys.index(key)
            print(key, " exists already !")
            return
        except:
            for d in self.data:
                # set initial value to none
                d[key] = None
            for i in self.adata_index:
                self.adata[i] += ' None'
        # add the new key at the end of the keys list but before indx
        self.keys.insert(len(self.keys)-1,key)
        # add the format information
        try:
            fi = self.fmt_characters.index(format)
        except:
            print('unknown format : ', format, ' use f instead')
            format = 'f'
        self.formats[key] =  format
        self.update_header()
        # self.update_adata()
    # end
    def delete_key(self,key):
        """
        remove a key and all values associated with it
        """
        # remove the data for the key
        for d in self.data:
            del d[key]
        # remove the format for this key
        fmt = self.formats.pop(key)
        # now remove the key from the key list
        self.keys.remove(key)
        print('key : ', key , ' and format : ', fmt, ' removed')
        self.update_header()
    # end

    def add_data(self, keys,line):
        """
        
        add data to the data file
        
        d.add_data('x:y:z','xval yval zval')
        

        xval, yval, zval are the values as they would be entered in a data file line
        
        both arguments are strings and describe a complete line i.e. values for all variables
        defined in the header line.

        
        """
        
        key_l = keys.split(':')
        # check the key list
        key_index=[]
        for k in self.keys[:-1]:  # skip the indx
            try:
                ki = key_l.index(k)
                key_index.append(ki)
            except:
                print(k, ' does not exist !, nothing added')
                return
        # sort the argumens according to the sequence of the keys
        lsp = line.split()
        fline = [lsp[i] for i in key_index]
        line = ''
        for fl in fline: line += fl+' '
        self.adata.append(line.strip())
        print(f'appending line {line}')
        f = self.parse_line(line.strip())
        self.data.append(self.make_dict(self.keys,f) )

    def add_header_comment(self, text):
        """
        add a comment line to the header. The # at the beginning is automatically added !

        * for a normal comment start with a space
        * to add a parameter start the comment with a \
        """
        self.adata.insert(self.headindex, '#' + text)
        self.headindex += 1
        
    def add_parameter(self, name, value):
        """
        add a parameter to the comment section
        """
        cmd = '\ {} = {} '.format(name, value)
        self.add_header_comment(cmd)
        
    def save(self, file = None):
        """

        Save the current datafile. 

        With the keyword: *file* = 'new_file'

        the datafile will be written into the new_file name

        """
        if file == None:
            o = open(self.filename,'w')
        else:
            o = open( file, 'w')
        self.write_all(o, complete_header = True)

    def make_fmt(self):
        fmt = ''
        for k in self.keys[:-1]:
            fmt += format_dict[self.formats[k]] + ', '
        return fmt.strip()[:-1]

    def make_csv(self):
        keys = self.keys[:-1]
        csv = [ ''.join([k + ',' for k in keys]) ]
        for l in self.data:
            fmt = self.make_fmt()
            data = [l[k] for k in keys]
            ll = fmt.format(*data)
            csv.append(ll)
        return csv

    def write_csv(self, f):
        """
        
        save the current file as a csv file
        
        f : file name  to be used
        
        """
        o = open(f,'w')
        csv = self.make_csv()
        for l in csv:
            o.write(l + '\n')
        o.close()


#
