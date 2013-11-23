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



def compute_function_1param(t,rt):
	b = rt - t
	return 1, b

def compute_function_2params(t1,rt1,t2,rt2):
	a = (rt1 -rt2)/(t1-t2)
	b = rt2 - a * t2
	return a, b
def f(ranges_and_coeffs,x):
	for (r, (a,b)) in ranges_and_coeffs:
		if r[0] <= x <  r[1]:
			return a*x+b

def compute_function(points):

	if len(points) < 2:
		s,v = points[0]
		coeffs = [((0,float('inf')) ,compute_function_1param(s,v) )]
	else:
		coeffs = []
		j = 0
		for [p1,p2] in [ points[i:i+2] for i in range(len(points)-1)]:
			a,b=compute_function_2params(p1[0],p1[1],p2[0],p2[1])
			print [p1,p2],a,b
			if j == 0:
				
				coeffs.append(((0,p1[0]),(a,b) ))
			coeffs.append(((p1[0],p2[0]),(a,b) ))
			if j == len(points)-2:
				coeffs.append(((p2[0],float("inf")),(a,b) ))
			j+=1
	print coeffs

	return coeffs

def syncro_time(coeffs,x,x_list, y_list):
#	print x.split(":")
	if len(x.split(":"))==3:
		t=convert_from_s(x)
		x_list.append(t)
		nt = f(coeffs,t)
		y_list.append(nt)
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
	sub = map(convert_from_s,option.sub)
	vid = map(convert_from_s,option.vid)
	if len(sub) != len(vid) :
		print "error not same number of point between subtitle and video"


	inputfile = option.inputfile
	outputfile = option.outputfile

	coeffs = compute_function(zip(sub,vid))

	inp = open(inputfile).read()
	outp = open(outputfile,'wb')

	x_list = []
	y_list = []
	for l in inp.split("\n"):
		x = l.split(":")
		if len(x) >= 3:

			ll = l.split()
#			print ll
			lll = map (lambda x:syncro_time(coeffs,x,x_list,y_list),ll)


			outp.write(" ".join(lll)+"\n")
		else:
			outp.write(l+"\n")

	import pylab
	import numpy
	
#	c , a = scipy.optimize.curve_fit(func,list(zip(*points)[0]),list(zip(*points)[1]))
	pylab.plot(sub,vid,'ro')
	x__ =numpy.linspace(0,max(x_list),1000)
	pylab.plot(x_list,y_list,"b.")
	pylab.plot(x__,x__,"g-")
	
	pylab.show()


