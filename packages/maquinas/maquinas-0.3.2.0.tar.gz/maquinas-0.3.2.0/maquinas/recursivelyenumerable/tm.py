# Base class for Finite Machines
from maquinas.exceptions import *
from ordered_set import OrderedSet
import re
import tempfile
import os
from collections import defaultdict

from PIL import Image
from IPython.display import display, HTML
from graphviz import Digraph

re_tape = re.compile(r'(\[B\]|epsilon|"[^"]+"|\w)')


class TuringMachine:
    """Turing machine"""

    def __init__(
        self, Q=[], sigma=[], gamma=[], B="𝖁", q_0=None, A=[], delta={}, force=False
    ):
        """Common class for Turing Machine

        :param Q: Ordered set of states (default is empty).
        :param sigma: Ordered set of terminal symbols (default is empty).
        :param gamma: Ordered set of tape symbols (default is empty).
        :param B: Blank symbol (default 𝖁).
        :param q_0: Initial state (default None).
        :param A: Set of acceptor states (default is empty).
        :param delta: List of transitions with the form tupla of tupla of q_i and a, and the list of q_f, a symbol and direction (default is empty).
        :param force: If True and states or symbols do not exists create them (default is False).
        :type force: bool
        """
        self.sigma = OrderedSet()
        self.B = B
        self.i = 0
        self.gamma = OrderedSet()
        self.gamma.add(self.B)
        self.gamma.update([self._filter(g) for g in gamma])
        self.gamma.update(sigma)
        self.sigma.update(sigma)
        self.Q = OrderedSet(Q)
        self.set_initial_state(q_0)
        self.set_aceptors(A, force=force)
        self.ttable = {}
        for (q_i, a), qs in delta:
            self.add_transition(
                q_i,
                self._filter(a),
                [(q_f, self._filter(a), self._ndir(Dir)) for q_f, a, Dir in qs],
            )
        self.curr = 0
        self.tape = ((), (self.B))

    def __getitem__(self, key):
        q, a = key
        return self.get_transition(q, a)

    def _nstate(self, q):
        return self.Q.index(q)

    def _nsymbol(self, a):
        return self.sigma.index(a)

    def _filter(self, t):
        if t == "[B]":
            return self.B
        elif t.lower() == "blank":
            return self.B
        return t

    def _dir(self, d):
        if d == 1:
            return "R"
        elif d == -1:
            return "L"
        else:
            return "N"

    def _ndir(self, d):
        if d == "R":
            return 1
        elif d == "L":
            return -1
        else:
            return 0

    def _ntsymbol(self, t):
        try:
            return self.gamma.index(self._filter(t))
        except KeyError as c:
            raise DoesNotExistsSymbol(c)

    def _state(self, nq):
        return self.Q.items[nq]

    def _symbol(self, na):
        return self.sigma.items[na]

    def _tsymbol(self, nz):
        return self.gamma.items[nz]

    def _status(self, status, states={}, symbols={}):
        return "|".join(f"{states.get(s,s)}" for s, _, _, _ in status)

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

    def tsymbols(self):
        """Gets tape symbols

        :returns: Tape symbols of machine
        :rtype: list"""
        return list(self.gamma)

    def tokens(self, r):
        """Gets  tokens for tape

        :returns: Tape symbols for machine
        :rtype: list"""
        return re_tape.findall(r)

    def _transition(self, nq_i, nt, nq_f, nt_, Dir):
        return (self._state(nq_i), self._tsymbol(nt)), (
            self._state(nq_f),
            self._tsymbol(nt_),
            Dir,
        )

    def __setitem__(self, key, value):
        q, t = key
        q_f, t_, Dir = value
        return self.add_transition(q, t, q_f, t_, Dir)

    def _get_transition(self, nq, nt):
        try:
            return self.ttable[nq][nt]
        except KeyError:
            return set()

    def delta(self, states):
        """Applies delta function

        :param states: Internal state composed by (state, tape negative positions, tape positive positions, and (current position, symbol)
        :param a: Symbol

        :returns: Destination state"""
        states_ = set()
        for nq, tn, tp, (c, a) in states:
            if c < 0:
                try:
                    na = tn[-c]
                except IndexError:
                    tn = tn + tuple(self.B for _ in range(len(tn), 1 - c))
                    na = tn[-c]
            else:
                try:
                    na = tp[c]
                except IndexError:
                    tp = tp + tuple(self.B for _ in range(len(tp), c + 1))
                    na = tp[c]
            qs = self._get_transition(nq, na)
            for nq_f, t_, Dir in qs:
                if c < 0:
                    tn = list(tn)
                    tn[c] = t_
                elif c >= 0:
                    tp = list(tp)
                    tp[c] = t_
                c = c + Dir
                if c < 0 and len(tn) <= abs(c):
                    tn = list(tn)
                    tn.append(self._ntsymbol(self.B))
                if c >= 0 and len(tp) <= abs(c):
                    tp = list(tp)
                    tp.append(self._ntsymbol(self.B))
                states_.add(
                    (nq_f, tuple(tn), tuple(tp), (len(tn) + c, self._tsymbol(na)))
                )
        return states_

    def _tape(self, nt, pt):
        return [t for t in reversed(tuple(nt))] + [t for t in pt]

    def delta_stepwise(self, w, q=None, max_steps=0):
        """Applies a step of delta extended function

        :param w: String
        :param q: Internal state where to start (default is initial state)
        :param max_steps: Maximun number of steps to consider

        :returns: Tuple with state of precessing at step, consisting of: state, left tape, right tape, (position, processed string)"""
        if q is None:
            states = set(
                [
                    (
                        self._nstate(self.q_0),
                        (),
                        tuple(self._ntsymbol(a) for a in w),
                        (0, ""),
                    )
                ]
            )
            yield self._index2label(states)
        steps = 0
        A = set(self._nstate(a) for a in self.A)
        while (
            len(states) > 0
            and len(set([q for q, _, _, _ in states]).intersection(self.A)) == 0
        ):
            states = self.delta(states)
            steps += 1
            yield self._index2label(states)
            if set([s for s, _, _, _ in states]).intersection(A):
                break
            if max_steps and steps >= max_steps:
                break

    def create_initial_istate(self, w):
        """Creates an initial internal state

        :param w: string for the tape

        :return: Returns internal initial state"""
        return set(
            [(self._nstate(self.q_0), (), tuple(self._ntsymbol(a) for a in w), (0, ""))]
        )

    def delta_extended(self, states, w, max_steps=None):
        """Applies delta extended function

        :param states: Internal states
        :param w: String
        :param max_steps: Maximum number of states

        :returns: Returns internal state after processing the full string"""

        if states is None:
            states = self.create_initial_istate(w)
        steps = 0
        while (
            len(states) > 0
            and len(set([self._state(q) for q, _, _, _ in states]).intersection(self.A))
            == 0
        ):
            states = self.delta(states)
            steps += 1
            res = [(q, tn, tp, c) for q, tn, tp, c in states]
            if max_steps and steps >= max_steps:
                return []
        return self._index2label(res)

    def _index2label(self, states_):
        return [
            (
                self._state(q),
                tuple(self._tsymbol(s) for s in l),
                tuple(self._tsymbol(s) for s in r),
                c,
            )
            for q, l, r, c in states_
        ]

    def _label2index(self, states):
        return [
            (
                self._nstate(q),
                tuple(self._ntsymbol(s) for s in l),
                tuple(self._ntsymbol(s) for s in r),
                c,
            )
            for q, l, r, c in states
        ]

    def items(self):
        """Iterator over the transitions

        :returns: Yeilds a tuple transition"""
        for nq_i, val in self.ttable.items():
            for nt, nq_fs in val.items():
                for (nq_f, nt_, Dir) in nq_fs:
                    yield self._transition(nq_i, nt, nq_f, nt_, Dir)

    def step(self, states):
        return self._index2label(self.delta(states))

    def get_transition(self, q, a):
        """Gets the destintion state or states for state, terminal symbol and stack symbol

        :param q: Source state
        :param a: Terminal symbol
        :returns: Destination state or states"""

        qs = self._get_transition(self._nstate(q), self._nsymbol(a))
        return [(self._state(s), self.tsymbol(a), d) for s, a, d in qs]

    def add_transition(self, q_i, t, qs, force=False, update=False):
        """Adds a transition

        :param q_i: Source state
        :param t: Tape symbol
        :param q_s: Destination state (q_f,t_2,dir)
        :param force: Force creation of elements
        :returns: None"""
        try:
            nq_i = self.add_state(q_i)
        except AlreadyExistsState:
            nq_i = self._nstate(q_i)
        try:
            nt = self.add_tsymbol(t)
        except AlreadyExistsSymbol:
            nt = self._ntsymbol(t)

        #TODO: Differenciate among sigma and gamma

        if force:
            for q_f, a_, _ in qs:
                try:
                    self.add_state(q_f)
                except AlreadyExistsState:
                    pass
                try:
                    self.add_tsymbol(a_)
                except AlreadyExistsSymbol:
                    pass

        qs = [(self._nstate(q), self._ntsymbol(t), Dir) for q, t, Dir in qs]

        if nq_i in self.ttable and nt in self.ttable[nq_i]:
            if update:
                self.ttable[nq_i][nt].update(qs)
            else:
                raise AlreadyExistsTMTransition(q_i, t, self)
        else:
            if not nq_i in self.ttable:
                self.ttable[nq_i] = {}
            if not nt in self.ttable[nq_i]:
                self.ttable[nq_i][nt] = set()
            self.ttable[nq_i][nt].update(qs)

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
        if a in self.gamma:
            raise AlreadyExistsSymbol(a)
        return self.sigma.add(a)
        return self.gamma.add(a)

    def add_tsymbol(self, t):
        """Adds a tape symbol

        :param t: Tape xymbol
        :returns: Indixes of symbol"""
        if t in self.gamma:
            raise AlreadyExistsSymbol(t)
        return self.gamma.add(t)

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

    def stepStatus(self, status):
        """Gives a step and calculates new status for Simulation

        :param Status: Status
        :returns: None"""
        if status.state is None:
            states = self._index2label(self.create_initial_istate(status.string))
        else:
            states = status.state
        states = self.step(self._label2index(states))
        status.position += 1
        status.step += 1
        status.state = states

    def accepts(self, w, max_steps=0):
        """Checks if string is accepted

        :param w: String
        :returns: None"""
        try:
            return self.acceptor(self.delta_extended(None, w, max_steps=max_steps))
        except:
            return False

    def acceptor(self, states):
        """Checks if state is an acceptor state

        :param states: State or states
        :type: Set

        :returns: None"""
        final = set([q for q, _, _, _ in states])
        if bool(final.intersection(self.A)):
            return True
        return False

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
        status=None,
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
        :param status: Status of the TM (default is None)

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
            status=status,
        )
        dot.render(filename, format="png", cleanup=True)

    def states2string(self, states):
        """Renders srting with the state of the TM

        :returns: String tiwh the states of the TM"""
        res = []
        for q, nt, pt, (c, a) in states:
            tape = self._tape(nt, pt)
            res.append(
                "{}, … {} _{}_ {} …".format(
                    q,
                    "".join([t for t in tape[:c]]),
                    tape[c],
                    "".join([t for t in tape[c + 1 :]]),
                )
            )
        return "|".join(res)

    def to_string(self, order_Q=None, order_gamma=None):
        """Creates a string

        :param order_Q: Order to print states
        :param order_sigma: Order to print alphabet
        :param order_gamma: Order to print stack alphabet

        :returns: None
        """
        largest_q = max([len(q) for q in self.Q])
        largest_q += 3
        largest_cell = {a: 2 for a in self.gamma}
        ttable = defaultdict(list)
        ttable_ = defaultdict(list)
        for (q_i, a), (q_f, a_, Dir) in self.items():
            ttable[(q_i, a)].append(f"{a}/{a_}→{q_f}:{self._dir(Dir)}")
        for (q_i, a), elements_cell in ttable.items():
            largest_cell[a] = max(largest_cell[a], len(",".join(elements_cell)))
        order_Q = list(self.Q) if not order_Q else order_Q
        order_gamma = list(self.gamma) if not order_gamma else order_gamma
        strings = []
        # Alphabet line
        strings.append(
            " " * (largest_q + 2)
            + "|"
            + "|".join(
                " {: ^{width}} ".format(a, width=l)
                for a in order_gamma
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
            for a in order_gamma:
                e = ttable[(q_i, a)]
                line.append(",".join(e))
            r = "|".join(
                " {: ^{width}} ".format(c, width=l)
                for c, a in zip(line, order_gamma)
                if (l := largest_cell[a])
            )
            strings[-1] += r + "|"
        return "\n".join(strings)

    def save_file(
        self, filename="machine.txt", order_Q=None, order_gamma=None
    ):
        """Saves a file

        :param filename: Name of filename (default is machine.txt)
        :param order_gamma: Order to print stack alphabet

        :returns: None
        """
        string = self.to_string(
            order_Q=order_Q, order_gamma=order_gamma
        )
        with open(filename, "w") as f:
            f.write(string)


    def summary(self):
        """Producrs summary of the PDA
        :returns: List with summary"""
        info = [
            "States  : " + ", ".join(self.states()),
            "Sigma   : " + ", ".join(self.symbols()),
            "Gamma   : " + ", ".join(self.tsymbols()),
            "Initial : " + self.q_0,
            "Aceptors: " + ", ".join(self.A),
            "Transitions:\n"
            + "\n".join(
                f" {q_i},{t}/{t_} → {q_f}:{self._dir(Dir)}"
                for (q_i, t), (q_f, t_, Dir) in self.items()
            ),
        ]
        return "\n".join(info)

    def print_summary(self):
        """Prints a summary of the PDA"""
        print(self.summary())

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
        status=None,
        one_arc=True,
        finished=False,
    ):
        """Graphs TM

            :param q_c: Set of current states to be highlited (default is empty)
            :param a_c: Set of current symbols to be highlited (default is empty)
            :param q_prev: Set of previos states to be highlited (default is empty)
            :param symbols: Replacements of the symbols to show (default is empty)
            :param states: Replacements of the states to show (default is empty)
            :param format: Format of image (default is svg)
        :param dpi: Resolution of image (default is "60.0")
            :param string: Label of string being analysed (default is None)
            :param status: Status of the TM (default is None)
            :param one_arc: Graph one arc in case of multiple transitions (default is True)
            :param finished: If has pass through final state (default is False)

            :returns: Returns Digraph object from graphviz"""
        if len(q_c) == 0:
            states_ = [(self._nstate(self.q_0), (), (), (0, ""))]
        else:
            states_ = q_c

        f = Digraph(comment="TM", format=format)
        f.attr(rankdir="LR", dpi=dpi)
        for i, (q_c_, nt, pt, (c, a)) in enumerate(states_):
            if len(q_c) > 0:
                q_c_ = set([q_c_])
            else:
                q_c_ = []
            with f.subgraph(name=f"cluster_{i}") as f_:
                self._graph(
                    f_,
                    i=i,
                    q_c=q_c_,
                    a_c=set([a]),
                    q_prev=q_prev,
                    symbols=symbols,
                    states=states,
                    tape=self._tape(nt, pt),
                    pos=c + len(nt),
                    dpi=dpi,
                    format=format,
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
        tape=None,
        status=None,
        one_arc=True,
        pos=None,
        finished=False,
    ):
        label_tape = None
        if len(self.A.intersection(q_c)) > 0:
            color_state = "limegreen"
        else:
            if status == None:
                color_state = "lightblue2"
            else:
                color_state = "orangered"

        f.attr(style="invis", labelloc="b")

        if tape:
            cells = []
            for i, c in enumerate(tape):
                if i == pos:
                    cells.append(f'<TD BGCOLOR="{color_state}">{symbols.get(c,c)}</TD>')
                else:
                    cells.append(f"<TD>{symbols.get(c,c)}</TD>")
            label_tape = f"< <TABLE BORDER='0' CELLBORDER='1' SIDES='TBRL'><TR>{' '.join(cells)}</TR></TABLE> >"

        if label_tape:
            f.attr(label=label_tape)

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
            (q_i, a), (q_f, a_, Dir) = info
            if (q_f in q_c and q_i in q_prev) and (a in a_c):
                edges[(f"{q_i}_{i}", f"{q_f}_{i}")].append(
                    (f"{symbols.get(a,a)}/{symbols.get(a_,a_)},{self._dir(Dir)}", True)
                )
            else:
                edges[(f"{q_i}_{i}", f"{q_f}_{i}")].append(
                    (f"{symbols.get(a,a)}/{symbols.get(a_,a_)},{self._dir(Dir)}", False)
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
            s_order = list(self.gamma)
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
                    for q_f, r, Dir in self.ttable[self._nstate(q_i)][
                        self._ntsymbol(a)
                    ]:
                        labels.append(
                            f"/{symbols.get(self._tsymbol(r),self._tsymbol(r))}→{self._state(q_f)},{self._dir(Dir)}"
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
        filename="tm.gif",
        symbols={},
        states={},
        dpi="90",
        show=True,
        loop=0,
        duration=500,
        max_steps=1000,
    ):
        """Saves an animation of  machine

        :param w: String to analysed during animation
        :param filename: Name of gif (default is tm.gif")
        :param symbols: Replacements of the symbols to show (default is empty)
        :param states: Replacements of the states to show (default is empty)
        :param dpi: Resolution of image (default is "90.0")
        :param show: In interactive mode return gif
        :param loop: Number of loops in annimation, cero is forever (default is 0)
        :param duration: Duration in msegs among steps (default is 500)
        :param max_steps: Maximum number of steps to consider (default is 1000)
        :returns: None or HTML for Ipython"""
        dirpath = tempfile.mkdtemp()
        i = 0
        images = []
        q_prev = set()
        max_images_height = 1
        status = None
        for ii, q in enumerate(self.delta_stepwise(w)):
            if len(q) == 0:
                status = self.accept(q_prev)
                if status:
                    break
                q = q_prev
                q_prev = set()
            if ii >= max_steps:
                break
            filename_ = os.path.join(dirpath, f"{i}")
            g = self.save_img(
                filename_,
                q_c=q,
                q_prev=set([q_c for q_c, _, _, _ in q]),
                symbols=symbols,
                states=states,
                status=status,
                dpi=dpi,
                format="png",
            )
            q_prev = q
            im = Image.open(filename_ + ".png")
            width, height = im.size
            max_images_height = max(max_images_height, height)
            images.append(im)
            i += 1
            filename_ = os.path.join(dirpath, f"{i}")
            g = self.save_img(
                filename_,
                q_c=q,
                status=status,
                symbols=symbols,
                states=states,
                dpi=dpi,
                format="png",
            )
            im = Image.open(filename_ + ".png")
            images.append(im)
            i += 1
        images.append(im)
        images.append(im)
        images.append(im)
        images.append(im)

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
            duration=500,
            loop=loop,
        )
        if show:
            return HTML(f'<img src="{filename}">')
        else:
            return
