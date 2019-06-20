import sys

from collections import deque

from settings import *
from tokens import Element, Operator


class Trees:
	"""Class containing the detailled information for each tree constructed from each rules in the inputs file
	"""
	def __init__(self, value, str_value):
		self.value = value
		self.str_value = str_value
		self.imply_nb = 0
		self.elements_nb = 0
		self.operator_nb = 0
		self.element_proved = []

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
		self.trees = []
		self.elements = {}


	def parse_lines(self, lines):
		
		facts = 0
		queries = 0
		for e in lines:
			line = e.strip()
			if line:
				if line[0] == '#' or line[0] == '\n':
					continue
				elif line[0] == '=':
					facts = 1
					if queries == 0:
						self.facts_list.append(line.split('#')[0].strip()[1:])
					else :
						print(f"Error : Facts in the input are stated after the queries.")
						sys.exit(0)
				elif line[0] == '?':
					queries = 1
					self.queries_list.append(line.split('#')[0].strip()[1:])
				else:
					if facts == 0 and queries == 0:
						self.rules_list.append(line.split('#')[0].strip())
					else :
						print(f"Error : Rules in the input are stated after the facts or queries.")
						sys.exit(0)
		if facts == 1:
			self.facts_list = [c for c in self.facts_list[0]]
		else:
			print(f"Error : Facts were not stated.")
			sys.exit(0)
		if queries == 1:
			self.queries_list = [c for c in self.queries_list[0]]
		else:
			print(f"Error : Queries were not stated.")
			sys.exit(0)

		return None


	def	build_trees(self):

		for rule in self.rules_list:
			output_queue = deque()
			operator_stack = deque()
			set_elements = set()
			for t in rule:
				if t in [' ', '='] or (t == '>' and '<' in rule):
					continue
				if ord(t) in range(ord('A'), ord('A') + 26):
					if t not in self.elements.keys():
						self.elements[t] = Element(t)
					output_queue.append(self.elements[t])
					set_elements.add(self.elements[t])
				else:
					operator = Operator(t)
					if t != '(' and t != ')':
						while (operator_stack and operator_stack[-1].precedence >= operator.precedence
						and operator_stack[-1].value != '('):
							output_queue.append(operator_stack.pop())
						operator_stack.append(operator)
					elif t == '(':
						operator_stack.append(operator)
					elif t == ')':
						while operator_stack and operator_stack[-1].value != '(':
							output_queue.append(operator_stack.pop())
						if not operator_stack:
							print("Error : Parentheses mismatch.")
							sys.exit(0)
						if operator_stack[-1].value == '(':
							operator_stack.pop()
			while operator_stack:
				if operator_stack[-1] == '(' or operator_stack[-1] == ')':
					print("Error : Parentheses mismatch.")
					sys.exit(0)
				output_queue.append(operator_stack.pop())

			self.trees.append(Trees(output_queue, rule))
			for e in set_elements:
				e.rules.append(output_queue)

		return None

	def check_query_list(self):
		for element in self.queries_list:
			if element not in self.elements.keys():
				print(f"Error : Element {element} in query list does not exist.")
				sys.exit(0)

	def check_rule(self, rule):
		consecutive_elements = 0
		consecutive_operators = 0
		for char in rule:
			if char in [' ', '<', '>']:
				continue
			elif char in ['(', '=', ')']:
				consecutive_elements = 0
				consecutive_operators = 0
			elif 'A' <= char <= 'Z':
				consecutive_operators = 0
				consecutive_elements += 1
				if consecutive_elements > 1:
					print(f"Error : Too many consecutives elements in {rule}.")
					sys.exit(0)
			elif char in ['!', '+', '^', '|']:
				consecutive_operators += 1
				consecutive_elements = 0
				if consecutive_operators > 1:
					print(f"Error : Too many consecutives operators in {rule}.")
					sys.exit(0)
			else:
				print(f"Error : Unauthorized token in {rule}.")
				sys.exit(0)
		if consecutive_operators > 0:
			print(f"Error : Extra operator does not match in {rule}.")
			sys.exit(0)
			
			
	def check_trees(self):
		for tree in self.trees:
			self.check_rule(tree.str_value)
			for token in tree.value:
				if isinstance(token, Element):
					tree.elements_nb += 1
				if isinstance(token, Operator) and (token.value == ">" or token.value == "<"):
					tree.imply_nb += 1
					if tree.imply_nb > 1:
						print(f"Error : Too many imply tokens in {tree.str_value}.")
						sys.exit(0)
				if isinstance(token, Operator) and token.value != ">" and token.value != "<":
					tree.operator_nb += 1

	def set_initial_facts(self):
		for f in self.facts_list:
			self.elements[f].status = TRUE

	def solve_queries(self):
		Element.facts_list = self.facts_list
		for q in self.queries_list:
			visited_tree = []
			self.elements[q].solver(visited_tree)










