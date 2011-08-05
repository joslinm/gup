// gup std - Device handler
// TODO MAYBE: Support for multiple GPU devices

// Context, device, and platform
cl_context gupContext;
cl_context_properties gupProperties[3];

cl_platform_id gupPlatform;
cl_uint gupPlatformCount;

cl_device_id gupDevice;
cl_uint gupDeviceCount;

// Init the gup device
void gupInitDevice() {
	cl_int err;
	// Get the platform IDs
	err = clGetPlatformIDs(1, &gupPlatform, &gupPlatformCount);
	if (err != CL_SUCCESS) {
		printf("Unable to get Platform ID. Error Code=%d\n",err);
		exit(1);
	}
	// Attempt to get a GPU device
	err = clGetDeviceIDs(gupPlatform, CL_DEVICE_TYPE_GPU, 1, &gupDevice, &gupDeviceCount);
	if (err != CL_SUCCESS) {
		// If we failed fallback to a CPU device
		err = clGetDeviceIDs(gupPlatform, CL_DEVICE_TYPE_CPU, 1, &gupDevice, &gupDeviceCount);
		if (err != CL_SUCCESS) {
			printf("Unable to get Device ID. Error Code=%d\n",err);
			exit(1);
		}
	}
	// Put the properties in here to give to the context
	gupProperties[0]= CL_CONTEXT_PLATFORM;
	gupProperties[1]= (cl_context_properties) gupPlatform;
	gupProperties[2]= 0;
	// Finally create the context with these properties
	gupContext = clCreateContext(gupProperties, 1, &gupDevice, NULL, NULL, &err);
	if (err != CL_SUCCESS) {
		printf("Unable to create context. Error Code=%d\n",err);
		exit(1);
	}
	// Let's put the command queue in here too for now, dunno where else to go
	//gupCmdQueue = clCreateCommandQueue(gupContext,gupDevice, 0, &err);
	//if (err != CL_SUCCESS) {
	//	printf("Unable to create command queue. Error Code=%d\n",err);
	//	exit(1);
	//}
}
