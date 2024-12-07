

from maquinas.exceptions import *
from maquinas.contextfree.cfg import *

g1=ContextFreeGrammar("S-> ACB; C-> ACB; C -> AB; A -> a; B->b")
g2=ContextFreeGrammar("S->aSb; S-> epsilon; S -> ab")

def test_noambiguous_g():
    """Test if noambiguos grammar was correctly generated"""
    assert len(g1.V)==4
    assert len(g1.sigma)==2
    print(len(g1.P))
    assert len(g1.P)==4
    assert g1.S=='S'

def test_noambiguous_accepted():
    """Test valid strings for pair of bes"""
    assert g1.accepts("aabb")
    assert g1.accepts("aaaaabbbbb")
    assert g1.accepts("aaaaaaaaaabbbbbbbbbb")

def test_noambiguous_rejected():
    """Test invalid strings for pair of bs"""
    assert g1.accepts("ab") == False
    assert g1.accepts("aab") == False
    assert g1.accepts("abb") == False
    assert g1.accepts("aaabb") == False
    assert g1.accepts("aabbb") == False
    assert g1.accepts("aaaaaabbbbb") == False
    assert g1.accepts("aaaaabbbbbb") == False
    assert g1.accepts("aaaaaaaaaaabbbbbbbbbb") == False
    assert g1.accepts("aaaaaaaaaabbbbbbbbbbbb") == False

def test_noambigous_properties():
    """Test propierties for no ambibuos grammar"""
    forests,chart,forest=g1.parse("aabb")
    print(list(g1.extract_trees(forest)))
    assert len(list(g1.extract_trees(forest)))==1

def test_ambiguous_g():
    """Test if noambiguos grammar was correctly generated"""
    assert len(g2.V)==1
    assert len(g2.sigma)==2
    assert len(g2.P)==1
    assert g2.S=='S'

def test_ambiguous_accepted():
    """Test valid strings for pair of bes"""
    assert g2.accepts("ab")
    assert g2.accepts("aabb")
    assert g2.accepts("aaabbb")
    assert g2.accepts("aaaaabbbbb")
    assert g2.accepts("aaaaaaaaaabbbbbbbbbb")

def test_ambiguous_rejected():
    """Test invalid strings for pair of bs"""
    assert g2.accepts("aab") == False
    assert g2.accepts("abb") == False
    assert g2.accepts("aaabb") == False
    assert g2.accepts("aabbb") == False
    assert g2.accepts("aaaaaabbbbb") == False
    assert g2.accepts("aaaaabbbbbb") == False
    assert g2.accepts("aaaaaaaaaaabbbbbbbbbb") == False
    assert g2.accepts("aaaaaaaaaabbbbbbbbbbbb") == False

def test_ambigous_properties():
    """Test propierties for no ambibuos grammar"""
    forests,chart,forest=g2.parse("aabb")
    assert len(list(g2.extract_trees(forest)))==2
