
// Simple XOR Encryption
__kernel void
xor_encrypt(__global char *key, __global char *inData, 
		__global float *outData, uint chunkIndex, uint rounds) {
	int keySize = get_global_id(0);
	int dataSize = get_global_id(1);
	int i, k = chunkIndex * keySize;
	for (i = 0; i < keyLength * rounds; i++) {
		if(dataSize <= k + i)break;
		outData[k + i] = inData[k + i] ^ key[i % keySize];
	}
}
