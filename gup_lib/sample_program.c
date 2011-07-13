// gcc sample_program.c -o sample_program -lOpenCL && ./sample_program

#include "gupstd.c"

#define BLOCK_SIZE 8

int main() {
	// const width = 32, height = 32
	const int width = 32;
	const int height = 32;
	
	printf("Initializing matrices...");
	// inputMatrix1 = newMatrix(width*height)
	// inputMatrix2 = newMatrix(width*height)
	// multMatrix = newMatrix(width*height)
	// transMatrix = newMatrix(width*height)
	gup_matrix inputMatrix1 = newMatrix(width*height);
	gup_matrix inputMatrix2 = newMatrix(width*height);
	gup_matrix multMatrix = newMatrix(width*height);
	gup_matrix multMatrix2 = newMatrix(width*height);
	///gup_matrix transMatrix = newMatrix(width*height);
	// for i=0 to width*height:
	//     inputMatrix1[i] = i / 100.0f;
	//     inputMatrix2[i] = i / 100.0f;
	//     multMatrix[i] = 0;
	//     transMatrix[i] = 0;
	int i;
	for(i=0;i<width*height;i++) {
		inputMatrix1[i] = i / 100.0f;
		inputMatrix2[i] = i / 100.0f;
		multMatrix[i] = 0;
		multMatrix2[i] = 0;
		///transMatrix[i] = 0;
	}
	printf("done\n");
	
	printf("Initializing gup for CPU...");
	// initCpu()
	gupInit(CL_DEVICE_TYPE_CPU);
	// input_buffer1 = newReadFloatBuffer(width*height, inputMatrix1)
	// input_buffer2 = newReadFloatBuffer(width*height, inputMatrix2)
	// output_buffer = newWriteFloatBuffer(width*height)
	cl_mem input_buffer1 = newReadFloatBuffer(height*width, inputMatrix1);
	cl_mem input_buffer2 = newReadFloatBuffer(height*width, inputMatrix2);
	cl_mem output_buffer = newWriteFloatBuffer(height*width);
	// global = [width, height]
	// local = [8, 8]
	size_t global[2] = {width, height};
	size_t local[2] = {BLOCK_SIZE, BLOCK_SIZE};
	printf("done\n");
	
	printf("Preparing kernel and program...");
	// initProgram()
	/// Perhaps we could compile all kernels to a single cl file
	/// that will always be the same and load them here before the program
	gupLoadKernel("sample_kernel.cl");
	gupCreateProgram();
	/// All the names of the kernels can be thrown into generated
	/// function calls like this, then after it is complete
	/// the source file will be freed from memory
	/// Maybe there can be an array of kernels or something...
	cl_kernel kernel = gupCreateKernel("multMatrixSimple");
	cl_kernel kernel2 = gupCreateKernel("multMatrix");
	free(gupKernelSrc);
	
	/// Something needs to be done about setting kernel args
	/// not sure what we will do in this situation.
	/// Maybe we will just generate this based off what was in
	/// the gup kernel function, for each kernel
	cl_int err;
	if (clSetKernelArg(kernel, 0, sizeof(cl_mem), &output_buffer) ||
		clSetKernelArg(kernel, 1, sizeof(cl_mem), &input_buffer1) ||
		clSetKernelArg(kernel, 2, sizeof(cl_mem), &input_buffer2) ||
		clSetKernelArg(kernel, 3, sizeof(cl_uint), &width) ||
		clSetKernelArg(kernel, 4, sizeof(cl_uint), &height) != CL_SUCCESS) {
		printf("Unable to set kernel arguments. Error Code=%d\n",err);
		exit(1);
	}
	if (clSetKernelArg(kernel2, 0, sizeof(cl_mem), &output_buffer) ||
		clSetKernelArg(kernel2, 1, sizeof(cl_mem), &input_buffer1) ||
		clSetKernelArg(kernel2, 2, sizeof(cl_mem), &input_buffer2) ||
		clSetKernelArg(kernel2, 3, sizeof(cl_uint), &width) ||
		clSetKernelArg(kernel2, 4, sizeof(cl_uint), &height) != CL_SUCCESS) {
		printf("Unable to set kernel arguments. Error Code=%d\n",err);
		exit(1);
	}
	printf("done\n");
	
	printf("Enqueue-ing and running kernel...");
	/// Assuming we make an array of kernels to run, 0 is the first kernel
	// runRangeKernel(0, 2, global, local)
	gupEnqueue2DRangeKernel(kernel, global, local);
	gupFinish(); // Wait until kernel completes
	printf("done\n");
	
	printf("Reading output data...");
	/// This could actually be remembered and generated here
	/// rather than having the following line of code, i think
	// multMatrix = readFloatBuffer(output_buffer, width*height)
	readFloatBuffer(output_buffer, width*height, multMatrix);
	printf("done\n");
	
	printf("Enqueue-ing and running optimized kernel...");
	/// Assuming we make an array of kernels to run, 1 is the second kernel
	// runRangeKernel(1, 2, global, local)
	gupEnqueue2DRangeKernel(kernel2, global, local);
	gupFinish(); // Wait until kernel completes
	printf("done\n");
	
	printf("Reading output data...");
	// multMatrix = readFloatBuffer(output_buffer, width*height)
	readFloatBuffer(output_buffer, width*height, multMatrix2);
	printf("done\n");
	
	printf("Saving matrix to file...");
	// file = open("matrix_output.txt")
	// for y=0 to height:
	//     for x=0 to width:
	//         write(file, multMatrix[y*width+x] + ", ")
	//     writeln(file)
	int x, y;
	FILE*file = fopen("matrix_output.txt","w");
	fprintf(file, "Simple Multiplication:\n");
	for(y=0;y<height;y++) {
	   for(x=0;x<width;x++) fprintf(file, "%.2f, ",multMatrix[y*height+x]);
	   fprintf(file, "\n");
	}
	fprintf(file, "\nOptimized Multiplication:\n");
	for(y=0;y<height;y++) {
	   for(x=0;x<width;x++) fprintf(file, "%.2f, ",multMatrix2[y*height+x]);
	   fprintf(file, "\n");
	}
	printf("done\n");
	
	printf("Cleaning up...");
	/// Automatically thrown in at end of generated function?
	clReleaseMemObject(input_buffer1);
	clReleaseMemObject(input_buffer2);
	clReleaseMemObject(output_buffer);
	clReleaseKernel(kernel);
	gupClose();
	free(inputMatrix1);
	free(inputMatrix2);
	free(multMatrix);
	free(multMatrix2);
	fclose(file);
	printf("done\n");
	
	printf("END OF LINE\n");
	
	return 0;
}
