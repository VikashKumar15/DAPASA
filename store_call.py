import networkx as nx

def get_proper(str):
	if str:
		str = str.replace('/', '.').strip(';')  
	result = []
	dict = {'V' : 'void', 'Z' : 'boolean', 'C' : 'char',
					'B' : 'byte', 'S' : 'short', 'I' : 'int',
					'J' : 'long', 'F' : 'float', 'D' : 'double'}
	list_len = 0
	if str:
		list = str.split(';')
		list_len = len(list)
	for j in range(list_len):
		if len(list[j]) == 0:
			result.append(list[j])
		elif len(list[j]) == 1:
			if list[j] in dict:
				result.append(dict[list[j]])
		else:
			length = len(list[j])
			brack = 0
			for i in range(length):
				if list[j][i] == 'L':
					if brack > 0:
						result.append(list[j][i + 1:] + '[]' * brack)
						brack = 0
					else:
						result.append(list[j][i + 1:])
					break
				elif list[j][i] == '[':
					brack += 1
				else:
					if brack > 0:
						if list[j][i] in dict:
							result.append(dict[list[j][i]] + '[]'*brack)
							brack = 0
					else:
						if list[j][i] in dict:
							result.append(dict[list[j][i]])
	return result

def get_proper_caller(caller_sign):
	caller_method, x = caller_sign.split('(')
	caller_args, caller_ret = x.split(')')
	return caller_method, ','.join(get_proper(caller_args)), get_proper(caller_ret)[0]
	
def get_proper_callee(callee_sign):
	l = callee_sign.split(';->')
	if (len(l) == 2):
		callee_class, x = callee_sign.split(';->')
		callee_method, callee_args, callee_ret = get_proper_caller(x)
		return callee_class[1:].replace('/', '.'), callee_method, callee_args, callee_ret

def save_call(smali_file, graph):
	f = open(smali_file, 'r')
	caller_class = ''
	for line in f:
		if not caller_class:
			caller_class = line.split()[-1][1:-1].replace('/', '.')
		if (line[:7] == '.method'):
			caller_sign = line.split()[-1]
			caller_method, caller_args, caller_return = get_proper_caller(caller_sign)
		elif 'invoke-' in line:
			callee_sign = line.split()[-1]
			l = get_proper_callee(callee_sign)
			if l:
				callee_class, callee_method, callee_args, callee_return = l
				caller = '<{}: {} {}({})>'.format(caller_class,caller_return,caller_method,caller_args)
				callee = '<{}: {} {}({})>'.format(callee_class,callee_return,callee_method,callee_args)
				if not graph.has_node(caller):
					graph.add_node(caller)
				if not graph.has_node(callee):
					graph.add_node(callee)
				graph.add_edge(caller, callee)
	f.close()
