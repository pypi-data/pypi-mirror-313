# Código para reducciones

## TODO: https://arxiv.org/abs/1010.5318
## https://arxiv.org/pdf/1210.6624v1

from maquinas.regular.dfa import DeterministicFiniteAutomaton as DFA
from maquinas.regular.ndfa import NonDeterministicFiniteAutomaton as NDFA
from maquinas.regular.ndfa_e import NonDeterministicFiniteAutomaton_epsilon as NDFA_e
from maquinas.regular.ndfa_e import epsilon
from maquinas.exceptions import *
import random


def split(m, qs_f, a):
    res = set()
    for qf in qs_f:
        for q in m.Q:
            try:
                if qf in m.get_transition(q, a):
                    res.add(q)
            except DoesNotExistsTransition:
                pass
    return res


def forward(m, qs, a):
    res = set()
    for q in qs:
        try:
            qf = m.get_transition(q, a)
            res.add(qf)
        except DoesNotExistsTransition:
            pass
    return res


def minimization_hopcroft(dfa, rename=True, remove_sink=True):
    """Minimization of a DFA through the Hofproft method, for more info checK:

    From http://www-igm.univ-mlv.fr/~berstel/Exposes/2009-06-08MinimisationLiege.pdf

    :param dfa: DFA to minimize
    :param rename: If true it will rename states after minimization process
    :param remove_sink: If true it will remove sink states
    """
    P_ = [dfa.A, dfa.Q.difference(dfa.A)]
    W_ = []
    for a in dfa.sigma:
        W_.append((P_[0], a))
    while len(W_) > 0:
        W, a = W_.pop(0)
        wsplit = split(dfa, W, a)
        P_new = []
        for P in P_:
            if len(P.intersection(wsplit)) == 0 or P.intersection(wsplit) == P:
                P_new.append(P)
                continue

            P_1 = wsplit.intersection(P)
            P_2 = set(P)
            for p in P_1:
                P_2.remove(p)
            P_new.append(P_1)
            P_new.append(P_2)
            for b in dfa.sigma:
                if (P, b) in W_:
                    W_.remove((P, b))
                    W_.append((P_1, b))
                    W_.append((P_2, b))
                else:
                    if len(P_1) > len(P_2):
                        W_.append((P_2, b))
                    else:
                        W_.append((P_1, b))
        P_ = P_new

    dfa_new = DFA(sigma=dfa.sigma)
    A = []
    original2new = {}
    for qs_i in P_:
        for q in qs_i:
            original2new[q] = qs_i

    for qs_i in P_:
        qs_il = [q for q in qs_i]
        qs_il.sort()
        qs_il = " ".join(qs_il)
        if dfa.q_0 in qs_i:
            initial = qs_il
        try:
            dfa_new.add_state(qs_il)
        except AlreadyExistsState:
            pass
        if len(dfa.A.intersection(qs_i)) > 0:
            A.append(qs_il)
        for a in dfa.sigma:
            qs_f = forward(dfa, qs_i, a)
            if qs_f:
                tmp = set()
                for q in qs_f:
                    tmp.update(original2new[q])
                qs_fl = [q for q in tmp]
                qs_fl.sort()
                qs_fl = " ".join(qs_fl)
                try:
                    dfa_new.add_state(qs_fl)
                except AlreadyExistsState:
                    pass
                dfa_new.add_transition(qs_il, a, qs_fl)

    dfa_new.set_initial_state(initial)
    dfa_new.set_aceptors(A)

    if rename:
        dfa_new.autorename()

    if remove_sink:
        dfa_new.remove_sink_states()

    return dfa_new
