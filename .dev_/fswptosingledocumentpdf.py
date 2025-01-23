from time import sleep
from sys import argv

# log path
_fp = "./singledocument.log"

# log handle
_fh = open(_fp, "w")

def lprint(*args, **kwargs):
    print(*args, **kwargs)
    kwargs["file"] = _fh
    return print(*args, **kwargs)

argv = [
	f"scriptname",
	f"E:/schanen/work-python/fswp2pdf/.data/TO11122024_7000mVAC200VDCAir_(VACUUM)__full_23.dat",
	f"E:/schanen/work-python/fswp2pdf/.data/TO11122024_7000mVAC200VDCAir_(VACUUM)__full_21.dat",
	f"E:/schanen/work-python/fswp2pdf/.data/TO11122024_7000mVAC200VDCAir_(VACUUM)__full_22.dat",
	]

lprint(f"processing: ")




lprint(f"done.")
_fh.close()

# sleep(2)
