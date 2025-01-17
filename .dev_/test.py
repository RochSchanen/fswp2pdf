# from sys import argv
# from fswp2pdf.fswp2pdf import export
# export(argv[1])

# C:\Program Files\LogicCircuit\LogicCircuit.exe
# C:\Windows\py.exe E:\schanen\work-python\fswp2pdf\.dev_\test.py "%1"

from sys import argv

fh = open("./result.txt", 'w')
for a in argv[1:]:
	fh.write(f"{a}\n")
fh.close()
