class Token:

    def __init__(self, type: str, obj):
        self.type = type   #Type ca peut etre OPERATOR, FACT, LOGIC ou EOF
        self.obj = obj  # La valeur est l'objet correspondant

    def __str__(self):
        return f"({self.type}, {self.obj.value})"


class Element:

    def __init__(self, value):
        self.value = value
        self.is_dependent = [] #plusieurs parents possibles
        self.implies = [] #plusieurs children possibles
        #self.activation = []  # a voir si on met une lsite ou un autre type. Ce serait la liste des conditions pour qu'il soit true
        self.status = False

    def __str__(self):
        return f"{self.value} : {self.activation}"


class EOF:

    def __init__(self):
        self.value = "EOF"




class Operator:

    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return f"{self.value}"


class Connective(Operator):

    def __init__(self, value: str):
        self.super().__init__(value)  # la valeur de l'operateur (un char) : | ^ + NOT...


class Logic(Operator):

    def __init__(self, value: str):  # implies or iif
        self.super().__init__(value)