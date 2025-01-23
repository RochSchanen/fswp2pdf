#
# file: fswptosingleplotpdf.py
# content: frequency sweep(s) to one single plot in one pdf document
# created: 2025 January 23, Thursday
# author: roch schanen
# modified:
# comment: Set debug "True" to run the script from sublime text

_DEBUG = False

#######
# LOG #
#######

# log path
_fp = "./singledocument.log"

# log handle
_fh = open(_fp, "w") if _DEBUG else None

def lprint(*args, **kwargs):
    # print(*args, **kwargs)
    kwargs["file"] = _fh
    return print(*args, **kwargs)

###########
# IMPORTS #
###########

# built-in imports
# ----------------
from sys import argv

# imports from package "https://matplotlib.org/"
# -----------------------------------------
from matplotlib.pyplot import get_cmap

# from the local package
# ----------------------
try:

    # import from built
    # -----------------
    from fswp2pdf import sielib
    from fswp2pdf import splotlib

except ImportError as error:

    # import from .
    # -------------
    import sielib
    import splotlib

#########
# DEBUG #
#########

if _DEBUG:
    argv = [
        f"scriptname",
        f"E:/schanen/work-python/fswp2pdf/.data/TO11122024_7000mVAC200VDCAir_(VACUUM)__full_23.dat",
        f"E:/schanen/work-python/fswp2pdf/.data/TO11122024_7000mVAC200VDCAir_(VACUUM)__full_21.dat",
        f"E:/schanen/work-python/fswp2pdf/.data/TO11122024_7000mVAC200VDCAir_(VACUUM)__full_22.dat",
        ]

###########
# PROCESS #
###########

lprint(f"processing: ")

###############
# import data #
###############

# init lists
N, T, F, X, Y = [], [], [], [], []
# loop through files
for a in argv[1:]:
    # import
    lprint(f"import {a}")
    info, data = sielib.import_TorsionOscilla_FreqScan_20241213_112400(a)
    # parse info, data
    n = list(info.values())[0]
    t, f, x, y = data
    # build data lists
    N.append(n)
    T.append(t)
    F.append(f)
    X.append(x)
    Y.append(y)

###################
# ENGINEERS UNITS #
###################

# rescale frequency data to engineer units
factor_f, prefix_f = splotlib.GetUnitPrefix(*F)
for i, f in enumerate(F): F[i] = f*factor_f

# rescale signal data to engineer units
factor_xy, prefix_xy = splotlib.GetUnitPrefix(*X, *Y)
for i, x in enumerate(X): X[i] = x*factor_xy
for i, y in enumerate(Y): Y[i] = y*factor_xy

#############
# plot data #
#############

# create document
doc = splotlib.Document(f"singleplot.pdf")

# create figure
fg, ax = splotlib.SelectFigure("myfig", "A4")

# choose map
m = get_cmap('Set1')

# add plot
for i, (n, f, x, y) in enumerate(zip(N, F, X, Y)):
    splotlib.Plot("myfig", f, x, "-", color = m(i), label = n)
    splotlib.Plot("myfig", f, y, "-", color = m(i))

# legend
splotlib.legend()

# labels
splotlib.Xlabel(f"Frequency / {prefix_f}Hz")
splotlib.Ylabel(f"Signal / {prefix_xy}V")

# range
splotlib.AutoRange("x", *F)
splotlib.AutoRange("y", *X, *Y)

# ticks
splotlib.AutoTick("x")
splotlib.AutoTick("y")

# grid
splotlib.AutoGrid()

# add figure to the document
doc.addfigure("myfig")

# update document
doc.updatefile()

# close document
doc.close()

# done
lprint(f"done.")
if _fh: _fh.close()
