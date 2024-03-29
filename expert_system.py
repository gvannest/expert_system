import sys
import argparse

from parsing import Inputs
from tokens import Element, Operator
from settings import *


def ft_argparser():
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"filename", type=str, help="Text file with the rule set, facts and queries to be solved")
	parser.add_argument("-i", "--interactive", action="store_true",
						help="Interactive facts mode, where the user can change facts or add new facts")
	parser.add_argument("-u", "--undetermined", action="store_true",
						help="Undetermined mode, where the user can clarify undetermined facts")
	parser.add_argument("-v", "--verbose", action="store_true",
						help="Verbose mode. Outputs the rules leading to a particular conclusion")
	args = parser.parse_args()
	return args


def ft_clear_undetermined(inputs, v):
	"""Function used only if teh Undetermined option is set on.
		Asks the user to clarify an undetermined fact if there exists one.
		Relaunch the solver once an undetermined facts has been clarify
	"""
	for c in inputs.queries_list:
		clearing = 'z'
		c_elem = inputs.elements[c]
		if c_elem.value not in inputs.facts_list and c_elem.undetermined:
			while clearing.lower() != 'y' and clearing.lower() != 'n':
				clearing = input(f"{c} is undetermined. Would you like to set its status? (y/n) : ")
			if clearing.lower() == 'y':
				new_status = 'z'
				while new_status.lower() != 't' and new_status.lower() != 'f':
					new_status = input(f"Please provide a status for {c} (t/f) : ")
				if new_status == 't':
					c_elem.status = TRUE
				elif new_status == 'f':
					c_elem.status = FALSE
				c_elem.undetermined = 0
				inputs.facts_list.append(c_elem.value)
				inputs.solve_queries()
				print_output(inputs, v)
				ft_clear_undetermined(inputs, v)
				break
	return None

def verbose(elem):
	message = ''
	if elem.proved_by == []:
		if elem.status:
			message = f"{elem.value} is a fact."
		else:
			for tree in elem.rules:
				if message != '':
					message += '\n\t'
				message += tree.str_value + " with:"
				for token in tree.value:
					if isinstance(token, Element) and token != elem:
						if token.status == 1:
							message += f"\n\t\t{token.value} is TRUE"
						elif token.undetermined == 1:
							message += f"\n\t\t{token.value} is UNDETERMINED"
						else:
							message += f"\n\t\t{token.value} is FALSE"
			message += f"\n\tSo, according to initial hypothesis {elem.value} is FALSE by design."
	else:
		for tree in elem.proved_by:
			message += tree.str_value
			for token in tree.value:
				if isinstance(token, Element) and token != elem:
					if token.status == 1:
						message += f"\n\t\t{token.value} is TRUE"
					elif token.undetermined == 1:
						message += f"\n\t\t{token.value} is UNDETERMINED"
					else:
						message += f"\n\t\t{token.value} is FALSE"
	return message


def print_output(inputs, v):
	last = inputs.queries_list[-1]
	for c in inputs.queries_list:
		c_elem = inputs.elements[c]
		if v:
			if c_elem.value not in inputs.facts_list and c_elem.undetermined:
				print(f"{c} is UNDETERMINED")
			elif c_elem.status:
				print(f"{c} is TRUE because:\n\t{verbose(c_elem)}")
			elif not c_elem.status:
				print(f"{c} is FALSE because:\n\t{verbose(c_elem)}")
		else:
			if c_elem.value not in inputs.facts_list and c_elem.undetermined:
				print(f"{c} is undetermined")
			elif c_elem.status:
				print(f"{c} is true")
			elif not c_elem.status:
				print(f"{c} is false")


def ft_interactive(inputs, v):
	""" Function which is called only if the Interactive Facts mode is set on.
		Asks the user whether he wants to change initial facts.
		Requests for new_facts and relaunch the solving process.
	"""
	change_facts = ''
	while change_facts.lower() != 'n':
		change_facts = input('Would you like to change the initial facts? (y/n)  ')
		while change_facts.lower() != 'y' and change_facts.lower() != 'n':
			change_facts = input('Would you like to change the initial facts? (y/n)  ')
		if change_facts.lower() == 'y':
			for rule in inputs.rules_list:
				print(rule)
			print(f"Initial facts : {inputs.initial_facts}")
			new_facts = input("Please provide a new set of facts (ex: XYZ) : ")
			new_facts = new_facts.replace(' ', '')
			if new_facts == '':
				new_facts = '='
			else:
				new_facts = '=' + new_facts if new_facts[0] != '=' else new_facts
			inputs.parse_lines([new_facts], 0)
			inputs.set_initial_facts()
			inputs.solve_queries()
			if args.undetermined:
				ft_clear_undetermined(inputs, v)
			print_output(inputs, v)
	return None


def standard_algo(filename, v):

	if not filename.endswith('.txt'):
		print("Error : please provide a valid file, in .txt format.")
		sys.exit(0)
	try:
		with open(filename, 'r') as file:
			lines = file.readlines()
	except Exception as e:
		print(f"{e} : Please provide a valid file as argument.")
		sys.exit(0)

	inputs = Inputs()
	inputs.parse_lines(lines, 1)
	inputs.check_rule()
	inputs.build_trees()
	inputs.set_initial_facts()
	inputs.check_query_list()
	inputs.check_trees()
	inputs.solve_queries()

	print_output(inputs, v)

	return inputs


def main(args):

	inputs = standard_algo(args.filename, args.verbose)

	if args.undetermined:
		ft_clear_undetermined(inputs, args.verbose)
	if args.interactive:
		ft_interactive(inputs, args.verbose)

	return None


if __name__ == "__main__":
	args = ft_argparser()
	main(args)
