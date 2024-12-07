# Código para Autómata Finito [Determinístic]

from maquinas.exceptions import *
from maquinas.regular.ndfa_e import *
from maquinas.regular.REParser import REParser

parser = REParser()


class RegularExpression:
    """Class for Regular Expressions

    :param er_string: regular expressiones.
    """

    def __init__(self, er_string):
        if len(er_string.strip()) == 0:
            raise NoStringWithDefinition(er_string, "RE")
        self.original = er_string
        self.ast = parser.parse(er_string, rulne_name="start")

    def __str__(self):
        return self.original

    def _ndfa_e(self, ast):
        if isinstance(ast, tuple):
            if len(ast) == 3:
                fst = self._ndfa_e(ast[0])
                snd = self._ndfa_e(ast[2])
                fa = fst.union(snd)
            elif len(ast) == 2:
                if not ast[1] == "*":
                    fst = self._ndfa_e(ast[0])
                    snd = self._ndfa_e(ast[1])
                    fa = fst.concat(snd)
                else:
                    fst = self._ndfa_e(ast[0])
                    fa = fst.kleene()
        else:
            if ast.startswith('"'):
                name = ast[1:-1]
            else:
                name = ast
            if name in ["empty", "∅"]:
                fa = ndfa_e_empty()
            elif name in ["epsilon", "ε"]:
                fa = ndfa_e_epsilon()
            else:
                fa = ndfa_e_single_symbol(name)
        return fa

    def ndfa_e(self):
        """Generates a NDFA-e equivalent to the ER

        :returns: NDFA-e equivalent to ER"""
        return self._ndfa_e(self.ast)
