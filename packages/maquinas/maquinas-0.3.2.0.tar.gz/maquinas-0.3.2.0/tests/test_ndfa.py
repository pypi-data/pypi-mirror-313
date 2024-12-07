import pytest

from maquinas.exceptions import *
from maquinas.regular import ndfa

m=ndfa.NonDeterministicFiniteAutomaton()

def test_empty_af():
    """Test if NDFA is empty"""
    assert len(m.Q)==0
    assert len(m.sigma)==0
    assert m.q_0==None
    assert len(m.A)==0
    assert len(m.ttable)==0

def test_adding_states():
    """Adds two states for empty NDFA"""
    m.add_state("q_0")
    m.add_state("q_1")
    assert len(m.Q)==2

def test_exception_alreadyexistsstate():
    """Fails if state already exists NDFA"""
    with pytest.raises(AlreadyExistsState):
        m.add_state("q_0")

def test_set_initial_state():
    """Sets initial state for NDFA"""
    m.set_initial_state("q_0")
    assert m.get_initial_state()=="q_0"

def test_set_initial_state_doesnotexisitsstate():
    """Fails because innitial state does not exists in NDFA"""
    with pytest.raises(DoesNotExistsState):
        m.set_initial_state("q_2")
        assert m.get_initial_state()=="q_0"

def test_adding_symbol():
    """Adds symbols to NDFA"""
    m.add_symbol("a")
    m.add_symbol("b")
    assert len(m.sigma)==2

def test_exception_alreadyexistssymbol():
    """Fails because symbols already existis in NDFA"""
    with pytest.raises(AlreadyExistsSymbol):
        m.add_symbol("a")

def test_adding_transitions():
    """Adds transitions to NDFA"""
    m.add_transition("q_0","a",["q_0"])
    m.add_transition("q_0","b",["q_1"])
    m.add_transition("q_1","a",["q_1"])
    m.add_transition("q_1","b",["q_0"])
    assert len(m.ttable)==2

def test_exception_alreadyexiststransition():
    """Fails becuase transition already exists in NDFA"""
    with pytest.raises(AlreadyExistsTransition):
        m.add_transition("q_1","b",["q_1"])

def test_delta():
    """Test transtions in NDFA"""
    assert m.delta("q_0","a") == set(["q_0"])
    assert m.delta("q_0","b") == set(["q_1"])
    assert m.delta("q_1","a") == set(["q_1"])
    assert m.delta("q_1","b") == set(["q_0"])


def test_delta_extendida():
    """Test extended transtions in NDFA"""
    assert m.delta_extended(["q_0"],"") == set(["q_0"])
    assert m.delta_extended(["q_0"],"a") == set(["q_0"])
    assert m.delta_extended(["q_0"],"b") == set(["q_1"])
    assert m.delta_extended(["q_0"],"abaaaaaab") == set(["q_0"])
    assert m.delta_extended(["q_1"],"abaaaaaab") == set(["q_1"])

def test_delta_step():
    """Test steps in delta_step in NDFA"""
    for qs,a,w in  m.delta_stepwise(""):
        pass
    assert qs == set(["q_0"])
    for qs,a,w in  m.delta_stepwise("a"):
        pass
    assert qs == set(["q_0"])
    for qs,a,w in  m.delta_stepwise("b"):
        pass
    assert qs == set(["q_1"])
    for qs,a,w in  m.delta_stepwise("abaaaaaab"):
        pass
    assert qs == set(["q_0"])
    for qs,a,w in  m.delta_stepwise("abaaaaaab",q="q_1"):
        pass
    assert qs,a == set(["q_1"])
