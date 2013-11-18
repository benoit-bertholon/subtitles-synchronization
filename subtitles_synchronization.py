#!/usr/bin/python





import optparse
import sys



def convert_from_s(stime):
	l = stime.split(":")
	if len(l) == 3 :
		l[2] = l[2].replace(",",".")
	time = int(l[0])*3600 +   int(l[1])*60 +   float(l[2]) 
	return time

def convert_to_s(time):
	s = "%02d:%02d:%06.3f" %(int(time/3600),int((time%3600)/60),float(time%60))
	s= s.replace(".",",")
	return s



def compute_function(t1,rt1,t2,rt2):
	a = (rt1 -rt2)/(t1-t2)
	b = rt2 - a * t2
	def f(t):
		return a *t + b
	print a, b
	return f

def syncro_time(f,x):
#	print x.split(":")
	if len(x.split(":"))==3:
		t=convert_from_s(x)
		nt = f(t)
		s=convert_to_s(nt)
		return s
	return x

if __name__ == "__main__":


	import optparse
	
	optparser = optparse.OptionParser(usage="usage: %prog [options]")

	optparser.add_option("-s" , dest="sub",default=[],action='append',help="time in subtitle")
	optparser.add_option("-v" , dest="vid",default=[], action='append',help="time in video")
	optparser.add_option("-i" , dest="inputfile",default="", help="output subtitle file")
	optparser.add_option("-o" , dest="outputfile",default="",help="input subtitle file")


	(option , arg ) = optparser.parse_args(sys.argv)
	[st1,st2,srt1,srt2] = sys.argv[1:5]
	inputfile = sys.argv[5]
	outputfile = sys.argv[6]
	[t1,t2,rt1,rt2] = map(convert_from_s,[st1,st2,srt1,srt2])
	print [t1,t2,rt1,rt2]
	f = compute_function(t1,rt1,t2,rt2)
	inp = open(inputfile).read()
	outp = open(outputfile,'wb')

	for l in inp.split("\n"):
		if len(l.split(':')) >= 3:
			ll = l.split()
#			print ll
			lll = map (lambda x:syncro_time(f,x),ll)
#			print " ".join(lll)
			outp.write(" ".join(lll)+"\n")
		else:
#			print l
			outp.write(l+"\n")

