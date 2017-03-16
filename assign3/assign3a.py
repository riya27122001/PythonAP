#Importing header files
import numpy as np
from scipy import *
from matplotlib.pyplot import *
from scipy.integrate import quad
from math import *

#Exponential Function
def expo(x):
	return e**x

#cos(cos(x)) Funxtion
def cosine(x):
	return np.cos(np.cos(x))

#Returns f(x)cos(x)
def u(x,func,k):
	return func(x)*np.cos(k*x)

#Return f(x)sin(x)
def v(x,func,k):
	return func(x)*np.sin(k*x)

#Finding 2*n+1 fourier coefficients for func(x) i.e. a0,a1,..an and b1,b2,..bn
def f_coeff(func,n):
	a = []
	
	a.append((1/(2*pi))*quad(func,0,2*pi)[0]) #a0
	for k in range(1,n+1):
		a.append((1/pi)*quad(u,0,2*pi,args=(func,k))[0]) #ak
		a.append((1/pi)*quad(v,0,2*pi,args=(func,k))[0]) #bk
	return a


#Fourier coeffcients for e^x
ans_exp = f_coeff(expo,25)

n= range(0,26) #Indices of fourier coefficients

#Fourier coeffcients for cos(cos(x))
ans_cos = f_coeff(cosine,25)

#Fourier coefficients by Least Square Approximation
#Creating a linearly spaced array with 400 points between 0 and 2*pi
x = linspace(0,2*pi,401)
x=x[:-1] # drop last term to have a proper periodic integral
b = expo(x) #exponential func for vector
A = zeros((400,51)) # allocate a matrix A with zeroes
A[:,0] = 1 #first column is 1s
for k in range(1,26):
	A[:,2*k-1] = np.cos(k*x) #cos(kx) column
	A[:,2*k] = np.sin(k*x) #sin(kx) column
c = np.linalg.lstsq(A,b)[0] #[0] gives first col of lstsq which is the best fit vector

a_coeff = np.fabs(insert(c[1::2],0,c[0])) #extracting a0,a1,...an in an array

#plotting first 51 fourier coefficients for e^x in semilog scale
title('Fourier Coefficients for $e^x$')
xlabel('$n$')
ylabel('First 51 Fourier Coefficients')
semilogy(n,np.fabs([ans_exp[0]]+ans_exp[1::2]),'bo') #an
semilogy(n[1:],np.fabs(ans_exp[2::2]),'ro') #bn
semilogy(n,a_coeff,'go') #least square an
semilogy(n[1:],np.fabs(c[2::2]),'go') #least square bn
legend(('$a_n$','$b_n$','Least square solution'),loc='best')
savefig('fig1_exp.pdf',format='pdf') #save figure as pdf
show()

#plotting first 51 fourier coefficients for e^x in loglog scale
title('Fourier Coefficients for $e^x$')
xlabel('$n$')
ylabel('First 51 Fourier Coefficients')
loglog(n,np.fabs([ans_exp[0]]+ans_exp[1::2]),'bo') #an
loglog(n[1:],np.fabs(ans_exp[2::2]),'ro') #bn
loglog(n,a_coeff,'go') #least square an
loglog(n[1:],np.fabs(c[2::2]),'go') #least square bn
legend(('$a_n$','$b_n$','Least square solution'),loc='best')
savefig('fig2_exp.pdf',format='pdf') #save figure as pdf
show()

#error plot for first 51 fourier coefficients for e^x in semilog scale
title('Absolute value of error in Fourier Coefficients for $e^x$')
xlabel('$n$')
ylabel('Error')
error = np.fabs(ans_exp-c)
semilogy(n,insert(error[1::2],0,error[0]),'bo') #an
semilogy(n[1:],error[2::2],'ro') #bn
legend(('Error in $a_n$','Error in $b_n$'),loc='best')
savefig('error_exp.pdf',format='pdf') #save figure as pdf
show()
#printing maximum error for e^x
print "Maximum error between Coefficients found by Integration and Least Squares Method:"
print 'e^x:'
print np.amax(error)



b = cosine(x) #cos(cos(x)) func for vector

c = np.linalg.lstsq(A,b)[0] #[0] gives first col of lstsq which is the best fit vector
a_coeff = np.fabs(insert(c[1::2],0,c[0])) #extracting a0,a1,...an in an array

title('Fourier Coefficients for $cos(cos(x))$')
xlabel('$n$')
ylabel('First 51 Fourier Coefficients')

#plotting first 51 fourier coefficients for cos(cos(x)) in semilog scale
semilogy(n,np.fabs([ans_cos[0]]+ans_cos[1::2]),'bo') #an
semilogy(n[1:],np.fabs(ans_cos[2::2]),'ro') #bn
semilogy(n,a_coeff,'go') #least square an
semilogy(n[1:],np.fabs(c[2::2]),'go') #least square bn
legend(('$a_n$','$b_n$','Least square solution'),loc='best')
savefig('fig1_cos(cos).pdf',format='pdf') #save figure as pdf
show()

title('Fourier Coefficients for $cos(cos(x))$')
xlabel('$n$')
ylabel('First 51 Fourier Coefficients')

loglog(n,np.fabs([ans_cos[0]]+ans_cos[1::2]),'bo') #an
loglog(n[1:],np.fabs(ans_cos[2::2]),'ro') #bn
loglog(n,a_coeff,'go') #least square an
loglog(n[1:],np.fabs(c[2::2]),'go') #least square bn
legend(('$a_n$','$b_n$','Least square solution'),loc='best')
savefig('fig2_cos(cos).pdf',format='pdf') #save figure as pdf
show()

#error plot for first 51 fourier coefficients for cos(cos(x)) in semilog scale
title('Absolute value of error in Fourier Coefficients for $cos(cos(x))$')
xlabel('$n$')
ylabel('Error')

error = np.fabs(ans_cos-c)
#printing maximum error for e^x
print 'cos(cos(x)):'
print np.amax(error)
semilogy(n,insert(error[1::2],0,error[0]),'bo')
semilogy(n[1:],error[2::2],'ro')
legend(('Error in $a_n$','Error in $b_n$'),loc='best')
savefig('error_cos(cos)).pdf',format='pdf') #save figure as pdf
show()


