// gcc sample_program.c -o sample_program -lOpenCL && ./sample_program

#include <gupstd.h>

#define BLOCK_SIZE 8

int main() {
	/// Thrown at the beginning of the main function
	gupKernelCount = 2;
	gupKernelNames = (char**) malloc(sizeof(int*) * gupKernelCount);
	gupKernelNames[0] = "multMatrixSimple";
	gupKernelNames[1] = "multMatrix";
	gupInitDevice();
	gupInitKernels();

	// const width = 32, height = 32
	const int width = 32;
	const int height = 32;
	
	printf("Initializing matrices...");
	// inputMatrix1 = newMatrix(width*height)
	// inputMatrix2 = newMatrix(width*height)
	// multMatrix = newMatrix(width*height)
	// multMatrix2 = newMatrix(width*height)
	gup_matrix inputMatrix1 = newMatrix(width*height);
	gup_matrix inputMatrix2 = newMatrix(width*height);
	gup_matrix multMatrix = newMatrix(width*height);
	gup_matrix multMatrix2 = newMatrix(width*height);
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
	}
	printf("done\n");
	
	printf("Memory stuff...");
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
	
	/// Something needs to be done about setting kernel args
	/// not sure what we will do in this situation.
	/// Maybe we will just generate this based off what was in
	/// the gup kernel function, for each kernel
	cl_int err;
	for(i=0;i<gupKernelCount;i++) {
		if (clSetKernelArg(gupKernels[i], 0, sizeof(cl_mem), &output_buffer) ||
			clSetKernelArg(gupKernels[i], 1, sizeof(cl_mem), &input_buffer1) ||
			clSetKernelArg(gupKernels[i], 2, sizeof(cl_mem), &input_buffer2) ||
			clSetKernelArg(gupKernels[i], 3, sizeof(cl_uint), &width) ||
			clSetKernelArg(gupKernels[i], 4, sizeof(cl_uint), &height) != CL_SUCCESS) {
			printf("Unable to set kernel arguments. Error Code=%d\n",err);
			exit(1);
		}
	}
	
	printf("Enqueue-ing and running kernel...");
	/// Assuming we make an array of kernels to run, 0 is the first kernel
	// runRangeKernel(0, 2, global, local)
	gupEnqueue2DRangeKernel(gupKernels[0], global, local);
	gupFinish(); // Wait until kernel completes
	/// This could actually be remembered and generated here
	/// rather than having the following line of code, i think
	// multMatrix = readFloatBuffer(output_buffer, width*height)
	readFloatBuffer(output_buffer, width*height, multMatrix);
	printf("done\n");
	
	printf("Enqueue-ing and running optimized kernel...");
	/// Assuming we make an array of kernels to run, 1 is the second kernel
	// runRangeKernel(1, 2, global, local)
	gupEnqueue2DRangeKernel(gupKernels[1], global, local);
	gupFinish(); // Wait until kernel completes
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
	//clReleaseKernel(gupKernels[0]);
	//clReleaseKernel(gupKernels[1]);
	//gupClose();
	free(inputMatrix1);
	free(inputMatrix2);
	free(multMatrix);
	free(multMatrix2);
	fclose(file);
	printf("done\n");
	
	printf("END OF LINE\n");
	
	///Thrown at the end - always
	gupClean();
	return 0;
}
