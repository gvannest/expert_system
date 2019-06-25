import sys

from collections import deque

from settings import *

class Element:
    """ Class representing an element of our Knowledge Base (such as A, B, C...)

        Attributes:
            * facts_list : list to keep track of element which have been proven by rules.
    """

    facts_list = []

    def __init__(self, value):
        """ Element class constructor.
        Attributes:
            * value : the letter associated with the current object
            * rules : list of rules associated with the current object
            * status : current status of the element. Can be TRUE or FALSE
            * undetermined : 1 if the element is undetermined, 0 otherwise
        """
        self.value = value
        self.rules = []
        self.proved_by = []
        self.status = FALSE
        self.undetermined = 0

    def solver(self, visited_tree):
        """Recursive function on each element of the tree, solving the query"""
        for tree in self.rules:
            if tree not in visited_tree:
                visited_tree.append(tree)
                solving_stack = deque()
                for e in tree.value:
                    if isinstance(e, Element):
                        solving_stack.append(e)
                        e.solver(visited_tree)
                    elif isinstance(e, Operator):
                        e.right = solving_stack.pop()
                        if e.value != '!':
                            e.left = solving_stack.pop()
                        e.eval_expr(tree)
                        solving_stack.append(e)

    def change_status(self, new_status, tree, imply=0):
        if self.value in Element.facts_list:
            if self.status != new_status:
                print(f"Incoherence on element {self.value}")
                sys.exit(0)
        else:
            self.status = new_status
            self.undetermined = 0
            self.proved_by.append(tree)
            if self.value not in Element.facts_list:
                Element.facts_list.append(self.value)


    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return self.__str__()


class Operator:
    """Class representing a comparison operator in our rules (AND, OR, XOR...).

    Attributes:
        * facts_list : list which tracks the operator objects which have been proved by the different rules.
    """

    facts_list = []

    def __init__(self, value):
        """Object attributes:
                * value [str] : the 'value' of our operator : +, |, ^, !
                * precedence : priority of the current operator
                * left [Element or Operator] : the left expression of our operator (can be an element or an operator linking two other expressions)
                * right [Element or Operator] : the right branch of our operator
                * status : the status of the expression True, False or Undetermined
        """
        self.value = value
        self.precedence = dic_precedences[self.value]
        self.left = None
        self.right = None
        self.status = FALSE


    def eval_expr(self, tree):
        """
        This functions evaluates the current operator (i.e. expression) given the status of its components.
        Hence here we go up the tree.
        For the imply operator, we call the eval components to evaluate the elements on the implied side of the rule.

        Return:
             None but changes the status of the current operator to True or False
        """
        def ft_and(tree):
            return self.left.status & self.right.status

        def ft_or(tree):
            return self.left.status | self.right.status

        def ft_xor(tree):
            return self.left.status ^ self.right.status

        def ft_not(tree):
            return self.right.status ^ 1

        def ft_imply(tree):
            if self.left.status == TRUE:
                if isinstance(self.left, Element):
                    if self.left.value not in Element.facts_list:
                        Element.facts_list.append(self.left.value)
                elif isinstance(self.left, Operator):
                    self.left.add_elem_factlist(tree)
                self.right.change_status(TRUE, tree, 1)
            return self.left.status

        def ft_iif(tree):
            if not ft_imply(tree) and self.right.status == TRUE:
                if isinstance(self.right, Element):
                    if self.right.value not in Element.facts_list:
                        Element.facts_list.append(self.right.value)
                elif isinstance(self.right, Operator):
                    self.right.add_elem_factlist(tree)
                self.left.change_status(TRUE, tree, 1)
            return self.left.status == self.right.status

        dic_operations = {
            '+' : ft_and,
            '|' : ft_or,
            '^' : ft_xor,
            '!' : ft_not,
            '>' : ft_imply,
            '<': ft_iif,
        }
        self.change_status(dic_operations[self.value](tree), tree)

        return None


    def eval_components(self, tree):
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

        def or_is_true(left, right, tree):
            if left.status == FALSE:
                if isinstance(left, Element) and left.value in Element.facts_list:
                    right.change_status(TRUE, tree, 1)
                elif isinstance(left, Operator) and left in Operator.facts_list:
                    right.change_status(TRUE, tree, 1)
                else:
                    ft_undetermined(left)
            if right.status == FALSE:
                if isinstance(right, Element) and right.value in Element.facts_list:
                    left.change_status(TRUE, tree, 1)
                elif isinstance(right, Operator) and right in Operator.facts_list:
                    left.change_status(TRUE, tree, 1)
                else:
                    ft_undetermined(right)
            if left.status == TRUE:
                if (isinstance(left, Element) and left.value not in Element.facts_list)\
                    or (isinstance(left, Operator) and left not in Operator.facts_list):
                    ft_undetermined(left)
            if right.status == TRUE:
                if (isinstance(right, Element) and right.value not in Element.facts_list)\
                    or (isinstance(right, Operator) and right not in Operator.facts_list):
                    ft_undetermined(right)

        def xor_solve(left, right, boolean, tree):
            if left.value in Element.facts_list or left in Operator.facts_list:
                if left.status == FALSE:
                    right.change_status(TRUE ^ boolean, tree, 1)
                else:
                    right.change_status(FALSE ^ boolean, tree, 1)
            if right.value in Element.facts_list or right in Operator.facts_list:
                if right.status == FALSE:
                    left.change_status(TRUE ^ boolean, tree, 1)
                else:
                    left.change_status(FALSE ^ boolean, tree, 1)
            if (isinstance(left, Element) and left.value not in Element.facts_list) \
                or isinstance(left, Operator) and left not in Operator.facts_list:
                if isinstance(right, Element) and right.value not in Element.facts_list:
                    ft_undetermined(left)
                    ft_undetermined(right)
                elif isinstance(right, Operator) and right not in Operator.facts_list:
                    ft_undetermined(left)
                    ft_undetermined(right)

        def and_is_false(left, right, tree):
            if left.status == TRUE:
                if isinstance(left, Element) and left.value in Element.facts_list:
                    right.change_status(FALSE, tree, 1)
                elif isinstance(left, Operator) and left in Operator.facts_list:
                    right.change_status(FALSE, tree, 1)
                else:
                    ft_undetermined(left)
            if right.status == TRUE:
                if isinstance(right, Element) and right.value in Element.facts_list:
                    left.change_status(FALSE, tree, 1)
                elif isinstance(right, Operator) and right in Operator.facts_list:
                    left.change_status(FALSE, tree, 1)
                else:
                    ft_undetermined(right)

        def ft_true(tree):
            if self.value == '+':
                self.right.change_status(TRUE, tree, 1)
                self.left.change_status(TRUE, tree, 1)
            elif self.value == '!':
                self.right.change_status(FALSE, tree, 1)
            elif self.value == '|':
                or_is_true(self.left, self.right, tree)
            elif self.value == '^':
                xor_solve(self.left, self.right, 0, tree)

        def ft_false(tree):
            if self.value == '|':
                self.right.change_status(FALSE, tree, 1)
                self.left.change_status(FALSE, tree, 1)
            elif self.value == '!':
                self.right.change_status(TRUE, tree, 1)
            elif self.value == '+':
                and_is_false(self.left, self.right, tree)
            elif self.value == '^':
                xor_solve(self.left, self.right, 1, tree)

        dic_operations = {
            TRUE : ft_true,
            FALSE : ft_false,
        }

        dic_operations[self.status](tree)

        return None

    def change_status(self, new_status, tree, imply=0):
        """Function called when there is a request for changing the status of the operator."""
        self.status = new_status
        self.add_oper_factlist()
        if imply:
            self.eval_components(tree)

    def add_elem_factlist(self, tree):
        if self.value != '|':
            if isinstance(self.left, Element):
                if self.left.value not in Element.facts_list:
                    Element.facts_list.append(self.left.value)
                if self.left.status != 1 and tree not in self.left.proved_by:
                    self.left.proved_by.append(tree)
            elif isinstance(self.left, Operator):
                self.left.add_elem_factlist(tree)
            if isinstance(self.right, Element):
                if self.right.value not in Element.facts_list:
                    Element.facts_list.append(self.right.value)
                if self.right.status != 1 and tree not in self.right.proved_by:
                    self.right.proved_by.append(tree)
            elif isinstance(self.right, Operator):
                self.right.add_elem_factlist(tree)

    def add_oper_factlist(self):
        if isinstance(self.left, Operator):
            self.left.add_oper_factlist()
        if isinstance(self.right, Operator):
            self.right.add_oper_factlist()
        if self.value == '+':
            if (self.left.value in Element.facts_list or self.left in Operator.facts_list)\
                and (self.right.value in Element.facts_list or self.right in Operator.facts_list):
                    Operator.facts_list.append(self)
            elif self.left.status == FALSE and (self.left.value in Element.facts_list or self.left in Operator.facts_list):
                    Operator.facts_list.append(self)
            elif self.right.status == FALSE and (self.right.value in Element.facts_list or self.right in Operator.facts_list):
                    Operator.facts_list.append(self)
        elif self.value == '^':
            if (self.left.value in Element.facts_list or self.left in Operator.facts_list)\
                and (self.right.value in Element.facts_list or self.right in Operator.facts_list):
                Operator.facts_list.append(self)
        elif self.value == '!':
            if self.right.value in Element.facts_list or self.right in Operator.facts_list:
                Operator.facts_list.append(self)
        elif self.value == '|':
            if (self.left.value in Element.facts_list or self.left in Operator.facts_list)\
                and (self.right.value in Element.facts_list or self.right in Operator.facts_list):
                Operator.facts_list.append(self)
            elif self.left.value in Element.facts_list or self.left in Operator.facts_list:
                if self.left.status == TRUE:
                    Operator.facts_list.append(self)
            elif self.right.value in Element.facts_list or self.right in Operator.facts_list:
                if self.right.status == TRUE:
                    Operator.facts_list.append(self)


    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return self.__str__()
