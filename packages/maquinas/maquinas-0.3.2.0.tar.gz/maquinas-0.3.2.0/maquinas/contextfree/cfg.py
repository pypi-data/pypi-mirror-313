# Código para Autómata Finito [Determinístic]
from maquinas.exceptions import *
from maquinas.regular.dfa import *
from maquinas.contextfree.CFGParser import CFGParser
import maquinas.parser.earley_parser as earley_parser
from ordered_set import OrderedSet
from IPython.display import display, HTML
import random
import itertools
import copy
import re

parser = CFGParser()


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


## TODO Allow more constructive way to produce grammar
## TODO Allow to pass a tokeniser to grammar
class ContextFreeGrammar:
    """Class for Context Free Grammar

    :param er_string: String with grammar
    :param S: Innitial symbol
    """

    def __init__(self, er_string, S=None):
        self.original = er_string
        self.Sigmariginal = er_string
        self.ast = parser.parse(er_string, rulne_name="start")
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
        tokens = [t for t in self.V] + [t for t in self.sigma]
        tokens.sort(key=len, reverse=True)
        self.re_tokens = re.compile("([{}])".format("|".join(tokens)))

    def parse(self, string):
        """Parses a string with grammar

        :param string: String to be parsed

        :returns: Tuple with Roots of trres, chart parser and forest
        """
        tokens = self.re_tokens.findall(string)
        if not len("".join(tokens)) == len(string):
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
        tokens = self.re_tokens.findall(string)
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

    ## TODO: Adds strategis for derivation
    def derivation(self, tree):
        """Iterator over derivation of a tree

        :param tree: Tree to retrieve derivation form

        :returns: Tuple with Roots of trres, chart parser and forest
        """
        tree = self._reduce_tree(tree)
        prev = None
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

    ## TODO: Adds formas for derivation (e.g., Latex)
    def print_derivations(self, string, ini=0, fin=None):
        """Print derivations over trees

        :param string: String to be parsed
        :param ini: Initial tree to start printing from
        :param final: Final tree to print
        """
        roots, chart, forest = self.parse(string)
        if roots:
            trees = self.extract_trees(forest)
            if fin:
                trees = trees[ini:fin]
            else:
                trees = trees[ini:]
            for i, tree in enumerate(trees):
                print("Tree #", ini + i)
                for j, step in enumerate(self.derivation(tree)):
                    if not j:
                        print("".join(step), end="")
                    else:
                        print(" ⇒ ", "".join(step), end="\n ")
                print()

    ## TODO adds replacement of symbols
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

    ## TODO associate string to chart
    def print_chart(self, string, chart, pointers=False):
        """Prints chart parser

        :param string: Original string fom parser
        :param chart: Chart parser
        :param pointers: Include pointers (default is no)
        """
        earley_parser.print_chart(string, chart, pointers=pointers)

    ## TODO associate string to chart
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

    def save_trees_img(self, trees, filename, format="svg", dpi="60.0", **params):
        """Saves trees into an image

        :param trees: List of tree data structures
        :param filename: Filename for the image file
        :param format: Image format (defualt svg)
        :param dpi: DPIs of fomat (default "60.0")
        :param params: Options to graph the tree"""
        dot = self.graph_trees(trees, **params)
        dot.render(filename, format=format, cleanup=True)

    def save_tree_img(self, tree, filename, format="svg", dpi="60.0", **params):
        """Saves a tree into an image

        :param tree: Tree data structures
        :param filename: Filename for the image file
        :param format: Image format (defualt svg)
        :param dpi: DPIs of fomat (default "60.0")
        :param params: Options to graph the tree"""
        dot = self.graph_tree(tree, **params)
        dot.render(filename, format=format, cleanup=True)

    def __str__(self):
        return self.original
