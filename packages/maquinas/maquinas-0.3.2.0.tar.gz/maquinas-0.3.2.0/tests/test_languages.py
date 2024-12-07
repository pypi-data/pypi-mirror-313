

from maquinas.languages import *

def test_alphabet_operations():
    sigma1=Alphabet(['a','b'])
    sigma2=Alphabet(['b','c'])
    assert len(sigma1.intersection(sigma2))==1
    assert len(sigma1.union(sigma2))==3

def test_alphabet_power():
    sigma1=Alphabet(['a','b'])
    assert len(sigma1.power(0))==1
    assert len(sigma1.power(1))==2
    assert len(sigma1.power(2))==4
    assert len(sigma1.power(4))==16

def test_alphabet_star():
    sigma1=Alphabet(['a','b'])
    assert sigma1.star().finite==False

def test_alphabet_validate():
    sigma1=Alphabet(['a','b'])
    assert sigma1.validate(['','a','b','ab','ba','aaaaa','bbbbba'])==True
    assert sigma1.validate(['c','bc','abc','bac','aaaaac','bbbbbac','aaaccccaaaa'])==False

def test_equal():
    sigma1=Alphabet(['a','b'])
    sigma2=Alphabet(['b','c'])
    sigma3=Alphabet(['a','b'])
    assert sigma1==sigma3
    assert sigma1!=sigma2



L0=Language()
L1=Language(['a','b'],sigma=['a','b'])
L2=Language(L1,sigma=['a','b'])
L3=Language(['aa','ab','ba','bb'],sigma=['a','b'])

def test_lenguages():
    ws=[w for w in L1]
    assert len(ws)==len(L1)
    ws=[w for w in L2]
    assert len(ws)==len(L2)

def test_infere_alphabet():
    assert Language(['a','b'],infere_alphabet=True).sigma==Alphabet(['a','b'])
    assert Language(['ab','ba'],infere_alphabet=True).sigma==Alphabet(['a','b'])
    assert Language(['ab','ba','c'],infere_alphabet=True).sigma==Alphabet(['a','b','c'])

def test_lenguages_star():
    L1_star=L1.star()
    assert L1_star.finite==False

def test_lenguages_concat():
    L1L2_concat=L1.concat(L2)
    L1_star=L1.star()
    assert L1L2_concat.finite==True
    assert len(L1L2_concat)==4
    assert len(L1.concat(L0))==0
    assert len(L1.concat(L3))==8
    assert L1.concat(L1_star).finite == False

def test_lenguages_union():
    L1_star=L1.star()
    L13=L1.union(L3)
    assert len(L13)==6
    assert L1_star.union(L13).finite == False

def test_lenguages_power():
    L1_power_0=L1.power(0)
    L1_power_1=L1.power(1)
    L1_power_2=L1.power(2)
    print(L1_power_2)
    L1_power_3=L1.power(3)
    L1_star=L1.star()
    assert len(L1_power_0)==1
    assert len(L1_power_1)==2
    assert len(L1_power_2)==4
    assert len(L1_power_3)==8
    assert len(L1_star.power(0))==1
    assert L1_star.power(1).finite==False
    assert L1_star.power(2).finite==False


def test_lenguages_reverse():
    L1_power_0_reverse=L1.power(0).reverse()
    L1_power_1_reverse=L1.power(1).reverse()
    L1_power_2_reverse=L1.power(2).reverse()
    L1_power_3_reverse=L1.power(3).reverse()
    L1_star_reverse=L1.star().reverse()
    assert len(L1_power_0_reverse)==1
    assert len(L1_power_1_reverse)==2
    assert len(L1_power_2_reverse)==4
    assert len(L1_power_3_reverse)==8
    assert len(L1_star_reverse.power(0))==1
    assert L1_star_reverse.finite==False
    assert L1_star_reverse.finite==False

Ø=empty_language(['a','b'])
ε=empty_string_language(['a','b'])
a=Language(['a'],['a','b'])
def test_notables():
    assert  Ø.is_empty_language()==True
    assert  ε.is_empty_string_language()==True
    assert  len(a)==1

def test_concatenation_notables():
    assert Ø.concat(Ø).is_empty_language()==True
    assert ε.concat(ε).is_empty_string_language()==True
    assert len(a.concat(a))==1
    assert Ø.concat(ε).is_empty_language()==True
    assert ε.concat(Ø).is_empty_language()==True
    assert Ø.concat(a).is_empty_language()==True
    assert a.concat(Ø).is_empty_language()==True
    assert len(ε.concat(a))==1
    assert len(a.concat(ε))==1
    assert ε.concat(a.star()).finite==False
    assert a.star().concat(ε).finite==False
    assert Ø.concat(a.star()).is_empty_language()==True
    assert a.star().concat(Ø).is_empty_language()==True
    assert ε.concat(a.plus()).finite==False
    assert a.plus().concat(ε).finite==False
    assert Ø.concat(a.plus()).is_empty_language()==True
    assert a.plus().concat(Ø).is_empty_language()==True


def test_union_notables():
    assert Ø.union(Ø).is_empty_language()==True
    assert ε.union(ε).is_empty_string_language()==True
    assert len(a.union(a))==1
    assert Ø.union(ε).is_empty_string_language()==True
    assert ε.union(Ø).is_empty_string_language()==True
    assert len(Ø.union(a))==1
    assert len(a.union(Ø))==1
    assert len(ε.union(a))==2
    assert len(a.union(ε))==2
    assert ε.union(a.star()).finite==False
    assert a.star().union(ε).finite==False
    assert Ø.union(a.star()).finite==False
    assert a.star().union(Ø).finite==False
    assert ε.union(a.plus()).finite==False
    assert a.plus().union(ε).finite==False
    assert Ø.union(a.plus()).finite==False
    assert a.plus().union(Ø).finite==False

def test_intersection_notables():
    assert Ø.intersection(Ø).is_empty_language()==True
    assert ε.intersection(ε).is_empty_string_language()==True
    assert len(a.intersection(a))==1
    assert Ø.intersection(ε).is_empty_language()==True
    assert ε.intersection(Ø).is_empty_language()==True
    assert Ø.intersection(a).is_empty_language()==True
    assert a.intersection(Ø).is_empty_language()==True
    assert ε.intersection(a).is_empty_language()==True
    assert a.intersection(ε).is_empty_language()==True
    assert ε.intersection(a.star(),expand_limit=20).is_empty_string_language()==True
    assert a.star().intersection(ε,expand_limit=20).is_empty_string_language()==True
    assert Ø.intersection(a.star()).is_empty_language()==True
    assert a.star().intersection(Ø).is_empty_language()==True
    assert ε.intersection(a.plus()).finite==False
    assert a.plus().intersection(ε).finite==False
    assert Ø.intersection(a.plus()).is_empty_language()==True
    assert a.plus().intersection(Ø).is_empty_language()==True

def test_power_notables():
    assert Ø.power(0).is_empty_string_language()==True
    assert Ø.power(1).is_empty_language()==True
    assert Ø.power(2).is_empty_language()==True
    assert ε.power(0).is_empty_string_language()==True
    assert ε.power(1).is_empty_string_language()==True
    assert ε.power(2).is_empty_string_language()==True
    assert a.power(0).is_empty_string_language()==True
    assert len(a.power(1))==1
    assert len(a.power(2))==1

def test_klene_notables():
    assert Ø.star().is_empty_string_language()==True
    assert ε.star().is_empty_string_language()==True
    assert a.star().finite==False
    assert Ø.plus().is_empty_language()==True
    assert ε.plus().is_empty_string_language()==True
    assert a.plus().finite==False

def test_mapping():
    m= Mapping(
            {'a':Language('0',sigma=[0,1]),
                'b':Language('1',sigma=[0,1])},
            infere_alphabet=True)
    assert len(m)==2
    assert m.sigma==Alphabet(['a','b'])
    assert m.sigma_==Alphabet([0,1])
    assert len(m.substitution("aabb"))==1

def test_projection():
    assert string_projection("aaaaaabbbbbbbbbbbaaaaaaa",["a"])=="aaaaaaaaaaaaa"
    assert L1.projection(["b"])==Language(["","b"],sigma=["b"])
    assert L1.star().projection(["b"]).finite==False

def test_quotient():
    assert string_right_quotient("aaab","b")=="aaa"
    assert string_right_quotient("aaa","b")==""
    assert string_left_quotient("baab","b")=="aab"
    assert string_left_quotient("aaab","b")==""
    assert L1.right_quotient("b")==empty_string_language(sigma=['a','b'])
    assert L1.left_quotient("a")==empty_string_language(sigma=['a','b'])
    assert L1.star().right_quotient("b").finite==False
    assert L1.star().left_quotient("b").finite==False

def test_cancellation():
    assert string_right_cancellation("aaab","b")=="aaa"
    assert string_right_cancellation("aaa","b")==""
    assert string_left_cancellation("baab","b")=="aab"
    assert string_left_cancellation("aaabb","b")=="b"
    assert L1.right_cancellation("b")==empty_string_language(sigma=['a','b'])
    assert L1.left_cancellation("a")==empty_string_language(sigma=['a','b'])
    assert L1.star().right_cancellation("b").finite==False
    assert L1.star().left_cancellation("b").finite==False
