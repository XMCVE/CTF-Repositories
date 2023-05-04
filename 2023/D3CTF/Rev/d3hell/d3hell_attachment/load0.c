#include <stdio.h>
#include <Windows.h>

int main()
{
	
	int a = LoadLibrary("d3runtime.dll");
	if(a==0)
		printf("%d",GetLastError());
 } 
