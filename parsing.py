import sys

from collections import deque

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
		self.trees = []
		self.elements = {}


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
		self.facts_list = [c for c in self.facts_list[0]]
		self.queries_list = [c for c in self.queries_list[0]]

		return None


	def	build_trees(self):

		for rule in self.rules_list:
			output_queue = deque()
			operator_stack = deque()
			set_elements = set()
			for t in rule:
				if t in [' ', '=']:
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

			self.trees.append(output_queue)
			for e in set_elements:
				e.rules.append(output_queue)

		return None

	def set_initial_facts(self):
		for f in self.facts_list:
			self.elements[f].status = TRUE
			self.elements[f].proved = 1

	def solve_queries(self):
		for q in self.queries_list:
			visited_tree = []
			if not self.elements[q].proved:
				self.elements[q].solver(visited_tree)









