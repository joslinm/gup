#Compiler

import grammar
import visitors	

class Compiler(object):
	def __init__(self, input_file, output_file):
		self.input_file = input_file
		self.output_file = output_file
	def compile(self):
		tokens = grammar.file_input.parseFile(self.input_file)
		pl = visitors.TranslateVisitor()
		tokens[0].accept(pl)
		
		f = open(self.output_file + '.c', 'w')
		for x in pl.tokens:
			f.write(x)

		if len(pl.kernels) > 0:
			f = open('kernels.cl', 'w')
			for x in pl.kernels:
				f.write(x)
			return True
		else:
			return False
		
