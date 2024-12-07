

from maquinas.exceptions import *
from maquinas.regular.rg import *

g1=RegularGrammar("S-> aS; S-> bA; A -> epsilon; A -> cA;")
g2=RegularGrammar("""
S → +A;
A → 0A;
B → 0C;
C → 0C;
D → +E;
E → 0F;
F → 0F;
S → -A;
A → 1A;
B → 1C;
C → 1C;
D → -E;
E → 1F;
F → 1F;
S → A;
A → 2A;
B → 2C;
C → 2C;
D → E;
E → 2F;
F → 2F;
A → 3A;
B → 3C;
C → 3C;
E → 3F;
F → 3F;
A → 4A;
B → 4C;
C → 4C;
E → 4F;
F → 4F;
A → 5A;
B → 5C;
C → 5C;
E → 5F;
F → 5F;
A → 6A;
B → 6C;
C → 6C;
E → 6F;
F → 6F;
A → 7A;
B → 7C;
C → 7C;
E → 7F;
F → 7F;
A → 8A;
B → 8C;
C → 8C;
E → 8F;
F → 8F;
A → 9A;
B → 9C;
C → 9C;
E → 9F;
F → 9F;
A → .B;
C → eD;
F → ε;
A → B;
C → ε
""")

def test_aesbces_g():
    """Test if noambiguos grammar was correctly generated"""
    assert len(g1.V)==2
    assert len(g1.sigma)==3
    assert len(g1.P)==2
    assert g1.S=='S'

def test_aesbces_accepted():
    """Test valid strings for aesbces"""
    assert g1.accepts("aab")
    assert g1.accepts("bcc")
    assert g1.accepts("aabcc")
    assert g1.accepts("aaabcc")
    assert g1.accepts("aabccc")
    assert g1.accepts("aaaaabcccc")
    assert g1.accepts("aaaaaaaaaabccccccccccccccccccccc")

def test_aesbces_rejected():
    """Test invalid strings for pair of bs"""
    assert g1.accepts("abb") == False
    assert g1.accepts("ac") == False
    assert g1.accepts("cb") == False
    assert g1.accepts("baacc") == False
    assert g1.accepts("bcccaa") == False

def test_aesbces_properties():
    """Test propierties for no ambibuos grammar"""
    forests,chart,forest=g1.parse("aabccccc")
    assert len(list(g1.extract_trees(forest)))==1

def test_float_numbers_g():
    """Test if noambiguos grammar was correctly generated"""
    assert len(g2.V)==7
    assert len(g2.sigma)==14
    assert len(g2.P)==7
    assert g2.S=='S'

def test_float_numbers_accepted():
    """Test valid strings for pair of bes"""
    assert g2.accepts("1.0")
    assert g2.accepts("0.3")
    assert g2.accepts("-2")
    assert g2.accepts("+15.0")
    assert g2.accepts("-0.19e-10")

def test_float_numbers_rejected():
    """Test invalid strings for pair of bs"""
    assert g2.accepts("--1") == False
    assert g2.accepts("1.0+") == False
    assert g2.accepts("-19.8ee-10") == False
    assert g2.accepts("-19.8e-10+4") == False

def test_float_numbers_properties():
    """Test propierties for no ambibuos grammar"""
    forests,chart,forest=g2.parse("-0.19e-10")
    assert len(list(g2.extract_trees(forest)))==1
