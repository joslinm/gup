#!/usr/bin/python2
import sys
import subprocess

inputFile = ""
outputFile = "gup.out"
	
for i in range(1, len(sys.argv)):
	if sys.argv[i] == "-o": #Set output filename
		output = sys.argv[i + 1]
		i += 1
	elif inputFile == "": #Set input filename
		inputFile = sys.argv[i]
	else:
		print "Invalid argument '" + sys.argv[i] + "'"

subprocess.check_output(['gcc', inputFile, '-o', outputFile, '-lOpenCL'])

subprocess.check_output(["./" + outputFile])

