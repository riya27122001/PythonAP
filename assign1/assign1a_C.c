#include <stdio.h>

int main()
{
	//Declaring variables
	int n, nold, k, new;
	//initialsing variables
	n=1; //second fibonacci num
	nold=1; //first fibonacci num
	//Printing first two fibonacci num
	printf("1 %d\n",nold );
	printf("2 %d\n",n);
	for (k = 3; k <= 10; ++k)
	{
		//generating new fibonacci num by adding last two
		new = n+nold;
		//updating last two num in series
		nold=n;
		n=new;
		//printing last fibonacci number
		printf("%d %d\n",k,new );
	}
	return 0;
}