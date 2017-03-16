#Importing header files
import numpy as np
from scipy import *
from matplotlib.pyplot import *
from scipy.integrate import quad
from math import *
from pylab import *
import mpl_toolkits.mplot3d.axes3d as p3
import sys
import scipy.signal as sp

# computes f(t) as mentioned in question for different time coefficients
def f(t,coeff):
	return cos(coeff*t)*exp(-0.05*t)
# computes frequency response given numerator and denominator polynomials	
def H(coeff):
	Num = np.poly1d([1.0])
	Den = np.poly1d([1.0,0.0,coeff**2])
	H = sp.lti(Num,Den)	
	return H	

# computes impulse response given numerator and denominator polynomials	of transfer function
def impulse_res(decay,color):
	Num = np.poly1d([1.0,decay])
	Den_1 = np.polyadd(np.polymul([1.0,decay],[1.0,decay]),[2.25])
	Den_2 = np.poly1d([1.0,0.0,2.25])
	Den = np.polymul(Den_1,Den_2)
	H = sp.lti(Num,Den) #transfer function(frequency response)
	#using impulse function to compute impulse response from transfer function
	t,x = sp.impulse(H,None,linspace(0,50,501)) 
	plot(t,x,color)
	
	return H

#plotting solution of a given differential equation for diffrent valus of decay parameter
title('Solution of given D.E. for different decay')
xlabel('t')
ylabel('x')
X = impulse_res(0.5,'r')
X = impulse_res(0.05,'g')
legend((r'$x^{..}+2.25x=cos(1.5t)e^{-0.50t}u(t)$','$x^{..}+2.25x=cos(1.5t)e^{-0.05t}u(t)$'),loc='best')
savefig('de_decay.pdf',format='pdf')
show()

#plotting solution of a given differential equation for diffrent values of time coefficient
title(r'Solution of $x^{..}+2.25x=cos(\alpha*t)e^{-0.50t}u(t)$')
xlabel('t')
ylabel('x')
for i in arange(1.40,1.65,0.05):
	t=linspace(0,50,501)
	t,y,svec=sp.lsim(H(1.5),f(t,i),t)
	plot(t,y,label=r"$\alpha$=%.2f" %i)	
legend(loc='best')	
savefig('de_time.pdf',format='pdf')
show()

#solution to differential equation representing coupled springs
#x
title(r'Solution to coupled equations: $x^{..}+(x-y)=0,y^{..}+2(y-x)=0$')
xlabel('t')
Num = np.poly1d([1.0,0.0,2.0])
Den = np.poly1d([1.0,0.0,3.0,0.0])
X = sp.lti(Num,Den)
t,x = sp.impulse(X,None,linspace(0,20,501)) #initial condition vector added

plot(t,x,'r')

#y
Num = np.poly1d([2.0])
Den = np.poly1d([1.0,0.0,3.0,0.0])
X = sp.lti(Num,Den)
t,y = sp.impulse(X,None,linspace(0,20,501))
plot(t,y,'g')
legend(('x','y'),loc='best')
savefig('impulse.pdf',format='pdf')
show()

#RLC circuit
#Bode plot for transfer function of an RLC circuit

Num = np.poly1d([1.0])
Den = np.poly1d([10.0**(-12),10.0**(-4),1.0])
H = sp.lti(Num,Den)
w,S,phi=H.bode()

#magnitude response

a=subplot(2,1,1)

xlabel(r'$\omega$')
ylabel(r'$\|H(e^{j\omega})\|$ in dB')
semilogx(w,S)
#frequency response
b=subplot(2,1,2)
xlabel(r'$\omega$')
ylabel(r'$ang(H(e^{j\omega}))$ in degrees')
suptitle('Bode plot of RLC filter') #super-title
semilogx(w,phi)
savefig('bode.pdf',format='pdf')
show()

#RLC filter output for a given input
title(r'RLC filter output for $v_i(t)=cos(10^{3}t)-cos(10^{6}t)$')
t=arange(0,0.03,10**-6)
v_i = np.cos(1000.0*t)-np.cos((10.0**6)*t)
t,y,svec=sp.lsim(H,v_i,t)
xlabel(r'$t$')
ylabel(r'$x$')
plot(t,y)
savefig('rlc.pdf',format='pdf')
show()

#Transient of RLC filter output for a given input
title(r'RLC filter output transient for $v_i(t)=cos(10^{3}t)-cos(10^{6}t)$')
t=arange(0,30.0*10**(-6),10**-6)
v_i = np.cos(1000.0*t)-np.cos((10.0**6)*t)
t,y,svec=sp.lsim(H,v_i,t)
xlabel(r'$t$')
ylabel(r'$x$')
plot(t,y)
savefig('rlc_trans.pdf',format='pdf')
show()


