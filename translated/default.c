#include <gupstd.h>
#define BLOCK_SIZE 8
int main() {
gupKernelCount = 1;
gupKernelNames = (char**) malloc(sizeof(int*) * gupKernelCount);
gupKernelNames[0] = "kernely";
gupInitDevice();
gupInitKernels();

const int width = 32;
const int height = 32;
	
printf("Initializing matrices...");
gup_matrix inputMatrix1 = newMatrix(width*height);
gup_matrix inputMatrix2 = newMatrix(width*height);
gup_matrix multMatrix = newMatrix(width*height);
gup_matrix multMatrix2 = newMatrix(width*height);
int i;
for(i=0;i<width*height;i++) {
	inputMatrix1[i] = i / 100.0f;
	inputMatrix2[i] = i / 100.0f;
	multMatrix[i] = 0;
	multMatrix2[i] = 0;
}
	
printf("Memory stuff...");

cl_mem input_buffer1 = newReadFloatBuffer(height*width, inputMatrix1);
cl_mem input_buffer2 = newReadFloatBuffer(height*width, inputMatrix2);
cl_mem output_buffer = newWriteFloatBuffer(height*width);
size_t global[2] = {width, height};
size_t local[2] = {BLOCK_SIZE, BLOCK_SIZE};
	
cl_int err;
for(i=0;i<gupKernelCount;i++) {
	if (clSetKernelArg(gupKernels[i], 0, sizeof(cl_mem), &output_buffer) ||
		clSetKernelArg(gupKernels[i], 1, sizeof(cl_mem), &input_buffer1) ||
		clSetKernelArg(gupKernels[i], 2, sizeof(cl_mem), &input_buffer2) ||
		clSetKernelArg(gupKernels[i], 3, sizeof(cl_uint), &width) ||
		clSetKernelArg(gupKernels[i], 4, sizeof(cl_uint), &height) != CL_SUCCESS) {
		printf("Unable to set kernel arguments. Error Code=%d",err);
		exit(1);
	}
}

clReleaseMemObject(input_buffer1);
clReleaseMemObject(input_buffer2);
clReleaseMemObject(output_buffer);

free(inputMatrix1);
free(inputMatrix2);
free(multMatrix);
free(multMatrix2);
	
inputMatrix1 = newMatrix(width*height);
inputMatrix2 = newMatrix(width*height);
multMatrix = newMatrix(width*height);
multMatrix2 = newMatrix(width*height);

for(i=0;i<width*height;i++) {
	inputMatrix1[i] = i / 100.0f;
	inputMatrix2[i] = i / 100.0f;
	multMatrix[i] = 0;
	multMatrix2[i] = 0;
}
	
input_buffer1 = newReadFloatBuffer(height*width, inputMatrix1);
input_buffer2 = newReadFloatBuffer(height*width, inputMatrix2);
output_buffer = newWriteFloatBuffer(height*width);
gupEnqueue2DRangeKernel("kernely", global, local);
gupFinish();
readFloatBuffer(output_buffer, width*height, multMatrix)
;

for (int z = 0; z < width*height; z++) {
printf("%f", multMatrix[z]);
}

clReleaseMemObject(input_buffer1);
clReleaseMemObject(input_buffer2);
clReleaseMemObject(output_buffer);

free(inputMatrix1);
free(inputMatrix2);
free(multMatrix);
free(multMatrix2);
gupClean();
 return 0;
}