# fswp2pdf

The package fswp2pdf is used to convert a "frequency sweep" data file into a pdf document with a plot of the absorption and dispersion channels and a lorentzian fit to both.

## sielib

```

import_TorsionOscilla_FreqScan_20241213_112400(fp)

```

## splotlib

```python

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

```

## sfitlib

```

UpZeroCrossing(X)
DownZeroCrossing(X)

LorentzAbsorptionFit_Function(t, p, w, h, o)
LorentzDispersionFit_Function(t, p, w, h, o)
LorentzAbsorptionFit_StartParameters(T, X)
LorentzDispersionFit_StartParameters(T, Y)
LorentzFitParametersDisplay(pAbs, pDis)

```
