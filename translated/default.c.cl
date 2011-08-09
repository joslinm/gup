__kernel void kernely(__global float *output, __global float *inputA, 
							   __global float *inputB, uint widthA, uint widthB)
		{
	int globalIdx = get_global_id(0);
	int globalIdy = get_global_id(1);
		float d ;
d = 0;
 int y = 0;for (y;y <= 31;y++)
 {
float e ;
float f ;
e = inputA[globalIdy * widthA + y];
 f = inputB[y * widthB + globalIdx];
 d += f * e;
}

 output[globalIdy * widthA + globalIdx] = d;
}

