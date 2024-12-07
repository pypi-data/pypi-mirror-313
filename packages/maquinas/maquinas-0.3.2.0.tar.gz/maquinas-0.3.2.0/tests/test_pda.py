import pytest

from maquinas.exceptions import *
from maquinas.contextfree.pda import *

m=PushDownAutomaton()

def test_empty_pda():
    """Test if PDA is empty"""
    assert len(m.Q)==0
    assert len(m.sigma)==1
    assert len(m.gamma)==2
    assert m.q_0==None
    assert m.Z_0=="Z₀"
    assert len(m.A)==0
    assert len(m.ttable)==0

def test_adding_states():
    """Adds three states for empty PDA"""
    m.add_state("q_0")
    m.add_state("q_1")
    m.add_state("q_2")
    assert len(m.Q)==3

def test_exception_alreadyexistsstate():
    """Fails if state already exists in PDA"""
    with pytest.raises(AlreadyExistsState):
        m.add_state("q_0")

def test_set_initial_state():
    """Sets initial state in PDA"""
    m.set_initial_state("q_0")
    assert m.get_initial_state()=="q_0"

def test_set_initial_state_doesnotexisitsstate():
    """Fails because innitial state does not exists in PDA"""
    with pytest.raises(DoesNotExistsState):
        m.set_initial_state("q_3")
        assert m.get_initial_state()=="q_3"

def test_adding_symbol():
    """Adds symbols to PDA"""
    m.add_symbol("a")
    m.add_symbol("b")
    assert len(m.sigma)==3

def test_exception_alreadyexistssymbol():
    """Fails because symbol already existis in PDA"""
    with pytest.raises(AlreadyExistsSymbol):
        m.add_symbol("a")

def test_exception_alreadyexistssymbol():
    """Fails because symbols already existis in PDA"""
    with pytest.raises(AlreadyExistsSymbol):
        m.add_qsymbol("Z0")

def test_adding_transitions():
    """Adds transitions to PDA"""
    m.add_transition("q_0","a","Z0",[("q_0",["A","Z0"])],force=True)
    m.add_transition("q_0","a","A",[("q_0",["A","A"])],force=True)
    m.add_transition("q_0","b","A",[("q_1",["epsilon"])],force=True)
    m.add_transition("q_1","b","A",[("q_1",["epsilon"])],force=True)
    m.add_transition("q_1","epsilon","Z0",[("q_2",["Z0"])],force=True)
    assert len(m.ttable)==2

def test_exception_alreadyexiststransition():
    """Fails becuase transition already exists in NDFA"""
    with pytest.raises(AlreadyExistsPDATransition):
        m.add_transition("q_0","a","Z0",[("q_0",["A","Z0"])])

def test_delta():
    """Test transtions in PDA"""
    istates=m.create_istates([("q_0",["Z0"])])
    assert "q_0" in [x for x,_ in m.delta(istates,"a")]
    istates=m.create_istates([("q_0",["A","Z0"])])
    assert "q_0" in [x for x,_ in m.delta(istates,"a")]
    assert "q_1" in [x for x,_ in m.delta(istates,"b")]
    istates=m.create_istates([("q_1",["A","Z0"])])
    assert "q_1" in [x for x,_ in m.delta(istates,"b")]
    istates=m.create_istates([("q_1",["Z0"])])
    assert "q_2" in [x for x,_ in m.delta(istates,"epsilon")]

def test_delta_extendida():
    """Test extended transtions in PDA"""
    istates=m.create_initial_istate()
    assert "q_0" in [x for x,_ in  m.delta_extended(istates,"")]
    assert "q_0" in [x for x,_ in  m.delta_extended(istates,"a")]
    assert "q_1" in [x for x,_ in  m.delta_extended(istates,"aab")]
    assert "q_1" in [x for x,_ in  m.delta_extended(istates,"aaabb")]
    assert "q_2" in [x for x,_ in  m.delta_extended(istates,"aaabbb")]
    assert len([x for x,_ in  m.delta_extended(istates,"aabbb")])==0

def test_delta_step():
    """Test steps in delta_step in PDA"""
    for q,a,w in  m.delta_stepwise(""):
        pass
    assert "q_0" in [x for x,_ in  q]
    for q,a,w in  m.delta_stepwise("a"):
        pass
    assert "q_0" in [x for x,_ in  q]
    for q,a,w in  m.delta_stepwise("aab"):
        pass
    assert "q_1" in [x for x,_ in  q]
    for q,a,w in  m.delta_stepwise("aaabb"):
        pass
    assert "q_1" in [x for x,_ in  q]
    for q,a,w in  m.delta_stepwise("aaabbb"):
        pass
    assert "q_2" in [x for x,_ in  q]
