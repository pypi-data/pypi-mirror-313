# Base class for Finite Machines
from maquinas.exceptions import *
from collections import defaultdict
from ordered_set import OrderedSet
import re
import tempfile
import os

from PIL import Image
from IPython.display import display, HTML
from graphviz import Digraph

re_queque = re.compile(r"(Z_?\d+|Z₀|epsilon|_[^_]+_|\w)")


class TwoStackPushDownAutomaton:
    """Common class for Two stack Push Down Automaton

    :param Q: Ordered set of states (default is empty).
    :param sigma: Ordered set of terminal symbols (default is empty).
    :param gamma: Ordered set of stack symbols (default is empty).
    :param q_0: Initial state (default None).
    :param Z_0: Initial stack symbol (default None).
    :param A: Set of acceptor states (default is empty).
    :param delta: List of transitions with the form tupla of tupla of q_i and a, and q_f (default is empty).
    :param force: If True and states or symbols do not exists create them (default is False).
    :type force: bool
    """

    def __init__(
        self, Q=[], sigma=[], gamma=[], q_0=None, Z_0=None, A=[], delta={}, force=False
    ):
        self.sigma = OrderedSet()
        self.sigma.add("ε")
        self.gamma = OrderedSet()
        self.gamma.add("ε")
        Z_0 = self.set_initial_qsymbol(Z_0)
        self.gamma.add(Z_0)
        self.sigma.update(sigma)
        self.gamma.update([self._filter(g) for g in gamma])
        self.Q = OrderedSet(Q)
        self.set_initial_state(q_0)
        self.set_aceptors(A, force=force)
        self.ttable = {}
        for (q_i, a, z1, z2), qs in delta:
            # Replace Z_0 or Z0 by Z₀ or epsilon for ε
            self.add_transition(
                q_i,
                self._filter(a),
                self._filter(z1),
                self._filter(z2),
                self._filter_stack(qs),
            )

    def _filter_stack(self, qs):
        return [
            (
                q,
                (
                    tuple(self._filter(t) for t in self.tokens(r1)),
                    tuple(self._filter(t) for t in self.tokens(r2)),
                ),
            )
            for (q, r1, r2) in qs
        ]

    def __getitem__(self, key):
        q, a, z1, z2 = key
        return self.get_transition(q, a, z1, z2)

    def _nstate(self, q):
        return self.Q.index(q)

    def _nsymbol(self, a):
        return self.sigma.index(self._filter(a))

    def _filter(self, z):
        if z in ["Z0", "Z_0"]:
            z = "Z₀"
        if z in ["epsilon"]:
            z = "ε"
        return z

    def _nqsymbol(self, z):
        return self.gamma.index(self._filter(z))

    def _state(self, nq):
        return self.Q.items[nq]

    def _symbol(self, na):
        return self.sigma.items[na]

    def _qsymbol(self, nz):
        return self.gamma.items[nz]

    def _status(self, status, states={}, symbols={}):
        return "|".join(
            f"{states.get(q,q)},\
            {''.join(symbols.get(z,z) for z in r1)}]①  {''.join(symbols.get(z,z) for z in r1)}]②"
            for q, (r1, r2) in status
        )

    def states(self):
        """Gets states

        :returns: States of machine
        :rtype: list"""
        return list(self.Q)

    def symbols(self):
        """Gets terminal symbols

        :returns: Terminal symbols of machine
        :rtype: list"""
        return list(self.sigma)

    def qsymbols(self):
        """Gets stack symbols

        :returns: Stack symbols of machine
        :rtype: list"""
        return list(self.gamma)

    def tokens(self, r):
        """Gets  tokens for stack

        :returns: Stack symbols for machine
        :rtype: list"""
        return re_queque.findall(r)

    def _transition(self, nq_i, na, nz1, nz2, nq_f, nq):
        return (
            self._state(nq_i),
            self._symbol(na),
            self._qsymbol(nz1),
            self._qsymbol(nz2),
        ), (self._state(nq_f), tuple(tuple(self._qsymbol(n) for n in nr) for nr in nq))

    def __setitem__(self, key, value):
        q, a, z1, z2 = key
        q_f, qs_1, q_s2 = value
        return self.add_transition(q, a, z1, z2, q_f, (qs_1, q_s2))

    def _get_transition(self, nq, na, nz1, nz2):
        try:
            return self.ttable[nq][na][nz1][nz2]
        except KeyError:
            return set()

    def expansion_epsilon(self, qs):
        """Applies expansion by epsilon in a set of states

        :param qs: Set of states

        :returns: Set of reachable states from qs"""
        qs__ = defaultdict(set)
        qs__.update(qs)
        change = True
        expanded = False
        while change:
            qs_ = defaultdict(set)
            qs_.update(qs__)
            qs_.update(self.delta(qs__, "ε", index=True))
            if len(set(qs__.keys()) ^ set(qs_.keys())) == 0:
                change = False
            else:
                expanded = True
            qs__ = qs_
        return qs__, expanded

    def delta_extended(self, states, w, index=False):
        """Applies delta extended function

        :param q: Internal state
        :param w: String
        :param index: If returns indexes instead of labesl (default False)

        :returns: Returns internal state after processing the full string"""
        if states is None:
            states = self.create_initial_istate()
        if len(w) == 0:
            res, _ = self.expansion_epsilon(states)
            if index:
                return res
            else:
                return self._index2label(res)
        else:
            *w_, a = w
            q_u = defaultdict(set)
            for k, v in self.delta_extended(states, w_, index=True).items():
                r_ = {k: v}
                q_u.update(self.delta(r_, a, index=True))
            res, _ = self.expansion_epsilon(q_u)
            if index:
                return res
            else:
                return self._index2label(res)

    def _index2label(self, states_):
        return dict(
            [
                (
                    (
                        self._state(nq_f),
                        (
                            tuple(self._qsymbol(z) for z in r[0]),
                            tuple(self._qsymbol(z) for z in r[1]),
                        ),
                    ),
                    set(tuple(self._qsymbol(n) for n in z) for z in nz),
                )
                for (nq_f, r), nz in states_.items()
            ]
        )

    def _label2index(self, states_):
        return dict(
            [
                (
                    (
                        self._nstate(nq_f),
                        (
                            tuple(self._nqsymbol(z) for z in r[0]),
                            tuple(self._nqsymbol(z) for z in r[1]),
                        ),
                    ),
                    set(tuple(self._nqsymbol(n) for n in z) for z in nz),
                )
                for (nq_f, r), nz in states_.items()
            ]
        )

    def create_istates(self, states):
        """Creates a internal state for de PDA

        :param states: List of tuples (state, stack)

        :returns: Usable internal state for the PDA"""

        return dict(
            [
                (
                    (
                        self._nstate(q),
                        tuple(tuple(self._nqsymbol(z) for z in q) for q in qs),
                    ),
                    set(),
                )
                for q, qs in states
            ]
        )

    def create_initial_istate(self):
        """Creates initial internal state for de PDA
        :returns: Usable internal state for the PDA"""
        return dict(
            [
                (
                    (
                        self._nstate(self.q_0),
                        ((self._nqsymbol(self.Z_0),), (self._nqsymbol(self.Z_0),)),
                    ),
                    set(),
                )
            ]
        )

    def delta(self, states, a, index=False):
        """Applies delta function

        :param states: Internal state composed by (state, stack)
        :param a: Symbol

        :returns: Destination state"""
        states_ = defaultdict(OrderedSet)
        na = self._nsymbol(self._filter(a))
        for nq, (ns1, ns2) in states:
            nz1 = ns1[0]
            nz2 = ns2[0]
            stack1 = ns1[1:]
            stack2 = ns2[1:]
            qs = self._get_transition(nq, na, nz1, nz2)
            for nq_f, (r1, r2) in qs:
                r1 = tuple(r1)
                r2 = tuple(r2)
                if len(r1) == 1 and r1[0] == 0:
                    s1_ = stack1
                else:
                    s1_ = r1 + stack1
                if len(r2) == 1 and r2[0] == 0:
                    s2_ = stack2
                else:
                    s2_ = r2 + stack2
                states_[(nq_f, (s1_, s2_))].add((nz1, nz2))
        if index:
            return states_
        else:
            return self._index2label(states_)

    def delta_stepwise(self, w, istates=None, mark_finished=False, index=False):
        """Applies a step of delta extended function

        :param w: String
        :param istates: Internal state where to start (default is initial state)
        :param mark_finished: Mark if finished (default is False)
        :param index: If returns indexes instead of labesl (default False)

        :returns: Tuple with state of precessing at step, consisting of: internal state, procesed symbol and processed string"""
        if istates is None:
            istates = self.create_initial_istate()
        if mark_finished:
            yield self._index2label(istates), "", w, len(w) == 0
        else:
            yield self._index2label(istates), "", w
        ix = 0
        for ix, a in enumerate(w):
            istates = self.delta(istates, a, index=True)
            istates, expanded = self.expansion_epsilon(istates)
            if mark_finished:
                yield self._index2label(istates), a, w[ix + 1 :], (ix + 1) == len(w)
            else:
                yield self._index2label(istates), a, w[ix + 1 :]

    def items(self):
        """Iterator over the transitions

        :returns: Yeilds a tuple transition"""
        for nq_i, t_ in self.ttable.items():
            for na, t__ in t_.items():
                for nz1, t___ in t__.items():
                    for nz2, nq_fs in t___.items():
                        for (nq_f, nr) in nq_fs:
                            yield self._transition(nq_i, na, nz1, nz2, nq_f, nr)

    def step(self, states, a):
        res, _ = self.expansion_epsilon(self.delta(states, a, index=True))
        return self._index2label(res)

    def get_transition(self, q, a, z1, z2):
        """Gets the destintion state or states for state, terminal symbol and stack symbol

        :param q: Source state
        :param a: Terminal symbol
        :param z: Stack symbol
        :returns: Destination state or states"""
        qs = self._get_transition(
            self._nstate(q), self._nsymbol(a), self._nqsymbol(z1), self._nqsymbol(z2)
        )
        return [
            (self._state(q), tuple(tuple(self._qsymbol(s) for s in r) for r in qr))
            for q, qr in qs
        ]

    def add_transition(self, q_i, a, z1, z2, qs, force=False, update=False):
        """Adds a transition

        :param q_i: Source state
        :param a: Terminal ymbol
        :param z1: Stack 1 symbol
        :param z2: Stack 2 symbol
        :param q_s: Destination state (q_f,q_1,q_2)
        :param forece: Force creation of elements
        :returns: None"""
        try:
            nq_i = self.add_state(q_i)
        except AlreadyExistsState:
            nq_i = self._nstate(q_i)
        try:
            na = self.add_symbol(self._filter(a))
        except AlreadyExistsSymbol:
            na = self._nsymbol(self._filter(a))
        try:
            nz1 = self.add_qsymbol(self._filter(z1))
        except AlreadyExistsSymbol:
            nz1 = self._nqsymbol(z1)
        try:
            nz2 = self.add_qsymbol(self._filter(z2))
        except AlreadyExistsSymbol:
            nz2 = self._nqsymbol(z2)

        if force:
            for q_f, rs in qs:
                try:
                    self.add_state(q_f)
                except AlreadyExistsState:
                    pass
                for r in rs:
                    for s in r:
                        try:
                            self.add_qsymbol(s)
                        except AlreadyExistsSymbol:
                            pass
        nqs = [
            (self._nstate(q), tuple(tuple(self._nqsymbol(s) for s in r) for r in qr))
            for q, qr in qs
        ]
        if (
            nq_i in self.ttable
            and na in self.ttable[nq_i]
            and nz1 in self.ttable[nq_i][na]
            and nz2 in self.ttable[nq_i][na][nz1]
        ) and not update:
            raise AlreadyExistsTSPDATransition(q_i, a, z1, z2, self)

        if not nq_i in self.ttable:
            self.ttable[nq_i] = {}
        if not na in self.ttable[nq_i]:
            self.ttable[nq_i][na] = {}
        if not nz1 in self.ttable[nq_i][na]:
            self.ttable[nq_i][na][nz1] = {}
        if not nz2 in self.ttable[nq_i][na][nz1]:
            self.ttable[nq_i][na][nz1][nz2] = set()
        self.ttable[nq_i][na][nz1][nz2].update(nqs)

    def add_state(self, q, initial=False):
        """Adds a state

        :param q: State or states
        :param initial: Set state as a initial
        :returns: Indixes of state or states"""
        if initial:
            self.q_0 = q
        if q in self.Q:
            raise AlreadyExistsState(q)
        if isinstance(q, (set, list)):
            return set(self.Q.add(q_) for q_ in q)
        else:
            return self.Q.add(q)

    def add_next_state(self, initial=False):
        """Adds a state with a infered name based on the number of states q_max. If the name state is already defined it looks the following integer available.

        :param q: State or states
        :param initial: Set state as a initial
        :returns: Next state generated and integer"""
        max_ix = len(self.Q)
        while f"q_{max_ix}" in self.Q:
            max_ix += 1
        q = f"q_{max_ix}"
        self.Q.add(q)
        if initial:
            self.q_0 = q
        return q, max_ix

    def add_symbol(self, a):
        """Adds a symbol

        :param a: Symbol
        :returns: Indixes of symbol"""
        if a in self.sigma:
            raise AlreadyExistsSymbol(self._filter(a))
        return self.sigma.add(a)

    def add_qsymbol(self, z):
        """Adds a stack symbol

        :param a: Symbol
        :returns: Indixes of symbol"""
        z = self._filter(z)
        if z in self.gamma:
            raise AlreadyExistsSymbol(z)
        return self.gamma.add(z)

    def set_initial_state(self, q, force=False):
        """Sets an initial state

        :param q: State
        :param force: If not defined it creates it (default is False)
        :returns: None"""
        if q is None:
            self.q_0 = None
            return None
        if not q in self.Q:
            if force:
                self.add_state(q)
            else:
                raise DoesNotExistsState(q)
        self.q_0 = q

    def set_initial_qsymbol(self, z=None, force=False):
        """Sets an initial symbol for the  stack

        :param q: State
        :param force: If not defined it creates it (default is False)
        :returns: None"""
        if z is None:
            self.Z_0 = "Z₀"
        else:
            if force and not z in self.gamma:
                self.gamma.add(z)
            self.Z_0 = z
        return self.Z_0

    def get_initial_state(self):
        """Gets an initial state

        :returns: State"""
        return self.q_0

    def set_aceptors(self, A, force=False):
        """Sets aceptors states

        :param A: States
        :param force: If not defined it creates it (default is False)
        :returns: None"""
        if force:
            self.add_state(A)
        self.A = set(A)

    def accepts(self, w):
        """Checks if string is accepted

        :param w: String
        :returns: None"""
        try:
            return self.acceptor(set([q for q, _ in self.delta_extended(None, w).keys()]))
        except KeyError:
            return False

    def acceptor(self, q):
        """Checks if state is an acceptor state

        :param q: State or states
        :type: Set

        :returns: None"""
        if isinstance(q, dict):
            q = set([q for q, _ in q.keys()])
            if bool(q.intersection(self.A)):
                return True
        if isinstance(q, list):
            q = set([q for q, _ in q])
            if bool(q.intersection(self.A)):
                return True
        elif isinstance(q, set):
            if bool(q.intersection(self.A)):
                return True
        else:
            if q in self.A:
                return True
        return False

    def stepStatus(self, status):
        """Gives a step and calculates new status for Simulation

        :param Status: Status
        :returns: None"""
        if status.state is None:
            states = self._index2label(self.create_initial_istate())
        else:
            states = status.state

        a = status.get_symbol_tape()
        states = self.step(self._label2index(states), a)
        status.position += 1
        status.step += 1
        status.state = states

    def states2string(self, states):
        """Renders srting with the state of the TSPDA

        :returns: String tiwh the states of teh TSPDA"""
        return " | ".join(
            [
                "{}, {}]① {}]②".format(s, " ".join(r1), " ".join(r2))
                for s, (r1, r2) in states
            ]
        )

    def to_string(self, order_Q=None, order_sigma=None, order_gamma=None):
        """Creates a string

        :param order_Q: Order to print states
        :param order_sigma: Order to print alphabet
        :param order_gamma: Order to print stack alphabet

        :returns: None
        """
        largest_q = max([len(q) for q in self.Q])
        largest_q += 3
        largest_cell = {a: 2 for a in self.sigma}
        ttable = defaultdict(list)
        ttable_ = defaultdict(list)
        for (q_i, a, z1, z2), (q_f, rs) in self.items():
            ttable[(q_i, a, z1, z2)].append(
                f"{z1}/{''.join(rs[0])},{z2}/{''.join(rs[1])}→{q_f}"
            )
            ttable_[(q_i, a)].append(ttable[(q_i, a, z1, z2)][-1])
        for (q_i, a), elements_cell in ttable_.items():
            largest_cell[a] = max(largest_cell[a], len(", ".join(elements_cell)))
        order_Q = list(self.Q) if not order_Q else order_Q
        order_sigma = list(self.sigma) if not order_sigma else order_sigma
        order_gamma = list(self.gamma) if not order_gamma else order_gamma
        strings = []
        # Alphabet line
        strings.append(
            " " * (largest_q + 2)
            + "|"
            + "|".join(
                " {: ^{width}} ".format(a, width=l)
                for a in order_sigma
                if (l := largest_cell[a])
            )
            + "|"
        )
        # Printing states
        for q_i in order_Q:
            q_l = q_i
            if q_i == self.q_0:
                q_l = f"->{q_i}"
            if q_i in self.A:
                q_l = f"{q_l}]"
            if q_i == self.q_0:
                strings.append(" {: <{width}}|".format(q_l, width=largest_q + 1))
            else:
                strings.append("   {: <{width}}|".format(q_l, width=largest_q - 1))
            line = []
            for a in order_sigma:
                s = []
                for z1 in order_gamma:
                    for z2 in order_gamma:
                        e = ttable[(q_i, a, z1, z2)]
                        if len(e) > 0:
                            s.append(", ".join(e))
                line.append(", ".join(s))
            r = "|".join(
                " {: ^{width}} ".format(c, width=l)
                for c, a in zip(line, order_sigma)
                if (l := largest_cell[a])
            )
            strings[-1] += r + "|"
        return "\n".join(strings)

    def save_file(
        self, filename="machine.txt", order_Q=None, order_sigma=None, order_gamma=None
    ):
        """Saves a file

        :param filename: Name of filename (default is machine.txt)
        :param order_sigma: Order to print alphabet
        :param order_gamma: Order to print stack alphabet

        :returns: None
        """
        string = self.to_string(
            order_Q=order_Q, order_sigma=order_sigma, order_gamma=order_gamma
        )
        with open(filename, "w") as f:
            f.write(string)

    def summary(self):
        """Producrs summary of the PDA
        :returns: List with summary"""
        info = [
            "States  : " + ", ".join(self.states()),
            "Sigma   : " + ", ".join(self.symbols()),
            "Gamma   : " + ", ".join(self.qsymbols()),
            "Initial : " + self.q_0,
            "Aceptors: " + ", ".join(self.A),
            "Transitions:\n"
            + "\n".join(
                f" {q_i},{a},{z1}/{''.join(r[0])},{z2}/{''.join(r[1])} → {q_f}"
                for (q_i, a, z1, z2), (q_f, r) in self.items()
            ),
        ]
        return "\n".join(info)

    def print_summary(self):
        """Prints a summary of the PDA"""
        print(self.summary())

    def save_img(
        self,
        filename,
        q_c=set(),
        a_c=set(),
        q_prev=set(),
        symbols={},
        states={},
        format="svg",
        dpi="60.0",
        string=None,
        stack=[],
        status=None,
        one_arc=True,
        finished=False,
        cleanup=True,
    ):
        """Saves machine as an image

        :param filename: Filename of image
        :param q_c: Set of current states to be highlited (default is empty)
        :param a_c: Set of current symbols to be highlited (default is empty)
        :param q_prev: Set of previos states to be highlited (default is empty)
        :param symbols: Replacements of the symbols to show (default is empty)
        :param states: Replacements of the states to show (default is empty)
        :param format: Format of image (default is svg)
        :param dpi: Resolution of image (default is "90.0")
        :param string: Label of string being analysed (default is None)
        :param stack: Status of the stack (default is None)
        :param status: Status of the PDA (default is None)
        :param one_arc: Graph one arc in case of multiple transitions (default is True)
        :param finished: If has pass through final state (default is False)

        :returns: None"""
        dot = self.graph(
            q_c=q_c,
            a_c=a_c,
            q_prev=q_prev,
            symbols=symbols,
            states=states,
            format=format,
            dpi=dpi,
            string=string,
            finished=finished,
            one_arc=one_arc,
            status=status,
            stack=stack,
        )
        dot.render(filename, format=format, cleanup=cleanup)

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
        stack=[],
        status=None,
        one_arc=True,
        finished=False,
    ):
        """Graphs TSPDA

        :param q_c: Set of current states to be highlited (default is empty)
        :param a_c: Set of current symbols to be highlited (default is empty)
        :param q_prev: Set of previos states to be highlited (default is empty)
        :param symbols: Replacements of the symbols to show (default is empty)
        :param states: Replacements of the states to show (default is empty)
        :param format: Format of image (default is svg)
        :param dpi: Resolution of image (default is "90.0")
        :param string: Label of string being analysed (default is None)
        :param stack: Status of the stack (default is None)
        :param status: Status of the TSPDA (default is None)
        :param one_arc: Graph one arc in case of multiple transitions (default is True)
        :param finished: If has pass through final state (default is False)

        :returns: Returns Digraph object from graphviz"""
        if len(q_c) == 0:
            states_ = self._index2label(self.create_initial_istate())
        else:
            states_ = q_c

        f = Digraph(comment="PDAs", format=format)
        f.attr(rankdir="LR", dpi=dpi)
        for i, ((q_c_, stack), zetas) in enumerate(states_.items()):
            with f.subgraph(name=f"cluster_{i}") as f_:
                self._graph(
                    f_,
                    i=i,
                    q_c=q_c_,
                    a_c=a_c,
                    q_prev=q_prev,
                    symbols=symbols,
                    states=states,
                    dpi=dpi,
                    format=format,
                    stack=stack,
                    zetas=zetas,
                    finished=finished,
                    status=status,
                    string=string,
                    one_arc=one_arc,
                )
        return f

    def _graph(
        self,
        f,
        i=0,
        q_c=set(),
        a_c=set(),
        q_prev=set(),
        states={},
        symbols={},
        format="svg",
        dpi="60.0",
        string=None,
        stack=[],
        status=None,
        one_arc=True,
        zetas=[],
        finished=False,
    ):
        label_string = None
        label_stack = None
        if status == None:
            color_state = "lightblue2"
        elif status and len(self.A.intersection(q_c)) > 0:
            color_state = "limegreen"
        else:
            color_state = "orangered"

        if string:
            l, c, r = string
            label_string = f"<TR><TD>{l}</TD> <TD><B>{c}</B></TD> <TD>{r}</TD></TR>"
            if finished and len(r) == 0:
                if self.acceptor(q_c):
                    color_state = "limegreen"
                else:
                    color_state = "orangered"
        if stack:
            label_middle = "".join([symbols.get(r_, r_) for r_ in stack[0]])
            label_stack1 = f"<TR><TD ALIGN='RIGHT'>{label_middle}</TD></TR>"
            label_middle = "".join([symbols.get(r_, r_) for r_ in stack[1]])
            label_stack2 = f"<TR><TD ALIGN='RIGHT'>{label_middle}</TD></TR>"

        f.attr(style="invis", labelloc="b")
        if label_string and label_stack1:
            f.attr(
                label=f"< <TABLE BORDER='0' ><TR><TD><TABLE BORDER='1' CELLBORDER='0' SIDES='TBR'>{label_stack1}</TABLE></TD></TR><TR><TD><TABLE BORDER='1' CELLBORDER='0' SIDES='TBR'>{label_stack2}</TABLE></TD></TR><TR><TD><TABLE BORDER='0'>{label_string}</TABLE></TD></TR></TABLE>>"
            )
        elif label_stack:
            f.attr(
                label=f"< <TABLE BORDER='1' CELLBORDER='0' SIDES='TBR'>{label_stack}</TABLE>>"
            )

        for q, _ in self.Q.map.items():
            if q in self.A:
                shape = "doublecircle"
            else:
                shape = "circle"
            if q in q_c:
                f.node(
                    name=f"{q}_{i}",
                    label=states.get(q, q),
                    shape=shape,
                    color=color_state,
                    style="filled",
                )
            else:
                f.node(name=f"{q}_{i}", label=states.get(q, q), shape=shape)

        edges = defaultdict(list)
        for e, info in enumerate(self.items()):
            (q_i, a, z1, z2), (q_f, (r1, r2)) = info
            r1_ = [symbols.get(r_, r_) for r_ in r1]
            r2_ = [symbols.get(r_, r_) for r_ in r2]
            if (
                (q_f in q_c and q_i in q_prev)
                and (a in a_c or a == "ε")
                and (z1, z2) in zetas
            ):
                edges[(f"{q_i}_{i}", f"{q_f}_{i}")].append(
                    (
                        f'{symbols.get(a,a)},{symbols.get(z1,z1)}/{"".join(r1_)},{symbols.get(z2,z2)}/{"".join(r2_)}',
                        True,
                    )
                )
            else:
                edges[(f"{q_i}_{i}", f"{q_f}_{i}")].append(
                    (
                        f'{symbols.get(a,a)},{symbols.get(z1,z1)}/{"".join(r1_)},{symbols.get(z2,z2)}/{"".join(r2_)}',
                        False,
                    )
                )

        for (q_i, q_f), labels in edges.items():
            if one_arc:
                tags = []
                colored_ = False
                for label, colored in labels:
                    if colored:
                        colored_ = True
                        tags.append(f'<FONT color="{color_state}">{label}</FONT>')
                    else:
                        tags.append(f"{label}")
                tags = f'< {"<BR/>".join(tags)} >'
                if colored_:
                    f.edge(q_i, q_f, label=tags, labelloc="b", color=color_state)
                else:
                    f.edge(q_i, q_f, label=tags, labelloc="b")
            elif not one_arc:
                for label, colored in labels:
                    if colored:
                        f.edge(
                            q_i,
                            q_f,
                            label=label,
                            labelloc="b",
                            color=color_state,
                            fontcolor=color_state,
                        )
                    else:
                        f.edge(q_i, q_f, label=label, labelloc="b")
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
        """Creates an HTML object for the table of the PDA

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
                    labels = []
                    for z1, info_ in self.ttable[self._nstate(q_i)][
                        self._nsymbol(a)
                    ].items():
                        z1 = self._qsymbol(z1)
                        for z2, info in info_.items():
                            z2 = self._qsymbol(z2)
                            for q_f, (r1, r2) in info:
                                r1_ = [
                                    symbols.get(self._qsymbol(r_), self._qsymbol(r_))
                                    for r_ in r1
                                ]
                                r2_ = [
                                    symbols.get(self._qsymbol(r_), self._qsymbol(r_))
                                    for r_ in r2
                                ]
                                labels.append(
                                    f'{symbols.get(a,a)},{symbols.get(z1,z1)}/{"".join(r1_)},{symbols.get(z2,z2)}/{"".join(r2_)}'
                                )
                    vals.append("<br/>".join(labels))
                except KeyError:
                    vals.append(empty_symbol)
            row = "</td><td>".join(vals)
            table += f"<tr><td {final}>{row}</td></tr>"
        table += "</table>"
        return display(HTML(table))

    def save_gif(
        self,
        w,
        filename="tspda.gif",
        symbols={},
        states={},
        dpi="90",
        show=True,
        loop=0,
        duration=500,
    ):
        """Saves an animation of  machine

        :param w: String to analysed during animation
        :param filename: Name of gif (default is "tspda.gif")
        :param symbols: Replacements of the symbols to show (default is empty)
        :param states: Replacements of the states to show (default is empty)
        :param dpi: Resolution of image (default is "90.0")
        :param show: In interactive mode return gif
        :param loop: Number of loops in annimation, cero is forever (default is 0)
        :param duration: Duration in msegs among steps (default is 500)
        :returns: None or HTML for Ipython"""
        dirpath = tempfile.mkdtemp()
        i = 0
        images = []
        q_prev = set()
        max_images_height = 1
        for q, a, w_, finished in self.delta_stepwise(
            w, mark_finished=True, index=True
        ):
            filename_ = os.path.join(dirpath, f"{i}")
            fin = len(w) - len(w_)
            processed = w[: max(0, int(i / 2) - 1)]
            a = a if a else " "
            g = self.save_img(
                filename_,
                q_c=q,
                a_c=set([a]),
                q_prev=q_prev,
                finished=finished,
                symbols=symbols,
                states=states,
                dpi=dpi,
                string=(processed, a, w_),
                format="png",
            )
            q_prev = set([q_c for q_c, _ in q])
            im = Image.open(filename_ + ".png")
            width, height = im.size
            max_images_height = max(max_images_height, height)
            images.append(im)
            i += 1
            filename_ = os.path.join(dirpath, f"{i}")
            g = self.save_img(
                filename_,
                q_c=q,
                symbols=symbols,
                dpi=dpi,
                string=(processed, a, w_),
                finished=finished,
                format="png",
            )
            im = Image.open(filename_ + ".png")
            if i == 0 or finished:
                images.append(im)
                images.append(im)
                images.append(im)
                images.append(im)
            images.append(im)
            i += 1
        for i, im in enumerate(images):
            im2 = Image.new("RGB", (width, max_images_height), (255, 255, 255))
            width, height = im.size
            im2.paste(im)
            images[i] = im2

        images[0].save(
            filename,
            save_all=True,
            append_images=images[1:],
            optimize=False,
            duration=duration,
            loop=loop,
        )
        if show:
            return HTML(f'<img src="{filename}">')
        else:
            return
