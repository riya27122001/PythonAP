#Importing header files
import numpy as np
from scipy import *
from matplotlib.pyplot import *
from scipy.integrate import quad
from math import *
from pylab import *
import mpl_toolkits.mplot3d.axes3d as p3
import sys

#returns index where value of y-index is i/10
def ret_idx(i):
	return np.where((10*np.array(Y[:,0,0])).astype(int)==i)[0][0]

# declaring array of points
#top part of bent wire
points_top_bent = zeros((8,2)) # allocate a matrix with zeroes
points_top_bent[:,0] = np.arange(1.0,0.5,-0.1/np.sqrt(2)) #assign values
points_top_bent[:,1] = np.arange(-0.9,-0.4,0.1/np.sqrt(2))

#right part of wire
points_rgt = zeros((10,2)) # allocate a matrix with zeroes
points_rgt[:,0] = 0.5 #assign values
points_rgt[:,1] = np.arange(-0.4,0.6,0.1)

#top part of wire
points_top = zeros((10,2)) # allocate a matrix with zeroes
points_top[:,0] = np.arange(0.4,-0.6,-0.1)#assign values
points_top[:,1] = 0.5

#left part of wire
points_lft = zeros((10,2)) # allocate a matrix with zeroes
points_lft[:,0] = -0.5#assign values
points_lft[:,1] = np.arange(0.4,-0.6,-0.1)

#bottom part of wire
points_btm = zeros((9,2)) # allocate a matrix with zeroes
points_btm[:,0] = np.arange(-0.4,0.5,0.1)#assign values
points_btm[:,1] = -0.5

#bottom part of bent wire
points_btm_bent = zeros((8,2)) # allocate a matrix with zeroes
points_btm_bentx = np.arange(0.9,0.4,-0.1/np.sqrt(2))#assign values
points_btm_benty = np.arange(-1.0,-0.5,0.1/np.sqrt(2))
points_btm_bent[:,0] = points_btm_bentx[::-1] #reversing array since I've started counting points
# from bottom for simplicity whereas it is supposed to be counted the other way round
points_btm_bent[:,1] = points_btm_benty[::-1]

#concatenate all points
points = np.concatenate((points_top_bent,points_rgt,points_top,points_lft,points_btm,points_btm_bent),axis=0)

#find centers
centers = (points[:-1]+points[1:])/2
#concatenate with zero column z-axis
centers = np.concatenate((centers,np.array([zeros(len(centers))]).transpose()),axis=1)

#find current direction by subtarcting
curr_dir=(points[1:]-points[:-1])*10
#concatenate with zero column z-axis
curr_dir = np.concatenate((curr_dir,np.array([zeros(len(curr_dir))]).transpose()),axis=1)



#plot points, centers and current direction
fig = figure()
title('Current direction in wire')


xlim(-1.0,1.1)
ylim(-1.0,1.1)
xticks(np.arange(-1.0,1.1,0.2))
yticks(np.arange(-1.0,1.1,0.2))
grid()
plot(points[:,0],points[:,1],'kx')
plot(centers[:,0],centers[:,1],'ro')
quiver(points[:-1,0],points[:-1,1],curr_dir[:,0],curr_dir[:,1],color='b')
 #quiver plot for current direction
legend(('Points on wire','Centers'))
savefig('current.pdf',format='pdf')
show()

x=np.arange(-1.0,1.1,0.1) # create x and y and z axes
y=np.arange(-1.0,1.1,0.1)
z=np.arange(-1.0,1.1,0.1)
X,Y,Z=meshgrid(x,y,z) # creates arrays out of x, y and z


# Field at point due to itself is assumed to be zero
#creating array of the size of meshgrid to store B in directions x,y and z
Bx=np.array(zeros((len(x),len(y),len(z))),dtype=float)
By=np.array(zeros((len(x),len(y),len(z))),dtype=float)
Bz=np.array(zeros((len(x),len(y),len(z))),dtype=float)

#evaluating field due to all the centers of wires one by one
for i,j in zip(centers,curr_dir):
	
	#position vector R
	Rx = X-i[0]
	Ry = Y-i[1]
	Rz = Z-i[2]
	
	#magnitude of R
	R = (Rx**2+Ry**2+Rz**2)**(0.5)

	#masking values where R is nearly 0
	R=np.ma.masked_where(R<0.00001, R)
	Rx=np.ma.masked_where(R<0.00001, Rx)
	Ry=np.ma.masked_where(R<0.00001, Ry)
	Rz=np.ma.masked_where(R<0.00001, Rz)
	
	#dB due to current element
	dBx=(10.0**(-5)*j[1]*Rz)/(R**3)
	dBy=(10.0**(-5)*-j[0]*Rz)/(R**3)
	dBz=(10.0**(-5)*(j[0]*Ry-j[1]*Rx))/(R**3)
	#adding all dB to get total field
	Bx=Bx+dBx
	By=By+dBy
	Bz=Bz+dBz
#plotting B at y=0.0
title(r"Arrow plot of $\vec{B}$ along the $x-z$ plane")
xlabel('$x$')
ylabel('$z$')
quiver(X,Z,Bx[ret_idx(0)],Bz[ret_idx(0)],scale=0.01)
savefig('B(y=0.0).pdf',format='pdf')
show()
#plotting B at y=-0.3
title(r"Arrow plot of $\vec{B}$ along the plane $y=-0.3cm$")
xlabel(r'$x$')
ylabel(r'$z$')
quiver(X,Z,Bx[ret_idx(-3)],Bz[ret_idx(-3)],scale=0.01)
savefig('B(y=-0.3).pdf',format='pdf')
show()
#plotting B at y=-0.5
title(r"Arrow plot of $\vec{B}$ along the plane $y=-0.5cm$")
xlabel(r'$x$')
ylabel(r'$z$')
quiver(X,Z,Bx[ret_idx(-5)],Bz[ret_idx(-5)],scale=0.01)
savefig('B(y=-0.5).pdf',format='pdf')
show()
#plotting B at y=-0.7
title(r"Arrow plot of $\vec{B}$ along the plane $y=-0.7cm$")
xlabel(r'$x$')
ylabel(r'$z$')
quiver(X,Z,Bx[ret_idx(-7)],Bz[ret_idx(-7)],scale=0.01)
savefig('B(y=-0.7).pdf',format='pdf')
show()