# file: sfitlib.py
# content: collection of fitting functions
# Created: 11 January 2025
# Author: Roch Schanen
# comments: this library is in development

version_history = {}

""" 
    development of common fitting functions library for work.
"""

# from package: "https://numpy.org/"
# ----------------------------------

from numpy import square
from numpy import argmin
from numpy import argmax
from numpy import flatnonzero

from numpy import pi
from numpy import cos
from numpy import sin

########################
## Lorentz functions ###
########################

def LorentzAbsorptionFit_Function(t, p, w, h, o):
    # data, position, width, height, offset
    x = (t-p)/w
    y = h/(1+square(x))
    return o + y

def LorentzDispersionFit_Function(t, p, w, h, o):
    # data, position, width, height, offset
    x = (t-p)/w
    y = x*h/(1+square(x))
    return o - y

#############################
## Zero crossing function ###
#############################

def DownZeroCrossing(X):
    I = X > 0.0
    C = I[:-1] & ~I[1:]
    return flatnonzero(C)

def UpZeroCrossing(X):
    I = X < 0.0
    C = I[:-1] & ~I[1:]
    return flatnonzero(C)

##############################
## Lorentz guess functions ###
##############################

def LorentzAbsorptionFit_StartParameters(T, X):
    al, ah = argmin(X), argmax(X)
    h = X[ah] - X[al]
    tl = UpZeroCrossing(X - h/2.0)[0]
    th = DownZeroCrossing(X - h/2.0)[0]
    return [T[ah], (T[th] - T[tl])/2.0, h, X[al]]

def LorentzDispersionFit_StartParameters(T, Y):
    al, ah = argmin(Y), argmax(Y)
    return [(T[al]+T[ah])/2.0, (T[al]-T[ah])/2.0, Y[ah]-Y[al], (Y[ah]+Y[al])/2.0]


###################################
## Lorentz parameters to string ###
###################################

def LorentzFitParametersDisplay(pAbs, pDis):

    from fswp2pdf.splotlib import GetUnitPrefix

    P1, P2 = pAbs[0], pDis[0]
    W1, W2 = pAbs[1], pDis[1]
    H1, H2 = pAbs[2], pDis[2]
    O1, O2 = pAbs[3], pDis[3]

    P_f,  P_p = GetUnitPrefix([P1, P2])
    W_f,  W_p = GetUnitPrefix([W1, W2])
    H_f,  H_p = GetUnitPrefix([H1, H2])
    O_f,  O_p = GetUnitPrefix([O1, O2])

    # define output block
    block = f"""
        position: {P1*P_f:7.3f}{P_p+'Hz':<2}, {P2*P_f:7.3f}{P_p+'Hz':<2}
        width   : {W1*W_f:6.2f}{W_p+'Hz':<3}, {W2*W_f:6.2f}{W_p+'Hz':<3}
        height  : {H1*H_f:6.2f}{H_p+ 'V':<3}, {H2*H_f:6.2f}{H_p+ 'V':<3}
        offset  : {O1*O_f:6.2f}{O_p+ 'V':<3}, {O2*O_f:6.2f}{O_p+ 'V':<3}
        """

    def padAndTrim(b):

        n, L = 0, b.split('\n')
        for l in L: n = max(n, len(l))
        
        p = f""
        for l in L: p = f"{p}{l:<{n}}\n"

        for l in p.split("\n"): # scan through each line
            m = len(l) # record line length
            if m: # skip empty lines
                c = 0 # setup space counter
                while c < m: # less thanend-of-line
                    if not l[c]==" ": break # spaces not available
                    c += 1 # increment space counter
                n = min(n, c) # select minimum value

        q = f"" # setup string
        for l in p.split("\n"): # scan through each line
            q = f"{q}\n{l[n:]}" # catenate trimmed lines

        return q

    # done
    return padAndTrim(block)

version_history["0.0"] = """
version 0.0 (11 January 2025)

    add fitting functions and tools: 
        
        - crossing detection:
            UpZeroCrossing()
            DownZeroCrossing()
        
        - Lorentz Absorption:
            LorentzAbsorptionFit_Function()
            LorentzAbsorptionFit_StartParameters()
        
        - Lorentz Dispersion
            LorentzDispersionFit_Function()
            LorentzDispersionFit_StartParameters()

        - export Lorentz parameters to text string:
            LorentzFitParametersDisplay()

"""

if __name__ == "__main__":

    ###  display version ###

    current_version = list(version_history.keys())[-1]

    print(f"sfitlib current version: {current_version}")
    print(f"------------------------")

    print()
    print(f"history")
    print(f"-------")
    for v in version_history.values():
        print(v)

    """ example codes """

    if current_version == "0.0":

        # from package: "https://scipy.org/"
        # ----------------------------------
        from scipy.optimize import curve_fit as fit

        # import data
        
        from fswp2pdf import sielib

        fp = "../.data/fswp_full_1.dat"
        info, data = sielib.import_TorsionOscilla_FreqScan_20241213_112400(fp)
        T, F, X, Y = data

        # fit data

        pAbs = LorentzAbsorptionFit_StartParameters(F, X)
        pAbs, pAbsCov = fit(LorentzAbsorptionFit_Function, F, X, pAbs)
        XF = LorentzAbsorptionFit_Function(F, *pAbs)
        
        pDis = LorentzDispersionFit_StartParameters(F, Y)
        pDis, pDisCov = fit(LorentzDispersionFit_Function, F, Y, pDis) 
        YF = LorentzDispersionFit_Function(F, *pDis)

        # plot data 

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

        # create document
        doc = splotlib.Document("../.output/sfitlib.pdf")

        # create figure
        splotlib.SelectFigure("myfig", "A4")
        
        # add plot
        splotlib.Plot("myfig", F, X, ".b")
        splotlib.Plot("myfig", F, Y, ".r")
        splotlib.Plot("myfig", F, XF, "-.k", linewidth = 0.6)
        splotlib.Plot("myfig", F, YF, "-.k", linewidth = 0.6)
        
        fn = fp.split("/")[-1]
        splotlib.Text(f"file: '{fn}'", "top")
        splotlib.Xlabel(f"Frequency / {prefix_f}Hz")
        splotlib.Ylabel(f"Signal / {prefix_xy}V")
        
        splotlib.AutoRange("x", F)
        splotlib.AutoRange("y", X, XF, Y, YF)
        
        splotlib.AutoTick("x")
        splotlib.AutoTick("y")
        
        splotlib.AutoGrid()

        print(LorentzFitParametersDisplay(pAbs, pDis))

        splotlib.Text(
            LorentzFitParametersDisplay(pAbs, pDis),
            "bottom",
            )

        # add figure
        doc.addfigure("myfig")

        # update document
        doc.updatefile()

# ROTATE BY AN ANGLE "A"
# def Rotate
# a_deg   = 20.0
# a_rad   = a_deg*pi/180
# xr      = X*cos(a_rad)-Y*sin(a_rad)
# yr      = X*sin(a_rad)+Y*cos(a_rad)
# X, Y    = xr, yr
# # To adjust the lockin, subtract the
# # value of a from the lockin phase.

# t += f"\nrotation : {-a_deg} degrees"
# headerText(t, fg)

# headerText = ""
# for k in info.keys():
#     headerText += f"{k:<8}: {info[k]}\n"
