#include <stdlib.h>
#include <stdio.h>
#include "CL/cl.h"

// Typedefs and shit
//#define matrix cl_float*

// Context and device
cl_context gupContext;
cl_context_properties gupProperties[3];

cl_platform_id gupPlatform;
cl_uint gupPlatformCount;

cl_device_id gupDevice;
cl_uint gupDeviceCount;

cl_command_queue gupCmdQueue;

cl_program gupProgram;
char* gupKernelSrc;

void gupGetProperties(cl_uint device_type){
	cl_int err;
	err = clGetPlatformIDs(1,&gupPlatform,&gupPlatformCount);
	if (err != CL_SUCCESS) {
		printf("Unable to get Platform ID. Error Code=%d\n",err);
		exit(1);
	}
	err = clGetDeviceIDs(gupPlatform, device_type, 1, &gupDevice, &gupDeviceCount);
	if (err != CL_SUCCESS) {
		printf("Unable to get Device ID. Error Code=%d\n",err);
		exit(1);
	}
	// context properties list - must be terminated with 0
	gupProperties[0]= CL_CONTEXT_PLATFORM;
	gupProperties[1]= (cl_context_properties) gupPlatform;
	gupProperties[2]= 0;
}

void gupCreateContext(){
	// create context
	cl_int err;
	gupContext = clCreateContext(gupProperties, 1, &gupDevice, NULL, NULL, &err);
	if (err != CL_SUCCESS) {
		printf("Unable to create context. Error Code=%d\n",err);
		exit(1);
	}
}

void gupCreateProgram(){
	cl_int err;
	gupProgram = clCreateProgramWithSource(gupContext, 1 ,(const char **) &gupKernelSrc, NULL, &err);
	if (err != CL_SUCCESS) {
		printf("Unable to create program object. Error Code=%d\n",err);
		exit(1);
	}
	err = clBuildProgram(gupProgram, 0, NULL, NULL, NULL, NULL);
	// If there is a problem say what it is
	if (err != CL_SUCCESS) {
		printf("Build failed. Error Code=%d\n", err);
		size_t len;
		char buffer[4096];
		// get the build log
		clGetProgramBuildInfo(gupProgram, gupDevice, CL_PROGRAM_BUILD_LOG, sizeof(buffer), buffer, &len);
		printf("--- Build Log -- \n %s\n", buffer);
		exit(1);
	}
}

// This should be called at the beginning of every gup program
// It takes care of most of the set up but should be configurable
void gupInit(cl_uint device_type){
	// By default we should attempt to create a gpu context, but if it
	// fails use the CPU. Just gotta find out how to do it.
	gupGetProperties(device_type);
	gupCreateContext();
	
	cl_int err;
	// create command queue 
	gupCmdQueue = clCreateCommandQueue(gupContext,gupDevice, 0, &err);
	if (err != CL_SUCCESS) {
		printf("Unable to create command queue. Error Code=%d\n",err);
		exit(1);
	}
}

cl_mem readFloatBuffer(cl_uint size, cl_float* data){
	cl_mem newBuffer = clCreateBuffer(gupContext, CL_MEM_READ_ONLY|CL_MEM_COPY_HOST_PTR, 
									sizeof(cl_float)*size, data, NULL);
	return newBuffer;
}

cl_mem writeFloatBuffer(cl_uint size){
	cl_mem newBuffer = clCreateBuffer(gupContext, CL_MEM_WRITE_ONLY, 
									sizeof(cl_float)*size, NULL, NULL);
	return newBuffer;
}

// Create a kernel
void gupLoadKernel(const char*fname){
	cl_int err;
	// Open kernel file and get size
	cl_int filelen;
	FILE*fp = fopen(fname,"r");
	fseek(fp, 0L, SEEK_END);
	filelen = ftell(fp);
	rewind(fp);
	// Put the data from the file into memory
	gupKernelSrc = malloc(sizeof(char)*(filelen+1));
	cl_int readlen = fread(gupKernelSrc, 1, filelen, fp);
	if(readlen != filelen) {
	   printf("error reading %s file\n",fname);
	   exit(1);
	}
	fclose(fp);
	// ensure the string is NULL terminated
	gupKernelSrc[filelen+1]='\0';
}

cl_kernel gupCreateKernel(const char*name){
	// Finally create the kernel
	cl_int err;
	cl_kernel newKernel = clCreateKernel(gupProgram, name, &err);
	if (err != CL_SUCCESS) {	
		printf("Unable to create kernel object. Error Code=%d\n",err);
		exit(1);
	}
	//printf("Hello!\n");
	return newKernel;
}

cl_float* newMatrix(int size){
	cl_float* mat;
	mat = malloc(sizeof(cl_float) * size);
	/*
	int i;
	for(i=0;i<size;i++) {
		inputMatrix1[i] = 0;
		inputMatrix2[i] = 0;
		results[i] = 0;
	}
	*/
	return mat;
}
