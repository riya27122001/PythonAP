#Assignment 7
from pylab import *
import numpy
import scipy.signal as sp

def getresponse(H): 
	t = linspace(0,50,501)
	t,h = sp.impulse(H,None,t)
	plot(t,h)
	show()

def getH(w,delay):
	return(sp.lti([1,delay],polymul(polyadd(polymul([1,delay],[1,delay]),[w**2]),[1,0,2.25])))

getresponse(getH(1.5,0.5))
getresponse(getH(1.5,0.05))

H=sp.lti([1],[1,0,2.25])
t = linspace(0,50,501)
for w in arange(1.4,1.6,0.05):
	u=cos(w*t)*exp(-0.05*t)
	t,y,svec = sp.lsim(H,u,t)
	plot(t,y)
	show()

t = linspace(0,20,501)
X = sp.lti([1,0,2],[1,0,3,0])
Y = sp.lti([2],[1,0,3,0])
t,x = sp.impulse(X,None,t)
t,y = sp.impulse(Y,None,linspace(0,20,501))
plot(t,x)
plot(t,y)
show()	

H = sp.lti([1],[10**-12,10**-4,1])
w,s,phi = H.bode()
subplot(2,1,1)
semilogx(w,s)
subplot(2,1,2)
semilogx(w,phi)
show()

t=arange(0,0.03,0.5*10**-6)
inp = cos(1000*t)-cos((10**6)*t)
t,y,vec=sp.lsim(H,inp,t)
plot(t,y)
show()