
#include "gupstd.h"

int main() {
	gupKernelCount = 1;
	gupKernelNames = (char**) malloc(sizeof(int*) * gupKernelCount);
	gupKernelNames[0] = "xor_encrypt";
	gupInitDevice();
	gupInitKernels();
	
	printf("Reading file");
	int key_size = 13, data_size;
	char key[13] = "Hello World!";
	char* inData;
	
	FILE* inFile = fopen(argv[1],"rb");
	fseek(inFile, 0L, SEEK_END);
	data_size = ftell(inFile);
	rewind(inFile);
	inData = malloc(data_size * sizeof(char));
	fread(inData,1,data_size,inFile);
	fclose(inFile);
	
	cl_mem memKey = newReadFloatBuffer(key_size, key);
	cl_mem memIn = newReadFloatBuffer(data_size, inData);
	cl_mem memOut = newWriteFloatBuffer(data_size);
	size_t global[2] = {key_size, data_size};
	size_t local[2] = {8,8};
	printf("done\n");
	
	cl_int err;
	if (clSetKernelArg(gupKernels[0], 0, sizeof(cl_mem), &memKey) ||
		clSetKernelArg(gupKernels[0], 1, sizeof(cl_mem), &memIn) ||
		clSetKernelArg(gupKernels[0], 2, sizeof(cl_mem), &memOut) ||
		clSetKernelArg(gupKernels[0], 3, sizeof(cl_uint), &) ||
		clSetKernelArg(gupKernels[0], 4, sizeof(cl_uint), &height) != CL_SUCCESS) {
		printf("Unable to set kernel arguments. Error Code=%d\n",err);
		exit(1);
	}
	
	printf("Enqueue-ing and running kernel...");
	gupEnqueue2DRangeKernel(gupKernels[0], global, local);
	readFloatBuffer(memOut, data_size, outData);
	printf("done\n");
	
	printf("Saving output file...");
	FILE*file = fopen("output.txt","wb");
	fwrite(outData,1,data_size,file);
	fclose(file);
	printf("done\n");
	
	printf("Cleaning up...");
	clReleaseMemObject(memKey);
	clReleaseMemObject(memIn);
	clReleaseMemObject(memOut);
	free(inData);
	free(outData);
	gupClean();
	printf("done\n");
	return 0;
}
