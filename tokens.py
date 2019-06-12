from collections import deque

from settings import *

class Tree:

    def __init__(self, tree):
        self.tree_str = tree_str
        self.tree = tree

class Element:
    """ Class representing an element of our Knowledge Base (such as A, B, C...)"""

    def __init__(self, value):
        self.value = value
        self.rules = []
        self.proven_rules = []
        self.proved = 0
        self.status = FALSE

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


    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return self.__str__()




class Operator:
    """Class respresenting a comparison operator in our rules (AND, OR, XOR...). """

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
            self.right.status = self.left.status
            self.left.proven = 1
            return self.left.status

        dic_operations = {
            '+' : ft_and,
            '|' : ft_or,
            '^' : ft_xor,
            '!' : ft_not,
            '>' : ft_imply,
        }

        self.status = dic_operations[self.value]()

        return None


    def eval_components(self):
        """
        This function evaluates the components inside the expression given the status of the operator (expression).
        Here we go down the tree.

        Return:
            None - it directly modifies the status of its components left and right
        """
        def ft_true():
            if self.value == '+':
                self.right.status = TRUE
                self.left.status = TRUE
            elif self.value == '!':
                self.left.status = FALSE
            else:
                self.right.status = UNDETERMINED
                self.left.status = UNDETERMINED

        def ft_false():
            if self.value == '|':
                self.right.status = FALSE
                self.left.status = FALSE
            elif self.value == '!':
                self.left.status = TRUE
            else:
                self.right.status = UNDETERMINED
                self.left.status = UNDETERMINED

        def ft_undeter():
            return None

        dic_operations = {
            TRUE : ft_true,
            FALSE : ft_false,
            UNDETERMINED : ft_undeter,
        }

        dic_operations[self.status]()

        return None


    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return self.__str__()




class LogicOperator:
    """
    Class representing a logical operator. For the time being there are two of them : IMPLIES and IIF (If and only if).
    """

    def __init__(self, value: int):
        self.value = value #IMPLIES , IIF

    # Ici il faudrait faire des regles un peu comme au dessus avec les implications
