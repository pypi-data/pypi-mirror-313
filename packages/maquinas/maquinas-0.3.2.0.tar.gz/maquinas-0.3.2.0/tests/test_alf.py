import pytest

from maquinas.exceptions import *
from maquinas.contextsensitive.alf import *

m=Alf()

def test_empty_tspda():
    """Test if TM is empty"""
    assert len(m.Q)==0
    assert len(m.sigma)==0
    assert len(m.gamma)==3 #Start symbols 
    assert m.q_0==None
    assert len(m.A)==0
    assert len(m.ttable)==0

def test_adding_states():
    """Adds three states for empty TM"""
    m.add_state("q_0")
    m.add_state("q_1")
    m.add_state("q_2")
    m.add_state("q_3")
    m.add_state("q_4")
    assert len(m.Q)==5

def test_exception_alreadyexistsstate():
    """Fails if state already exists in TM"""
    with pytest.raises(AlreadyExistsState):
        m.add_state("q_0")

def test_set_initial_state():
    """Sets initial state in TM"""
    m.set_initial_state("q_0")
    assert m.get_initial_state()=="q_0"

def test_set_aceptors():
    """Sets aceptors in TM"""
    m.set_aceptors(["q_4"])
    assert len(m.A) ==1

def test_set_initial_state_doesnotexisitsstate():
    """Fails because innitial state does not exists in TM"""
    with pytest.raises(DoesNotExistsState):
        m.set_initial_state("q_5")
        assert m.get_initial_state()=="q_5"

def test_adding_symbol():
    """Adds symbols to TM"""
    m.add_symbol("a")
    m.add_symbol("b")
    m.add_tsymbol("X")
    assert len(m.sigma)==2

def test_exception_alreadyexistssymbol():
    """Fails because symbol already existis in TM"""
    with pytest.raises(AlreadyExistsSymbol):
        m.add_symbol("a")

def test_exception_alreadyexistssymbol():
    """Fails because symbols already existis in TM"""
    with pytest.raises(AlreadyExistsSymbol):
        m.add_tsymbol("X")

def test_adding_transitions():
    """Adds transitions to TM"""
    m.add_transition("q_0","a",[("q_1","X",1)],force=True)
    m.add_transition("q_0","Y",[("q_3","Y",1)],force=True)
    m.add_transition("q_1","a",[("q_1","a",1)],force=True)
    m.add_transition("q_1","Y",[("q_1","Y",1)],force=True)
    m.add_transition("q_1","b",[("q_2","Y",-1)],force=True)
    m.add_transition("q_2","a",[("q_2","a",-1)],force=True)
    m.add_transition("q_2","Y",[("q_2","Y",-1)],force=True)
    m.add_transition("q_2","X",[("q_0","X",1)],force=True)
    m.add_transition("q_3","Y",[("q_3","Y",1)],force=True)
    m.add_transition("q_3",m.B,[("q_4",m.B,1)],force=True)
    assert len(m.ttable)==4

def test_exception_alreadyexiststransition():
    """Fails becuase transition already exists in TM"""
    with pytest.raises(AlreadyExistsTMTransition):
        m.add_transition("q_0","a",[("q_0","X",'R')],force=True)

def test_delta_extendida():
    #Potenciales problemas
    """Test extended transtions in TM"""
    assert len([x for x,_ in  m.delta_extended(None,"")])==0
    m.clean()
    assert len([x for x,_ in  m.delta_extended(None,"a")])==0
    m.clean()
    assert len([x for x,_ in  m.delta_extended(None,"aaab")])==0
    m.clean()
    assert len([x for x,_ in  m.delta_extended(None,"aaabb")])==0
    m.clean() #Limpuar cuando la siguiente cadena sea de longitud mas grande que la anterior
    assert "q_4" in [x for x,_,_ in  m.delta_extended(None,"aaabbb")]  

def test_delta_step():
    """Test steps in delta_step in TM"""
    m.clean()  #La cinta y otros estados se crean en funcion de la cadena de entrada (pruebas por default)
    for q in  m.delta_stepwise(""):
        pass
    m.clean()
    assert len(q)==0
    m.clean()
    for q in  m.delta_stepwise("a"):
        pass
    assert len(q)==0
    m.clean()
    for q in  m.delta_stepwise("aab"):
        pass
    assert len(q)==0
    m.clean()
    for q in  m.delta_stepwise("aaabb"):
        pass
    assert len(q)==0
    m.clean()
    for q in  m.delta_stepwise("aaabbb"):
        pass
    print(q)
    assert "q_4" in [x for x,_,_ in  q]
