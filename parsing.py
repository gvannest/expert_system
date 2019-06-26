import sys

from collections import deque

from settings import *
from tokens import Element, Operator


class Trees:
    """Class containing the detailed information for each tree constructed from each rule in the input file"""

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
        self.initial_facts = []
        self.queries_list = []
        self.trees = []
        self.elements = {}

    def reinit_elements(self):
        for e in self.elements.values():
            e.undetermined = 0
            e.status = FALSE

    def parsing_error(self, message):
        print(message)
        sys.exit(0)

    def parse_lines(self, lines, flag_first):

        rules = 0
        facts = 0
        queries = 0
        queries_list = ''
        self.facts_list = []
        if not flag_first:
            self.reinit_elements()
        for e in lines:
            line = e.strip()
            if line:
                if line[0] == '#' or line[0] == '\n':
                    continue
                elif line[0] == '=':
                    facts = 1
                    if queries == 0:
                        self.facts_list.append(line.split('#')[0].strip()[1:])
                    elif flag_first:
                        self.parsing_error(
                            "Error : Facts in the input are stated after the queries.")
                elif line[0] == '?':
                    queries = 1
                    queries_list = line.split('#')[0].strip()[1:]
                else:
                    if facts == 0 and queries == 0:
                        rules = 1
                        self.rules_list.append(line.split('#')[0].strip())
                    elif flag_first:
                        self.parsing_error(
                            "Error : Rules in the input are stated after the facts or queries.")
        if facts == 1:
            self.facts_list = [c if 'A' <= c <= 'Z' else self.parsing_error(
                f"Error : Token {c} is unauthorized in fact list.") for c in self.facts_list[0]]
        else:
            self.parsing_error("Error : Facts were not stated.")
        if queries == 1:
            for query in queries_list:
                if query not in self.queries_list:
                    self.queries_list.append(query)
        elif flag_first:
            self.parsing_error("Error : Queries were not stated.")
        if rules == 0 and flag_first:
            self.parsing_error("Error : There are no rules in input file.")

        return None

    def check_rule(self):
        prev_char = ''
        for rule in self.rules_list:
            consecutive_elements = 0
            consecutive_operators = 0
            for char in rule:
                if char in [' ']:
                    continue
                elif char in ['<', '>']:
                    consecutive_operators += 1
                elif char in ['(', '=', ')']:
                    consecutive_elements = 0
                    consecutive_operators = 0
                elif 'A' <= char <= 'Z':
                    consecutive_operators = 0
                    consecutive_elements += 1
                    if consecutive_elements > 1:
                        self.parsing_error(
                            f"Error : Too many consecutives elements in {rule}.")
                elif char in ['!', '+', '^', '|']:
                    consecutive_operators += 1
                    consecutive_elements = 0
                    if consecutive_operators > 1:
                        if char != '!':
                            self.parsing_error(
                                f"Error : Too many consecutives operators in {rule}.")
                        elif char == '!' and prev_char in ['+', '^', '|', '>', '<']:
                            continue
                else:
                    self.parsing_error(
                        f"Error : Unauthorized token in {rule}.")
                prev_char = char
            if consecutive_operators > 0:
                self.parsing_error(
                    f"Error : Extra operator does not match in {rule}, rule is incomplete.")

    def build_trees(self):
        for rule in self.rules_list:
            output_queue = deque()
            operator_stack = deque()
            set_elements = set()
            for t in rule:
                if t in [' ', '='] or (t == '>' and '<' in rule):
                    continue
                if 'A' <= t <= 'Z':
                    if t not in self.elements.keys():
                        self.elements[t] = Element(t)
                    output_queue.append(self.elements[t])
                    set_elements.add(self.elements[t])
                elif t in dic_precedences.keys():
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
                            self.parsing_error("Error : Parentheses mismatch.")
                        if operator_stack[-1].value == '(':
                            operator_stack.pop()
                else:
                    self.parsing_error(
                        f"Error : Token {t} is not authorized in {rule}.")

            while operator_stack:
                if operator_stack[-1].value == '(' or operator_stack[-1].value == ')':
                    self.parsing_error("Error : Parentheses mismatch.")
                output_queue.append(operator_stack.pop())

            new_tree = Trees(output_queue, rule)
            self.trees.append(new_tree)
            for e in set_elements:
                e.rules.append(new_tree)

        return None

    def check_query_list(self):
        for element in self.queries_list:
            if element not in self.elements.keys():
                self.parsing_error(
                    f"Error : Element {element} in query list does not exist.")

    def check_trees(self):
        for tree in self.trees:
            for token in tree.value:
                if isinstance(token, Operator) and (token.value == ">" or token.value == "<"):
                    tree.imply_nb += 1
                    if tree.imply_nb > 1:
                        self.parsing_error(
                            f"Error : Too many imply tokens in {tree.str_value}.")
            if tree.imply_nb < 1:
                self.parsing_error(
                    f"Error : No imply token in {tree.str_value}.")

    def set_initial_facts(self):
        for f in self.facts_list:
            self.elements[f].status = TRUE
            self.initial_facts.append(f)

    def solve_queries(self):
        Element.facts_list = self.facts_list
        for elem in self.elements.values():
            elem.undetermined = 0
        for q in self.queries_list:
            visited_tree = []
            self.elements[q].solver(visited_tree)
        for f in self.facts_list:
            visited_tree = []
            self.elements[f].solver(visited_tree)