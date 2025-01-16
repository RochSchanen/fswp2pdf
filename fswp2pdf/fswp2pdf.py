#
# file: fswp2pdf.py
# content: fswp2pdf module
# created: 2025 January 16 Thursday
# modified:
# modification: add export
# author: roch schanen
# comment:

version_history = {}

""" 
    
    a single export function for the data conversion to pdf.

"""

def export(fp):

    ###############
    # import data #
    ###############

    from fswp2pdf import sielib

    info, data = sielib.import_TorsionOscilla_FreqScan_20241213_112400(fp)

    headerText = ""
    for k in info.keys():
        headerText = f"{headerText}{k:<8}: {info[k]}\n"

    T, F, X, Y = data

    ############
    # fit data #
    ############

    # from package: "https://scipy.org/"
    # ----------------------------------
    from scipy.optimize import curve_fit as fit

    from fswp2pdf import sfitlib

    pAbs = sfitlib.LorentzAbsorptionFit_StartParameters(F, X)
    pAbs, pAbsCov = fit(sfitlib.LorentzAbsorptionFit_Function, F, X, pAbs)
    XF = sfitlib.LorentzAbsorptionFit_Function(F, *pAbs)

    pDis = sfitlib.LorentzDispersionFit_StartParameters(F, Y)
    pDis, pDisCov = fit(sfitlib.LorentzDispersionFit_Function, F, Y, pDis) 
    YF = sfitlib.LorentzDispersionFit_Function(F, *pDis)

    #############
    # plot data #
    #############

    from fswp2pdf import splotlib

    # rescale frequency data to engineer units
    factor_f, prefix_f = splotlib.GetUnitPrefix(F)
    F *= factor_f

    # rescale signal data to engineer units
    factor_xy, prefix_xy = splotlib.GetUnitPrefix(X, XF, Y, YF)
    X  *= factor_xy
    XF *= factor_xy
    Y  *= factor_xy
    YF *= factor_xy

    # create document strip
    doc = splotlib.Document(fp[:-len(fp.split('.')[-1])]+"pdf")

    # create figure
    splotlib.SelectFigure("myfig", "A4")

    # add plot
    splotlib.Plot("myfig", F, X, ".b")
    splotlib.Plot("myfig", F, Y, ".r")
    splotlib.Plot("myfig", F, XF, "-.k", linewidth = 0.6)
    splotlib.Plot("myfig", F, YF, "-.k", linewidth = 0.6)

    splotlib.AutoRange("x", F)
    splotlib.AutoRange("y", X, XF, Y, YF)
    splotlib.AutoTick("x")
    splotlib.AutoTick("y")
    splotlib.AutoGrid()

    splotlib.Xlabel(f"Frequency / {prefix_f}Hz")
    splotlib.Ylabel(f"Signal / {prefix_xy}V")

    splotlib.Text(headerText, "top")
    splotlib.Text(sfitlib.LorentzFitParametersDisplay(pAbs, pDis), "bottom")

    # add figure
    doc.addfigure("myfig")

    # update document
    doc.updatefile()

    # done
    return

version_history["0.0"] = """
version 0.0 (16 January 2025)

    add export()

"""
 
########
# info #
########

if __name__ == "__main__":

    ###  display version ###

    current_version = list(version_history.keys())[-1]

    print(f"fswp2pdf current version: {current_version}")
    print(f"-------------------------")

    print()
    print(f"history")
    print(f"-------")
    for v in version_history.values():
        print(v)

    #############
    # tests 0.0 #
    #############

    if current_version == "0.0":

        export("../.data/fswp_full_1.dat")

    #############
    # tests x.x #
    #############

    if current_version == "x.x":
        pass
