#ifndef GUP_STD
#define GUP_STD

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "CL/cl.h"

#define gup_matrix cl_float*
#define gup_kernel cl_int

#include "gupdevice.h"
#include "gupmem.h"
#include "gupkernel.h"

void gupClean() {
	int i;
	for(i=0;i<gupKernelCount;i++) {
		clReleaseKernel(gupKernels[i]);
	}
	free(gupKernels);
	free(gupKernelNames);
	//for(int i=0;i<gupMemCount;i++) {
	//	
	//}
	//free(gupMem);
	clReleaseProgram(gupProgram);
	clReleaseCommandQueue(gupCmdQueue);
	clReleaseContext(gupContext);
}

cl_mem newReadFloatBuffer(cl_uint size, cl_float* data){
	cl_mem newBuffer = clCreateBuffer(gupContext, CL_MEM_READ_ONLY|CL_MEM_COPY_HOST_PTR, 
									sizeof(cl_float)*size, data, NULL);
	return newBuffer;
}

cl_mem newWriteFloatBuffer(cl_uint size){
	cl_mem newBuffer = clCreateBuffer(gupContext, CL_MEM_WRITE_ONLY, 
									sizeof(cl_float)*size, NULL, NULL);
	return newBuffer;
}

void readFloatBuffer(cl_mem source, cl_int size, cl_float* destination){
	// read the output back to host memory
	cl_int err;
	err = clEnqueueReadBuffer(gupCmdQueue, source, CL_TRUE, 0, sizeof(cl_float)*size, 
								  destination, 0, NULL, NULL);
	if (err != CL_SUCCESS) {
		printf("Error enqueuing read buffer command. Error Code=%d\n",err);
		exit(1);
	}
}

gup_matrix newMatrix(int size){
	gup_matrix mat;
	mat = malloc(sizeof(cl_float) * size);
	return mat;
}

#endif
