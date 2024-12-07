# Function to load machines
import re
from maquinas.regular.dfa import *
from maquinas.regular.ndfa import *
from maquinas.regular.ndfa_e import *
from maquinas.contextfree.pda import *
from maquinas.recursivelyenumerable.tspda import *
from maquinas.recursivelyenumerable.tm import *
from maquinas.exceptions import *

re_state = re.compile(r"^\s*(?P<initial>->)?\s*(?P<state>.*[^\]])[^\]]*(?P<final>])?$")
re_z_slash_final = re.compile(r"^s*(?P<Z>[^\/]+)/(?P<slash>.*)(->|→)(?P<final>[^,]+)")
re_z_slash = re.compile(r"^s*(?P<Z>[^\/]+)/(?P<slash>.*)")
re_a_a_final_dir = re.compile(r"^s*(?P<a>[^\/]+)/(?P<aa>.*)(->|→)(?P<final>[^,]+):(?P<Dir>R|L)")


def load_fa(string):
    """Loads a finite automata: DFA, NDFA, NDFA-e from a string

    :param string: recieves a string with the definition of the FA
    :return: An auomata"""

    def _read_row(line):
        """Reads a line of a FA"""
        row = [a.strip() for a in line.split("|")]
        origin = _read_state(row[0])
        return origin, _read_states(row[1:])

    def _read_states(states):
        """Reads a destination states of a FA"""
        return [[s.strip() for s in state.split(",")] for state in states]

    header = False
    delta = {}
    for line in string.split("\n"):
        line = line.strip()
        if len(line) == 0 or line.startswith("#"):
            continue
        if not header:
            sigma = _read_sigma(line)
            header = True
        else:
            origin, states = _read_row(line)
            delta[origin] = states
    type_machine = 1
    if "epsilon" in sigma:
        type_machine = 3
    if "ε" in sigma:
        type_machine = 3
    if type_machine == 1:
        for o, states in delta.items():
            for s in states:
                if len(s) > 1:
                    type_machine = 2
                    break
            if type_machine == 2:
                break
    m = _create_fa_by_type(type_machine)
    for a in sigma:
        try:
            m.add_symbol(a)
        except AlreadyExistsSymbol:
            pass
    A = set()
    for (ini, fin, q_i), states in delta.items():
        if fin:
            A.add(q_i)
        for a, state in zip(sigma, states):
            state = [s for s in state if len(s) > 0]
            if len(state) > 0:
                if type_machine == 1 and len(state) == 1:
                    m.add_transition(q_i, a, state[0], force=True)
                else:
                    m.add_transition(q_i, a, state, force=True)
        if ini:
            m.set_initial_state(q_i)
    m.set_aceptors(A)
    return m

def load_tm(string):
    """Loads a Turing Machine

    :param string: recieves a string with the definition of the PDA
    :return: A TM"""
    m = TuringMachine()

    def _read_row(line):
        """Reads a line of a TM"""
        row = [a.strip() for a in line.split("|")]
        origin = _read_state(row[0])
        return origin, _read_states(row[1:])

    def _read_states(states):
        """Reads a destination states of a TM"""
        return [
            [_read_a_a_final_dir(s.strip()) for s in state.split(",") if len(s) > 0]
            for state in states
        ]

    def _read_a_a_final_dir(z_slash_final):
        m_ = re_a_a_final_dir.match(z_slash_final)
        return m_.group("a"), m_.group("aa"), m_.group("final"),m_.group('Dir')

    header = False
    delta = {}
    for line in string.split("\n"):
        line = line.strip()
        if len(line) == 0 or line.startswith("#"):
            continue
        if not header:
            sigma = _read_sigma(line)
            header = True
        else:
            origin, states = _read_row(line)
            delta[origin] = states
    for a in sigma:
        try:
            m.add_symbol(a)
        except AlreadyExistsSymbol:
            pass
    A = set()
    for (ini, fin, q_i), states in delta.items():
        if fin:
            A.add(q_i)
        for a, state in zip(sigma, states):
            for a,a_,q_f,Dir in state:
                m.add_transition(q_i, a, [(q_f, a_, m._ndir(Dir))], force=True, update=True)
        if ini:
            m.set_initial_state(q_i)
    m.set_aceptors(A)
    return m


def load_pda(string):
    """Loads a Push Down Automataton

    :param string: recieves a string with the definition of the PDA
    :return: A PDA"""
    m = PushDownAutomaton()

    def _read_row(line):
        """Reads a line of a PDA"""
        row = [a.strip() for a in line.split("|")]
        origin = _read_state(row[0])
        return origin, _read_states(row[1:])

    def _read_states(states):
        """Reads a destination states of a FA"""
        return [
            [_read_z_slash_final(s.strip()) for s in state.split(",") if len(s) > 0]
            for state in states
        ]

    def _read_z_slash_final(z_slash_final):
        m_ = re_z_slash_final.match(z_slash_final)
        return m._filter(m_.group("Z")), m.tokens(m_.group("slash")), m_.group("final")

    header = False
    delta = {}
    for line in string.split("\n"):
        line = line.strip()
        if len(line) == 0 or line.startswith("#"):
            continue
        if not header:
            sigma = _read_sigma(line)
            header = True
        else:
            origin, states = _read_row(line)
            delta[origin] = states
    for a in sigma:
        try:
            m.add_symbol(a)
        except AlreadyExistsSymbol:
            pass
    A = set()
    for (ini, fin, q_i), states in delta.items():
        if fin:
            A.add(q_i)
        for a, state in zip(sigma, states):
            for z, z_, q_f in state:
                m.add_transition(q_i, a, z, [(q_f, z_)], force=True, update=True)
        if ini:
            m.set_initial_state(q_i)
    m.set_aceptors(A)
    return m


def load_tspda(string):
    """Loads a Two Stack Push Down Automataton

    :param string: recieves a string with the definition of the TSPDA
    :return: A TSPDA"""
    m = TwoStackPushDownAutomaton()

    def _read_row(line):
        """Reads a line of a PDA"""
        row = [a.strip() for a in line.split("|")]
        origin = _read_state(row[0])
        return origin, _read_states(row[1:])

    def _read_states(states):
        """Reads a destination states of a FA"""
        return [
            [
                _read_z_slash_final(z1.strip(), z2_q.strip())
                for z1, z2_q in zip(segs[::2], segs[1::2])
                if len(segs) > 0
            ]
            for state in states
            if (segs := state.split(","))
        ]

    def _read_z_slash_final(z1_slash, z2_slash_final):
        m2_ = re_z_slash_final.match(z2_slash_final)
        m1_ = re_z_slash.match(z1_slash)
        return (
            m._filter(m1_.group("Z")),
            m.tokens(m1_.group("slash")),
            m._filter(m2_.group("Z")),
            m.tokens(m2_.group("slash")),
            m2_.group("final"),
        )

    header = False
    delta = {}
    for line in string.split("\n"):
        line = line.strip()
        if len(line) == 0 or line.startswith("#"):
            continue
        if not header:
            sigma = _read_sigma(line)
            header = True
        else:
            origin, states = _read_row(line)
            delta[origin] = states
    for a in sigma:
        try:
            m.add_symbol(a)
        except AlreadyExistsSymbol:
            pass
    A = set()
    for (ini, fin, q_i), states in delta.items():
        if fin:
            A.add(q_i)
        for a, state in zip(sigma, states):
            for z1, z1_, z2, z2_, q_f in state:
                m.add_transition(
                    q_i, a, z1, z2, [(q_f, (z1_, z2_))], force=True, update=True
                )
        if ini:
            m.set_initial_state(q_i)
    m.set_aceptors(A)
    return m


def _read_state(state):
    """Reads a source state of a FA"""
    m = re_state.match(state)
    return (
        m.group("initial") != None,
        m.group("final") != None,
        m.group("state").strip(),
    )


def _create_fa_by_type(type_machine):
    if type_machine == 1:
        return DeterministicFiniteAutomaton()
    elif type_machine == 2:
        return NonDeterministicFiniteAutomaton()
    elif type_machine == 3:
        return NonDeterministicFiniteAutomaton_epsilon()


def _read_sigma(line):
    """Reads an alphabet sigma"""
    return [a.strip() for a in line.split("|") if len(a.strip()) > 0]


def load_jflap(string, state_prefix=lambda x: f"{x}"):
    """Reads a jflap string file definition

    :param string: string with the content of a .jff JFLAP format
    :param state_prefix: function that attach a prefix to the states. Useful when states are numbersi
    :return: An automata"""
    import xml.etree.ElementTree as ET

    root = ET.fromstring(string)
    type_machine = root.find("type").text

    # TODO load other type of inputs: pda, re, grammar
    if type_machine == "fa":
        m = _load_jflap_fa(root, state_prefix=state_prefix)
    elif type_machine == "pda":
        m = _load_jflap_pda(root, state_prefix=state_prefix)
    if type_machine.startswith("turing"):
        m = _load_jflap_tm(root, state_prefix=state_prefix)
    return m

def _load_jflap_tm(root, state_prefix=lambda x: f"{x}"):
    """Loads a jflap xml TM description"""
    m = TuringMachine()
    A = set()
    id2name = {}
    for e in root.iter("state"):
        if "name" in e.attrib:
            q = state_prefix(e.attrib["name"])
            id2name[e.attrib["id"]] = q
        else:
            q = state_prefix(e.attrib["id"])
            id2name[e.attrib["id"]] = q
        try:
            m.add_state(q)
        except AlreadyExistsState:
            pass
        if not e.find("initial") is None:
            m.set_initial_state(q)
        if not e.find("final") is None:
            A.add(q)
    for e in root.iter("block"):
        if "name" in e.attrib:
            q = state_prefix(e.attrib["name"])
            id2name[e.attrib["id"]] = q
        else:
            q = state_prefix(e.attrib["id"])
            id2name[e.attrib["id"]] = q
        try:
            m.add_state(q)
        except AlreadyExistsState:
            pass
        if not e.find("initial") is None:
            m.set_initial_state(q)
        if not e.find("final") is None:
            A.add(q)

    m.set_aceptors(A)
    for e in root.iter("transition"):
        a = e.find("read").text
        if not a:
            a = m.B
        else:
            try:
                m.add_symbol(a)
            except AlreadyExistsSymbol:
                pass
            try:
                m.add_tsymbol(a)
            except AlreadyExistsSymbol:
                pass
        a_ = e.find("write").text
        if not a_:
            a_ = m.B
        else:
            try:
                m.add_symbol(a_)
            except AlreadyExistsSymbol:
                pass
            try:
                m.add_tsymbol(a_)
            except AlreadyExistsSymbol:
                pass
        Dir = e.find("move").text
        if Dir == 'L':
            Dir = -1
        elif Dir == 'R':
            Dir = 1
        else:
            Dir = 0

        q_i = id2name[e.find("from").text]
        q_f = id2name[e.find("to").text]
        m.add_transition(q_i, a, [(q_f, a_, Dir)], force=False, update=True)

    return m


def _load_jflap_pda(root, state_prefix=lambda x: f"{x}"):
    """Loads a jflap xml PDA description"""
    m = PushDownAutomaton(Z_0="Z")
    A = set()
    id2name = {}
    for e in root.iter("state"):
        if "name" in e.attrib:
            q = state_prefix(e.attrib["name"])
            id2name[e.attrib["id"]] = q
        else:
            q = state_prefix(e.attrib["id"])
            id2name[e.attrib["id"]] = q
        try:
            m.add_state(q)
        except AlreadyExistsState:
            pass
        if not e.find("initial") is None:
            m.set_initial_state(q)
        if not e.find("final") is None:
            A.add(q)
    m.set_aceptors(A)
    for e in root.iter("transition"):
        a = e.find("read").text
        if not a:
            a = "epsilon"
        else:
            try:
                m.add_symbol(a)
            except AlreadyExistsSymbol:
                pass
        q_i = id2name[e.find("from").text]
        q_f = id2name[e.find("to").text]
        pop = e.find("pop").text
        if not pop:
            pop = "epsilon"
        try:
            m.add_qsymbol(a)
        except AlreadyExistsSymbol:
            pass
        push = e.find("push").text
        if not push:
            push = ["epsilon"]
        else:
            push = m.tokens(push)
            for p in push:
                try:
                    m.add_qsymbol(p)
                except AlreadyExistsSymbol:
                    pass
        m.add_transition(q_i, a, pop, [(q_f, push)], force=False)

    return m


def _load_jflap_fa(root, state_prefix=lambda x: f"{x}"):
    """Loads a jflap xml fa description"""

    type_machine = 0
    if any(t.find("read").text == None for t in root.iter("transition")):
        type_machine = 3
    else:
        trans = set()
        for e in root.iter("transition"):
            if (e.find("from").text, e.find("read").text) in trans:
                type_machine = 2
                break
            trans.add((e.find("from").text, e.find("read").text))
        if type_machine == 0:
            type_machine = 1
    m = _create_fa_by_type(type_machine)
    A = set()
    id2name = {}
    for e in root.iter("state"):
        if "name" in e.attrib:
            q = state_prefix(e.attrib["name"])
            id2name[e.attrib["id"]] = q
        else:
            q = state_prefix(e.attrib["id"])
            id2name[e.attrib["id"]] = q
        try:
            m.add_state(q)
        except AlreadyExistsState:
            pass
        if not e.find("initial") is None:
            m.set_initial_state(q)
        if not e.find("final") is None:
            A.add(q)
    m.set_aceptors(A)
    for e in root.iter("transition"):
        a = e.find("read").text
        if not a:
            a = "epsilon"
        else:
            try:
                m.add_symbol(a)
            except AlreadyExistsSymbol:
                pass
        q_i = id2name[e.find("from").text]
        q_f = id2name[e.find("to").text]
        if type_machine == 1:
            m.add_transition(q_i, a, q_f, force=True)
        else:
            m.add_transition(q_i, a, [q_f], force=True, update=True)

    return m
