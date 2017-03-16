#Importing header files
import numpy as np
from scipy import *
from matplotlib.pyplot import *
from scipy.integrate import quad
from math import *
from pylab import *
import mpl_toolkits.mplot3d.axes3d as p3
import sys

if (len(sys.argv)>1):
	elec_size=sys.argv[1] #electrode size
	Nx=sys.argv[2] #size along x
	Ny=sys.argv[3] #size along y
	Niter=sys.argv[4] #number of iterations to perform
else:
	Nx=25 #size along x
	Ny=25 #size along y
	elec_size=10 #electrode size
	Niter=2000 #number of iterations to perform


#function to calculate potential
def potential_func(elec_size, Nx, Ny):
	#electrode assumed to be in the middle
	Nbegin = int((Nx-elec_size)/2)+1 #starting point of electrode
	Nend = Nbegin+ elec_size-1 #ending point of electrode
	phi = zeros((Ny,Nx)) #intialising potential matrix
	V0=1.0 #voltage of top electrode
	phi[0,Nbegin:(Nend+1)]=V0
	
	#calcutating error between two iteration
	errors = []
	iters = range(Niter)
	for k in iters:
		#copying phi
		oldphi = phi.copy()
		#updating phi
		phi[1:-1,1:-1]=0.25*(phi[1:-1,0:-2]+ phi[1:-1,2:]+ phi[0:-2,1:-1]+ phi[2:,1:-1])
		#boundary conditions
		#at boundary electric field is 0, so value of phi at one edge off boundary is same as boundary
		phi[1:-1,0]=phi[1:-1,1]
		phi[1:-1,-1]=phi[1:-1,-2]
		phi[0,:Nbegin]=phi[1,:Nbegin]
		phi[0,(Nend+1):]=phi[1,(Nend+1):]
		phi[-1,:Nbegin]=phi[-2,:Nbegin]
		phi[-1,(Nend+1):]=phi[-2,(Nend+1):]
		errors.append(fabs(phi-oldphi).max())
	return phi, errors	

#error estimation
def error_est(errors,Nx,Ny):
	V0=1.0
	iters = range(Niter)
	title('Evolution of errors with iteration')	
	xlabel('Iteration')
	ylabel('Error')
	semilogy(iters[::50],errors[::50],'ro')
	#calculating B for exponential fit
	a = ones((len(errors),2)) # allocate a matrix A with ones
	#first column is ones
	a[:,1] = iters #second column is iteration number
	b = np.log(errors)#result side is log of errors
	lst_sq = np.linalg.lstsq(a,b)[0] #least square approximation
	#A and B are found
	A = np.exp(lst_sq[0])
	B = lst_sq[1]
	#curve fit for errors = y found using A and B
	y = A*np.exp(B*array(iters))

	semilogy(iters,y,'r')


	#calculating B for exponential fit starting from 500th iteration for better fit
	a = ones((len(errors)-500,2)) # allocate a matrix A with ones
	#first column is ones
	
	a[:,1] = iters[500:] #second column is iteration number
	b = np.log(errors[500:]) #result side is log of errors
	lst_sq = np.linalg.lstsq(a,b)[0]#least square approximation
	#A and B are found
	A = np.exp(lst_sq[0])
	B = lst_sq[1]
	print "Least square approximation: A=%f, B=%f" %(A, B)
	#curve fit for errors = y found using A and B
	y = A*np.exp(B*array(iters[500:]))
	semilogy(iters[500:],y,'g')
	legend(('error','fit 1','fit 2'))
	savefig('err_fit'+str(elec_size)+'.pdf',format='pdf')
	show()
	#expression for estimated error between potentials
	print "Final estimated error in potential: %f" %((-A/B)*np.exp(B*(2000.0+0.5)))
	#Surface plot for potential
	fig1=figure(2) # open a new figure
	ax=p3.Axes3D(fig1) # Axes3D is the means to do a surface plot
	x=arange(1,Nx+1) # create x and y axes
	y=arange(1,Ny+1)
	X,Y=meshgrid(x,y) # creates arrays out of x and y
	title('The 3-D surface plot of the potential')
	surf = ax.plot_surface(Y, X, phi, rstride=1, cstride=1, cmap=cm.jet,linewidth=0)
	savefig('surface_plot'+str(elec_size)+'.pdf',format='pdf')
	show()

	#Contour plot for potential
	fig2=figure(3)
	CS = contour(x, y, phi)
	clabel(CS, inline=1, fontsize=10)

	title('Contour plot for potential')
	savefig('contour_plot'+str(elec_size)+'.pdf',format='pdf')
	show()

	#current  density
	Jx=zeros((Ny,Nx))
	Jy=zeros((Ny,Nx))
	#calculating current density for inner matrix points by effectively differentiating potential
	Jy[1:-1,1:-1]=0.5*(phi[0:-2,1:-1] - phi[2:,1:-1])
	Jx[1:-1,1:-1]=0.5*(phi[1:-1,0:-2] - phi[1:-1,2:])
	title('The vector plot of current flow')
	quiver(y,x,Jy.transpose(),Jx.transpose())
	savefig('curr_plot'+str(elec_size)+'.pdf',format='pdf')
	show()

	#finding total current
	curr_enter = sum(Jy[1,1:-1]) #adding current density in y-direction at entry
	curr_exit = sum(Jy[-2,1:-1]) #adding current density in y-direction at exit
	curr_avj = (curr_exit+curr_enter)/2.0 #average current 
	curr_diff = fabs(curr_enter-curr_exit) #diffenence or error in current

	print "Niter: %d Iavj=%f Idiff=%f" %(Niter, curr_avj, curr_diff)
	#finding resistance
	print "The resistance is thus approximated to be: %f ohms." %(V0/curr_avj)
	
	
#Mean square error in potential
def meansq_err(phi,Nx,Ny):	
	idx = zeros((Ny,Nx)) #initialising index matrix
	#creating a matrix which contains the y-index for phi marix
	idx[0:,]=np.array(range(Ny)) 
	idx = idx.transpose()
	idx=array(idx)
	phi=array(phi)
	#average least square error by finding sum of squares of errors 
	#and dividing by no. of points at which potential is estimated(Nx*Ny)
	meansq_err = (1.0/(Nx*Ny))*sum((phi-1.0*((Ny-idx)/Ny))**2)
	return meansq_err
	
	

phi,errors=potential_func(elec_size,Nx,Ny)
error_est(errors,Nx,Ny)
elec_size=Nx
phi,errors=potential_func(elec_size,Nx,Ny) #elec_size = Nx
error_est(errors,Nx,Ny)
#comparing least square errors for diff values of Nx and Ny while maintaining their ratio
error_meansq =  meansq_err(phi,Nx,Ny)
print "Mean square error for Nx=%d,Ny=%d and no. of iterations = %d is %f" %(Nx,Ny,Niter,error_meansq)
Nx=50
Ny=50
phi=potential_func(Nx,Nx,Ny)[0]
error_meansq =  meansq_err(phi,Nx,Ny)
print "Mean square error for Nx=%d,Ny=%d and no. of iterations = %d is %f" %(Nx,Ny,Niter,error_meansq)
Nx=100
Ny=100
phi=potential_func(Nx,Nx,Ny)[0]
error_meansq =  meansq_err(phi,Nx,Ny)
print "Mean square error for Nx=%d,Ny=%d and no. of iterations = %d is %f" %(Nx,Ny,Niter,error_meansq)
#plotting mean square error for different Nx and Ny

iters = range(Niter)
title('Evolution of errors with No. of point of estimation')	
xlabel('Edge length of conductor')
ylabel('Error')
rng = range(10,51)
err=[]
for i in rng:
	err.append(meansq_err(potential_func(i,i,i)[0],i,i))

plot(rng,err)
savefig('err_plot.pdf',format='pdf')
show()
