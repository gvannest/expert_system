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
		print("value.status : {}\n".format(v.status))
		print("value.rules : {}\n".format(v.rules))

	inputs.solve_queries()
	print("====== After ======")
	for e, v in inputs.elements.items():
		print("key : {}".format(e))
		print("value.status : {}\n".format(v.status))
		print("value.rules : {}\n".format(v.rules))


	return None


if __name__ == "__main__":
	main(sys.argv)