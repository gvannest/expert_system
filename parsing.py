from settings import *
from tokens import Element, Operator, LogicOperator

class Inputs:
	"""Class containing our inputs : it parses the lines from the text file and group them into three lists:
		- a list with the rules
		- a list with the facts
		- a list with the queries

		It also builds the AST (Abstract Syntax Tree)
	"""
	def __init__(self):
		self.rules_list = []
		self.facts_list = []
		self.queries_list = []
		self.nodes = set()

	def parse_lines(self, lines):

		for e in lines:
			line = e.strip()
			if line:
				if line[0] == '#' or line[0] == '\n':
					continue
				elif line[0] == '=':
					self.facts_list.append(line.split('#')[0].strip()[1:])
				elif line[0] == '?':
					self.queries_list.append(line.split('#')[0].strip()[1:])
				else:
					self.rules_list.append(line.split('#')[0].strip())

		return None

	#
	# def parse_nodes(self):
	# 	"""Parse la liste de regles (self.rules_list) et retourne un ensemble (set) contenant tous les facts
	# 	du graphe.
	# 	"""
	#
	# 	expression = self.rules_list[0]
	# 	list_ascii = [x + ord('A') for x in range(ord('Z') - ord('A'))]
	# 	i = 0
	# 	position = 'left'
	# 	for c in expression:
	# 		if c.isspace():
	# 			continue
	# 		if c in list_ascii:



