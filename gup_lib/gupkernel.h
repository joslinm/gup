// gup std - Kernel handler

cl_command_queue gupCmdQueue;

cl_program gupProgram;
char* gupKernelSrc;

cl_int gupKernelCount;
cl_kernel* gupKernels;
char** gupKernelNames;

cl_int gupMemCount;
cl_mem* gupMem;

// Load kernel file into memory
void gupLoadKernelFile(const char*fname){
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

void gupCreateProgram(){
	cl_int err;
	gupProgram = clCreateProgramWithSource(gupContext, 1 ,(const char **) &gupKernelSrc, 
										   NULL, &err);
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
		clGetProgramBuildInfo(gupProgram, gupDevice, CL_PROGRAM_BUILD_LOG, 
							  sizeof(buffer), buffer, &len);
		printf("--- Build Log -- \n %s\n", buffer);
		exit(1);
	}
}

cl_kernel gupCreateKernel(const char*name){
	// Finally create the kernel
	cl_int err;
	cl_kernel newKernel = clCreateKernel(gupProgram, name, &err);
	if (err != CL_SUCCESS) {	
		printf("Unable to create kernel object. Error Code=%d\n",err);
		exit(1);
	}
	return newKernel;
}

void gupInitKernels() {
	cl_int err;
	// Start with the command queue
	gupCmdQueue = clCreateCommandQueue(gupContext,gupDevice, 0, &err);
	if (err != CL_SUCCESS) {
		printf("Unable to create command queue. Error Code=%d\n",err);
		exit(1);
	}
	//cl_int num_kernels = n;
	gupKernels = (cl_kernel*) malloc(sizeof(int*) * gupKernelCount);
	//gupKernelNames = names;
	gupLoadKernelFile("kernels.cl");
	gupCreateProgram();
	//gupKernels = malloc(sizeof(ptr) * 
	int i;
	for(i=0;i<gupKernelCount;i++){
		gupKernels[i] = gupCreateKernel(gupKernelNames[i]);
	}
	free(gupKernelSrc);
}

void gupEnqueue2DRangeKernel(cl_kernel kernel, size_t* global, size_t* local) {
	// Enqueue the kernel object
	cl_int err;
	err = clEnqueueNDRangeKernel(gupCmdQueue, kernel, 2, NULL, global, local, 0, NULL, NULL);
	if (err != CL_SUCCESS) {
		printf("Unable to enqueue kernel command. Error Code=%d\n",err);
		exit(1);
	}
}

void gupFinish(){
	clFinish(gupCmdQueue);
}
