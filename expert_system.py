import sys

from collections import deque

from parsing import Inputs


def main(argv):

	try:
		with open(argv[1], 'r') as file:
			lines = file.readlines()
	except IndexError as e:
		print("Please provide a valid file as argument.")
		sys.exit(0)

	inputs = Inputs()
	inputs.parse_lines(lines)
	inputs.build_trees()
	inputs.set_initial_facts()
	print(inputs.queries_list)

	print("====== before ======")
	for e, v in inputs.elements.items():
		print("key : {}".format(e))
		print("- status : {}".format(v.status))
		print("- rules : {}".format(v.rules))
		print("- proved : {}\n".format(v.proved))

	inputs.solve_queries()
	print("====== After ======")
	for e, v in inputs.elements.items():
		print("key : {}".format(e))
		print("- status : {}".format(v.status))
		print("- rules : {}".format(v.rules))
		print("- proved : {}\n".format(v.proved))

	for c in inputs.queries_list:
		c_elem = inputs.elements[c]
		if c_elem.proved and c_elem.status:
			print(f"{c} is True")
		elif c_elem.proved and not c_elem.status:
			print(f"{c} is False")
		else:
			print(f"{c} is Undetermined")


	return None


if __name__ == "__main__":
	main(sys.argv)