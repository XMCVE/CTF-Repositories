#include <stdio.h> 

void  decrypt(unsigned int *A,unsigned int *B){
	int j;
	unsigned int v0 = A[0],v1 = A[1],delta = 0x405006,sum = delta * 32;
	for(j=0;j<32;j++){
	
		v1 -= (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + B[(sum >> 11) & 3]);
		
		sum -= delta;
		
		v0 -= (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + B[sum & 3]);
	
	}
	A[0] = v0;
	A[1] = v1;

}
unsigned int data[]={0x3C5F791A, 0x1A38CC7,0xA532267E, 0x8EFB0F27};
unsigned int key[]={0x114514, 0x1919810,0x24270047,9};


int main()
{
	decrypt(&data[0],key);
	decrypt(&data[2],key);
	
}
