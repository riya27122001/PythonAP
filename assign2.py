#Importing header files
from numpy import *
from scipy import *
from matplotlib.pyplot import *
from scipy.integrate import quad
from math import *

#Function given in question 1
def func(t):
	return 1/(1+t*t)
#Tan inverse function
def tan_inv(x):
	y = []
	#Building up array of integrals by appending
	for a in x:
		y.append(quad(func,0,a)[0]) #quad to compute integrals acc to given formula
	
	return y
#error in tan inv func computed by integral wrt arctan library function
def err_tan_inv(x):
	y = []
	
	for a in x:
		y.append(fabs(quad(func,0,a)[0]-arctan(a))) #building error in array
	
	return y
#computing tan inverse with trapezoidal integral without cumsum
#acc to expression given in question
def trap_tan_inv_loop(x,h):
	
	var = 0
	var1 = []
	#looping to find cummulative sum
	for j in arange(0,(x[-1]+h),h):
		var += func(j)
		var1.append(h*(var - 0.5*(func(0)+func(j)))) #appending sum to array cummulatively
	
	return var1
#Trapezoidal tan inverse integral with cummulative sum
def trap_tan_inv(x,h):
	
	j = arange(0,(x[-1]+h),h) #array at regular intervals split at h
	var = cumsum(func(j)) #cummulative sum of the function at those points
	var = h*(var - 0.5*(func(0)+func(j))) #trapezoidal integral computed acc to expression
	if hasattr(x, "__len__"): #if input is an array
		step= (len(var)-1)/(len(x)-1) #making o/p an array same length as that of i/p
		return var[::step]
	else:
		return var #else returning single value
	
#Error estimation and restriction to 10^-8
def err_est():
	#starting with interval h as 0.1
	h=[0.1]
	e=[] #estimated error array
	exact_e=[] #exact error array
	flg=0 #flg becomes 1 when error less than 10^-8
	x=arange(0,(5+h[-1]),h[-1]) #making x a regular interval array with interval as last element of h i.e. h[-1]
	y=trap_tan_inv(x,h[-1]) #storing trapezoidal intgral of those values in y
	while flg==0: #when error > than desired value
		h.append(h[-1] / 2) #halving last element and appending
		x=arange(0,(5+h[-1]),h[-1]) #creating x with new interval
		y_new=trap_tan_inv(x,h[-1]) #calculating y again and storing in y_new
		max_error=0
		max_exact_error=0
		for i in range(0,len(y)):
			error=fabs(y_new[2*i]-y[i]) #calculating error at common points in subsequent steps as backward step
			exact_error=fabs(y[i]-arctan(x[2*i])) #calculating error between those common points and comparing with arctan function
			#calculating maxima for exact and estimated error
			if (error>max_error):
				max_error=error
			if (exact_error>max_exact_error):
				max_exact_error=exact_error
		#appending to exact and estimated error arrays
		e.append(max_error)
		exact_e.append(max_exact_error)
		#checking if error < 10^-8
		if (max_error<pow(10,-8)):
			flg=1 
		#updating old vector y to y_new	
		y=y_new
	
	
	#plotting estimated and approximate error in log-log plot
	loglog(h[:len(h)-1],exact_e,'ro')
	
	loglog(h[:len(h)-1],e,'g+')
	
	ylabel('Error')
	xlabel(r'$h$')
	title('Exact Error and Estimated Error of trapezoidal function.\n')
	legend(('Exact error','Estimated error'),loc='best')
	show()
	return h[-1]
	

#Main Function code
x = linspace(0,5,51) #Creating linearly spaced array of 51 elements with linearly spaced from 0 to 5
y =func(x) #Computing func for the vector x
plot(x,y) #Plotting func(x) with vector x
title(r"Plot of $1/(1+t^{2})$") #Title of plot
xlabel('t') #Label of x-axis
ylabel(r"$1/(1+t^{2})$") #Label of y-axis
show() #Show plot

#Computing tan inverse computed by integral and arctan function and trapezoidal function
y = tan_inv(x) 
z = arctan(x)
a = trap_tan_inv(x,0.1) #trapezoidal func with steps of 0.1
#tabulating and printing comparison of tan inverse computed by quad integral and arctan function
print "x\t arctan(x)-Function\t arctan(x)-Integral\t"
for i in range(0,51):
	print "%7.5f" %(x[i]),"\t ","%7.5f" %(z[i]),"\t ","%7.5f" %(y[i])
#Plotting tan inverse computed by integral and arctan function and trapezoidal function
plot(x,y,'ro')
plot(x,z,'k')
plot(x,a,'g+')
legend(('quad fn',r"$tan^{-1} x$" ,'Trapezoidal Function'),loc='best')
xlabel(r'$x$')
ylabel(r'$\int_{0}^{x} du/(1+u^2)$')
title('Comparison of $tan^{-1}$ as computed by $\int_{0}^{x} du/(1+u^2)$ and arctan()\n')
show()

#Plotting error in tan_inv function by quad integral method
y = err_tan_inv(x)
semilogy(x,y,'ro')
xlabel(r'$x$')
ylabel('Error')

title('Error in $\int_{0}^{x} dx/(1+x^2)$ \n')
show()

#Estimating and restricting error to 10^-8 in trapezoidal integral method
h = err_est() #returning h where error is restricted
print h
#Plotting tan inverse computed by integral and arctan function and trapezoidal function

y = tan_inv(x) 
z = arctan(x)
a = trap_tan_inv(x,h) #trapezoidal integral computed with computed h from error estimation


plot(x,y,'ro') #quad integral
plot(x,z,'k') #arctan
plot(x,a,'g+') #trapezoidal
legend(('quad fn',r"$tan^{-1} x$" ,'Trapezoidal Function'),loc='best')
xlabel(r'$x$')
ylabel(r'$\int_{0}^{x} du/(1+u^2)$')
title('Comparison of $tan^{-1}$ as computed by $\int_{0}^{x} du/(1+u^2)$ and arctan()\n')
show()