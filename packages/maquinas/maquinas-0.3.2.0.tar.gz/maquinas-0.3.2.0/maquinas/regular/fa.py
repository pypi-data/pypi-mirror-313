# Base class for Finite Machines
from maquinas.exceptions import *
from ordered_set import OrderedSet
import tempfile
import os
from PIL import Image
from IPython.display import display, HTML, Markdown, clear_output


class FiniteAutomaton:
    """Common class for finite automaton

    :param Q: Ordered set of states (default is empty).
    :param sigma: Ordered set of symbols (default is empty).
    :param q_0: Initial state (default None).
    :param A: Set of acceptor states (default is empty).
    :param delta: List of transitions with the form tupla of tupla of q_i and a, and q_f (default is empty).
    :param force: If True and states or symbols do not exists create them (default is False).
    :type force: bool
    :param epsilon: The Finite Automaton includes epsilon (default is None)
    :type epsilon: bool
    """

    def __init__(
        self, Q=[], sigma=[], q_0=None, A=[], delta=[], force=False, epsilon=False
    ):
        self.sigma = OrderedSet()
        self.e = epsilon
        if epsilon:
            self.sigma.add(epsilon)
        self.sigma.update(sigma)
        self.Q = OrderedSet(Q)
        self.set_initial_state(q_0, force=force)
        self.set_aceptors(A, force=force)
        self.ttable = {}
        for (q_i, a), q_f in delta:
            self.add_transition(q_i, a, q_f, force=force)

    def __getitem__(self, key):
        q, a = key
        return self.get_transition(q, a)

    def _nstate(self, q):
        """Gets index of state or states given a state or states

        :param q: State or states
        :returns: index of state q or indexes of states q"""
        if isinstance(q, set) or isinstance(q, list):
            return set(self.Q.index(n) for n in q)
        if q is None:
            return set()
        else:
            return self.Q.index(q)

    def _nsymbol(self, a):
        """Gets index of symbol given a symbol

        :param a: Symbol a
        :returns: index of symbol a"""
        return self.sigma.index(a)

    def _state(self, nq):
        """Gets state or states given an index or indexes

        :param nq: Index of state
        :returns: State or states"""
        if isinstance(nq, set):
            return set(self.Q.items[n] for n in nq)
        else:
            return self.Q.items[nq]

    def _symbol(self, na):
        """Gets symbol given an index of a symbol

        :param na: Index of symbol
        :returns: Symbol"""
        return self.sigma.items[na]

    def states(self):
        """Gets states

        :returns: States of machine
        :rtype: list"""
        return list(self.Q)

    def symbols(self):
        """Gets symbols

        :returns: Symbols of machine
        :rtype: list"""
        return list(a for a in self.sigma if not a == self.e)

    def _transition(self, nq_i, na, nq_f):
        """Gets transition triplet given the index of states and symbol

        :param nq_i: Index of source state
        :param na: Index of symbol
        :param nq_f: Index of destination state
        :returns: Transition tuple"""
        return (self._state(nq_i), self._symbol(na)), self._state(nq_f)

    def __setitem__(self, key, value):
        q, a = key
        return self.add_transition(q, a, value)

    def _get_transition(self, nq, na):
        """Gets the index or indexes of the destintion states for a index state and symbol

        :param nq: Index of source state
        :param na: Index of symbol
        :returns: Index of destination state or states"""
        if isinstance(nq, set) or isinstance(nq, list):
            new = set()
            for nq_ in nq:
                try:
                    new = new | self.ttable[nq_][na]
                except KeyError:
                    pass
            return new
        else:
            try:
                return self.ttable[nq][na]
            except KeyError:
                raise DoesNotExistsTransition(nq, na)

    def get_transition(self, q, a):
        """Gets the destintion state or states for state and symbol

        :param nq: Source state
        :param na: Symbol
        :returns: Destination state or states"""
        res = self._get_transition(self._nstate(q), self._nsymbol(a))
        if isinstance(res, set) or isinstance(res, list):
            return set([self._state(q) for q in res])
        else:
            return self._state(res)

    def items(self):
        """Iterator over the transitions

        :returns: Yeilds a tuple transition"""
        for nq_i, t_ in self.ttable.items():
            for na, nq_f in t_.items():
                yield self._transition(nq_i, na, nq_f)

    def print_summary(self, symbols={}, states={}, **args):
        """Print a summary of the AF

        :param symbols: Replacements of the symbols to print
        :param states: Replacements of the states to print
        :param args: Parameters for the print
        :returns: None"""
        print(self.summary(symbols=symbols, states=states), **args)

    def print_transitions(self, w, symbols={}, states={}, **args):
        """Print a transition for the string w

        :param w: Replacements of the symbols to print
        :param states: Replacements of the states to print
        :param args: Parameters for the print
        :returns: None"""
        for q, a, w_ in self.delta_stepwise(w):
            if a:
                print(f"{symbols.get(a,a)} → {states.get(q,q)}", end=",\n ", **args)
            else:
                print(f"{states.get(q,q)}", end=",\n ", **args)

    def add_transition(self, q_i, a, q_f, force=False, update=False):
        """Adds a transition

        :param q_i: Source state
        :param a: Symbol
        :param q_f: Destination state
        :params force: Forces the creation of new symbols or states
        :params update: If transition exists, updates it
        :returns: None"""
        if a == "epsilon":
            a = "ε"
        try:
            na = self._nsymbol(a)
        except KeyError:
            if force and a != "ε":
                na = self.add_symbol(a)
            else:
                raise DoesNotExistsSymbol(a)
        try:
            nq_i = self._nstate(q_i)
        except KeyError:
            if force:
                nq_i = self.add_state(q_i)
            else:
                raise DoesNotExistsState(q_i)

        try:
            nq_f = self._nstate(q_f)
        except KeyError:
            if force:
                nq_f = self.add_state(q_f)
            else:
                raise DoesNotExistsState(q_f)

        if nq_i and nq_i in self.ttable and na in self.ttable[nq_i]:
            if update:
                self.ttable[nq_i][na].update(nq_f)
            else:
                raise AlreadyExistsTransition(q_i, a, self)
        else:
            try:
                self.ttable[nq_i][na] = nq_f
            except KeyError:
                self.ttable[nq_i] = {}
                self.ttable[nq_i][na] = nq_f

    def add_state(self, q, initial=False):
        """Adds a state

        :param q: State or states
        :param initial: Set state as a initial
        :returns: Indixes of state or states"""
        if initial:
            self.q_0 = q
        if isinstance(q, (set, list)):
            return set(self.Q.add(q_) for q_ in q)
        else:
            if q in self.Q:
                raise AlreadyExistsState(q)
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
        if a == "epsilon":
            a = "ε"
        if a in self.sigma:
            raise AlreadyExistsSymbol(a)
        return self.sigma.add(a)

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

    def get_aceptors(self):
        """Gets aceptors states

        :returns: States"""
        return self.A

    def autorename(self, start=0, avoid=[]):
        """Autorenames the states with a patter of q_n, where n is a consicutive integer

        :param start: Staring numbering (default is 0)
        :param avoid: List of labelings to avoid (default is empty)
        :returns: None"""
        replacements = [(q, f"q_{start+ix}") for q, ix in self.Q.map.items()]
        ix = len(self.Q) + start
        new_A = set()
        while len(replacements) > 0:
            old, new = replacements.pop(0)
            if new == old:
                if old in self.A:
                    new_A.add(new)
                if old == self.q_0:
                    self.q_0 = new
                continue
            elif new in self.Q or new in avoid:
                replacements.append((old, f"q_{ix}"))
                ix += 1
            else:
                self.replace_state(old, new)
                if old in self.A:
                    new_A.add(new)
                if old == self.q_0:
                    self.q_0 = new
        self.A = new_A

    def remove_states(self, states):
        """Remove states

        :param states: List of states to remove
        :returns: None"""
        Q_ = OrderedSet()
        ttable_ = {}
        for q in self.Q:
            if not q in states:
                Q_.add(q)

        ttable_ = {}
        for nq_i, tt in self.ttable.items():
            q_i = self.Q.items[nq_i]
            if q_i in states:
                continue
            nq_i_ = Q_.map[q_i]
            for na, nqs in tt.items():
                if isinstance(nqs, set):
                    qs = [self.Q.items[q] for q in nqs]
                    res = set([Q_.index(q) for q in qs if not q in states])
                else:
                    q = self.Q.items[nqs]
                    if q in states:
                        continue
                    res = Q_.index(q)
                try:
                    ttable_[nq_i_][na] = res
                except KeyError:
                    ttable_[nq_i_] = {}
                    ttable_[nq_i_][na] = res
        self.Q = Q_
        self.ttable = ttable_

    def remove_sink_states(self):
        """Remove states that do no go to any place

        :returns: None"""
        Q_ = OrderedSet()
        idx_remove = set()
        for nq, q in enumerate(self.Q):
            if not q in self.A:
                if not nq in self.ttable:
                    idx_remove.add(nq)
                    continue
            destination = set()
            # If state is loopy
            for na, a in enumerate(self.sigma):
                try:
                    res = self.ttable[nq][na]
                except KeyError:
                    continue
                if isinstance(res, set):
                    destination = destination | res
                else:
                    destination.add(res)
            if len(destination) == 1 and nq in destination and q not in self.A:
                idx_remove.add(nq)
                continue
            Q_.add(q)

        ttable_ = {}
        for nq_i_, q_i in enumerate(Q_):
            nq_i = self.Q.map[q_i]
            for na, a in enumerate(self.sigma):
                try:
                    res = self.ttable[nq_i][na]
                except KeyError:
                    continue
                if isinstance(res, set):
                    qs = [self.Q.items[nq] for nq in res if not nq in idx_remove]
                    res = set([Q_.index(q) for q in qs])
                else:
                    if res in idx_remove:
                        continue
                    q = self.Q.items[res]
                    res = Q_.index(q)
                try:
                    ttable_[nq_i_][na] = res
                except KeyError:
                    ttable_[nq_i_] = {}
                    ttable_[nq_i_][na] = res
        self.Q = Q_
        self.ttable = ttable_

    def _status(self, status, states={}, symbols={}):
        return status

    def step(self, q, a):
        return self.delta(q, a)

    def stepStatus(self, status):
        """Gives a step and calculates new status for Simulation

        :param Status: Status
        :returns: None"""
        if status.state is None:
            q_c = self.q_0
        else:
            q_c = status.state

        a = status.get_symbol_tape()
        q_c = self.step(q_c, a)
        status.position += 1
        status.step += 1
        status.state = q_c

    def accepts(self, w):
        """Checks if string is accepted

        :param w: String
        :returns: None"""
        try:
            return self.acceptor(self.delta_extended(None, w))
        except KeyError:
            return False
        except DoesNotExistsTransition:
            return False

    def acceptor(self, q):
        """Checks if state is an acceptor state

        :param q: State or states
        :returns: None"""
        if isinstance(q, set):
            if len(q.intersection(self.A)) > 0:
                return True
        else:
            if q in self.A:
                return True
        return False

    def replace_symbol(self, old, new):
        """Replace a symbol

        :param old: Symbol to be replaced
        :param new: Symbol to replace with
        :returns: None"""
        ix = self.sigma.index(old)
        del self.sigma.map[old]
        self.sigma.map[new] = ix
        self.sigma.items[ix] = new

    def replace_state(self, old, new):
        """Replace a state

        :param old: State to be replaced
        :param new: State to replace with
        :returns: None"""
        if new in self.Q:
            raise AlreadyExistsState(new)
        ix = self.Q.index(old)
        del self.Q.map[old]
        self.Q.map[new] = ix
        self.Q.items[ix] = new
        if old == self.q_0:
            self.q_0 = new

    def add_error_state(self, e_label="q_E"):
        """Adds a error state (sink state)

        :param e_label: Label for the error state
        :returns: None"""
        empty_cell = False
        for nq, q in enumerate(self.Q):
            for na, a in enumerate(self.sigma):
                if not nq in self.ttable:
                    empty_cell = True
                    break
                elif not na in self.ttable[nq] or (
                    isinstance(self.ttable[nq][na], set)
                    and len(self.ttable[nq][na]) == 0
                ):
                    empty_cell = True
                    break
            if empty_cell:
                break
        if empty_cell:
            self.add_state(e_label)
            for nq, q in enumerate(self.Q):
                for na, a in enumerate(self.sigma):
                    if (
                        not nq in self.ttable
                        or not na in self.ttable[nq]
                        or (
                            isinstance(self.ttable[nq][na], set)
                            and len(self.ttable[nq][na]) == 0
                        )
                    ):
                        self.add_transition(q, a, e_label, force=True)

    def reachable_states(self):
        """Calculate the set of states which are reacheble

        :returns: List of reachable states"""
        # https://en.wikipedia.org/wiki/DFA_minimization#Unreachable_states
        reachable = set([self.q_0])
        new = set([self.q_0])
        while len(new) > 0:
            temp = set()
            for q in new:
                for a in self.sigma:
                    try:
                        states = self.get_transition(q, a)
                        if isinstance(states, set):
                            temp.update(states)
                        else:
                            temp.add(states)
                    except DoesNotExistsTransition:
                        pass
            new = temp.difference(reachable)
            reachable = reachable.union(new)
        return reachable

    def unreachable_states(self):
        """Calculate the set of states which are unreacheble

        :returns: List of unreachable states"""
        return set(self.Q.difference(self.reachable_states()))

    def remove_unreachable(self):
        """Removes the set of states which are unreacheble

        :returns: List of unreachable states"""
        self.remove_states(self.unreachable_states())

    def to_string(self, order_Q=None, order_sigma=None):
        """Creates a string

        :param order_Q: Order to print states
        :param order_sigma: Order to print vocabulary

        :returns: None
        """
        largest_sigma = max([len(a) for a in self.sigma])
        largest_q = max([len(q) for q in self.Q])
        largest_q += 3
        largest_cell = 0
        for (q_i, a), q_f in self.items():
            largest_cell = max(largest_cell, len(",".join(q_f)))
        largest_cell += 2
        if not order_Q:
            order_Q = list(self.Q)
        if not order_sigma:
            order_sigma = list(self.sigma)
        strings = []
        # Alphabet line
        strings.append(
            " " * (largest_q + 2)
            + "|"
            + "|".join("{: ^{width}}".format(a, width=largest_cell) for a in order_sigma)
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
                try:
                    s = self[(q_i, a)]
                    if isinstance(s, set):
                        line.append(",".join(s))
                    else:
                        line.append(s)
                except DoesNotExistsTransition:
                    line.append("")
            r = "|".join("{: ^{width}}".format(c, width=largest_cell) for c in line)
            strings[-1] += r + "|"
        return "\n".join(strings)

    def save_file(self, filename="machine.txt", order_Q=None, order_sigma=None):
        """Saves a file

        :param filename: Name of filename (default is machine.txt)
        :param order_Q: Order to print states
        :param order_sigma: Order to print vocabulary

        :returns: None
        """
        string = self.to_string(order_Q=order_Q, order_sigma=order_sigma)
        with open(filename, "w") as f:
            f.write(string)

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
    ):
        """Saves machine as an image

        :param filename: Filename of image
        :param q_c: Set of current states to be highlited (default is empty)
        :param a_c: Set of current symbols to be highlited (default is empty)
        :param q_prev: Set of previos states to be highlited (default is empty)
        :param symbols: Replacements of the symbols to show (default is empty)
        :param states: Replacements of the states to show (default is empty)
        :param format: Format of image (default is svg)
        :param dpi: Resolution of image (default is "60.0")
        :param string: Label of string being analysed (default is None)
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
        )
        dot.render(filename, format=format, cleanup=True)

    def save_gif(
        self,
        w,
        filename="maquina.gif",
        symbols={},
        states={},
        dpi="90",
        show=False,
        loop=0,
        duration=500,
    ):
        """Saves an animation of  machine

        :param w: String to analysed during animation
        :param filename: Name of gif (default is "maquina.gif")
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
        for q, a, w_ in self.delta_stepwise(w):
            filename_ = os.path.join(dirpath, f"{i}")
            fin = len(w) - len(w_)
            if fin:
                processed = w[: fin - 1]
            else:
                processed = " "
            a = a if a else " "
            if isinstance(q, set):
                g = self.save_img(
                    filename_,
                    q_c=q,
                    a_c=set([a]),
                    q_prev=q_prev,
                    symbols=symbols,
                    states=states,
                    dpi=dpi,
                    string=(processed, a, w_),
                    format="png",
                )
                q_prev = q
            else:
                g = self.save_img(
                    filename_,
                    q_c=set([q]),
                    a_c=set([a]),
                    q_prev=q_prev,
                    symbols=symbols,
                    states=states,
                    dpi=dpi,
                    string=(processed, a, w_),
                    format="png",
                )
                q_prev = set([q])
            im = Image.open(filename_ + ".png")
            images.append(im)
            i += 1
            filename_ = os.path.join(dirpath, f"{i}")
            if isinstance(q, set):
                g = self.save_img(
                    filename_,
                    q_c=q,
                    symbols=symbols,
                    dpi=dpi,
                    string=(processed, a, w_),
                    format="png",
                )
            else:
                g = self.save_img(
                    filename_,
                    q_c=set([q]),
                    symbols=symbols,
                    dpi=dpi,
                    string=(processed, a, w_),
                    format="png",
                )
            im = Image.open(filename_ + ".png")
            if i == 0 or len(w_) == 0:
                images.append(im)
                images.append(im)
                images.append(im)
                images.append(im)
            images.append(im)
            i += 1

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
