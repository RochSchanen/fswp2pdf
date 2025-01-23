from time import sleep
print(f"from sys import argv")
from sys import argv
print(f"from fswp2pdf.fswp2pdf import exportSingle")
from fswp2pdf.fswp2pdf import exportSingle
print(f"create logfile ./singlepage(s).log")
fh = open("./singlepage(s).log", 'w')
for a in argv[1:]:
	print(f"process {a}: ", end = "")
	fh.write(f"process {a}: ")
	exportSingle(a)
	print(f"ok")
	fh.write(f"ok\n")
fh.close()
print(f"close logfile")
sleep(2)
