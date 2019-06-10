import sys

from classes import Inputs

def parse_lines(lines):

	rules_list = []
	facts_list = []
	queries_list = []

	for e in lines:
		line = e.strip()
		if line :
			if line[0] == '#' or line[0] == '\n':
				continue
			elif line[0] == '=':
				facts_list.append(line.split('#')[0].strip()[1:])
			elif line[0] == '?':
				queries_list.append(line.split('#')[0].strip()[1:])
			else:
				rules_list.append(line.split('#')[0].strip())

	return Inputs(rules_list, facts_list, queries_list)


def main(argv):

	try:
		with open(argv[1], 'r') as file:
			lines = file.readlines()
	except IndexError as e:
		print("Please provide a valid file as argument.")
		sys.exit(0)

	inputs = parse_lines(lines)

	print(inputs.rules_list)
	print(inputs.facts_list)
	print(inputs.queries_list)


	return None


if __name__ == "__main__":
    main(sys.argv)