from maquinas.regular.fa import FiniteAutomaton
from maquinas.exceptions import *
from IPython.display import display, HTML
from graphviz import Digraph


class DeterministicFiniteAutomaton(FiniteAutomaton):
    """Class for Deterministic Finite Automaton

    :param Q: Ordered set of states (default is empty).
    :param sigma: Ordered set of symbols (default is empty).
    :param q_0: Initial state (default None).
    :param A: Set of acceptor states (default is empty).
    :param delta: List of transitions with the form tupla of tupla of q_i and a, and q_f (default is empty).
    :param force: If True and states or symbols do not exists create them (default is False).
    :type force: bool
    """

    def __init__(self, Q=[], sigma=[], q_0=None, A=[], delta={}, force=False):
        super().__init__(Q, sigma, q_0, A, delta)

    def delta(self, q, a):
        """Applies delta function

        :param q: Source state
        :param a: Symbol

        :returns: Destination state"""
        return self.get_transition(q, a)

    def delta_extended(self, q, w):
        """Applies delta extended function

        :param q: Source state
        :param w: String

        :returns: Destination state after processing the full string"""
        if q is None:
            q = self.q_0
        if len(w) == 0:
            return q
        else:
            *w_, a = w
            return self.delta(self.delta_extended(q, w_), a)

    def delta_stepwise(self, w, q=None):
        """Applies a step of delta extended function

        :param w: String
        :param q: Source state (default is initial state)

        :returns: Tuple with state of precessing at step, consisting of: destination state, procesed symbol and processed string"""

        q_c = self.q_0 if q is None else q
        yield q_c, "", w
        for ix, a in enumerate(w):
            q_c = self.delta(q_c, a)
            yield q_c, a, w[ix + 1 :]

    def summary(self, symbols={}, states={}):
        """Produces a summary of the AF

        :param symbols: Replacements of the symbols to print
        :param states: Replacements of the states to print
        :returns: List with summary"""
        info = [
            "States  : " + ", ".join([symbols.get(q, q) for q in self.states()]),
            "Sigma   : " + ", ".join([symbols.get(a, a) for a in self.symbols()]),
            "Initial : " + symbols.get(self.q_0, self.q_0),
            f"Aceptors: {{{', '.join([symbols.get(q, q) for q in self.A])}}}",
            "Transitions:",
            "\n".join(
                f" {states.get(q_i,q_i)},{symbols.get(a,a)} → {states.get(q_f,q_f)}"
                for (q_i, a), q_f in self.items()
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
        """Graphs DFA

        :param q_c: Set of current states to be highlited (default is empty)
        :param a_c: Set of current symbols to be highlited (default is empty)
        :param q_prev: Set of previos states to be highlited (default is empty)
        :param symbols: Replacements of the symbols to show (default is empty)
        :param states: Replacements of the states to show (default is empty)
        :param format: Format of image (default is svg)
        :param dpi: Resolution of image (default is "60.0")
        :param string: Label of string being analysed (default is None)
        :returns: Returns Digraph object from graphviz"""

        f = Digraph(comment="dfa", format=format)
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
            (q_i, a), q_f = info
            if q_i in q_prev and a in a_c:
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
        empty_transition="",
        color_final="#32a852",
    ):
        """Creates an HTML object for the table of the DFA

        :param symbols: Replacements of the symbols to show (default is empty)
        :param states: Replacements of the states to show (default is empty)
        :param  q_order: Order to use for state
        :param  s_order: Order to use for symbols
        :param empty_transition: Symbol to print for empty transitin (default is "")
        :param color_final: RGB string for color of final state (default is "#32a852")

        :returns: Display object for IPython"""
        if not s_order:
            s_order = list(self.sigma)
            s_order.sort()
        if not q_order:
            q_order = list(self.Q)
            q_order.sort()
        symbs_h = "</strong></td><td><strong>".join([states.get(q, q) for q in s_order])
        table = f"<table><tr><td></td><td><strong>{symbs_h}</strong></td></tr>"
        for q_i in q_order:
            vals = []
            initial = "⟶" if q_i == self.q_0 else ""
            final = f'bgcolor="{color_final}"' if q_i in self.A else ""
            vals.append(f"<strong>{initial}{states.get(q_i,q_i)}</strong>")
            for a in s_order:
                try:
                    q_fs = self[q_i, a]
                    q_fs_ = [states.get(q, q) for q in q_fs]
                    vals.append(",".join(q_fs_))
                except DoesNotExistsTransition:
                    vals.append("")
            row = "</td><td>".join(vals)
            table += f"<tr><td {final}>{row}</td></tr>"
        table += "</table>"
        return display(HTML(table))
