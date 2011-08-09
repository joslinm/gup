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
	elif inputFile == dir + "/translated/default": #Set input filename
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
	subprocess.check_call(['gcc', inputFile, '-o', outputFile, 
		'-lOpenCL', '-L%s' % cl_lib, '-l%s' % cl_inc, '-l%s' % dir + '/gup_lib',
		'-std=c99'])
	subprocess.check_call(["./" + outputFile])
else:
	subprocess.check_call(['gcc', inputFile, '-o', outputFile])
	subprocess.check_call([outputFile])
