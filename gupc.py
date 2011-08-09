#!/usr/bin/python27
import sys
import subprocess
import os

dir = os.getcwd()
cl_lib = dir + 'opencl/lib/'
cl_inc = dir + 'opencl/include'

os.chdir(dir + '/scanner')
from scanner import compiler

inputGup = ""
inputFile = ""
outputFile = "gup.out"
	
for i in range(1, len(sys.argv)):
	if sys.argv[i] == "-o": #Set output filename
		output = sys.argv[i + 1]
		i += 1
	elif inputGup == "":
		inputGup = sys.argv[i]
	elif inputFile == "": #Set input filename
		inputFile ='translated/' +  sys.argv[i]
	elif outputFile == 'gup.out':
		outputFile = 'translated/' + sys.argv[i]
	else:
		print "Invalid argument '" + sys.argv[i] + "'"


piler = compiler.Compiler(inputGup, inputFile)
kernel = piler.compile()

if (kernel):
	subprocess.check_call(['gcc', inputFile, '-o', outputFile, 
		'-lOpenCL', '-L%s' % cl_lib, '-l%s' % cl_inc])
	subprocess.check_call(["./" + outputFile])
else:
	subprocess.check_call(['gcc', inputFile, '-o', outputFile])
	subprocess.check_call(["./" + outputFile])
