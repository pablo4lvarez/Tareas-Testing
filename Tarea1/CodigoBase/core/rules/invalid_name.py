from ..rule import *
import re

# Clases que permiten detectar el uso de un nombre invalido en clases, metodos y funciones

class InvalidNameVisitor(WarningNodeVisitor):

    def __init__(self):
        super().__init__()

    def visit_ClassDef(self, node):
        if not re.match('^[A-Z][a-zA-Z0-9]*$', node.name):
            print('Invalid class name!!', node.name)
            self.addWarning('InvalidName', node.lineno, 'invalid class name ' + node.name)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        if not re.match('[a-z ][a-z0-9 ]{2,30}$', node.name):
            print('Invalid function name!!', node.name)
            self.addWarning('InvalidName', node.lineno, 'invalid function name ' + node.name)
            
        self.generic_visit(node)


class InvalidNameRule(Rule):
    def analyze(self, ast):
        visitor = InvalidNameVisitor()
        visitor.visit(ast)
        warnings = visitor.warningsList()
        for warning in warnings:
            print('printin in the warnings iteration...')
            print(warning)
    
    @classmethod
    def name(cls):
        return 'invalid-name'
