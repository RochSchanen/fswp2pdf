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

from numpy import pi
from numpy import cos
from numpy import sin

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

version_history["0.0"] = """
version 0.0 (11 January 2025):
    add fitting functions: 
        LorentzAbsorption()
        LorentzDispersion()
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

        # manual fit

        LorentzAbsorptionFitParameters = [88.295, 0.047, 500E-6, 0.0]
        XF = LorentzAbsorption(F, *LorentzAbsorptionFitParameters)
        
        LorentzDispersionFitParameters = [88.295, 0.047, 500E-6, 345E-6]
        YF = LorentzDispersion(F, *LorentzDispersionFitParameters)

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
        splotlib.Plot("myfig", F, XF, "-.c")
        splotlib.Plot("myfig", F, YF, "-.r")
        
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

# # define starting parameters and fit
# parSx = [32705.0, 5.0, 1.0,  2.0]
# parSy = [32705.0, 5.0, 1.0, 18.0]

# # parX = parSx
# parX, parXC = fit(FX, F, X, p0 = parSx)
# # parY = parSy
# parY, parYC = fit(FY, F, Y, p0 = parSy)

# # plot fits
# ax.plot(F, FX(F, *parX), "--k", linewidth = 0.6)
# ax.plot(F, FY(F, *parY), "--k", linewidth = 0.6)

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
