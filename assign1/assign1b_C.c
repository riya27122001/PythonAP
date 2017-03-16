//In given question, all values in list have same data type, so in C we can use an array
#include <stdio.h>
#include <math.h>

int main()
{
	//Declaring variables
	double n[1000];
	double alpha = M_PI;
	
	int var, k;
	//Initialising array
	n[0]=0.2;
	//Loop for given algorithm
	for (k = 1; k < 1000; ++k)
	{
		//now var is the number required by the algorithm
		//it may have 2,1 or 0 digits before decimal place
		//appending var to array 'n'
		n[k] = ((n[k-1]+alpha) - (int)(n[k-1]+alpha))*100;
		
		//digits after decimal acc as total 4 digits
		if(n[k] < 1) //0 digits before decimal
			printf("%.4f\n",n[k]);
		else if(n[k] < 10) //1 digit before decimal
			printf("%.3f\n",n[k] );
		else //2 digits before decimal
			printf("%.2f\n",n[k] );
	
		
	}
	return 0;
}