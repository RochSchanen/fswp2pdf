

# from package: "https://numpy.org/"
from numpy import pi, cos, sin

# from package: "https://scipy.org/"
from scipy.optimize import curve_fit as fit

# ROTATE BY AN ANGLE "A" BEFORE DISPLAY
# def Rotate
# a_deg   = 20.0
# a_rad   = a_deg*pi/180
# xr      = X*cos(a_rad)-Y*sin(a_rad)
# yr      = X*sin(a_rad)+Y*cos(a_rad)
# X, Y    = xr, yr
# # To adjust the lockin, substract the
# # value of a from the lockin phase.


# Aborption
def FX(t, p, w, h, o):
    x = (t-p)/w
    y = h/(1+square(x))
    return o + y

# Dispersion
def FY(t, p, w, h, o):
    x = (t-p)/w
    y = x*h/(1+square(x))
    # inverse sign on request
    return o - y

# define starting parameters and fit
parSx = [32705.0, 5.0, 1.0,  2.0]
parSy = [32705.0, 5.0, 1.0, 18.0]

# parX = parSx
parX, parXC = fit(FX, F, X, p0 = parSx)
# parY = parSy
parY, parYC = fit(FY, F, Y, p0 = parSy)

# plot fits
ax.plot(F, FX(F, *parX), "--k", linewidth = 0.6)
ax.plot(F, FY(F, *parY), "--k", linewidth = 0.6)

for l in L[:10]:
    t += l[2:]
t += f"\nrotation : {-a_deg} degrees"
headerText(t, fg)

# export fit results to footer text
t =  f"                   phase      quadrature\n\n"
t += f"position :{parX[0]:12.3f}Hz, {parY[0]:12.3f}Hz\n"
t += f"width    :{parX[1]:12.3f}Hz, {parY[1]:12.3f}Hz\n"
t += f"height   :{parX[2]:12.3f}{s}V, {parY[2]:12.3f}{s}V\n"
t += f"offset   :{parX[3]:12.3f}{s}V, {parY[3]:12.3f}{s}V\n"
footerText(t, fg)

headerText = ""
for k in info.keys():
    headerText += f"{k:<8}: {info[k]}\n"

