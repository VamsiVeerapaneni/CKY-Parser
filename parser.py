'''
parser.py
Frederik Roenn Stensaeth
11.04.15

A Python implementation of the CKY algorithm for generating parse trees, 
given a CFG (in almost-CNF) and a sentence.
'''

import sys
import os.path

def parser(grammar_filename, sentence):
	"""
	parser() takes a sentence and parses it according to the given grammar.

	@params: filename where grammar is recorded,
			 sentence to be parsed.
	@return: n/a.
	"""
	grammar = getGrammar(grammar_filename)

	backpointer_lst = cky(grammar, sentence)

	printParseTree(backpointer_lst)

def cky(grammar, sentence):
	"""
	ckY() takes sentence and parses it according to the provided grammar.

	@parmas: grammar (dictionary),
			 sentence (string).
	@return: table (results from the algorithm),
			 backpointers for the solution.
	"""
	n = len(sentence)
	# Should we make this a dictionary? --> less memory.
	table = [[None for i in range(n)] for j in range(n)]
	# Should we make this a dictionary? --> less memory.
	backpointers = [[[] for i in range(n)] for j in range(n)]

	for j in range(1, len(sentence)):
		# table[j - 1][j] += {A if A -> words[j] \in gram}
		# Does this actually work or do we need an 'if'?
		for i in range(j - 2, 0):
			for k in range(i + 1, j - 1):
				# table[i][j] += {A if A -> B C \in gram,
				# 				  B \in table[i][k]
				#				  C \in table[k][j]}

	return backpointers[0][n - 1]

def printParseTree(parse_tree, backpointers):
	"""
	printParseTree() takes a parse tree and prints it out.

	@params: parse tree (embeded lists)
	@return: n/a.
	"""
	# Code

def getGrammar(grammar_filename):
	"""
	getGrammar() takes the filename of the file where our grammar rules are
	listed and reads these rules into a dictionary. The dictionary with the
	rules recorded is returned.
	
	Rules:
	- Lines beginning with # are comments.
	- All other lines are of the form X --> Y Z, X --> Y, X --> t.
	- Strings beginning with an uppercase letter are nonterminals.
	- Strings beginning with a lowercase letter are terminals.

	@params: filename of file where the grammar rules are listed.
	@return: dictionary w/ grammar rules.
	"""
	try:
		grammar_text = open(sys.argv[1], 'r')

	except Exception,e:
		# print e
		printError()

	grammar = {}
	# Loops over each line in the grammar file we were given to record the
	# grammar rules.
	for line in grammar_text:
		# We do not want to read the comments.
		if line[0] != '#':
			# Finds the different parts of the rule.
			rule = line.split('->')
			if len(rule) != 2:
				printError(1)

			rule[0] = rule[0].strip()
			rule[1] = rule[1].strip()

			# Makes sure the grammar is of the proper form.
			right_side = rule[1].split()
			if len(right_side) > 2:
				printError(1)

			left_side = rule[0].split()
			if len(left_side) != 1:
				printError(1)
			elif left_side[0][0] != left_side[0][0].higher():
				printError(1)

			# If we have seen a derivation before, we add it to the list.
			if rule[0] in grammar:
				if right_side in grammar[rule[0]]:
					printError(1)
				else:
					grammar[rule[0]] = grammar[rule[0]].append(right_side)
			# If we have not seen a derivation before we need to add it to
			# the dictionary.
			else:
				grammar[rule[0]] = [right_side]

	return grammar

def printError(num):
	"""
	printError() prints out an error message and exits the program.

	@params: number that tells us where the error is coming from.
				0 --> general error.
				1 --> grammar file.
	@return: n/a.
	"""
	if num == 1:
		print('Error in the grammar file provided.')
	else:
		print('Error.')

	print('Usage: $ python3 parser.py <filename for grammar> <sentence>')

def main():
	if len(sys.argv) != 3:
		printError(0)
	elif not os.path.isfile(sys.argv[1]):
		printError(0)

	parser(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
	main()