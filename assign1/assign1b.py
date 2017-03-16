
#should we round off or format specifier
import math

n = [0.2]
alpha = math.pi
for k in range(1,1000):
	#now var is the number required by the algorithm
	#it has zero digits before decimal place
	var = ((n[k-1]+alpha) - (int)(n[k-1]+alpha))*100
	#appending var to list 'n'
	n.append(var)
	#n[k] has 2,1, or 0 digits before decimal place
	#total 4 digits
	if n[k] < 1: #0 digits before decimal, so 4 digit after decimal
		print "%.4f" %(n[k])
	elif n[k] < 10: #1 digits before decimal, so 3 digit after decimal
		print "%.3f" %(n[k])
	else: #2 digits before decimal, so 2 digit after decimal
		print "%.2f" %(n[k])
	