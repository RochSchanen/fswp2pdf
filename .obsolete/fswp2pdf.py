#
# file: fswp2pdf.py
# content: fswp2pdf module
# created: 2025 January 16 Thursday
# modified:
# modification: add exportMultiple
# author: roch schanen
# comment:

version_history = {}

""" 
    - a single file export plot function to pdf.
    - a multiple files export function to pdf

"""

def exportSingle(fp):

    ###############
    # import data #
    ###############

    try: # import from built
        from fswp2pdf import sielib
    except ImportError as error:
        # local import
        import sielib

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

    try: # import from built
        from fswp2pdf import sfitlib
    except ImportError as error:
        # local import
        import sfitlib

    pAbs = sfitlib.LorentzAbsorptionFit_StartParameters(F, X)
    pAbs, pAbsCov = fit(sfitlib.LorentzAbsorptionFit_Function, F, X, pAbs)
    XF = sfitlib.LorentzAbsorptionFit_Function(F, *pAbs)

    pDis = sfitlib.LorentzDispersionFit_StartParameters(F, Y)
    pDis, pDisCov = fit(sfitlib.LorentzDispersionFit_Function, F, Y, pDis) 
    YF = sfitlib.LorentzDispersionFit_Function(F, *pDis)

    #############
    # plot data #
    #############

    try: # import from built
        from fswp2pdf import splotlib
    except ImportError as error:
        # local import
        import splotlib

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

    # close document
    doc.close()

    # done
    return

version_history["0.0"] = """
version 0.0 (16 January 2025)

    add exportSingle()

"""

########
# info #
########

if __name__ == "__main__":

    _fp = "../.output/fswp2pdf.txt"
    _fh = open(_fp, "w")
    def lprint(*args, **kwargs):
        print(*args, **kwargs)
        kwargs["file"] = _fh
        return print(*args, **kwargs)

    ###  display version ###

    current_version = list(version_history.keys())[-1]

    lprint(f"fswp2pdf current version: {current_version}")
    lprint(f"-------------------------")

    lprint()
    lprint(f"history")
    lprint(f"-------")
    for v in version_history.values():
        lprint(v)

    # test list
    TESTS = [
        current_version,
        # "0.0",
        # "0.1",
        # "x.x",
        ]

    #############
    # tests 0.0 #
    #############

    if "0.0" in TESTS:

        lprint("running test version 0.0")

        exportSingle("../.data/fswp_full_1.dat")

    # #############
    # # tests 0.1 #
    # #############

    # if "0.1" in TESTS:
        
    #     lprint("running test version 0.1")
        
    #     exportMultiple([
    #         "TO11122024_7000mVAC200VDCAir_(VACUUM)__full_21",
    #         "TO11122024_7000mVAC200VDCAir_(VACUUM)__full_22",
    #         "TO11122024_7000mVAC200VDCAir_(VACUUM)__full_23",
    #         ])

    #############
    # tests x.x #
    #############

    if "x.x" in TESTS:

        lprint("running test version x.x")
