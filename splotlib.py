# file = splotlib.py
# content: collection of plotting and pdf export functions
# Created: 13 December 2024
# Author: Roch Schanen
# comments: this library is currently in development

version_history = {}

""" 

    --- motivation ---

    There is always a competition between simplicity and flexibility.
    
    SIMPLICITY is for making one plot in one simple command:
        for example, pdf_plot("data source", "plot name") would load the data
        and export a plot to a pdf file. if data source is omitted, a dialogue
        box is opened to select the filename. If multiple files are selected,
        a multi-page pdf document is generated (default). The plot styles is
        determined from the datafile content.   
        
    FLEXIBILITY is for the user to define manually the style and other
        characteristics of the plot, the output-file formats. Thus, the
        different elements of the plot have to be considered and must be
        tunable. This is where the structure of the plot is essential.
        Also, the data structures have to be easily reachable. Useful
        analytical tools must also be considered.

    How do we go from the DATA file to the PDF file? Several existing library
    are used to help us in this task. They must be platform independent (this
    is already why python is used in the first place).
    
"""

# From "https://matplotlib.org/"
# ------------------------------

from matplotlib.pyplot import figure
from matplotlib.pyplot import fignum_exists
from matplotlib.backends.backend_pdf import PdfPages

# From "https://numpy.org/"
# -------------------------

from numpy import exp
from numpy import ceil
from numpy import floor
from numpy import log10
from numpy import absolute
from numpy import linspace

########################
### "Aclass" formats ###
########################

class AClass():

    """ 

        On instantiation, a list of sizes for each format (A class type)
        is generated. A paper size is obtained using the PaperSize() method
        with a string argument which value is between "A0" and "A10". For
        example, to get the size of an A4 paper in millimeters, you can use:

        w, h = AClass().PaperSize("A4")

    """
    
    def __init__(self):
        # largest size
        d = {"A0" : (841, 1189)}
        # smaller sizes
        for i in range(10):
            W, H = d[f"A{i}"]
            d[f"A{i+1}"] = (round(H/2), W)
        # register dictionary
        self.sizes = d
        # done
        return

    def PaperSize(self, Format):
        return self.sizes[Format]

####################
### selectFigure ###
####################

_CurrentFigure = None
_CurrentFigureAxes = None

def SelectFigure(name, 
        size        =       "A4",   # choose from A0 to A10
        border      =       15.0,   # percentage of the full page
        orientation =  "portrait",  # use "portrait" or "landscape"
        ):

    if not fignum_exists(name):
        # create default figure and axes
        fg = figure(name)
        # get paper dimensions in mm (Short and Large)
        # size is a string describing the document size.
        # so far, only A-class sizes are implemented.
        S, L = AClass().PaperSize(size)
        # compute axes width and height in paper units:
        # border is the minimum border size surrounding the axes
        # this is the left and right borders for portrait orientation
        # this is the top and bottom borders for landscape orientation
        # both axes are constrained to have the same length in mm
        # thus they have a fixed ratio S/L in page units (fraction of 1.0)
        m = border/100.0    # short border size in page units
        l = 1.0-2.0*m       # axis length (large value in page units)
        s = l*S/L           # axis length (small value in page units)
        q = (1.0-s)/2.0     # large border size in page units
        # compute paper size and margins from the page orientation
        # W and w for width, H and h for height, x and y the axes offset
        (W, H, w, h, x, y) = {
            "PORTRAIT":  (S, L, l, s, m, q),
            "LANDSCAPE": (L, S, s, l, q, m),
        }[orientation.upper()]
        # set figure size in inches
        fg.set_size_inches(W/25.4, H/25.4)
        # create axes (position and size)
        ax = fg.add_axes([x, y, w, h])

    else:
        # select any existing figure
        fg = figure(name)
        # get the figure first axes
        ax = fg.get_axes()[0]

    # update current values
    global _CurrentFigure
    global _CurrentFigureAxes
    _CurrentFigure       = fg
    _CurrentFigureAxes   = ax

    # done (return figure and axes)
    return fg, ax

# get the current figure handle
def cfg():
    return _CurrentFigure

# get the current axes handle
def cfa():
    return _CurrentFigureAxes

################
### Document ###
################

class Document():

    def __init__(self, pathname, *figures):
        self.pathname   = pathname
        self.filehandle = None
        self.figures = figures if figures else []
        self.updatefile()
        return

    def _openfile(self):
        self.filehandle = PdfPages(self.pathname)
        return self.filehandle

    def _closefile(self):
        self.filehandle.close()
        return

    def addfigure(self, name):
        if not name in self.figures:
            self.figures.append(name)
        return

    def updatefile(self):
        if self.figures:
            self._openfile()
            for f in self.figures:
                args = SelectFigure(f)
                self.filehandle.savefig(args[0])
            self._closefile()
        return

#####################
## plot functions ###
#####################

def _getTickIntervals(start, stop, ticks):

    ln10 = 2.3025850929940459

    # trial table
    T = [0.010, 0.020, 0.025, 0.050,
         0.100, 0.200, 0.250, 0.500,
         1.000, 2.000, 2.500, 5.000]

    # corresponding tick sub division intervals
    S = [5.0,   4.0,   5.0,   5.0,
         5.0,   4.0,   5.0,   5.0,
         5.0,   4.0,   5.0,   5.0]

    span = stop - start                         # get span
    d = exp(ln10 * floor(log10(span)))          # find decade
    span /= d                                   # re-scale

    # find number of ticks below and closest to n
    i, m = 0, floor(span / T[0])                # start up
    while m > ticks:                            # next try?
        i, m = i + 1, floor(span / T[i + 1])    # try again 

    # re-scale
    mi =  d * T[i]   # main tick intervals
    si = mi / S[i]   # sub tick intervals

    # done
    return mi, si

def _getTickPositions(start, stop, ticks):

    # get intervals
    mi, si = _getTickIntervals(start, stop, ticks)

    # main ticks (round is the built-in python version)
    ns = ceil(start / mi - 0.001) * mi  # start
    ne = floor(stop / mi + 0.001) * mi  # end
    p  = round((ne - ns) / mi) + 1      # fail safe
    M  = linspace(ns, ne, p)            # main positions

    # sub ticks (round is the built-in python version)
    ns = ceil(start / si + 0.001) * si  # start
    ne = floor(stop / si - 0.001) * si  # end
    p  = round((ne - ns) / si) + 1      # fail safe
    S  = linspace(ns, ne, p)            # sub positions

    # done
    return M, S

def GetUnitPrefix(*tables):
    # find minimum and maximum in first table
    S, E = min(tables[0]), max(tables[0])
    # find minimum and maximum in all tables
    for T in tables[1:]:
        s, e = min(T), max(T)
        S, E = min(S, s), max(E, e)
    # get the maximum absolute value
    ma = max(absolute(S), absolute(E))
    # compute prefactor and prefix
    prefactor, prefix = {   
         0: (1E+00, ""),
        -1: (1E+03, "m"),
        -2: (1E+06, "µ"),
        -3: (1E+09, "n"),
        -4: (1E+12, "p"),
        +1: (1E-03, "K"),
        +2: (1E-06, "M"),
        +3: (1E-09, "G"),
        +4: (1E-12, "T"),
    }[int(floor(log10(ma)/3))]
    # done
    return prefactor, prefix 

def AutoRange(axis, *data, origin = False):
    # fixed extensions (left, right)
    l, r = 0.1, 0.1 # (switch left, right to low, high?)
    # find limits
    S, E = min(data[0]), max(data[0])
    for d in data[1:]:
        s, e = min(d), max(d)
        S, E = min(S, s), max(E, e)
    # add origin
    if origin: S, E = min(S, 0.0), max(E, 0.0)
    # prevent zero length (scale 1.0 to the decade?)
    if S == E: S, E = S-1.0, E+1.0
    # extend
    S, E = S-(E-S)*l, E+(E-S)*r
    # apply to selected axis
    {"x": cfa().set_xlim,
     "y": cfa().set_ylim,
        }[axis](S, E)
    return 

def AutoTick(axis, ticks = 5):
    # get current limits
    s, e = {
        "x": cfa().get_xlim,
        "y": cfa().get_ylim
        }[axis]()
    # get tick positions
    M, S = _getTickPositions(s, e, ticks)
    # get method on selected axis
    set_ticks = {
        "x": cfa().set_xticks,
        "y": cfa().set_yticks
        }[axis]
    # apply minor and major ticks
    set_ticks(M)
    set_ticks(S, minor = True)
    # apply tick styles
    cfa().tick_params(axis = axis, which = "both", direction = "in")
    return

def AutoGrid(axis = "both"):
    cfa().grid("on", axis = axis, which = "minor", linewidth = 0.3)
    cfa().grid("on", axis = axis, which = "major", linewidth = 0.6)
    return    

def AutoStyle(x, *Y, xticks = 7, yticks = 7, origin_x = False, origin_y = False):
    AutoRange("x",  x, origin = origin_x)
    AutoRange("y", *Y, origin = origin_y)
    AutoTick("x", xticks)
    AutoTick("y", yticks)
    AutoGrid()
    # done
    return

def Xlabel(t):
    return cfa().set_xlabel(t)

def Ylabel(t):
    return cfa().set_ylabel(t)

def Xlim(S, E):
    return cfa().set_xlim(S, E)

def Ylim(S, E):
    return cfa().set_ylim(S, E)

def Plot(*args, **kwargs):
    if isinstance(args[0], str):
        SelectFigure(args[0])
        args = args[1:]
    return cfa().plot(*args, **kwargs)

def Text(text, position = "top"):
    # get plot bounds (in page units)
    l, b, w, h = cfa().get_position().bounds
    # compute position from bounds
    x, y = {
        "LEFT"      : (    l/2, 0.5),
        "RIGHT"     : (l+w+l/2, 0.5),
        "BOTTOM"    : (0.5, b/2),
        "TOP"       : (0.5, b+h+b/2),
    }[position.upper()]
    # instantiate text
    tx = cfg().text(x, y, text)
    # setup fonts
    tx.set_fontfamily('monospace')
    tx.set_fontsize("small")
    # setup alignment    
    tx.set_horizontalalignment('center')
    tx.set_verticalalignment('center')
    # done
    return tx

version_history["0.0"] = """
version 0.0
(13 december 2024):
    
    implemented:

        AClass()
        AClass.PaperSize(Format)
        
        Document(pathname[, *figures])
        Document.openfile()
        Document.closefile()
        Document.updatefile()
        Document.addfigure(name)
        Document.list()

        SelectFigure(name[, size][, border][, orientation])
        cfg()
        cfa()
        _getTickIntervals(start, stop, ticks)
        _getTickPositions(start, stop, ticks)
        GetUnitPrefix(*tables)
        AutoRange(axis, *data[, origin])
        AutoTick(axis[, ticks])
        AutoGrid([axis])
        AutoStyle(x, *Y[, xticks][, yticks][, origin_x][, origin_y])
        Xlabel(t), Ylabel(t)
        Xlim(S, E), Ylim(S, E)
        Plot(*args, **kwargs)
        Text(text[, position])
"""

if __name__ == "__main__":

    ###  display version ###

    current_version = list(version_history.keys())[-1]

    print(f"splotlib current version: {current_version}")
    print(f"-------------------------")

    print()
    print(f"history")
    print(f"-------")
    for v in version_history.values():
        print(v)

    """ example codes """

    if current_version == "0.0":

        # import data
        import sielib
        fp = ".source/fswp_full_1.dat"
        info, data = sielib.import_TorsionOscilla_FreqScan_20241213_112400(fp)
        T, F, X, Y = data

        # rescale frequency data to engineer units
        factor_f, prefix_f = GetUnitPrefix(F)
        F *= factor_f

        # rescale signal data to engineer units
        factor_xy, prefix_xy = GetUnitPrefix(X, Y)
        X *= factor_xy
        Y *= factor_xy

        # create document
        doc = Document(".output/myfig.pdf")

        # create figure
        SelectFigure("myfig", "A4")
        
        # add plot
        Plot("myfig", F, X, F, Y)
        
        Text(f"file: '{fp}'", "top")
        Xlabel(f"Frequency / {prefix_f}Hz")
        Ylabel(f"Signal / {prefix_xy}V")
        
        AutoRange("x", F)
        AutoRange("y", X, Y)
        
        AutoTick("x")
        AutoTick("y")
        
        AutoGrid()

        # add figure
        doc.addfigure("myfig")

        # update document
        doc.updatefile()
