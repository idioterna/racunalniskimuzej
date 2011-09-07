# coding=utf8
import os.path
import subprocess
import sys
from tempfile import NamedTemporaryFile

def write_label(outf, invst):

	url = "http://racunalniski-muzej.si/i/%d" % invst

	ps = """9 8 moveto (%(url)s) (eclevel=L width=0.6 height=0.6) /qrcode /uk.co.terryburton.bwipp findresource exec
newpath
ISOArial 10 scalefont setfont
60.000000 42.000000 moveto
(Ra) show
/ccaron glyphshow
(unalni) show
/scaron glyphshow
(ki) show
60.000000 32.000000 moveto
(muzej) show
60.000000 9.000000 moveto
(Inv. ) show
/scaron glyphshow
(t. %(invst)04d) show
stroke
BREAK
""" % {'invst': invst, 'url': url}

	outf.write(ps)

def main():
	if len(sys.argv) < 2:
		print "UPORABA: python nalepke.py [od]-[do] [labelnation parametri]"
		return

	od, do = map(int, sys.argv[1].split("-"))

	lnargs = sys.argv[2:]

	codefile = NamedTemporaryFile()

	for invst in xrange(od, do):
		write_label(codefile, invst)

	codefile.flush()

	lnpath = os.path.abspath(os.path.join(os.path.dirname(__file__), "labelnation"))
	lnout = NamedTemporaryFile()

	subprocess.call([lnpath, 
		'-d', 'BREAK',
		'-c', '-i', codefile.name,
		'-o', lnout.name] + lnargs)

	outf = open("nalepke.ps", "wb")

	barcodepath = os.path.join(os.path.dirname(__file__), "barcode.ps")
	outf.write(open(barcodepath).read())
	outf.write(lnout.read())

main()
