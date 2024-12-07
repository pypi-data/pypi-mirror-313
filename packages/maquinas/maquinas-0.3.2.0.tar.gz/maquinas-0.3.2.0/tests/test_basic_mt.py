

from maquinas.exceptions import *
from maquinas.recursivelyenumerable.tm import TuringMachine
m=TuringMachine(
    Q=['q_0','q_1','q_2','q_3','q_4'],
     sigma=['a','b'],
     gamma=['X','Y'],
     q_0='q_0',
     A=['q_4'],
     delta=[
        (('q_0','a'),[('q_1','X','R')]),
        (('q_0','Y'),[('q_3','Y','R')]),
        (('q_1','a'),[('q_1','a','R')]),
        (('q_1','Y'),[('q_1','Y','R')]),
        (('q_1','b'),[('q_2','Y','L')]),
        (('q_2','a'),[('q_2','a','L')]),
        (('q_2','Y'),[('q_2','Y','L')]),
        (('q_2','X'),[('q_0','X','R')]),
        (('q_3','Y'),[('q_3','Y','R')]),
        (('q_3','[B]'),[('q_4','[B]','R')]),
     ]
)

def test_anbn_tm():
    """Test if m was correctly generated"""
    assert len(m.Q)==5
    m.print_summary()
    assert len(m.sigma)==2
    assert len(m.gamma)==5
    assert m.q_0=="q_0"
    assert len(m.A)==1
    assert len(m.ttable)==4

def test_anbn_accepted():
    """Test valid strings for anbn by TM"""
    assert m.accepts("ab",max_steps=1000)
    assert m.accepts("aabb",max_steps=1000)
    assert m.accepts("aaabbb",max_steps=1000)
    assert m.accepts("aaaabbbb",max_steps=1000)
    assert m.accepts("a"*10+"b"*10,max_steps=1000)

def test_anbn_rejected():
    """Test invalid strings for anbn by TM"""
    assert m.accepts("",max_steps=1000)==False
    assert m.accepts("b",max_steps=1000)==False
    assert m.accepts("bb",max_steps=1000)==False
    assert m.accepts("abbb",max_steps=1000)==False
    assert m.accepts("abbbc",max_steps=1000)==False
    assert m.accepts("aababab",max_steps=1000)==False
    assert m.accepts("aabababcc",max_steps=1000)==False
    assert m.accepts("aaababaaabacc",max_steps=1000)==False
    assert m.accepts("baaababaaaabbaaaabaaaaaabaa",max_steps=1000)==False
    assert m.accepts("cbaaababaaaabbaaaabaaaaaabaa",max_steps=1000)==False

