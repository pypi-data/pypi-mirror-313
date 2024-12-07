

from maquinas.exceptions import *
from maquinas.regular import dfa
from maquinas.regular.minimization import *

# Creating automata finito
one_one=DFA(Q=['A','B','C','D','E','F'],
                         sigma=['0','1'],
                         q_0='A',
                         A=['C','D','E'],
                         delta=[
                            (('A','0'),'B'),
                            (('A','1'),'C'),
                            (('B','0'),'A'),
                            (('B','1'),'D'),
                            (('C','0'),'E'),
                            (('C','1'),'F'),
                            (('D','0'),'E'),
                            (('D','1'),'F'),
                            (('E','0'),'E'),
                            (('E','1'),'F'), 
                            (('F','0'),'F'),
                            (('F','1'),'F'), 
                         ])

bes_divisible_by_3=DFA(Q=['q_0','q_1','q_2','q_3'],
                         sigma=['a','b'],
                         q_0='q_0',
                         A=['q_0','q_3'],
                         delta=[
                            (('q_0','a'),'q_0'),
                            (('q_0','b'),'q_1'),
                            (('q_1','a'),'q_1'),
                            (('q_1','b'),'q_2'),
                            (('q_2','a'),'q_2'),
                            (('q_2','b'),'q_3'),
                            (('q_3','a'),'q_3'),
                            (('q_3','b'),'q_1'),
                         ])

new_one=DFA(Q=['0','1','2','3','4','5','6'],
                         sigma=['a','b'],
                         q_0='1',
                         A=['5','0'],
                         delta=[
                            (('0','a'),'0'),
                            (('0','b'),'0'),
                            (('1','a'),'2'),
                            (('1','b'),'5'),
                            (('2','a'),'3'),
                            (('2','b'),'0'),
                            (('3','a'),'3'),
                            (('3','b'),'4'),
                            (('4','a'),'3'),
                            (('4','b'),'0'),
                            (('5','a'),'6'),
                            (('5','b'),'0'),
                            (('6','a'),'0'),
                            (('6','b'),'5'),
                         ])

def test_hopcroft():
    mini=minimization_hopcroft(one_one,rename=False)
    assert len(mini.Q)==2
    mini=minimization_hopcroft(one_one)
    assert len(mini.Q)==2
    mini=minimization_hopcroft(bes_divisible_by_3)
    assert len(mini.Q)==3
    mini=minimization_hopcroft(new_one)
    assert len(mini.Q)==6


def test_add_error_state():
    mini=minimization_hopcroft(one_one,rename=False)
    mini.add_error_state()
    assert len(mini.Q)==3
    mini=minimization_hopcroft(one_one)
    mini.add_error_state()
    assert len(mini.Q)==3
    mini=minimization_hopcroft(bes_divisible_by_3)
    mini.add_error_state()
    assert len(mini.Q)==3
    mini=minimization_hopcroft(new_one)
    mini.add_error_state()
    assert len(mini.Q)==6


