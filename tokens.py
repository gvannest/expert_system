import sys

from collections import deque

from settings import *

class Element:
    """ Class representing an element of our Knowledge Base (such as A, B, C...)"""

    facts_list = []

    def __init__(self, value):
        self.value = value
        self.rules = []
        self.proven_rules = []
        self.proved = 0
        self.status = FALSE
        self.undetermined = 0

    def solver(self, visited_tree):
        for tree in self.rules:
            if tree not in visited_tree:
                visited_tree.append(tree)
                solving_stack = deque()
                for e in tree:
                    if isinstance(e, Element):
                        solving_stack.append(e)
                        e.solver(visited_tree)
                    elif isinstance(e, Operator):
                        e.right = solving_stack.pop()
                        if e.value != '!':
                            e.left = solving_stack.pop()
                        e.eval_expr()
                        solving_stack.append(e)

    def change_status(self, new_status, imply=0):
        if self.value in Element.facts_list:
            if self.status != new_status:
                print(f"Incoherence sur l'element {self.value}")
                sys.exit(0)
        else:
            self.status = new_status
            self.undetermined = 0
            Element.facts_list.append(self.value)


    def __str__(self):
        return f"value : {self.value} - status : {self.status} - proved : {self.proved}"

    def __repr__(self):
        return self.__str__()




class Operator:
    """Class respresenting a comparison operator in our rules (AND, OR, XOR...). """

    facts_list = []

    def __init__(self, value):
        """Object attributes:
                * value [str] : the 'value' of our operator : +, |, ^, !
                * left [Element or Operator] : the left expression of our operator (can be an element or an operator linking two other expressions)
                * right [Element or Operator] : the right branch of our operator
                * status : the status of the expression True, False or Undetermined
        """
        self.value = value
        self.precedence = dic_precedences[self.value]
        self.left = None
        self.right = None
        self.status = FALSE


    def eval_expr(self):
        """
        This functions evaluates the current operator (i.e. expression) given the statuses of its components.
        Hence here we go up the tree.

        Return:
             TRUE or FALSE
        """
        def ft_and():
            return self.left.status & self.right.status

        def ft_or():
            return self.left.status | self.right.status

        def ft_xor():
            return self.left.status ^ self.right.status

        def ft_not():
            return self.right.status ^ 1

        def ft_imply():
            if self.left.status == TRUE:
                if isinstance(self.left, Element):
                    Element.facts_list.append(self.left.value)
                elif isinstance(self.left, Operator):
                    self.left.add_elem_factlist()
                self.right.change_status(TRUE, 1)
            return self.left.status

        def ft_iif():
            if not ft_imply() and self.right.status == TRUE:
                if isinstance(self.right, Element):
                    Element.facts_list.append(self.right.value)
                elif isinstance(self.right, Operator):
                    self.right.add_elem_factlist()
                self.left.change_status(TRUE, 1)
            return self.left.status == self.right.status

        dic_operations = {
            '+' : ft_and,
            '|' : ft_or,
            '^' : ft_xor,
            '!' : ft_not,
            '>' : ft_imply,
            '<': ft_iif,
        }
        self.change_status(dic_operations[self.value]())

        return None


    def eval_components(self):
        """
        This function evaluates the components inside the expression given the status of the operator (expression).
        Here we go down the tree.

        Return:
            None - it directly modifies the status of its components left and right
        """
        def ft_undetermined(token):
            if isinstance(token, Element):
                token.undetermined = 1
            elif isinstance(token, Operator):
                ft_undetermined(token.right)
                ft_undetermined(token.left)

        def or_is_true(left, right):
            if left.status == FALSE:
                if isinstance(left, Element) and left.value in Element.facts_list:
                    right.change_status(TRUE, 1)
                elif isinstance(left, Operator) and left in Operator.facts_list:
                    right.change_status(TRUE, 1)
                elif right.status == FALSE:
                    ft_undetermined(left)
            if right.status == FALSE:
                if isinstance(right, Element) and right.value in Element.facts_list:
                    left.change_status(TRUE, 1)
                elif isinstance(right, Operator) and right in Operator.facts_list:
                    left.change_status(TRUE, 1)
                elif left.status == FALSE:
                    ft_undetermined(right)

        def ft_true():
            if self.value == '+':
                self.right.change_status(TRUE, 1)
                self.left.change_status(TRUE, 1)
            elif self.value == '!':
                self.right.change_status(FALSE, 1)
            elif self.value == '|':
                or_is_true(self.left, self.right)
            elif self.value == '^':
                if self.left.value in Element.facts_list:
                    if self.left.value == FALSE:
                        self.right.change_status(TRUE, 1)
                    else:
                        self.right.change_status(FALSE, 1)
                if self.right.value in Element.facts_list:
                    if self.right.value == FALSE:
                        self.left.change_status(TRUE, 1)
                    else:
                        self.left.change_status(FALSE, 1)
                if self.left.value not in Element.facts_list and self.right.value not in Element.facts_list:
                    ft_undetermined(self.left)
                    ft_undetermined(self.right)

        def ft_false():
            if self.value == '|':
                self.right.change_status(FALSE, 1)
                self.left.change_status(FALSE, 1)
            elif self.value == '!':
                self.right.change_status(TRUE, 1)
            elif self.value == '+':
                if self.left.status == TRUE:
                    self.right.change_status(FALSE, 1)
                elif self.right.status == TRUE:
                    self.left.change_status(FALSE, 1)
                else:
                    if self.left.value not in Element.facts_list:
                        ft_undetermined(self.left)
                    if self.right.value not in Element.facts_list:
                        ft_undetermined(self.right)
            elif self.value == '^':
                if self.left.value in Element.facts_list:
                    if self.left.value == FALSE:
                        self.right.change_status(FALSE, 1)
                    else:
                        self.right.change_status(TRUE, 1)
                if self.right.value in Element.facts_list:
                    if self.right.value == FALSE:
                        self.left.change_status(FALSE, 1)
                    else:
                        self.left.change_status(TRUE, 1)
                if self.left.value not in Element.facts_list and self.right.value not in Element.facts_list:
                    ft_undetermined(self.left)
                    ft_undetermined(self.right)


        dic_operations = {
            TRUE : ft_true,
            FALSE : ft_false,
        }

        dic_operations[self.status]()

        return None

    def change_status(self, new_status, imply=0):
        self.status = new_status
        self.add_oper_factlist()
        if imply:
            self.eval_components()

    def add_elem_factlist(self):
        if self.value != '|':
            if isinstance(self.left, Element):
                Element.facts_list.append(self.left.value)
            elif isinstance(self.left, Operator):
                self.left.add_elemt_factlist()
            if isinstance(self.right, Element):
                Element.facts_list.append(self.right.value)
            elif isinstance(self.right, Operator):
                self.right.add_elemt_factlist()

    def add_oper_factlist(self):
        if isinstance(self.left, Operator):
            self.left.add_oper_factlist()
        if isinstance(self.right, Operator):
            self.right.add_oper_factlist()
        if self.value == '+' and self.value != '^':
            if self.left.value in Element.facts_list and self.right.value in Element.facts_list:
                Operator.facts_list.append(self)
        elif self.value == '!':
            if self.right.value in Element.facts_list:
                Operator.facts_list.append(self)
        elif self.value == '|':
            if self.left.status == TRUE:
                Operator.facts_list.append(self)
            elif self.right.status == TRUE:
                Operator.facts_list.append(self)
            elif self.left.value in Element.facts_list and self.right.value in Element.facts_list:
                Operator.facts_list.append(self)



    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return self.__str__()
