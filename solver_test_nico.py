def solve(element, operand = '>'):
	if element.proven_rules != []:
		return element.status
	for rule in element.rules:
		if read_rules(rule, element) is True:
			element.proven_rules.append(rule)
			element.rules.remove(rule)
			return True


def read_rules(element_rules, elements):
	element_queue = deque()
	for rule in element_rules:
		while rule:
			if rule[0] in elements.values():
				element_queue.append(rule.popleft())
			else:
				print(element_queue[0])
				print(element_queue[1])
				sys.exit(0)
				if rule[0] == '+':
					return solve(element_queue[0]) & solve(element_queue[1])
				elif rule[0] == '|':
					return solve(element_queue[0]) | solve(element_queue[1])
				# elif str(rule[0]) == '^':
				# elif str(rule[0]) == '!':

if __name__ == "__main__":
	read_rules(inputs.elements['C'].rules, inputs.elements)