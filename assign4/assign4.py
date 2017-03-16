#Importing header files
import numpy as np
from scipy import *
from matplotlib.pyplot import *
from scipy.integrate import quad
from math import *
from scipy.special import jv

#Extracting subvector starting from x0 from a vector x
#x is an increasing vector
def subvec(x,x0):
	v1 = x[np.where(x>=x0)] #indices of x where value >= x0 are extracted
	v2 = jv(1,v1) #computing bessel fn for extracted vector
	return v1,v2 #returning extracted vector and its bessel fn

#returns cos fn divide by sqrt(x)
def cos_with_amp(x):
	return np.cos(x)/x**(0.5)	

#returns sin fn divide by sqrt(x)
def sin_with_amp(x):
	return np.sin(x)/x**(0.5)

#adds randomised noise to passed vector
def vec_with_noise(x,eps):
	x = x+eps*randn(len(x)) #noise*randomised vector of length of x
	return x

#Function to compute 'v' as in given expression in question
def calcnu(x,x0,c,eps,model):
	
	v = [] #v array
	err = [] #error array
	print "A and B for model %c with noise = %f:\n" %(model,eps)
	print "A\t\t\tB\n" #printing out header for values of A and B as computed in expression
	for i in x0:
		b = subvec(x,i)[1] #extracted subvector from linerly spaced vector
		b = vec_with_noise(b,eps) #adding noise
		A = zeros((len(subvec(x,i)[0]),2)) # allocate a matrix A with zeroes
		if model=='b':
			A[:,0] = np.cos(subvec(x,i)[0]) #first column is cos
			A[:,1] = np.sin(subvec(x,i)[0]) #first column is sin
		elif model=='c':
			A[:,0] = cos_with_amp(subvec(x,i)[0]) #first column is cos with amplitude 1/sqrt(x)
			A[:,1] = sin_with_amp(subvec(x,i)[0]) #first column is sin with amplitude 1/sqrt(x)
		
		a = np.linalg.lstsq(A,b)[0][0] #a is first val of lst sq vector
		b = np.linalg.lstsq(A,b)[0][1] #b is second val of lst sq vector
		print "%7.6f\t%7.6f\n" %(a,b) #printing out values of A and B as computed in expression
		phi = math.acos(a/(a**2+b**2)**(0.5)) #calculating phase from a and b: a/sqrt(a^2 + b^2)
		vi = (phi-math.pi/4)*(2/math.pi) #phi = v*pi/2 + pi/4
		v.append(vi) #v vector
		err.append(np.fabs(1-vi)) # error
	#plotting v
	plot(x0,v,c)
	return err #returning error

#Function to plot 'v' i.e Bessel Index for different no. of measurements in same range 0 to 20
def bessel_idx(num):
	x = linspace(0,20,num) #linearly spaced vector
	diff = 20.0/(num-1) #linear difference
	x0 = arange(diff, 18+diff, diff) #points to extract subvector from
	
	title('Estimation of Bessel index $v$')
	xlabel('$x_0$')
	ylabel('$v$')
	#computaion and plots acc to diff models
	err1=calcnu(x,x0,'bo',0,'b')
	err2=calcnu(x,x0,'go',0,'c')
	err3=calcnu(x,x0,'ro',0.01,'c')
	legend(('$\epsilon=0$, model (b)','$\epsilon=0$, model (c)','$\epsilon=1.0e-02$, model (c)'),loc='best')

	savefig('v_bessel'+str(num)+'.pdf',format='pdf') #save figure as pdf
	show()
	title('Error in Estimation of Bessel index $v$')
	xlabel('$x_0$')
	ylabel('Error')
	#computaion and plots of error acc to diff models
	plot(x0,err1,'bo')
	plot(x0,err2,'go')
	plot(x0,err3,'ro')
	legend(('$\epsilon=0$, model (b)','$\epsilon=0$, model (c)','$\epsilon=1.0e-02$, model (c)'),loc='best')

	savefig('err_bessel'+str(num)+'.pdf',format='pdf') #save figure as pdf
	show()
	#printing maximum error for all models
	print "Max error for model(b) without noise: %f" %(amax(err1))
	print "Max error for model(c) without noise: %f" %(amax(err2))
	print "Max error for model(c) with noise=0.01: %f" %(amax(err3))
	


#Main Function
bessel_idx(41) #bessel for 41 points
bessel_idx(61) #bessel for 61 points
bessel_idx(81) #bessel for 81 points







