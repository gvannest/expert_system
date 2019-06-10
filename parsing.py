from tokens import Token, Fact, EOF, Connective, Logic

class Inputs:


	def __init__(self, rules_list=None, facts_list=None, queries_list=None):
		self.rules_list = rules_list
		self.facts_list = facts_list
		self.queries_list = queries_list
		if rules_list:
			self.nodes = self.parse_nodes()


	def parse_nodes(self):
		"""Parse la liste de regles (self.rules_list) et retourne un ensemble (set) contenant tous les facts
		du graphe.
		"""

		expression = self.rules_list[0]
		list_ascii = [x + ord('A') for x in range(ord('Z') - ord('A'))]
		i = 0
		position = 'left'
		for c in expression:
			if c.isspace():
				continue
			if c in list_ascii:



