#define BLOCKSIZE 8

// simple matrix multiplication
__kernel void multMatrixSimple(__global float *mO, __global float *mA, 
							   __global float *mB, uint widthA, uint widthB) {
	int globalIdx = get_global_id(0);
	int globalIdy = get_global_id(1);
	float sum =0;
	for (int i=0; i< widthA; i++) {
		float tempA = mA[globalIdy * widthA + i];
		float tempB = mB[i * widthB + globalIdx];
		sum += tempA * tempB;
	}
	mO[globalIdy * widthA + globalIdx] = sum;
}

// optimized matrix multiplication using work-group and local memory
__kernel void multMatrix(__global float *mO, __global float *mA,
						 __global float *mB, uint widthA, uint widthB) {
	uint lx = get_local_id(0);
	uint ly = get_local_id(1);
	int gx = get_group_id(0);
	int gy = get_group_id(1);
	// calculate the starting index of the global array for the each sub matrix
	uint iSubA = BLOCKSIZE * gy * widthA;
	uint iSubB = BLOCKSIZE * gx;
	// get the number of groups in
	int n = get_num_groups(0);
	// varaiable to hold the running total
	float sum = 0;
	// for each block   
	for(int i=0; i< n;i++) {
		// declare local memory for each sub matrix
		__local float tA[BLOCKSIZE][BLOCKSIZE];
		__local float tB[BLOCKSIZE][BLOCKSIZE];
		// copy a portion of the input matrices into the sub matrices
		tA[ly][lx] = mA[ly*widthA + lx + (iSubA + i* BLOCKSIZE)];
		tB[ly][lx] = mB[ly*widthB + lx + (iSubB + i* BLOCKSIZE * widthB)];
		// wait for all work-items int the group to finish copying
		barrier(CLK_LOCAL_MEM_FENCE);
		// multiply the two sub matrices together. 
		for(int k=0; k<BLOCKSIZE; k++) {
			sum += tA[ly][k] * tB[k][lx];
		}
	}
	// copy the final result to the output buffer
	int globalIdx=get_global_id(0);
	int globalIdy=get_global_id(1);
	mO[globalIdy * widthA + globalIdx] = sum;
}
