#Importing header files
import numpy as np
from scipy import *
from matplotlib.pyplot import *
from scipy.integrate import quad
from math import *
import pylab as p
import mpl_toolkits.mplot3d.axes3d as p3
import sys
import scipy.signal as sp
from sympy import *

s=symbols('s')
def lowpass(R1,R2,C1,C2,G,Vi):
	
	A=Matrix([[0.0, 0.0, 1.0, -1.0/G],[-1.0/(1.0+s*R2*C2), 1.0, 0, 0],[0, -G, G, 1.0],[-1.0/R1-1.0/R2-s*C1,1.0/R2,0.0,s*C1]])
	b=Matrix([[0.0],[0.0],[0.0],[1.0/R1]])
	V=A.inv()*b
	Vo=Vi*V[3]
	print Vo
	return (A,b,Vo)

A,b,Vo=lowpass(1000.0,1000.0,1.0e-6,1.0e-6,1000.0,1.0)
print 'G=1000'
print Vo
Vstep = Vo/s

title('Magnitude of Frequency Response for Impulse and Step for given Circuit')
w=p.logspace(0,8,801)
ss=1j*w
hf=lambdify(s,Vo,'numpy')
hf_step=lambdify(s,Vstep,'numpy')
v=hf(ss)
v_step=hf_step(ss)
p.loglog(w,abs(v),lw=2)
p.loglog(w,abs(v_step),lw=2)
p.grid(True)
legend(('Impulse Response','Step Response'),loc='best')
xlabel(r'$\omega$')
ylabel(r'$|H(e^{j\omega})|$')
p.show()


#Step response
H = sp.syms2tf(Vstep)
t,x=sp.impulse(H,None,linspace(0,10,101))
p.plot(t,x)
p.show()