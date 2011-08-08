'''Visitors

The base class Visitor should be inherited by all other Visitor classes. It will handle 
dispatching & is packaged with the necessary utility methods such as merge
'''

translate_table = {'True' : 'true', 'False': 'false'''}

#General Visitor (Should be inherited)
class Visitor(object):
	def __init__(self):
		self.tokens = []
		self.kernels = []
		self.kernel_stack = []
		self.name_stack = []
		import actions
		self.symbols = actions.symbol_table
		self.functions = actions.functions
		
	#General dispatch method
	def visit(self,*args):
		name = type(args[0]).__name__
		elem = args[0]
		visit_func = self._func(type(elem).__name__)
		visit_func(elem)
		
	#Calls function from its string name
	def _func(self,name):
		f = getattr(self, 'visit_' + name)
		return f
		
	#Going in reverse order coinicides with the stack
	#Fills in any non-str positions from right-left
	def merge(self,element, debug=False):
		l = range(len(element))
		l.reverse()
		for x in l:
			if type(element[x]) != type(''):
				a = self.tokens.pop()
				if debug:
					print "Popping " + a
					
				element[x] = a
		r = ' '.join(element)
		self.tokens.append(r)
		print self.tokens
	def append(self, trailer):
		x = self.tokens.pop()
		x += trailer
		self.tokens.append(x)
	def prepend(self, pre):
		x = self.tokens.pop()
		x = pre + x
		self.tokens.append(x)
	
	#[ROOT]
	def visit_Root(self, element): 
		#(stmt | NEWLINE)*
		pass

	##[STMT]
	def visit_Statement(self, element): 
		#(simple_stmt ^ compound_stmt)
		pass

	### [COMPOUND_STATEMENT] ^ [SIMPLE_STATEMENT]
	def visit_SimpleStatement(self, element):
		#(small_stmt)
		pass
	def visit_CompoundStatement(self, element):
		#(if_stmt | while_stmt | for_stmt | funcdef | classdef | decorated)*
		pass

	####
	#Simple Statement --> 4th level: small_stmt
	####		
	def visit_SmallStatement(self, element):
		pass
		
	####
	#Compound Statement --> 4th level: if|while|for|funcdef|classdef|decorated
	####				
	def visit_IfStatement(self, element):
		pass
	def visit_ForStatement(self, element):
		pass
	def visit_WhileStatement(self, element):
		pass
	def visit_FunctionDeclaration(self, element):
		pass
	def visit_ClassDeclaration(self, element):
		pass
	def visit_DecoratedDeclaration(self, element):
		pass

	####
	#Small Statement --> 5th level: expr_stmt|print_stmt|del_stmt|pass_stmt|flow_stmt|import_stmt
	####
	def visit_ExpressionStatement(self, element):
		pass		
	def visit_PrintStatement(self, element):
		pass		
	def visit_DeleteStatement(self, element):
		pass
	def visit_PassStatement(self, element):
		pass
	def visit_ImportStatement(self, element):
		pass

	###
	#Flow Statement --> pass, break, continue
	###
	def visit_FunctionCall(self, element):
		pass
	def visit_FlowStatement(self, element):
		pass
	def visit_ContinueStatement(self, element):
		pass
	def visit_BreakStatement(self, element):
		pass
	def visit_PassStatement(self, element):
		pass
	def visit_ReturnStatement(self, element):
		pass

	#################################################################
	# # # # # # # # # # # # L O W E R   #   L E V E L S # # # # # # # ## # # # # # # # ## # # # # # 
	#################################################################

	####
	#Compound Statements' 4th level --> test,suite,exprlist, parameters
	#NOTE: Consider turning if test: while test: for x in y: def NAME parameters: into their respective branch classes
	####
	def visit_Suite(self, element): #(small_stmt ^ compound_stmt)
		pass
	def visit_Parameters(self, element):
		pass

	####
	#Test --> COMPARISON --> [EXPRESSION] --> smaller expressions
	####
	def visit_Test(self, element):
		pass	
	def visit_Comparison(self, element):
		pass
	def visit_Expression(self, element):
		pass
	def visit_ArithmeticExpression(self, element):
		pass

	####
	#Atom --> [NAME | NUMBER | STRING]
	####
	def visit_Atom(self, element):
		pass
	def visit_Name(self, element):
		pass
	def visit_String(self, element):
		pass
	def visit_Number(self, element):
		pass

class TranslateVisitor(Visitor):
	import actions
	
	#Visit methods
	def visit_Root(self, element):
		print type(element).__name__
		declarations = ''
		for y,x in self.symbols.iteritems():
			if  1 == x['scope']:
				if not x['declared']:
					if x['type'] == 'char[250]':
						declarations += '%s %s = %s;\n' % (x['type'], y, x['value'])
					else:
						declarations += '%s %s ;\n' % (x['type'], y)
				print declarations
		if len(self.kernels) > 0:
			names = []
			declarations += 'gupKernelCount = %s\n' % len(self.kernel_stack)
			declarations += 'gupKernelNames = (char**) malloc(sizeof(int*) * gupKernelCount);\n'
			for x in self.kernels:
				names.append(self.kernel_stack.pop())
			for x in range(len(names)):
				declarations += 'gupKernelNames[%s] = %s\n' % (x, names[x])
			
			declarations += 'gupInitDevice();\n'
			declarations += 'gupInitKernels();\n'
			
			declarations += '''
const int width = 32;
const int height = 32;
	
printf("Initializing matrices...");
gup_matrix inputMatrix1 = newMatrix(width*height);
gup_matrix inputMatrix2 = newMatrix(width*height);
gup_matrix multMatrix = newMatrix(width*height);
gup_matrix multMatrix2 = newMatrix(width*height);
int i;
for(i=0;i<width*height;i++) {
	inputMatrix1[i] = i / 100.0f;
	inputMatrix2[i] = i / 100.0f;
	multMatrix[i] = 0;
	multMatrix2[i] = 0;
}
	
printf("Memory stuff...");

cl_mem input_buffer1 = newReadFloatBuffer(height*width, inputMatrix1);
cl_mem input_buffer2 = newReadFloatBuffer(height*width, inputMatrix2);
cl_mem output_buffer = newWriteFloatBuffer(height*width);
size_t global[2] = {width, height};
size_t local[2] = {BLOCK_SIZE, BLOCK_SIZE};
	
cl_int err;
for(i=0;i<gupKernelCount;i++) {
	if (clSetKernelArg(gupKernels[i], 0, sizeof(cl_mem), &output_buffer) ||
		clSetKernelArg(gupKernels[i], 1, sizeof(cl_mem), &input_buffer1) ||
		clSetKernelArg(gupKernels[i], 2, sizeof(cl_mem), &input_buffer2) ||
		clSetKernelArg(gupKernels[i], 3, sizeof(cl_uint), &width) ||
		clSetKernelArg(gupKernels[i], 4, sizeof(cl_uint), &height) != CL_SUCCESS) {
		printf("Unable to set kernel arguments. Error Code=%d",err);
		exit(1);
	}
}
'''
				
		if len(declarations) > 0:
			self.tokens.insert(0,declarations)
			if len(self.kernels) > 0:
				self.tokens.insert(0,
				"#include <gupstd.h>\n" +
				"#define BLOCK_SIZE 8\n" +
				"int main() {\n")
				self.tokens.append('gupClean();\n return 0;\n}')
			else:
				self.tokens.insert(0, 
				"#include <stdio.h>\n" + 
				"#include <stdlib.h>\n" +
				"int main() {\n")
				self.tokens.append('}')
				
	def visit_Statement(self,element):
		print type(element).__name__
		print element
		
	def visit_CompoundStatement(self,element):
		print type(element).__name__
		print element
		
	def visit_SimpleStatement(self,element):
		print type(element).__name__
		print element
		
	def visit_SmallStatement(self,element):
		print type(element).__name__
		print element
		
		self.append(';\n')
		
	def visit_Suite(self, element):
		print type(element).__name__
		print element
		print self.tokens
		print self.symbols
		declarations = ''
		for y,x in self.symbols.iteritems():
			if element.hash == x['scope']:
				if not x['declared']:
					if x['type'] == 'char[250]':
						declarations += '%s %s = %s' % (x['type'], y, x['value'])
					declarations += '%s %s ;\n' % (x['type'], y)
					self.symbols[y]['declared'] = True
		
		self.merge(element)
		self.prepend(' {\n%s' % declarations)
		self.append('}\n\n')

	def visit_IfStatement(self, element):
		print type(element).__name__
		print element
		
		self.merge(element)
		
	def visit_ForStatement(self, element):
		print type(element).__name__
		print self.tokens
		print element
		print self.tokens
		
		suite = self.tokens.pop()
		max = self.tokens.pop()
		min = self.tokens.pop()
		definition = self.tokens.pop()
		
		for_branch = 'for (int %s = %s;' % (definition, min)
		for_branch += '%s <= %s;' % (definition, max)
		for_branch += '%s++)' % definition
		for_branch += '\n%s' % suite
		
		self.tokens.append(for_branch)

		
	def visit_WhileStatement(self, element):
		#print type(element).__name__
		pass
	def visit_ExpressionStatement(self, element):
		##e.g. COMPARISON '=' COMPARISON 
		print type(element).__name__
		print element
		print self.tokens
		#
		length = len(element)
		if length % 3 == 0:
			self.name_stack.append(element[0].get_child_str())
			self.merge(element)
			
	def visit_PrintStatement(self, element):
		print type(element).__name__
		print element
		print len(element)
		print len(element) % 2
		
		length = len(element)
		if length == 1:
			pass
		elif length % 2 == 0:
			name_obj = element[1].find_child('Name')
			if name_obj:
				if self.symbols[name_obj[0]]['type'] == 'int':
					element[0] = 'printf("%d"'
					element[0] += ', %s)' % name_obj[0]
					self.tokens.pop() #remove test off the rhs
					self.tokens.append(element[0])
				elif self.symbols[name_obj[0]]['type'] == 'float':
					element[0] = 'printf("%f"'
					element[0] += ', %s)' % name_obj[0]
					self.tokens.pop() #remove test off the rhs
					self.tokens.append(element[0])
			else:
				element[0] = 'printf('
				self.merge(element)
				self.append(')')
	
	def visit_FunctionCall(self, element):
		print type(element).__name__
		print element
		print self.tokens

		import actions
		func = actions.functions[element[0].get_child_str()]
		params = []
		for x in range(func['num_params']):
			params.append(self.tokens.pop())
		params.reverse()
		func_name = self.tokens.pop()
		func_ = '{0}({1})'.format(func_name, ','.join(params))
		
		if func['kernel']:
			kernel_call = '''
clReleaseMemObject(input_buffer1);
clReleaseMemObject(input_buffer2);
clReleaseMemObject(output_buffer);

free(inputMatrix1);
free(inputMatrix2);
free(multMatrix);
free(multMatrix2);
	
inputMatrix1 = newMatrix(width*height);
inputMatrix2 = newMatrix(width*height);
multMatrix = newMatrix(width*height);
multMatrix2 = newMatrix(width*height);

for(i=0;i<width*height;i++) {
	inputMatrix1[i] = i / 100.0f;
	inputMatrix2[i] = i / 100.0f;
	multMatrix[i] = 0;
	multMatrix2[i] = 0;
}
	
input_buffer1 = newReadFloatBuffer(height*width, inputMatrix1);
input_buffer2 = newReadFloatBuffer(height*width, inputMatrix2);
output_buffer = newWriteFloatBuffer(height*width);
gupEnqueue2DRangeKernel("%s", global, local);
gupFinish();
readFloatBuffer(output_buffer, width*height, multMatrix)
''' % func_.strip('();')
		#Have to leave off ending semicolon because small_stmt puts that in
			self.tokens.append(kernel_call)
		else:
			self.tokens.append(func_)
	
	def visit_KernelDeclaration(self, element):
		print type(element).__name__
		print element
		print self.tokens
		#[NAME, STMT]
		stmt = self.tokens.pop()
		name = self.tokens.pop()
		kernel_decl = '''
		__kernel void %s(__global float *output, __global float *inputA, 
							   __global float *inputB, uint widthA, uint widthB)
		'''	 % name						   
		stmt_pre = '''{
	int globalIdx = get_global_id(0);
	int globalIdy = get_global_id(1);
		'''
		
		stmt = stmt_pre + stmt.lstrip(' { \n')
		self.kernels.append(kernel_decl.lstrip(' \t \n') + stmt)
		self.kernel_stack.append(name)
		
	def visit_FunctionDeclaration(self, element):
		print type(element).__name__
		print element
		print self.tokens
		
		if self.functions[self.tokens[0]]['kernel']:
			print "is kernel"
			pass
		else:
			pass#Compute stuff here

	def visit_Test(self, element):
		print type(element).__name__
		print element
		
		
	def visit_Expression(self, element):
		print type(element).__name__
		print element
		
	def visit_ArithmeticExpression(self, element):
		print type(element).__name__
		print element
		
		length = len(element)
		if length == 1:
			pass
		else:
			self.merge(element)
	
	def visit_Power(self, element):
		print type(element).__name__
		print element
		length = len(element)
		
		if(length == 2):
			trailer = self.tokens.pop()
			name = self.tokens.pop()

			if name == 'inputA':
				self.tokens.append(name + ('[globalIdy * widthA + %s]' % trailer))
			elif name == 'inputB':
				self.tokens.append(name + ('[%s * widthB + globalIdx]' % trailer))

			
	def visit_Comparison(self, element):
		print type(element).__name__
		print element
		print len(element)
		length = len(element)

		if length == 1:
			pass
		elif length % 3 == 0:
			self.merge(element)
			self.prepend('(')
			self.append(')')
	
	def visit_Atom(self, element):
		pass
	def visit_Number(self, element):
		print type(element).__name__
		print element
		self.tokens.append(element[0])
	def visit_Name(self, element):
		print type(element).__name__
		print element
		print element.type
		
		if element[0] == 'output':
			self.tokens.append('output[globalIdy * widthA + globalIdx]')
			print self.tokens
		else:
			self.tokens.append(element[0])
	def visit_String(self, element):
		print type(element).__name__
		print element
		
		self.tokens.append(element[0])
	
	


	
