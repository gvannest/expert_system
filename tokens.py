from settings import *


class Element:
    """ Class representing an element of our Knowledge Base (such as A, B, C...)"""

    def __init__(self, value):
        self.value = value
        self.rules = []
        self.status = FALSE


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
        # self.left = left
        # self.right = right
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
            return self.left.status ^ 1

        dic_operations = {
            '+' : ft_and,
            '|' : ft_or,
            '^' : ft_xor,
            '!' : ft_not,
        }

        return dic_operations[self.value]()


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
