#!/usr/bin/python27
import sys
import subprocess
import os
from scanner import compiler

dir = os.getcwd()
cl_lib = dir + '/opencl/lib/'
cl_inc = dir + '/opencl/include'

inputGup = ""
inputFile = dir + "/translated/default"
outputFile = dir + "/translated/gupout"
	
for i in range(1, len(sys.argv)):
	if sys.argv[i] == "-o": #Set output filename
		output = sys.argv[i + 1]
		i += 1
	elif inputGup == "":
		inputGup = sys.argv[i]
	elif inputFile == dir + "/translated/default":
		inputFile ='/translated/' +  sys.argv[i]
	elif outputFile == dir + '/translated/gup.out':
		outputFile = '/translated/' + sys.argv[i]
	else:
		print "Invalid argument '" + sys.argv[i] + "'"

if not os.path.exists(inputGup):
	if not '.gup' in inputGup:
		if os.path.exists(dir + '/test_code/' + inputGup + '.gup'):
			inputGup = dir + '/test_code/' + inputGup + '.gup'
	
piler = compiler.Compiler(inputGup, inputFile)
kernel = piler.compile()

if (kernel):
	subprocess.check_call(['gcc', inputFile + '.c', '-o', outputFile, 
		'-lOpenCL', '-L%s' % cl_lib, '-I%s' % cl_inc, '-I%s' % dir + '/gup_lib',
		'-std=c99'])
	subprocess.check_call([outputFile])
else:
	try:
		subprocess.check_call(['gcc', inputFile + '.c', '-o', outputFile])
		subprocess.check_call([outputFile])
	except:
		print "Warning: Non-Zero exit code thrown."
