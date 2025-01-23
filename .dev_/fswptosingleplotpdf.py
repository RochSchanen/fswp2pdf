from time import sleep
from sys import argv

# argv = [
#     f"scriptname",
#     f"E:/schanen/work-python/fswp2pdf/.data/TO11122024_7000mVAC200VDCAir_(VACUUM)__full_23.dat",
#     f"E:/schanen/work-python/fswp2pdf/.data/TO11122024_7000mVAC200VDCAir_(VACUUM)__full_21.dat",
#     f"E:/schanen/work-python/fswp2pdf/.data/TO11122024_7000mVAC200VDCAir_(VACUUM)__full_22.dat",
#     ]

# log path
_fp = "./singleplot.log"

# log handle
_fh = open(_fp, "w")

def lprint(*args, **kwargs):
    print(*args, **kwargs)
    kwargs["file"] = _fh
    return print(*args, **kwargs)

lprint(f"processing: ")

###############
# import data #
###############

try: # import from built
    from fswp2pdf import sielib
except ImportError as error:
    # local import
    import sielib


N, T, F, X, Y = [], [], [], [], []

for a in argv[1:]:

    lprint(f"import {a}")

    info, data = sielib.import_TorsionOscilla_FreqScan_20241213_112400(a)

    # headerText = ""
    # for k in info.keys():
    #     headerText = f"{headerText}{k:<8}: {info[k]}\n"

    n = list(info.values())[0]

    t, f, x, y = data

    N.append(n)
    T.append(t)
    F.append(f)
    X.append(x)
    Y.append(y)

#############
# plot data #
#############

try: # import from built
    from fswp2pdf import splotlib
except ImportError as error:
    # local import
    import splotlib

# rescale frequency data to engineer units
factor_f, prefix_f = splotlib.GetUnitPrefix(*F)
for i, f in enumerate(F): F[i] = f*factor_f

# rescale signal data to engineer units
factor_xy, prefix_xy = splotlib.GetUnitPrefix(*X, *Y)
for i, x in enumerate(X): X[i] = x*factor_xy
for i, y in enumerate(Y): Y[i] = y*factor_xy

# create document strip
doc = splotlib.Document(f"singleplot.pdf")

# create figure
fg, ax = splotlib.SelectFigure("myfig", "A4")

from matplotlib.pyplot import get_cmap
# choose map
m = get_cmap('Set1')

# add plot
for i, (n, f, x, y) in enumerate(zip(N, F, X, Y)):
    splotlib.Plot("myfig", f, x, "-", color = m(i), label = n)
    splotlib.Plot("myfig", f, y, "-", color = m(i))

splotlib.legend()

splotlib.Xlabel(f"Frequency / {prefix_f}Hz")
splotlib.Ylabel(f"Signal / {prefix_xy}V")

splotlib.AutoRange("x", *F)
splotlib.AutoRange("y", *X, *Y)

splotlib.AutoTick("x")
splotlib.AutoTick("y")

splotlib.AutoGrid()

# add figure
doc.addfigure("myfig")

# update document
doc.updatefile()
# close
doc.close()

lprint(f"done.")
_fh.close()

sleep(2)
