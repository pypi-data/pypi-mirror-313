# Código para Autómata Finito [Determinístic]
from maquinas.exceptions import *
from maquinas.regular.dfa import *
from maquinas.regular.RGParser import RGParser
import maquinas.parser.earley_parser as earley_parser
from ordered_set import OrderedSet
from IPython.display import display, HTML
import random
import itertools
import copy
import re

parser = RGParser()

# TODO: Check the left version and the extended


def _flat(vals, ini=[]):
    if isinstance(vals, tuple):
        ini1 = _flat(vals[0])
        ini2 = _flat(vals[1])
        return ini1 + ini2
    else:
        return [vals]


def _flat_tree(tree, acc=[]):
    if len(tree) == 2 and tree[-1][-1] == ";":
        acc = _flat_tree(tree[0])
        acc.append(tree[1])
        return acc
    return [tree]


class RegularGrammar:
    """Class for Context Free Grammar

    :param er_string: String with grammar
    :param S: Innitial symbol
    :param type: Type of grammar (default is 'right')
    """

    def __init__(self, er_string, S=None, type="right"):
        self.original = er_string
        self.Sigmariginal = er_string
        self.ast = parser.parse(er_string, rule_name="start")
        if len(self.ast) == 2:
            self.ast = _flat_tree(self.ast[0]) + [self.ast[1]]
        else:
            self.ast = _flat_tree(self.ast[0]) + [self.ast[1], self.ast[2]]
        self.V = set()
        self.sigma = set()
        self.P = {}
        replacements = {"epsilon": "ε"}
        for p in self.ast:
            head = p[0]
            if head not in self.sigma:
                self.V.add(head.replace('"', ""))
        for p in self.ast:
            body = _flat(p[2])
            body = [
                replacements.get(p.replace('"', ""), p.replace('"', "")) for p in body
            ]
            try:
                self.P[p[0]].append(body)
            except KeyError:
                self.P[p[0]] = [body]
            for val in body:
                if not val in self.V:
                    if not val == "ε":
                        self.sigma.add(val.replace('"', ""))
        if S:
            self.S = S
        else:
            self.S = self.ast[0][0]
        for alpha, betas in self.P.items():
            for beta in betas:
                if not alpha in self.V:
                    return "Error"
                if type == "right":
                    if (
                        not len(beta) == 2
                        and beta[0] in self.sigma
                        and beta[1] in self.V
                    ):
                        return "Error"
                elif type == "left":
                    if (
                        not len(beta) == 2
                        and beta[0] in self.sigma
                        and beta[1] in self.V
                    ):
                        return "Error"

        tokens = [t for t in self.V] + [t for t in self.sigma]
        tokens.sort(key=len, reverse=True)
        self.re_tokens = re.compile(
            "|".join(["".join([f"[{t_}]" for t_ in t]) + "\s*" for t in tokens])
        )

    def tokenize(self, string):
        return [t.strip() for t in self.re_tokens.findall(string)]

    def parse(self, string):
        """Parses a string with grammar

        :param string: String to be parsed

        :returns: Tuple with Roots of trres, chart parser and forest
        """
        tokens = self.tokenize(string)
        if len(tokens) == 0:
            return False, [], {}
        chart = earley_parser.parse(tokens, self.P, self.S, self.sigma)
        forest = earley_parser.extract_forest(self.S, chart, self.sigma, tokens)
        roots = earley_parser.verify_chart(chart, tokens, self.S)
        return roots, chart, forest

    def accepts(self, string):
        """Parses a string with grammar and determines if accepts it

        :param string: String to be parsed

        :returns: Tuple with Roots of trres, chart parser and forest
        """
        tokens = self.tokenize(string)
        if not len("".join(tokens)) == len(string):
            return False, [], {}
        chart = earley_parser.parse(tokens, self.P, self.S, self.sigma)
        roots = earley_parser.verify_chart(chart, tokens, self.S)
        return len(roots) > 0

    def _reduce_tree(self, tree):
        if len(tree) == 1:
            return tree
        head, children = tree
        subtree = []
        for child in children:
            child_ = self._reduce_tree(child)
            if child_[0]["partial"]:
                for grandchild in child_[1]:
                    subtree.append(grandchild)
            else:
                subtree.append(child_)
        return (head, subtree)

    def derivation(self, tree):
        """Iterator over derivation of a tree

        :param tree: Tree to retrieve derivation form

        :returns: Tuple with Roots of trres, chart parser and forest
        """
        tree = self._reduce_tree(tree)
        for i, nodes in enumerate(self.delta_analyse_tree(tree)):
            if i == 0:
                string = [("", "") for _ in range(nodes[0][1], nodes[0][2])]
            for node in nodes:
                ini, fin = node[1], node[2]
                if ini != fin:
                    pre, label = string[ini]
                    string[ini] = (pre, node[0])
                else:
                    if ini == len(string):
                        string.append(("", ""))
                    pre, label = string[ini]
                    string[ini] = (node[0], label)
            yield [l[0] + l[1] for l in string]

    def print_derivations(self, string, ini=0, fin=None):
        """Print derivations over trees

        :param string: String to be parsed
        :param ini: Initial tree to start printing from
        :param final: Final tree to print
        """
        roots, chart, forest = self.parse(string)
        if roots:
            trees = self.extract_trees(forest)
            for i, tree in enumerate(trees):
                if i <= ini:
                    continue
                if i > fin:
                    break
                print("Tree #", ini + i)
                for j, step in enumerate(self.derivation(tree)):
                    if not j:
                        print("".join(step), end="")
                    else:
                        print(" ⇒ ", "".join(step), end="\n ")
                print()

    def summary(self):
        """Generates summary of grammar"""
        info = [
            "No terminal : " + ", ".join(self.V),
            "Terminals   : " + ", ".join(self.sigma),
            "Start       : " + ", ".join(self.S),
            "Productions :\n"
            + "\n".join(
                f" {alpha} → {' | '.join(''.join(beta) for beta in betas)}"
                for alpha, betas in self.P.items()
            ),
        ]
        return "\n".join(info)

    def print_summary(self):
        """Prints summary of grammar"""
        return print(self.summary())

    def _delta_analyse_tree(self, tree):
        if len(tree) == 2:
            _, children = tree
            children_ = [t[0]["label"] for t in children]
            yield children_
            for child in children:
                yield from self._delta_analyse_tree(child)

    def delta_analyse_tree(self, tree):
        """Iteraror over analysis of a tree

        :param tree: Tree
        """
        tree = self._reduce_tree(tree)
        current, children = tree
        yield [current["label"]]
        children_ = [t[0]["label"] for t in children]
        yield children_
        for child in children:
            yield from self._delta_analyse_tree(child)

    def print_chart(self, string, chart, pointers=False):
        """Prints chart parser

        :param string: Original string fom parser
        :param chart: Chart parser
        :param pointers: Include pointers (default is no)
        """
        earley_parser.print_chart(string, chart, pointers=pointers)

    def chart2table(self, string, chart, pointers=False):
        """Creates HTML for chart parser

        :param string: Original string fom parser
        :param chart: Chart parser
        :param pointers: Include pointers (default is no)

        :returns: Display object for IPython"""
        earley_parser.chart2table(string, chart, pointers=pointers)

    def graph_forest(self, forest, **params):
        """Graph the forest structure

        :param forest: Forest structure
        :param params: Options to graph the tree

        :returns: Graphviz object"""
        return earley_parser.graph_forest(forest, **params)

    def extract_forest(self, chart):
        """Extract forest from chart object

        :param chart: Chart parser

        :returns: Forest data structure"""
        return earley_parser.extract_forest(self.S, chart, self.sigma)

    def extract_trees(self, forest, max_depth=None, max_ancesters=3):
        """Extract trees from forest structure

        :param forest: Forest data structure
        :param max_depth: Maximum depth to explore (default is None)
        :param max_ancester: Maximum number of the same ancester (default is 3)
        :returns: Trees data structure"""
        return earley_parser.extract_trees(
            forest, self.sigma, max_depth=max_depth, max_ancesters=max_ancesters
        )

    def graph_tree(self, tree, **params):
        """Graphs a tree

        :param tree: Tree data structure
        :param params: Options to graph the tree
        :returns: Graphviz objec"""
        return earley_parser.graph_tree(tree, **params)

    def graph_trees(self, trees, **params):
        """Graphs trees

        :param trees: Tree data structures
        :param params: Options to graph the tree
        :returns: Graphviz objec"""
        return earley_parser.graph_trees(trees, **params)

    def save_trees_img(self, trees, filename, **params):
        """Saves trees into an image

        :param trees: Tree data structures
        :param filename: Filename for the image file
        :param params: Options to graph the tree"""
        dot = self.graph_trees(trees)
        dot.render(filename, format="png", cleanup=True)

    def __str__(self):
        return self.original
