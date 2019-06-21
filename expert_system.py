import sys

from collections import deque

from parsing import Inputs


def main(argv):

	try:
		with open(argv[1], 'r') as file:
			lines = file.readlines()
	except Exception as e:
		print(f"{e} : Please provide a valid file as argument.")
		sys.exit(0)

	inputs = Inputs()
	inputs.parse_lines(lines)
	inputs.build_trees()
	inputs.set_initial_facts()
	inputs.check_query_list()
	inputs.check_trees()
	inputs.solve_queries()
	

	for c in inputs.queries_list:
		c_elem = inputs.elements[c]
		if c_elem.value not in inputs.facts_list and c_elem.undetermined:
			print(f"{c} is Undetermined")
		elif c_elem.status:
			print(f"{c} is True")
		elif not c_elem.status:
			print(f"{c} is False")


	return None


if __name__ == "__main__":
	main(sys.argv)