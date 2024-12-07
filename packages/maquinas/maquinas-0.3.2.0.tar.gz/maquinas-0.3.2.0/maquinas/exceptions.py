# Eceptions for library


class AlreadyExistsState(Exception):
    """Already exists state"""

    def __init__(self, q):
        self.q = q
        msg = f"State '{q}' already exists in machine"
        super().__init__(msg)


class AlreadyExistsSymbol(Exception):
    """Already Exists Symbol"""

    def __init__(self, a):
        self.a = a
        msg = f"Symbol '{a}' already exists in machine"
        super().__init__(msg)


class AlreadyExistsTransition(Exception):
    """Already exists transition"""

    def __init__(self, q_i, a, m):
        self.a = a
        self.q_i = q_i
        self.m = m
        msg = f"Transition ({q_i},{a}) already exists with destination {m[q_i,a]}"
        super().__init__(msg)


class AlreadyExistsTMTransition(Exception):
    """Already exists transition Turing Machine"""

    def __init__(self, q_i, a, m):
        self.a = a
        self.q_i = q_i
        self.m = m
        msg = f"Transition ({q_i},{a}) already exists with destination {m.get_transition(q_i,a)}"
        super().__init__(msg)


class AlreadyExistsTSPDATransition(Exception):
    """Already exists transition two stack"""

    def __init__(self, q_i, a, z1, z2, m):
        self.a = a
        self.q_i = q_i
        self.m = m
        self.z1 = z1
        self.z2 = z2
        msg = f"Transition ({q_i},{a},{z1},{z2}) already exists with destination {m.get_transition(q_i,a,z1,z2)}"
        super().__init__(msg)


class AlreadyExistsPDATransition(Exception):
    """Already exists transition"""

    def __init__(self, q_i, a, z, m):
        self.a = a
        self.q_i = q_i
        self.m = m
        self.z = z
        msg = f"Transition ({q_i},{a},{z}) already exists with destination {m.get_transition(q_i,a,z)}"
        super().__init__(msg)


class DoesNotExistsTransition(Exception):
    """Does not exists transition"""

    def __init__(self, q_i, a):
        self.a = a
        self.q_i = q_i
        msg = f"Transition ({q_i},{a}) is not defined in machine"
        super().__init__(msg)


class DoesNotExistsState(Exception):
    """Does not exists state"""

    def __init__(self, q):
        self.q = q
        msg = f"State {q} is not defined in machine"
        super().__init__(msg)


class DoesNotExistsSymbol(Exception):
    """Does not exists symbol defined"""

    def __init__(self, a):
        self.a = a
        msg = f"Symbol '{a}' is not defined in machine"
        super().__init__(msg)


class NoIntitialStateDefined(Exception):
    """There is not initial state defined"""

    def __init__(self):
        msg = f"There is not initial state defined"
        super().__init__(msg)


class NoStringWithDefinition(Exception):
    """No string with definition of RE or grammar"""

    def __init__(self, s, t):
        self.s = s
        self.t = t
        msg = f"The {t} was provided with an empty definition '{s}'"
        super().__init__(msg)


class NoSymbolInMachine(Exception):
    """No symbol in the definition in the machine"""

    def __init__(self, s, ts):
        self.s = s
        self.ts = ts
        msg = f"The {s} symbol is not part of the terminals: {','.join(ts)}"
        super().__init__(msg)


class AlphabetsDoNotMatch(Exception):
    """Alphabets for an operation do not match"""

    def __init__(self, a1, a2):
        self.a1 = a1
        self.a2 = a2
        msg = f"Alphabet {a1} do not match alphabet {a2}"
        super().__init__(msg)


class MappingDoesMatchAlphabet(Exception):
    """Alphabet for a mapping does not match"""

    def __init__(self, m, a):
        self.m = m
        self.a = a
        msg = f"Keys im {m} do not match alphabet {a}"
        super().__init__(msg)
