#
# file: fswptosinglepagepdf.py
# content: frequency sweep(s) to single page(s) pdf document
# created: 2025 January 23, Thursday
# author: roch schanen
# modified:
# comment: Set debug "True" to run the script from sublime text

_DEBUG = False

#######
# LOG #
#######

# log path
_fp = "./singlepage(s).log"

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

# imports from package "https://scipy.org/"
# -----------------------------------------
from scipy.optimize import curve_fit as fit

# from the local package
# ----------------------
try:

    # import from built
    # -----------------
    from fswp2pdf import sielib
    from fswp2pdf import splotlib
    from fswp2pdf import sfitlib

except ImportError as error:

    # import from .
    # -------------
    import sielib
    import splotlib
    import sfitlib

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

# loop through files
for a in argv[1:]:

    ###############
    # import data #
    ###############

    # import
    lprint(f"\t{a}")
    info, data = sielib.import_TorsionOscilla_FreqScan_20241213_112400(a)
    # parse info
    headerText = ""
    for k in info.keys():
        headerText = f"{headerText}{k:<8}: {info[k]}\n"
    # get file name
    fn = list(info.values())[0]
    # parse data
    T, F, X, Y = data

    ############
    # fit data #
    ############

    pAbs = sfitlib.LorentzAbsorptionFit_StartParameters(F, X) # guess parameters
    pAbs, pAbsCov = fit(sfitlib.LorentzAbsorptionFit_Function, F, X, pAbs) # fit
    XF = sfitlib.LorentzAbsorptionFit_Function(F, *pAbs) # compute fit's data points

    pDis = sfitlib.LorentzDispersionFit_StartParameters(F, Y) # guess parameters
    pDis, pDisCov = fit(sfitlib.LorentzDispersionFit_Function, F, Y, pDis) # fit
    YF = sfitlib.LorentzDispersionFit_Function(F, *pDis) # compute fit's data points

    ###################
    # ENGINEERS UNITS #
    ###################

    # rescale frequency data to engineer units
    factor_f, prefix_f = splotlib.GetUnitPrefix(F)
    F *= factor_f

    # rescale signal data to engineer units
    factor_xy, prefix_xy = splotlib.GetUnitPrefix(X, Y, XF, YF)
    X  *= factor_xy
    Y  *= factor_xy
    XF *= factor_xy
    YF *= factor_xy

    #############
    # plot data #
    #############

    # create new figure
    fg, ax = splotlib.SelectFigure(fn)

    # add plots
    splotlib.Plot(fn, F, X, ".b")
    splotlib.Plot(fn, F, Y, ".r")
    splotlib.Plot(fn, F, XF, "-.k", linewidth = 0.6)
    splotlib.Plot(fn, F, YF, "-.k", linewidth = 0.6)

    # labels
    splotlib.Xlabel(f"Frequency / {prefix_f}Hz")
    splotlib.Ylabel(f"Signal / {prefix_xy}V")

    # range
    splotlib.AutoRange("x", F)
    splotlib.AutoRange("y", X, Y, XF, YF)

    # ticks
    splotlib.AutoTick("x")
    splotlib.AutoTick("y")

    # grid
    splotlib.AutoGrid()

    # file info
    splotlib.Text(headerText, "top")

    # fit results
    splotlib.Text(sfitlib.LorentzFitParametersDisplay(pAbs, pDis), "bottom")

    ###################
    # create document #
    ###################

    # create document
    doc = splotlib.Document(a[:-len(a.split('.')[-1])]+"pdf")

    # add figure
    doc.addfigure(fn)

    # update document
    doc.updatefile()

    # close document
    doc.close()

# done
lprint(f"done.")
if _fh: _fh.close()
