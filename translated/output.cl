__kernel void kernely(__global float *output, __global float *inputA, 
							   __global float *inputB, uint widthA, uint widthB)
		{
	int globalIdx = get_global_id(0);
	int globalIdy = get_global_id(1);
		float d ;
d = 5;
 for (int y = 0;y <= 100;y++)
 {
float e ;
e = inputA[globalIdy * widthA + y];
 d += a;
}

 output[globalIdy * widthA + globalIdx] = d;
}

__kernel void kernelz(__global float *output, __global float *inputA, 
							   __global float *inputB, uint widthA, uint widthB)
		{
	int globalIdx = get_global_id(0);
	int globalIdy = get_global_id(1);
		float c ;
c = 5;
 for (int y = 0;y <= 100;y++)
 {
float a ;
float b ;
a = inputA[globalIdy * widthA + y];
 b = inputB[y * widthB + globalIdx];
 c += a * c;
}

 output[globalIdy * widthA + globalIdx] = c;
}

