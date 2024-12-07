
from maquinas.contextsensitive.alf import *
from maquinas.io import * 
#from maquinas.exceptions import *
#from maquinas.recursivelyenumerable.tm import TuringMachine
m=Alf(Q=['q_0','q_1','q_2','q_3','q_4'],
         sigma=['a','b'],
         gamma=['X','Y'],
         q_0='q_0',
         A=['q_4'],
         delta=[
            (('q_0','a'),[('q_1','X','R')]),
            (('q_1','a'),[('q_1','a','R')]),
            (('q_1','Y'),[('q_1','Y','R')]),
            (('q_1','b'),[('q_2','Y','L')]),
            (('q_2','Y'),[('q_2','Y','L')]),
            (('q_2','a'),[('q_2','a','L')]),
            (('q_2','X'),[('q_0','X','R')]),
            (('q_0','Y'),[('q_3','Y','R')]),
            (('q_3','Y'),[('q_3','Y','R')]),
            (('q_3','[B]'),[('q_4','[B]','L')]),
         ]
    )

abc=Alf(Q=['q_0','q_1','q_2','q_3','q_4','q_5'],
         sigma=['a','b','c'],
         gamma=['X','Y','Z'],
         q_0='q_0',
         A=['q_5'],
         delta=[
            (('q_0','a'),[('q_1','X','R')]),
            (('q_1','a'),[('q_1','a','R')]),
            (('q_1','Y'),[('q_1','Y','R')]),
            (('q_1','b'),[('q_2','Y','R')]),

            (('q_2','Z'),[('q_2','Z','R')]),
            (('q_2','b'),[('q_2','b','R')]),

            (('q_2','c'),[('q_3','Z','L')]),

            (('q_3','Y'),[('q_3','Y','L')]),
            (('q_3','Z'),[('q_3','Z','L')]),
            (('q_3','a'),[('q_3','a','L')]),
            (('q_3','b'),[('q_3','b','L')]),
            (('q_3','X'),[('q_0','X','R')]),

            (('q_0','Y'),[('q_4','Y','R')]),
            (('q_0','[B]'),[('q_5','[B]','R')]), #Condicion de aceptacion para ""
            (('q_4','Y'),[('q_4','Y','R')]),
            (('q_4','Z'),[('q_4','Z','R')]),
            (('q_4','[B]'),[('q_5','[B]','R')]),
         ]
    )

def test_anbn_alf():
    """Test if m was correctly generated"""
    assert len(m.Q)== 5
    m.print_summary()
    assert len(m.sigma)==2
    assert len(m.gamma)==7
    assert m.q_0=="q_0"
    assert len(m.A)==1
    assert len(m.ttable)==4

def test_anbn_accepted():
    """Test valid strings for anbn by TM"""
    assert m.accepts("ab",max_steps=1000)
    m.clean()
    assert m.accepts("aabb",max_steps=1000)
    m.clean()
    assert m.accepts("aaabbb",max_steps=1000)
    m.clean()
    assert m.accepts("aaaabbbb",max_steps=1000)
    m.clean()
    assert m.accepts("a"*10+"b"*10,max_steps=1000)
    m.clean()

def test_anbn_rejected():
    """Test invalid strings for anbn by TM"""
    assert m.accepts("",max_steps=1000)==False
    m.clean()
    assert m.accepts("b",max_steps=1000)==False
    m.clean()
    assert m.accepts("bb",max_steps=1000)==False
    m.clean()
    assert m.accepts("abbb",max_steps=1000)==False
    m.clean()
    assert m.accepts("abbbc",max_steps=1000)==False
    m.clean()
    assert m.accepts("aababab",max_steps=1000)==False
    m.clean()
    assert m.accepts("aabababcc",max_steps=1000)==False
    m.clean()
    assert m.accepts("aaababaaabacc",max_steps=1000)==False
    m.clean()
    assert m.accepts("baaababaaaabbaaaabaaaaaabaa",max_steps=1000)==False
    m.clean()
    assert m.accepts("cbaaababaaaabbaaaabaaaaaabaa",max_steps=1000)==False
    m.clean()




def test_anbncn_alf():
    """Test if m was correctly generated"""
    assert len(abc.Q)== 6
    abc.print_summary()
    assert len(abc.sigma)== 3
    assert len(abc.gamma)== 9  #Star symbols
    assert abc.q_0=="q_0"
    assert len(abc.A)==1
    assert len(abc.ttable)== 5

def test_anbncn_accepted():
    """Test valid strings for anbn by Alf"""
    assert abc.accepts("",max_steps=1000)
    abc.clean()
    assert abc.accepts("abc",max_steps=1000)
    abc.clean()
    assert abc.accepts("aabbcc",max_steps=1000)
    abc.clean()
    assert abc.accepts("aaabbbccc",max_steps=1000)
    abc.clean()
    assert abc.accepts("aaaabbbbcccc",max_steps=1000)
    abc.clean()
    assert abc.accepts("a"*10+"b"*10+"c"*10,max_steps=1000)
    abc.clean()

def test_anbncn_rejected():
    """Test invalid strings for anbn by TM"""
    #assert abc.accepts("",max_steps=1000)==False  #Si deberia aceptar 
    #abc.clean()
    assert abc.accepts("b",max_steps=1000)==False
    abc.clean()
    assert abc.accepts("bc",max_steps=1000)==False
    abc.clean()
    assert abc.accepts("cba",max_steps=1000)==False
    abc.clean()
    assert abc.accepts("bca",max_steps=1000)==False
    abc.clean()
    assert abc.accepts("acb",max_steps=1000)==False
    abc.clean()
    assert abc.accepts("abb",max_steps=1000)==False
    abc.clean()
    assert abc.accepts("abbb",max_steps=1000)==False
    abc.clean()
    assert abc.accepts("abbbc",max_steps=1000)==False
    abc.clean()
    assert abc.accepts("aababab",max_steps=1000)==False
    abc.clean()
    assert abc.accepts("aabababcc",max_steps=1000)==False
    abc.clean()
    assert abc.accepts("aaababaaabacc",max_steps=1000)==False
    abc.clean()
    assert abc.accepts("baaababaaaabbaaaabaaaaaabaa",max_steps=1000)==False
    abc.clean()
    assert abc.accepts("cbaaababaaaabbaaaabaaaaaabaa",max_steps=1000)==False
    abc.clean()

