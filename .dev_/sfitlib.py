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

########################
## Lorentz functions ###
########################

def LorentzAbsorption(t, p, w, h, o):
    # data, position, width, height, offset
    x = (t-p)/w
    y = h/(1+square(x))
    return o + y

def LorentzDispersion(t, p, w, h, o):
    # data, position, width, height, offset
    x = (t-p)/w
    y = x*h/(1+square(x))
    return o - y

def LorentzAbsorptionFitStartParameters(T, X):
    al, ah = argmin(X), argmax(X)
    h = X[ah] - X[al]
    tl = UpZeroCrossing(X - h/2.0)[0]
    th = DownZeroCrossing(X - h/2.0)[0]
    return [T[ah], (T[th] - T[tl])/2.0, h, X[al]]

def LorentzDispersionFitStartParameters(T, Y):
    al, ah = argmin(Y), argmax(Y)
    return [(T[al]+T[ah])/2.0, (T[al]-T[ah])/2.0, Y[ah]-Y[al], (Y[ah]+Y[al])/2.0]


version_history["0.0"] = """
version 0.0 (11 January 2025):
    add fitting functions: 
        LorentzAbsorption()
        LorentzDispersion()
        DownZeroCrossing()
        UpZeroCrossing()
        LorentzAbsorptionFitStartParameters()
        LorentzDispersionFitStartParameters()
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

        # [88.295, 0.047, 500E-6, 0.0]
        pAbs = LorentzAbsorptionFitStartParameters(F, X)
        pAbs, pAbsCov = fit(LorentzAbsorption, F, X, pAbs)
        XF = LorentzAbsorption(F, *pAbs)
        
        # [88.295, 0.047, 500E-6, 345E-6]
        pDis = LorentzDispersionFitStartParameters(F, Y)
        pDis, pDisCov = fit(LorentzDispersion, F, Y, pDis) 
        YF = LorentzDispersion(F, *pDis)

        print(pAbs, pDis)

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

# for l in L[:10]:
#     t += l[2:]
# t += f"\nrotation : {-a_deg} degrees"
# headerText(t, fg)

# # export fit results to footer text
# t =  f"                   phase      quadrature\n\n"
# t += f"position :{parX[0]:12.3f}Hz, {parY[0]:12.3f}Hz\n"
# t += f"width    :{parX[1]:12.3f}Hz, {parY[1]:12.3f}Hz\n"
# t += f"height   :{parX[2]:12.3f}{s}V, {parY[2]:12.3f}{s}V\n"
# t += f"offset   :{parX[3]:12.3f}{s}V, {parY[3]:12.3f}{s}V\n"
# footerText(t, fg)

# headerText = ""
# for k in info.keys():
#     headerText += f"{k:<8}: {info[k]}\n"
