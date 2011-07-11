#include "gupstd.c"
#define BLOCK_SIZE 8

int main() {
	const int width = 1024;
	const int height = 1024;
	
	// OpenCL host variables
	cl_kernel kernel;
	cl_mem input_buffer1, input_buffer2, output_buffer;
	size_t global[2];
	size_t local[2];
	
	printf("Initializing matrices...");

	cl_float* inputMatrix1 = newMatrix(width*height);
	cl_float* inputMatrix2 = newMatrix(width*height);
	cl_float* results = newMatrix(width*height);
	cl_uint i;
	for(i=0;i<width*height;i++) {
		inputMatrix1[i] = i;
		inputMatrix2[i] = i;
		results[i] = 0;
	}
	printf("done\n");
	
	printf("Initializing gup...");
	gupInit(CL_DEVICE_TYPE_CPU);
	printf("done\n");
	
	printf("Preparing kernel and program...");
	gupLoadKernel("sample_kernel.cl");
	
	input_buffer1 = readFloatBuffer((cl_uint)height*width, inputMatrix1);
	input_buffer2 = readFloatBuffer((cl_uint)height*width, inputMatrix2);
	output_buffer = writeFloatBuffer((cl_uint)height*width);
	
	cl_int err;
	// set the global & local work size
	global[0]= width;
	global[1]= height;
	local[0]=BLOCK_SIZE;
	local[1]=BLOCK_SIZE;
	
	gupCreateProgram();
	
	kernel = gupCreateKernel("multMatrixSimple");
	
	// set the kernel arguments
	if ( clSetKernelArg(kernel, 0, sizeof(cl_mem), &output_buffer) ||
         clSetKernelArg(kernel, 1, sizeof(cl_mem), &input_buffer1) ||
         clSetKernelArg(kernel, 2, sizeof(cl_mem), &input_buffer2) ||
         clSetKernelArg(kernel, 3, sizeof(cl_uint), &width) ||
         clSetKernelArg(kernel, 4, sizeof(cl_uint), &height) != CL_SUCCESS) {
		printf("Unable to set kernel arguments. Error Code=%d\n",err);
		exit(1);
	}
	printf("done\n");
	
	printf("Enqueue-ing and running kernel...");
	// Enqueue the kernel object with 
	// Dimension size = 2, 
	// global worksize = global, 
	// local worksize = local
	// No event wait list
	err = clEnqueueNDRangeKernel(gupCmdQueue, kernel, 2, NULL, global, local, 0, NULL, NULL);
	if (err != CL_SUCCESS) {
		printf("Unable to enqueue kernel command. Error Code=%d\n",err);
		exit(1);
	}

	// wait for the command to finish
	clFinish(gupCmdQueue);
	printf("done\n");
	
	printf("Reading output data...");
	// read the output back to host memory
	err = clEnqueueReadBuffer(gupCmdQueue, output_buffer, CL_TRUE, 0, sizeof(cl_float)*width*height, results, 0, NULL, NULL);
	if (err != CL_SUCCESS) {
		printf("Error enqueuing read buffer command. Error Code=%d\n",err);
		exit(1);
	}
	printf("done\n");
	
	printf("Cleaning up...");
	// clean up
	clReleaseMemObject(input_buffer1);
	clReleaseMemObject(input_buffer2);
	clReleaseMemObject(output_buffer);
	clReleaseProgram(gupProgram);
	clReleaseKernel(kernel);
	clReleaseCommandQueue(gupCmdQueue);
	clReleaseContext(gupContext);
	printf("done\n");
	
	// print out the transposed matrix 
	printf("Saving matrix to file...");
	int x, y;
	FILE*file = fopen("matrix_output.txt","w");
	for(y=0;y<height;y++) {
	   for(x=0;x<width;x++) {
	      fprintf(file, "%.2f , ",results[y*height+x]);
	   }
	   fprintf(file, "\n");
	}
	printf("done\n");
	
	// Get rid of all that shit
	free(gupKernelSrc);
	free(inputMatrix1);
	free(inputMatrix2);
	free(results);
	
	printf("END OF LINE\n");
	
	// GTFO
	return 0;
}
