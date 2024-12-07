import pytest

from maquinas.exceptions import *
from maquinas.regular.RE import RegularExpression

def test_empty_re():
    """Fails not RE provided"""
    with pytest.raises(NoStringWithDefinition):
        m=RegularExpression('  ').ndfa_e()

def test_empty_re():
    """Test empty re"""
    m=RegularExpression('empty').ndfa_e()
    assert len(m.Q)==1
    assert len(m.sigma)==1
    assert m.q_0=='q_0'
    assert len(m.A)==0
    assert len(m.ttable)==0

def test_epsilon_re():
    """Test epsilon re"""
    m=RegularExpression('epsilon').ndfa_e()
    assert len(m.Q)==1
    assert len(m.sigma)==1
    assert m.q_0=='q_0'
    assert len(m.A)==1
    assert len(m.ttable)==1

def test_symbol_re():
    """Test symbol re"""
    m=RegularExpression('a').ndfa_e()
    assert len(m.Q)==2
    assert len(m.sigma)==2
    assert m.q_0=='q_0'
    assert len(m.A)==1
    assert len(m.ttable)==1

def test_full_re():
    """Test all operations re"""
    m=RegularExpression('(a*ba*ba*)*+a*').ndfa_e()
    assert len(m.Q)==23
    assert len(m.sigma)==3
    assert m.q_0=='q_0'
    assert len(m.A)==2
    assert len(m.ttable)==23
