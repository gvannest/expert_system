import sys

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
	print(inputs.rules_list)

	return None


if __name__ == "__main__":
    main(sys.argv)