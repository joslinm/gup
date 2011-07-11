// gcc sample_program.c -o sample_program -lOpenCL && ./sample_program

#include "gupstd.c"

#define BLOCK_SIZE 8

int main() {
	const int width = 32;
	const int height = 32;
	
	printf("Initializing matrices...");
	gup_matrix inputMatrix1 = newMatrix(width*height);
	gup_matrix inputMatrix2 = newMatrix(width*height);
	gup_matrix results = newMatrix(width*height);
	
	int i;
	for(i=0;i<width*height;i++) {
		inputMatrix1[i] = i / 100.0f;
		inputMatrix2[i] = i / 100.0f;
		results[i] = 0;
	}
	printf("done\n");
	
	printf("Initializing gup for CPU...");
	gupInit(CL_DEVICE_TYPE_CPU);
	gup_mem input_buffer1 = newReadFloatBuffer(height*width, inputMatrix1);
	gup_mem input_buffer2 = newReadFloatBuffer(height*width, inputMatrix2);
	gup_mem output_buffer = newWriteFloatBuffer(height*width);
	printf("done\n");
	
	printf("Preparing kernel and program...");
	gupLoadKernel("sample_kernel.cl");
	// set the global & local work size
	size_t global[2] = {width, height};
	size_t local[2] = {BLOCK_SIZE, BLOCK_SIZE};
	
	gupCreateProgram();
	gup_kernel kernel = gupCreateKernel("multMatrixSimple");
	// After all kernels are built free the source from memory
	free(gupKernelSrc);
	
	gup_int err;
	// set the kernel arguments
	if (clSetKernelArg(kernel, 0, sizeof(gup_mem), &output_buffer) ||
		clSetKernelArg(kernel, 1, sizeof(gup_mem), &input_buffer1) ||
		clSetKernelArg(kernel, 2, sizeof(gup_mem), &input_buffer2) ||
		clSetKernelArg(kernel, 3, sizeof(gup_uint), &width) ||
		clSetKernelArg(kernel, 4, sizeof(gup_uint), &height) != CL_SUCCESS) {
		printf("Unable to set kernel arguments. Error Code=%d\n",err);
		exit(1);
	}
	printf("done\n");
	
	printf("Enqueue-ing and running kernel...");
	gupEnqueueRangeKernel(kernel, 2, global, local);
	gupFinish(); // Wait until kernel completes
	printf("done\n");
	
	printf("Reading output data...");
	readFloatBuffer(output_buffer, width*height, results);
	printf("done\n");
	
	printf("Cleaning up...");
	// clean up
	clReleaseMemObject(input_buffer1);
	clReleaseMemObject(input_buffer2);
	clReleaseMemObject(output_buffer);
	clReleaseKernel(kernel);
	gupClose();
	printf("done\n");
	
	// print out the transposed matrix 
	printf("Saving matrix to file...");
	int x, y;
	FILE*file = fopen("matrix_output.txt","w");
	for(y=0;y<height;y++) {
	   for(x=0;x<width;x++) fprintf(file, "%.2f, ",results[y*height+x]);
	   fprintf(file, "\n");
	}
	printf("done\n");
	
	// Get rid of all that shit
	free(inputMatrix1);
	free(inputMatrix2);
	free(results);
	
	printf("END OF LINE\n");
	
	// GTFO
	return 0;
}
