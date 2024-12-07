# Código para Autómata Finito No Determinístico con transición epsilon

from maquinas.regular.fa import FiniteAutomaton
from maquinas.exceptions import *

from IPython.display import display, HTML
from graphviz import Digraph

epsilon = "ε"

## TODO allow no strict
## TODO loaders
## TODO compress links in one
class NonDeterministicFiniteAutomaton_epsilon(FiniteAutomaton):
    """Class for Deterministic Finite Automaton

    :param Q: Ordered set of states (default is empty).
    :param sigma: Ordered set of symbols (default is empty).
    :param q_0: Initial state (default None).
    :param A: Set of acceptor states (default is empty).
    :param delta: List of transitions with the form tupla of tupla of q_i and a, and q_f (default is empty).
    :param force: If True and states or symbols do not exists create them (default is False).
    :type force: bool
    """

    def __init__(self, Q=[], sigma=[], q_0=None, A=[], delta=[], force=False):
        super().__init__(Q, sigma, q_0, A, delta, epsilon=epsilon)
        self.e = epsilon

    def expansion_epsilon(self, qs):
        """Applies expansion by epsilon in a set of states

        :param qs: Set of states

        :returns: Set of reachable states from qs"""
        qs__ = set(q for q in qs)
        change = True
        while change:
            qs_ = set()
            for q in qs__:
                qs_.add(q)
                try:
                    qs_.update(self.get_transition(q, self.e))
                except DoesNotExistsTransition:
                    pass
            if len(qs__ ^ qs_) == 0:
                change = False
            qs__ = qs_
        return qs__

    def delta(self, q, a):
        """Applies delta function

        :param q: Source state
        :param a: Symbol

        :returns: Destination state"""
        try:
            return self.expansion_epsilon(self.get_transition(q, a))
        except DoesNotExistsTransition:
            return set()

    def delta_extended(self, q, w):
        """Applies delta extended function

        :param q: Source state
        :param w: String

        :returns: Destination state after processing the full string"""
        if q is None:
            q = set([self.q_0])
        if len(w) == 0:
            return self.expansion_epsilon(q)
        else:
            *w_, a = w
            q_u = set()
            for r in self.delta_extended(q, w_):
                q_u.update(self.delta(r, a))
            return self.expansion_epsilon(q_u)

    def delta_stepwise(self, w, q=None):
        """Applies a step of delta extended function

        :param w: String
        :param q: Source state (default is initial state)

        :returns: Tuple with state of precessing at step, consisting of: destination state, procesed symbol and processed string"""
        q_c = set([self.q_0]) if q is None else set(q)
        yield q_c, "", w
        for ix, a in enumerate(w):
            q_c = self.delta(q_c, a)
            q_c = self.expansion_epsilon(q_c)
            yield q_c, a, w[ix + 1 :]

    def summary(self, symbols={}, states={}):
        """Produces a summary of the AF

        :param symbols: Replacements of the symbols to print
        :param states: Replacements of the states to print
        :returns: List with summary"""
        info = [
            "States  : " + ", ".join([symbols.get(q, q) for q in self.states()]),
            "Sigma   : "
            + ", ".join([symbols.get(a, a) for a in self.symbols() if not a == self.e]),
            "Initial : " + symbols.get(self.q_0, self.q_0),
            f"Aceptors: {{{', '.join([symbols.get(q, q) for q in self.A])}}}",
            "Transitions:",
            "\n".join(
                f" {states.get(q_i,q_i)},{symbols.get(a,a)} → {{{', '.join(tuple(states.get(q_f,q_f) for q_f in q_fs))}}}"
                for (q_i, a), q_fs in self.items()
            ),
        ]
        return "\n".join(info)

    def graph(
        self,
        q_c=set(),
        a_c=set(),
        q_prev=set(),
        symbols={},
        states={},
        format="svg",
        dpi="60.0",
        string=None,
        **args,
    ):
        """Graphs NDFA_e

        :param q_c: Set of current states to be highlited (default is empty)
        :param a_c: Set of current symbols to be highlited (default is empty)
        :param q_prev: Set of previos states to be highlited (default is empty)
        :param symbols: Replacements of the symbols to show (default is empty)
        :param states: Replacements of the states to show (default is empty)
        :param format: Format of image (default is svg)
        :param dpi: Resolution of image (default is "60.0")
        :param string: Label of string being analysed (default is None)
        :returns: Returns Digraph object from graphviz"""
        f = Digraph(comment="af", format=format)
        f.attr(rankdir="LR", dpi=dpi)
        color_state = "lightblue2"
        if string:
            l, c, r = string
            f.attr(label=f"<{l} <B>{c}</B> {r}>")
            if len(r) == 0:
                if len(self.A.intersection(q_c)) > 0:
                    color_state = "limegreen"
                else:
                    color_state = "orangered"
        f.node(name="__initial__", label="", shape="none", height=".0", width=".0")
        for q, q_ in self.Q.map.items():
            if q in self.A:
                shape = "doublecircle"
            else:
                shape = "circle"
            if q in q_c:
                f.node(
                    name=q,
                    label=states.get(q, q),
                    shape=shape,
                    color=color_state,
                    style="filled",
                )
            else:
                f.node(name=q, label=states.get(q, q), shape=shape)

        f.edge("__initial__", self.q_0)
        for e, info in enumerate(self.items()):
            (q_i, a), q_fs = info
            for q_f in q_fs:
                if (q_i in q_prev and a in a_c) or (q_prev and q_i in q_c and a == "ε"):
                    f.edge(
                        q_i,
                        q_f,
                        label=symbols.get(a, a),
                        color=color_state,
                        fontcolor=color_state,
                    )
                else:
                    f.edge(q_i, q_f, label=symbols.get(a, a))
        return f

    def table(
        self,
        symbols={},
        states={},
        q_order=None,
        s_order=None,
        color_final="#32a852",
        empty_symbol="∅",
    ):
        """Creates an HTML object for the table of the DFA

        :param symbols: Replacements of the symbols to show (default is empty)
        :param states: Replacements of the states to show (default is empty)
        :param  q_order: Order to use for states
        :param  s_order: Order to use for symbols
        :param color_final: RGB string for color of final state (default is "#32a852")

        :returns: Display object for IPython"""
        if not s_order:
            s_order = list(self.sigma)
            s_order.sort()
        if not q_order:
            q_order = list(self.Q)
            q_order.sort()
        symbs_h = "</strong></td><td><strong>".join(
            [symbols.get(q, q) for q in s_order]
        )
        table = f"<table><tr><td></td><td><strong>{symbs_h}</strong></td></tr>"
        for q_i in q_order:
            vals = []
            initial = "⟶" if q_i == self.q_0 else ""
            final = f'bgcolor="{color_final}"' if q_i in self.A else ""
            vals.append(f"<strong>{initial}{states.get(q_i,q_i)}</strong>")
            for a in s_order:
                try:
                    q_fs = set(states.get(q_f, q_f) for q_f in self[q_i, a])
                    if len(q_fs) > 0:
                        vals.append(",".join(q_fs))
                    else:
                        vals.append(empty_symbol)
                except DoesNotExistsTransition:
                    vals.append(empty_symbol)
            row = "</td><td>".join(vals)
            table += f"<tr><td {final}>{row}</td></tr>"
        table += "</table>"
        return display(HTML(table))

    def union(self, other, label_a="ᴬ", label_b="ᴮ"):
        """Unites this NDFA_e with other NDFA-e

        :param other: Other NDFA-e
        :param label_a: Label to append to states of this NDFA-e (default is "ᴬ")
        :param label_b: Label to append to states of other NDFA-e (default is "ᴮ")

        :returns: Returns NDFA resultinf of the union of this an another NDFA-e"""
        new = NonDeterministicFiniteAutomaton_epsilon()
        new.add_state("q_0", initial=True)
        new.sigma = self.sigma.union(other.sigma)
        new.A = set()
        for q in self.Q:
            name = f"{q}{label_a}"
            new.Q.add(name)
            if q in self.A:
                new.A.add(name)
        for q in other.Q:
            name = f"{q}{label_b}"
            new.Q.add(name)
            if q in other.A:
                new.A.add(name)

        skip = 1
        for nq_i, t_ in self.ttable.items():
            for na, nqs_f in t_.items():
                a = self.sigma.items[na]
                na = new.sigma.index(a)
                try:
                    new.ttable[nq_i + skip][na] = set([nq + skip for nq in nqs_f])
                except KeyError:
                    new.ttable[nq_i + skip] = {}
                    new.ttable[nq_i + skip][na] = set([nq + skip for nq in nqs_f])

        skip = len(self.Q) + 1
        for nq_i, t_ in other.ttable.items():
            for na, nqs_f in t_.items():
                a = other.sigma.items[na]
                na = new.sigma.index(a)
                try:
                    new.ttable[nq_i + skip][na] = set([nq + skip for nq in nqs_f])
                except KeyError:
                    new.ttable[nq_i + skip] = {}
                    new.ttable[nq_i + skip][na] = set([nq + skip for nq in nqs_f])
        new.ttable[0] = {}
        new.ttable[0][0] = set([1, skip])
        return new

    def concat(
        self,
        other,
        label_a="ᴬ",
        label_b="ᴮ",
    ):
        """Concatenates of this NDFA_e with other NDFA-e

        :param other: Other NDFA-e
        :param label_a: Label to append to states of this NDFA-e (default is "ᴬ")
        :param label_b: Label to append to states of other NDFA-e (default is "ᴮ")

        :returns: Returns NDFA resulting of the concatenation of this an another NDFA-e"""
        new = NonDeterministicFiniteAutomaton_epsilon()
        new.sigma = self.sigma.union(other.sigma)
        new.A = set()
        for q in self.Q:
            name = f"{q}{label_a}"
            if q == self.q_0:
                new.set_initial_state(name, force=True)
            new.Q.add(name)
        for q in other.Q:
            name = f"{q}{label_b}"
            new.Q.add(name)
            if q in other.A:
                new.A.add(name)

        skip = 0
        for nq_i, t_ in self.ttable.items():
            for na, nqs_f in t_.items():
                a = self.sigma.items[na]
                na = new.sigma.index(a)
                try:
                    new.ttable[nq_i + skip][na] = set([nq + skip for nq in nqs_f])
                except KeyError:
                    new.ttable[nq_i + skip] = {}
                    new.ttable[nq_i + skip][na] = set([nq + skip for nq in nqs_f])

        skip = len(self.Q)
        for nq_i, t_ in other.ttable.items():
            for na, nqs_f in t_.items():
                a = other.sigma.items[na]
                na = new.sigma.index(a)
                try:
                    new.ttable[nq_i + skip][na] = set([nq + skip for nq in nqs_f])
                except KeyError:
                    new.ttable[nq_i + skip] = {}
                    new.ttable[nq_i + skip][na] = set([nq + skip for nq in nqs_f])

        for q in self.A:
            nq = self.Q.index(q)
            if nq in new.ttable:
                if 0 in new.ttable[nq]:
                    new.ttable[nq][0].add(skip)
                else:
                    new.ttable[nq][0] = set([skip])
            else:
                new.ttable[nq] = {}
                new.ttable[nq][0] = set([skip])
        return new

    def kleene(self, label="ᴬ"):
        """Applies Kleene closure to this NDFA_e

        :param label: Label to append to states of this NDFA-e (default is "ᴬ")

        :returns: Returns NDFA resulting of the application of Kleen closure to this NDFA-e"""
        new = NonDeterministicFiniteAutomaton_epsilon()
        new.add_state("q_0", initial=True)
        new.sigma = self.sigma
        new.A = set()
        for q in self.Q:
            name = f"{q}{label}"
            new.Q.add(name)
        new.add_state("q_f")
        new.A.add("q_f")
        nq_f = len(new.Q) - 1

        skip = 1
        for nq_i, t_ in self.ttable.items():
            for na, nqs_f in t_.items():
                a = self.sigma.items[na]
                na = new.sigma.index(a)
                try:
                    new.ttable[nq_i + skip][na] = set([nq + skip for nq in nqs_f])
                except KeyError:
                    new.ttable[nq_i + skip] = {}
                    new.ttable[nq_i + skip][na] = set([nq + skip for nq in nqs_f])
        new.ttable[0] = {}
        new.ttable[0][0] = set([1, nq_f])
        new.ttable[nq_f] = {}
        new.ttable[nq_f][0] = set([0])

        for q in self.A:
            nq = self.Q.index(q)
            if nq + skip in new.ttable:
                if 0 in new.ttable[nq + skip]:
                    new.ttable[nq + skip][0].add(nq_f)
                else:
                    new.ttable[nq + skip][0] = set([nq_f])
            else:
                new.ttable[nq + skip] = {}
                new.ttable[nq + skip][0] = set([nq_f])

        return new


def ndfa_e_single_symbol(symbol):
    """NDFA-e for language of a single symbol

    :param symbol: Symbol to be accepted by NDFA-e

    :returns: NDFA-e for language of a single symbol"""
    fa = NonDeterministicFiniteAutomaton_epsilon()
    fa.add_transition("q_0", symbol, ["q_1"], force=True)
    fa.set_initial_state("q_0")
    fa.set_aceptors(["q_1"])
    return fa


def ndfa_e_epsilon():
    """NDFA-e for empty string language

    :returns: NDFA-e for empty string language"""
    fa = NonDeterministicFiniteAutomaton_epsilon()
    fa.add_transition("q_0", epsilon, ["q_0"], force=True)
    fa.set_initial_state("q_0", force=True)
    fa.set_aceptors(["q_0"])
    return fa


def ndfa_e_empty():
    """NDFA-e for empty language

    :returns: NDFA-e for empty language"""
    fa = NonDeterministicFiniteAutomaton_epsilon()
    fa.set_initial_state("q_0", force=True)
    fa.set_aceptors([])
    return fa
