import pytest

from maquinas.exceptions import *
from maquinas.recursivelyenumerable.tspda import TwoStackPushDownAutomaton
m=TwoStackPushDownAutomaton()

def test_empty_tspda():
    """Test if TSPDA is empty"""
    assert len(m.Q)==0
    assert len(m.sigma)==1
    assert len(m.gamma)==2
    assert m.q_0==None
    assert m.Z_0=="Z₀"
    assert len(m.A)==0
    assert len(m.ttable)==0

def test_adding_states():
    """Adds three states for empty TSPDA"""
    m.add_state("q_0")
    m.add_state("q_1")
    m.add_state("q_2")
    m.add_state("q_3")
    assert len(m.Q)==4

def test_exception_alreadyexistsstate():
    """Fails if state already exists in TSPDA"""
    with pytest.raises(AlreadyExistsState):
        m.add_state("q_0")

def test_set_initial_state():
    """Sets initial state in TSPDA"""
    m.set_initial_state("q_0")
    assert m.get_initial_state()=="q_0"

def test_set_initial_state_doesnotexisitsstate():
    """Fails because innitial state does not exists in TSPDA"""
    with pytest.raises(DoesNotExistsState):
        m.set_initial_state("q_4")
        assert m.get_initial_state()=="q_4"

def test_adding_symbol():
    """Adds symbols to TSPDA"""
    m.add_symbol("a")
    m.add_symbol("b")
    m.add_symbol("c")
    assert len(m.sigma)==4

def test_exception_alreadyexistssymbol():
    """Fails because symbol already existis in TSPDA"""
    with pytest.raises(AlreadyExistsSymbol):
        m.add_symbol("a")

def test_exception_alreadyexistssymbol():
    """Fails because symbols already existis in TSPDA"""
    with pytest.raises(AlreadyExistsSymbol):
        m.add_qsymbol("Z0")

def test_adding_transitions():
    """Adds transitions to TSPDA"""
    m.print_summary()
    m.add_transition("q_0","a","Z0","Z0",[("q_0",(["A","Z0"],["A","Z0"]))],force=True)
    m.add_transition("q_0","a","A","A",  [("q_0",(["A","A"],["A","A"]))],force=True)
    m.add_transition("q_0","b","A","A"  ,[("q_1",(["epsilon"],["A"]))],force=True)
    m.add_transition("q_1","b","A","A",  [("q_1",(["epsilon"],["A"]))],force=True)
    m.add_transition("q_1","c","Z0","A", [("q_2",(["Z0"],["epsilon"]))],force=True)
    m.add_transition("q_2","c","Z0","A", [("q_2",(["Z0"],["epsilon"]))],force=True)
    m.add_transition("q_2","epsilon","Z0","Z0", [("q_3",(["Z0"],["Z0"]))],force=True)
    assert len(m.ttable)==3

def test_exception_alreadyexiststransition():
    """Fails becuase transition already exists in TSPDA"""
    with pytest.raises(AlreadyExistsTSPDATransition):
        m.add_transition("q_0","a","Z0","Z0",[("q_0",(["A","Z0"],["A","Z0"]))],force=True)

def test_delta():
    """Test transtions in TSPDA"""
    istates=m.create_istates([("q_0",(["Z0"],["Z0"]))])
    assert "q_0" in [x for x,_ in m.delta(istates,"a")]
    istates=m.create_istates([("q_0",(["A","Z0"],["A","Z0"]))])
    assert "q_0" in [x for x,_ in m.delta(istates,"a")]
    assert "q_1" in [x for x,_ in m.delta(istates,"b")]
    istates=m.create_istates([("q_1",(["A","Z0"],["A","Z0"]))])
    assert "q_1" in [x for x,_ in m.delta(istates,"b")]
    istates=m.create_istates([("q_2",(["Z0"],["A","Z0"]))])
    assert "q_2" in [x for x,_ in m.delta(istates,"c")]
    istates=m.create_istates([("q_2",(["Z0"],["Z0"]))])
    assert "q_3" in [x for x,_ in m.delta(istates,"epsilon")]

def test_delta_extendida():
    """Test extended transtions in TSPDA"""
    istates=m.create_initial_istate()
    assert "q_0" in [x for x,_ in  m.delta_extended(istates,"")]
    assert "q_0" in [x for x,_ in  m.delta_extended(istates,"a")]
    assert "q_1" in [x for x,_ in  m.delta_extended(istates,"aab")]
    assert "q_1" in [x for x,_ in  m.delta_extended(istates,"aaabb")]
    assert "q_1" in [x for x,_ in  m.delta_extended(istates,"aaabbb")]
    assert "q_2" in [x for x,_ in  m.delta_extended(istates,"aaabbbc")]
    assert "q_3" in [x for x,_ in  m.delta_extended(istates,"aaabbbccc")]
    assert len([x for x,_ in  m.delta_extended(istates,"aabbbccc")])==0

def test_delta_step():
    """Test steps in delta_step in TSPDA"""
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
    assert "q_1" in [x for x,_ in  q]
    for q,a,w in  m.delta_stepwise("aaabbbc"):
        pass
    assert "q_2" in [x for x,_ in  q]
    for q,a,w in  m.delta_stepwise("aaabbbccc"):
        pass
    assert "q_3" in [x for x,_ in  q]
