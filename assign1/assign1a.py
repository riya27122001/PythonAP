n=1
nold=1
#printing first two fibonacci numbers
print 1,nold
print 2,n
#looping from 3 t0 10
for k in range(3,11):
	#generating new fibonacci num by adding last two
	new = n+nold
	#updating last two num in series
	nold=n
	n=new
	#printing last fibonacci number
	print k,new
