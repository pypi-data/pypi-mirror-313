
import tempfile
import os

from maquinas.io import *

dfa="""
         |  a  | b  |
-> q0    | q0 | q1 |
   q1  ] | q1 | q0 |
"""

ndfa="""
         |  a    | b  |
-> q0    | q0    | q1 |
   q1  ] | q1    |    |
   q2    | q1,q2 | q1,q2  |
"""

ndfa_e="""
         |  a    | b  | epsilon 
-> q0    | q0    |    | q2
   q1  ] | q1    | q0 | 
   q2    | q1,q2 | q1,q2  | q2
"""

pda="""
       |     ε     |          a          |    b    |
->q_0  |           | Z₀/AZ₀→q_0,A/AA→q_0 | A/ε→q_1 |
  q_1  | Z₀/Z₀→q_2 |                     | A/ε→q_1 |
  q_2] |           |                     |         |
"""

tspda="""
        |        ε        |                a                 |      b      |       c       |
 ->q_0  |                 | Z₀/AZ₀,Z₀/AZ₀→q_0, A/AA,A/AA→q_0 | A/ε,A/A→q_1 |               |
   q_1  |                 |                                  | A/ε,A/A→q_1 | Z₀/Z₀,A/ε→q_2 |
   q_2  | Z₀/Z₀,Z₀/Z₀→q_3 |                                  |             | Z₀/Z₀,A/ε→q_2 |
   q_3] |                 |                                  |             |               |
"""

tm="""
        |     a     |     b     |     X     |     Y     |     𝖁     |
 ->q_0  | a/X→q_1:R |           |           | Y/Y→q_3:R |           |
   q_3  |           |           |           | Y/Y→q_3:R | 𝖁/𝖁→q_4:L |
   q_1  | a/a→q_1:R | b/Y→q_2:L |           | Y/Y→q_1:R |           |
   q_2  | a/a→q_2:L |           | X/X→q_0:R | Y/Y→q_2:L |           |
   q_4] |           |           |           |           |           |
"""

jflap_dfa="""
<structure>
<type>fa</type>
<automaton>
<!--The list of states.-->
<state id="0" name="q0">
<x>83.0</x>
<y>139.0</y>
<initial/>
</state>
<state id="1" name="q1">
<x>235.0</x>
<y>61.0</y>
</state>
<state id="2" name="q2">
<x>545.0</x>
<y>136.0</y>
</state>
<state id="3" name="q3">
<x>391.0</x>
<y>231.0</y>
</state>
<state id="4" name="q4">
<x>287.0</x>
<y>285.0</y>
</state>
<state id="5" name="q5">
<x>504.0</x>
<y>391.0</y>
</state>
<state id="6" name="q6">
<x>161.0</x>
<y>329.0</y>
<final/>
</state>
<!--The list of transitions.-->
<transition>
<from>3</from>
<to>5</to>
<read>a</read>
</transition>
<transition>
<from>1</from>
<to>2</to>
<read>b</read>
</transition>
<transition>
<from>4</from>
<to>5</to>
<read>b</read>
</transition>
<transition>
<from>5</from>
<to>4</to>
<read>b</read>
</transition>
<transition>
<from>3</from>
<to>4</to>
<read>b</read>
</transition>
<transition>
<from>6</from>
<to>1</to>
<read>a</read>
</transition>
<transition>
<from>4</from>
<to>6</to>
<read>a</read>
</transition>
<transition>
<from>1</from>
<to>0</to>
<read>a</read>
</transition>
<transition>
<from>0</from>
<to>2</to>
<read>b</read>
</transition>
<transition>
<from>2</from>
<to>0</to>
<read>b</read>
</transition>
<transition>
<from>6</from>
<to>5</to>
<read>b</read>
</transition>
<transition>
<from>0</from>
<to>6</to>
<read>a</read>
</transition>
<transition>
<from>5</from>
<to>2</to>
<read>a</read>
</transition>
<transition>
<from>2</from>
<to>3</to>
<read>a</read>
</transition>
</automaton>
</structure>
"""


jflap_nfa="""
<structure>
<type>fa</type>
<!--The list of states.-->
<state id="9">
<x>317.0</x>
<y>284.0</y>
</state>
<state id="7">
<x>467.0</x>
<y>62.0</y>
</state>
<state id="8">
<x>585.0</x>
<y>61.0</y>
</state>
<state id="0">
<x>68.0</x>
<y>215.0</y>
<initial/>
</state>
<state id="4">
<x>242.0</x>
<y>59.0</y>
</state>
<state id="5">
<x>373.0</x>
<y>56.0</y>
</state>
<state id="2">
<x>237.0</x>
<y>164.0</y>
</state>
<state id="10">
<x>209.0</x>
<y>345.0</y>
</state>
<state id="3">
<x>311.0</x>
<y>117.0</y>
</state>
<state id="12">
<x>462.0</x>
<y>354.0</y>
</state>
<state id="1">
<x>169.0</x>
<y>214.0</y>
</state>
<state id="6">
<x>524.0</x>
<y>125.0</y>
<final/>
</state>
<state id="11">
<x>564.0</x>
<y>292.0</y>
<final/>
</state>
<!--The list of transitions.-->
<transition>
<from>3</from>
<to>6</to>
<read/>
</transition>
<transition>
<from>2</from>
<to>3</to>
<read>a</read>
</transition>
<transition>
<from>1</from>
<to>9</to>
<read>a</read>
</transition>
<transition>
<from>9</from>
<to>11</to>
<read/>
</transition>
<transition>
<from>6</from>
<to>7</to>
<read>b</read>
</transition>
<transition>
<from>12</from>
<to>11</to>
<read>b</read>
</transition>
<transition>
<from>11</from>
<to>12</to>
<read>b</read>
</transition>
<transition>
<from>9</from>
<to>6</to>
<read/>
</transition>
<transition>
<from>3</from>
<to>11</to>
<read/>
</transition>
<transition>
<from>4</from>
<to>5</to>
<read>a</read>
</transition>
<transition>
<from>1</from>
<to>2</to>
<read>a</read>
</transition>
<transition>
<from>3</from>
<to>4</to>
<read>a</read>
</transition>
<transition>
<from>7</from>
<to>8</to>
<read>b</read>
</transition>
<transition>
<from>10</from>
<to>9</to>
<read>a</read>
</transition>
<transition>
<from>9</from>
<to>10</to>
<read>a</read>
</transition>
<transition>
<from>8</from>
<to>6</to>
<read>b</read>
</transition>
<transition>
<from>5</from>
<to>3</to>
<read>a</read>
</transition>
<transition>
<from>0</from>
<to>1</to>
<read>a</read>
</transition>
</structure>
"""

jflap_extra="""<?xml version="1.0" encoding="UTF-8" standalone="no"?><!--Created with JFLAP 7.1.--><structure>&#13;
        <type>fa</type>&#13;
        <automaton>&#13;
                <!--The list of states.-->&#13;
                <state id="0" name="q0">&#13;
                        <x>358.0</x>&#13;
                        <y>271.0</y>&#13;
                        <initial/>&#13;
                        <final/>&#13;
                </state>&#13;
                <state id="1" name="q1">&#13;
                        <x>495.0</x>&#13;
                        <y>128.0</y>&#13;
                </state>&#13;
                <state id="2" name="q2">&#13;
                        <x>475.0</x>&#13;
                        <y>444.0</y>&#13;
                </state>&#13;
                <state id="3" name="q3">&#13;
                        <x>748.0</x>&#13;
                        <y>134.0</y>&#13;
                </state>&#13;
                <state id="4" name="q4">&#13;
                        <x>751.0</x>&#13;
                        <y>448.0</y>&#13;
                </state>&#13;
                <state id="5" name="q5">&#13;
                        <x>995.0</x>&#13;
                        <y>137.0</y>&#13;
                </state>&#13;
                <state id="6" name="q6">&#13;
                        <x>1022.0</x>&#13;
                        <y>446.0</y>&#13;
                </state>&#13;
                <state id="7" name="q7">&#13;
                        <x>1171.0</x>&#13;
                        <y>282.0</y>&#13;
                        <final/>&#13;
                </state>&#13;
                <!--The list of transitions.-->&#13;
                <transition>&#13;
                        <from>4</from>&#13;
                        <to>5</to>&#13;
                        <read>5</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>4</from>&#13;
                        <to>5</to>&#13;
                        <read>4</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>2</from>&#13;
                        <to>3</to>&#13;
                        <read>9</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>4</from>&#13;
                        <to>5</to>&#13;
                        <read>7</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>2</from>&#13;
                        <to>3</to>&#13;
                        <read>8</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>4</from>&#13;
                        <to>5</to>&#13;
                        <read>6</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>4</from>&#13;
                        <to>5</to>&#13;
                        <read>1</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>4</from>&#13;
                        <to>5</to>&#13;
                        <read>0</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>4</from>&#13;
                        <to>5</to>&#13;
                        <read>3</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>4</from>&#13;
                        <to>5</to>&#13;
                        <read>2</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>2</from>&#13;
                        <to>3</to>&#13;
                        <read>3</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>2</from>&#13;
                        <to>3</to>&#13;
                        <read>2</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>2</from>&#13;
                        <to>3</to>&#13;
                        <read>1</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>2</from>&#13;
                        <to>3</to>&#13;
                        <read>0</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>2</from>&#13;
                        <to>3</to>&#13;
                        <read>7</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>4</from>&#13;
                        <to>5</to>&#13;
                        <read>9</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>2</from>&#13;
                        <to>3</to>&#13;
                        <read>6</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>4</from>&#13;
                        <to>5</to>&#13;
                        <read>8</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>2</from>&#13;
                        <to>3</to>&#13;
                        <read>5</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>2</from>&#13;
                        <to>3</to>&#13;
                        <read>4</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>4</from>&#13;
                        <to>6</to>&#13;
                        <read>3</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>4</from>&#13;
                        <to>6</to>&#13;
                        <read>2</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>4</from>&#13;
                        <to>6</to>&#13;
                        <read>1</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>4</from>&#13;
                        <to>6</to>&#13;
                        <read>0</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>4</from>&#13;
                        <to>6</to>&#13;
                        <read>7</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>4</from>&#13;
                        <to>6</to>&#13;
                        <read>6</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>4</from>&#13;
                        <to>6</to>&#13;
                        <read>5</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>4</from>&#13;
                        <to>6</to>&#13;
                        <read>4</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>4</from>&#13;
                        <to>6</to>&#13;
                        <read>9</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>4</from>&#13;
                        <to>6</to>&#13;
                        <read>8</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>3</from>&#13;
                        <to>6</to>&#13;
                        <read>5</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>3</from>&#13;
                        <to>6</to>&#13;
                        <read>4</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>3</from>&#13;
                        <to>6</to>&#13;
                        <read>7</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>3</from>&#13;
                        <to>6</to>&#13;
                        <read>6</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>3</from>&#13;
                        <to>6</to>&#13;
                        <read>1</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>3</from>&#13;
                        <to>6</to>&#13;
                        <read>0</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>3</from>&#13;
                        <to>6</to>&#13;
                        <read>3</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>3</from>&#13;
                        <to>6</to>&#13;
                        <read>2</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>3</from>&#13;
                        <to>6</to>&#13;
                        <read>9</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>3</from>&#13;
                        <to>6</to>&#13;
                        <read>8</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>3</from>&#13;
                        <to>5</to>&#13;
                        <read>3</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>3</from>&#13;
                        <to>5</to>&#13;
                        <read>2</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>3</from>&#13;
                        <to>5</to>&#13;
                        <read>1</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>3</from>&#13;
                        <to>5</to>&#13;
                        <read>0</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>3</from>&#13;
                        <to>5</to>&#13;
                        <read>7</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>2</from>&#13;
                        <to>4</to>&#13;
                        <read>9</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>3</from>&#13;
                        <to>5</to>&#13;
                        <read>6</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>2</from>&#13;
                        <to>4</to>&#13;
                        <read>8</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>3</from>&#13;
                        <to>5</to>&#13;
                        <read>5</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>3</from>&#13;
                        <to>5</to>&#13;
                        <read>4</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>2</from>&#13;
                        <to>4</to>&#13;
                        <read>5</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>2</from>&#13;
                        <to>4</to>&#13;
                        <read>4</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>3</from>&#13;
                        <to>5</to>&#13;
                        <read>9</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>2</from>&#13;
                        <to>4</to>&#13;
                        <read>7</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>3</from>&#13;
                        <to>5</to>&#13;
                        <read>8</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>2</from>&#13;
                        <to>4</to>&#13;
                        <read>6</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>2</from>&#13;
                        <to>4</to>&#13;
                        <read>1</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>2</from>&#13;
                        <to>4</to>&#13;
                        <read>0</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>2</from>&#13;
                        <to>4</to>&#13;
                        <read>3</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>2</from>&#13;
                        <to>4</to>&#13;
                        <read>2</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>0</from>&#13;
                        <to>1</to>&#13;
                        <read>4</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>0</from>&#13;
                        <to>1</to>&#13;
                        <read>5</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>0</from>&#13;
                        <to>1</to>&#13;
                        <read>1</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>0</from>&#13;
                        <to>1</to>&#13;
                        <read>2</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>0</from>&#13;
                        <to>1</to>&#13;
                        <read>3</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>1</from>&#13;
                        <to>3</to>&#13;
                        <read>9</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>1</from>&#13;
                        <to>3</to>&#13;
                        <read>8</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>1</from>&#13;
                        <to>3</to>&#13;
                        <read>5</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>1</from>&#13;
                        <to>3</to>&#13;
                        <read>4</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>1</from>&#13;
                        <to>3</to>&#13;
                        <read>7</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>1</from>&#13;
                        <to>3</to>&#13;
                        <read>6</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>1</from>&#13;
                        <to>3</to>&#13;
                        <read>1</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>1</from>&#13;
                        <to>3</to>&#13;
                        <read>0</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>1</from>&#13;
                        <to>3</to>&#13;
                        <read>3</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>1</from>&#13;
                        <to>3</to>&#13;
                        <read>2</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>1</from>&#13;
                        <to>4</to>&#13;
                        <read>9</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>1</from>&#13;
                        <to>4</to>&#13;
                        <read>8</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>1</from>&#13;
                        <to>4</to>&#13;
                        <read>3</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>1</from>&#13;
                        <to>4</to>&#13;
                        <read>2</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>1</from>&#13;
                        <to>4</to>&#13;
                        <read>1</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>1</from>&#13;
                        <to>4</to>&#13;
                        <read>0</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>1</from>&#13;
                        <to>4</to>&#13;
                        <read>7</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>1</from>&#13;
                        <to>4</to>&#13;
                        <read>6</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>1</from>&#13;
                        <to>4</to>&#13;
                        <read>5</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>1</from>&#13;
                        <to>4</to>&#13;
                        <read>4</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>5</from>&#13;
                        <to>7</to>&#13;
                        <read>7</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>5</from>&#13;
                        <to>7</to>&#13;
                        <read>6</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>5</from>&#13;
                        <to>7</to>&#13;
                        <read>5</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>5</from>&#13;
                        <to>7</to>&#13;
                        <read>4</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>5</from>&#13;
                        <to>7</to>&#13;
                        <read>3</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>5</from>&#13;
                        <to>7</to>&#13;
                        <read>2</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>5</from>&#13;
                        <to>7</to>&#13;
                        <read>1</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>5</from>&#13;
                        <to>7</to>&#13;
                        <read>0</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>0</from>&#13;
                        <to>2</to>&#13;
                        <read>2</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>0</from>&#13;
                        <to>2</to>&#13;
                        <read>3</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>0</from>&#13;
                        <to>2</to>&#13;
                        <read>1</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>0</from>&#13;
                        <to>2</to>&#13;
                        <read>4</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>5</from>&#13;
                        <to>7</to>&#13;
                        <read>9</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>0</from>&#13;
                        <to>2</to>&#13;
                        <read>5</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>5</from>&#13;
                        <to>7</to>&#13;
                        <read>8</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>6</from>&#13;
                        <to>7</to>&#13;
                        <read>1</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>6</from>&#13;
                        <to>7</to>&#13;
                        <read>0</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>6</from>&#13;
                        <to>7</to>&#13;
                        <read>3</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>6</from>&#13;
                        <to>7</to>&#13;
                        <read>2</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>6</from>&#13;
                        <to>7</to>&#13;
                        <read>5</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>6</from>&#13;
                        <to>7</to>&#13;
                        <read>4</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>6</from>&#13;
                        <to>7</to>&#13;
                        <read>7</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>6</from>&#13;
                        <to>7</to>&#13;
                        <read>6</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>6</from>&#13;
                        <to>7</to>&#13;
                        <read>9</read>&#13;
                </transition>&#13;
                <transition>&#13;
                        <from>6</from>&#13;
                        <to>7</to>&#13;
                        <read>8</read>&#13;
                </transition>&#13;
        </automaton>&#13;
</structure>
"""

jflap_pda="""
<structure>;
	<type>pda</type>;
	<automaton>;
		<!--The list of states.-->;
		<state id="0" name="q0">;
			<x>213.0</x>;
			<y>273.0</y>;
			<initial/>;
		</state>;
		<state id="1" name="q1">;
			<x>395.0</x>;
			<y>276.0</y>;
		</state>;
		<state id="2" name="q2">;
			<x>706.0</x>;
			<y>275.0</y>;
		</state>;
		<state id="3" name="q3">;
			<x>570.0</x>;
			<y>417.0</y>;
		</state>;
		<state id="4" name="q4">;
			<x>462.0</x>;
			<y>441.0</y>;
			<final/>;
		</state>;
		<!--The list of transitions.-->;
		<transition>;
			<from>0</from>;
			<to>0</to>;
			<read>b</read>;
			<pop>B</pop>;
			<push>BB</push>;
		</transition>;
		<transition>;
			<from>0</from>;
			<to>0</to>;
			<read>b</read>;
			<pop>Z</pop>;
			<push>BZ</push>;
		</transition>;
		<transition>;
			<from>1</from>;
			<to>1</to>;
			<read>a</read>;
			<pop>A</pop>;
			<push>AA</push>;
		</transition>;
		<transition>;
			<from>1</from>;
			<to>1</to>;
			<read>a</read>;
			<pop>Z</pop>;
			<push>AZ</push>;
		</transition>;
		<transition>;
			<from>3</from>;
			<to>4</to>;
			<read/>;
			<pop>Z</pop>;
			<push/>;
		</transition>;
		<transition>;
			<from>1</from>;
			<to>1</to>;
			<read>a</read>;
			<pop>B</pop>;
			<push/>;
		</transition>;
		<transition>;
			<from>1</from>;
			<to>2</to>;
			<read>b</read>;
			<pop>A</pop>;
			<push/>;
		</transition>;
		<transition>;
			<from>2</from>;
			<to>2</to>;
			<read>b</read>;
			<pop>A</pop>;
			<push/>;
		</transition>;
		<transition>;
			<from>3</from>;
			<to>3</to>;
			<read>b</read>;
			<pop>A</pop>;
			<push/>;
		</transition>;
		<transition>;
			<from>2</from>;
			<to>3</to>;
			<read>m</read>;
			<pop/>;
			<push/>;
		</transition>;
		<transition>;
			<from>1</from>;
			<to>3</to>;
			<read>m</read>;
			<pop/>;
			<push/>;
		</transition>;
		<transition>;
			<from>0</from>;
			<to>3</to>;
			<read>m</read>;
			<pop/>;
			<push/>;
		</transition>;
		<transition>;
			<from>0</from>;
			<to>1</to>;
			<read>a</read>;
			<pop>Z</pop>;
			<push>AZ</push>;
		</transition>;
		<transition>;
			<from>0</from>;
			<to>1</to>;
			<read>a</read>;
			<pop>B</pop>;
			<push/>;
		</transition>;
	</automaton>;
</structure>
"""

jflap_tm="""<?xml version="1.0" encoding="UTF-8" standalone="no"?><!--Created with JFLAP 7.1.--><structure>&#13;
	<type>turingbb</type>&#13;
	<automaton>&#13;
		<!--The list of states.-->&#13;
		<block id="0" name="q0">&#13;
			<tag>Machine0</tag>&#13;
			<x>65.0</x>&#13;
			<y>168.0</y>&#13;
			<initial/>&#13;
		</block>&#13;
		<block id="1" name="q1">&#13;
			<tag>Machine1</tag>&#13;
			<x>205.0</x>&#13;
			<y>168.0</y>&#13;
		</block>&#13;
		<block id="2" name="q2">&#13;
			<tag>Machine2</tag>&#13;
			<x>346.0</x>&#13;
			<y>167.0</y>&#13;
		</block>&#13;
		<block id="3" name="q3">&#13;
			<tag>Machine3</tag>&#13;
			<x>502.0</x>&#13;
			<y>172.0</y>&#13;
		</block>&#13;
		<block id="4" name="q4">&#13;
			<tag>Machine4</tag>&#13;
			<x>659.0</x>&#13;
			<y>172.0</y>&#13;
		</block>&#13;
		<block id="5" name="q5">&#13;
			<tag>Machine5</tag>&#13;
			<x>812.0</x>&#13;
			<y>167.0</y>&#13;
		</block>&#13;
		<block id="6" name="q6">&#13;
			<tag>Machine6</tag>&#13;
			<x>961.0</x>&#13;
			<y>171.0</y>&#13;
		</block>&#13;
		<block id="7" name="q7">&#13;
			<tag>Machine7</tag>&#13;
			<x>760.0</x>&#13;
			<y>38.0</y>&#13;
		</block>&#13;
		<block id="8" name="q8">&#13;
			<tag>Machine8</tag>&#13;
			<x>462.0</x>&#13;
			<y>33.0</y>&#13;
		</block>&#13;
		<block id="9" name="q9">&#13;
			<tag>Machine9</tag>&#13;
			<x>925.0</x>&#13;
			<y>335.0</y>&#13;
		</block>&#13;
		<block id="10" name="q10">&#13;
			<tag>Machine10</tag>&#13;
			<x>418.0</x>&#13;
			<y>520.0</y>&#13;
		</block>&#13;
		<block id="11" name="q11">&#13;
			<tag>Machine11</tag>&#13;
			<x>285.0</x>&#13;
			<y>317.0</y>&#13;
		</block>&#13;
		<block id="12" name="q12">&#13;
			<tag>Machine12</tag>&#13;
			<x>1095.0</x>&#13;
			<y>170.0</y>&#13;
		</block>&#13;
		<block id="13" name="q13">&#13;
			<tag>Machine13</tag>&#13;
			<x>400.0</x>&#13;
			<y>268.0</y>&#13;
		</block>&#13;
		<block id="14" name="q14">&#13;
			<tag>Machine14</tag>&#13;
			<x>103.0</x>&#13;
			<y>388.0</y>&#13;
		</block>&#13;
		<block id="15" name="q15">&#13;
			<tag>Machine15</tag>&#13;
			<x>215.0</x>&#13;
			<y>440.0</y>&#13;
		</block>&#13;
		<block id="16" name="q16">&#13;
			<tag>Machine16</tag>&#13;
			<x>527.0</x>&#13;
			<y>559.0</y>&#13;
		</block>&#13;
		<block id="17" name="q17">&#13;
			<tag>Machine17</tag>&#13;
			<x>661.0</x>&#13;
			<y>598.0</y>&#13;
		</block>&#13;
		<block id="18" name="q18">&#13;
			<tag>Machine18</tag>&#13;
			<x>779.0</x>&#13;
			<y>479.0</y>&#13;
		</block>&#13;
		<block id="19" name="q19">&#13;
			<tag>Machine19</tag>&#13;
			<x>1006.0</x>&#13;
			<y>491.0</y>&#13;
			<final/>&#13;
		</block>&#13;
		<block id="20" name="q20">&#13;
			<tag>Machine20</tag>&#13;
			<x>962.0</x>&#13;
			<y>630.0</y>&#13;
		</block>&#13;
		<block id="21" name="q21">&#13;
			<tag>Machine21</tag>&#13;
			<x>1297.0</x>&#13;
			<y>428.0</y>&#13;
		</block>&#13;
		<block id="22" name="q22">&#13;
			<tag>Machine22</tag>&#13;
			<x>1152.0</x>&#13;
			<y>422.0</y>&#13;
		</block>&#13;
		<block id="23" name="q23">&#13;
			<tag>Machine23</tag>&#13;
			<x>1447.0</x>&#13;
			<y>427.0</y>&#13;
		</block>&#13;
		<block id="24" name="q24">&#13;
			<tag>Machine24</tag>&#13;
			<x>1635.0</x>&#13;
			<y>430.0</y>&#13;
		</block>&#13;
		<block id="25" name="q25">&#13;
			<tag>Machine25</tag>&#13;
			<x>1633.0</x>&#13;
			<y>216.0</y>&#13;
		</block>&#13;
		<block id="26" name="q26">&#13;
			<tag>Machine26</tag>&#13;
			<x>1465.0</x>&#13;
			<y>216.0</y>&#13;
		</block>&#13;
		<block id="27" name="q27">&#13;
			<tag>Machine27</tag>&#13;
			<x>1317.0</x>&#13;
			<y>217.0</y>&#13;
		</block>&#13;
		<block id="28" name="q28">&#13;
			<tag>Machine28</tag>&#13;
			<x>1221.0</x>&#13;
			<y>213.0</y>&#13;
		</block>&#13;
		<block id="29" name="q29">&#13;
			<tag>Machine29</tag>&#13;
			<x>1115.0</x>&#13;
			<y>277.0</y>&#13;
		</block>&#13;
		<block id="30" name="q30">&#13;
			<tag>Machine30</tag>&#13;
			<x>525.0</x>&#13;
			<y>423.0</y>&#13;
		</block>&#13;
		<!--The list of transitions.-->&#13;
		<transition>&#13;
			<from>10</from>&#13;
			<to>18</to>&#13;
			<read>I</read>&#13;
			<write>I</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>18</from>&#13;
			<to>19</to>&#13;
			<read/>&#13;
			<write/>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>11</from>&#13;
			<to>14</to>&#13;
			<controlx>146</controlx>&#13;
			<controly>225</controly>&#13;
			<read>1</read>&#13;
			<write>1</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>6</from>&#13;
			<to>12</to>&#13;
			<read>1</read>&#13;
			<write>1</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>16</from>&#13;
			<to>17</to>&#13;
			<read>1</read>&#13;
			<write>1</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>7</from>&#13;
			<to>8</to>&#13;
			<read>1</read>&#13;
			<write>1</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>14</from>&#13;
			<to>15</to>&#13;
			<read>1</read>&#13;
			<write>1</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>4</from>&#13;
			<to>5</to>&#13;
			<read>1</read>&#13;
			<write>1</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>11</from>&#13;
			<to>13</to>&#13;
			<read>0</read>&#13;
			<write>X</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>10</from>&#13;
			<to>16</to>&#13;
			<read>1</read>&#13;
			<write>1</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>22</from>&#13;
			<to>21</to>&#13;
			<read>1</read>&#13;
			<write>1</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>5</from>&#13;
			<to>9</to>&#13;
			<read/>&#13;
			<write/>&#13;
			<move>L</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>21</from>&#13;
			<to>23</to>&#13;
			<read>1</read>&#13;
			<write>1</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>24</from>&#13;
			<to>25</to>&#13;
			<read>1</read>&#13;
			<write>1</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>28</from>&#13;
			<to>29</to>&#13;
			<read>1</read>&#13;
			<write>1</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>3</from>&#13;
			<to>4</to>&#13;
			<read>1</read>&#13;
			<write>1</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>22</from>&#13;
			<to>9</to>&#13;
			<read/>&#13;
			<write>I</write>&#13;
			<move>L</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>15</from>&#13;
			<to>10</to>&#13;
			<read>1</read>&#13;
			<write>1</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>15</from>&#13;
			<to>20</to>&#13;
			<read>0</read>&#13;
			<write>Y</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>27</from>&#13;
			<to>28</to>&#13;
			<read>1</read>&#13;
			<write>1</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>30</from>&#13;
			<to>10</to>&#13;
			<read>1</read>&#13;
			<write>1</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>1</from>&#13;
			<to>2</to>&#13;
			<read>0</read>&#13;
			<write>X</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>29</from>&#13;
			<to>21</to>&#13;
			<read>1</read>&#13;
			<write>1</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>25</from>&#13;
			<to>26</to>&#13;
			<read>0</read>&#13;
			<write>0</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>17</from>&#13;
			<to>0</to>&#13;
			<controlx>-4</controlx>&#13;
			<controly>737</controly>&#13;
			<read>0</read>&#13;
			<write>0</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>29</from>&#13;
			<to>9</to>&#13;
			<read/>&#13;
			<write>I</write>&#13;
			<move>L</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>8</from>&#13;
			<to>2</to>&#13;
			<read>0</read>&#13;
			<write>0</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>13</from>&#13;
			<to>3</to>&#13;
			<read>1</read>&#13;
			<write>1</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>0</from>&#13;
			<to>1</to>&#13;
			<read>1</read>&#13;
			<write>1</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>12</from>&#13;
			<to>7</to>&#13;
			<read>0</read>&#13;
			<write>0</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>2</from>&#13;
			<to>3</to>&#13;
			<read>1</read>&#13;
			<write>1</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>9</from>&#13;
			<to>11</to>&#13;
			<read>X</read>&#13;
			<write>X</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>5</from>&#13;
			<to>6</to>&#13;
			<read>1</read>&#13;
			<write>1</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>9</from>&#13;
			<to>9</to>&#13;
			<read>I</read>&#13;
			<write>I</write>&#13;
			<move>L</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>9</from>&#13;
			<to>9</to>&#13;
			<read>0</read>&#13;
			<write>0</write>&#13;
			<move>L</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>9</from>&#13;
			<to>9</to>&#13;
			<read>1</read>&#13;
			<write>1</write>&#13;
			<move>L</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>26</from>&#13;
			<to>27</to>&#13;
			<read>1</read>&#13;
			<write>1</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>20</from>&#13;
			<to>22</to>&#13;
			<read>1</read>&#13;
			<write>1</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>3</from>&#13;
			<to>3</to>&#13;
			<read>0</read>&#13;
			<write>0</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>13</from>&#13;
			<to>13</to>&#13;
			<read>0</read>&#13;
			<write>0</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>24</from>&#13;
			<to>24</to>&#13;
			<read>0</read>&#13;
			<write>0</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>22</from>&#13;
			<to>22</to>&#13;
			<read>I</read>&#13;
			<write>I</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>0</from>&#13;
			<to>0</to>&#13;
			<read>0</read>&#13;
			<write>0</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>7</from>&#13;
			<to>7</to>&#13;
			<read>0</read>&#13;
			<write>0</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>27</from>&#13;
			<to>27</to>&#13;
			<read>0</read>&#13;
			<write>0</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>29</from>&#13;
			<to>29</to>&#13;
			<read>I</read>&#13;
			<write>I</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>30</from>&#13;
			<to>30</to>&#13;
			<read>0</read>&#13;
			<write>0</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>20</from>&#13;
			<to>20</to>&#13;
			<read>0</read>&#13;
			<write>0</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>26</from>&#13;
			<to>26</to>&#13;
			<read>0</read>&#13;
			<write>0</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>22</from>&#13;
			<to>22</to>&#13;
			<read>0</read>&#13;
			<write>0</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>2</from>&#13;
			<to>2</to>&#13;
			<read>0</read>&#13;
			<write>0</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>4</from>&#13;
			<to>4</to>&#13;
			<read>0</read>&#13;
			<write>0</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>14</from>&#13;
			<to>14</to>&#13;
			<read>0</read>&#13;
			<write>0</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>5</from>&#13;
			<to>5</to>&#13;
			<read>I</read>&#13;
			<write>I</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>10</from>&#13;
			<to>10</to>&#13;
			<read>0</read>&#13;
			<write>0</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>28</from>&#13;
			<to>28</to>&#13;
			<read>0</read>&#13;
			<write>0</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>18</from>&#13;
			<to>18</to>&#13;
			<read>I</read>&#13;
			<write>I</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>29</from>&#13;
			<to>29</to>&#13;
			<read>0</read>&#13;
			<write>0</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>5</from>&#13;
			<to>5</to>&#13;
			<read>0</read>&#13;
			<write>0</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>23</from>&#13;
			<to>24</to>&#13;
			<read>0</read>&#13;
			<write>0</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<transition>&#13;
			<from>9</from>&#13;
			<to>30</to>&#13;
			<read>Y</read>&#13;
			<write>Y</write>&#13;
			<move>R</move>&#13;
		</transition>&#13;
		<!--The list of automata-->&#13;
		<Machine22/>&#13;
		<Machine21/>&#13;
		<Machine20/>&#13;
		<Machine26/>&#13;
		<Machine25/>&#13;
		<Machine24/>&#13;
		<Machine23/>&#13;
		<Machine29/>&#13;
		<Machine28/>&#13;
		<Machine27/>&#13;
		<Machine8/>&#13;
		<Machine7/>&#13;
		<Machine9/>&#13;
		<Machine11/>&#13;
		<Machine10/>&#13;
		<Machine30/>&#13;
		<Machine15/>&#13;
		<Machine14/>&#13;
		<Machine13/>&#13;
		<Machine12/>&#13;
		<Machine19/>&#13;
		<Machine18/>&#13;
		<Machine17/>&#13;
		<Machine16/>&#13;
		<Machine0/>&#13;
		<Machine2/>&#13;
		<Machine1/>&#13;
		<Machine4/>&#13;
		<Machine3/>&#13;
		<Machine6/>&#13;
		<Machine5/>&#13;
	</automaton>&#13;
</structure>
"""

def test_load_dfa():
    """Test  load a DFA from string"""
    m=load_fa(dfa)
    assert len(m.Q)==2
    assert len(m.sigma)==2
    assert m.q_0=='q0'
    assert len(m.A)==1
    assert len(m.ttable)==2

def test_load_ndfa():
    """Test  load a NDFA from string"""
    m=load_fa(ndfa)
    assert len(m.Q)==3
    assert len(m.sigma)==2
    assert m.q_0=='q0'
    assert len(m.A)==1
    assert len(m.ttable)==3

def test_load_ndfa_e():
    """Test  load a NDFA-e from string"""
    m=load_fa(ndfa_e)
    assert len(m.Q)==3
    assert len(m.sigma)==3
    assert m.q_0=='q0'
    assert len(m.A)==1
    assert len(m.ttable)==3

def test_savefile():
    """Test saving file"""
    m=load_fa(dfa)
    outfile_path = tempfile.mkstemp()[1]
    m.save_file(outfile_path)
    assert os.path.exists(outfile_path)

def test_load_jflap_dfa():
    """Test loading jflap dfa"""
    m=load_jflap(jflap_dfa)
    assert len(m.Q)==7
    assert len(m.sigma)==2
    assert m.q_0=='q0'
    assert len(m.A)==1
    assert len(m.ttable)==7

def test_load_jflap_nfa():
    """Test loading jflap NDFA-e"""
    m=load_jflap(jflap_nfa, lambda x: f'q{x}')
    assert len(m.Q)==13
    assert len(m.symbols())==2
    assert m.q_0=='q0'
    assert len(m.A)==2
    assert len(m.ttable)==13

def test_load_jflap_extra():
    """Test loading jflap extra"""
    m=load_jflap(jflap_extra)
    assert len(m.ttable)>0


def test_string_dfa():
    """Creating string from DFA"""
    m1=load_fa(dfa)
    s=m1.to_string()
    m2=load_fa(s)
    assert len(m1.Q)==len(m2.Q)
    assert len(m1.symbols())==len(m2.symbols())
    assert m1.q_0==m2.q_0
    assert len(m1.A)==len(m2.A)
    assert len(m1.ttable)==len(m2.ttable)

def test_string_ndfa():
    """Creating string from NDFA"""
    m1=load_fa(ndfa)
    s=m1.to_string()
    m2=load_fa(s)
    assert len(m1.Q)==len(m2.Q)
    assert len(m1.symbols())==len(m2.symbols())
    assert m1.q_0==m2.q_0
    assert len(m1.A)==len(m2.A)
    assert len(m1.ttable)==len(m2.ttable)

def test_string_ndfa_e():
    """Creating string from NDFA-e"""
    m1=load_fa(ndfa_e)
    s=m1.to_string()
    m2=load_fa(s)
    assert len(m1.Q)==len(m2.Q)
    assert len(m1.symbols())==len(m2.symbols())
    assert m1.q_0==m2.q_0
    assert len(m1.A)==len(m2.A)
    assert len(m1.ttable)==len(m2.ttable)


def test_string_pda():
    """Creating string from NDFA-e"""
    m1=load_pda(pda)
    s=m1.to_string()
    m2=load_pda(s)
    assert len(m1.Q)==len(m2.Q)
    assert len(m1.symbols())==len(m2.symbols())
    assert m1.q_0==m2.q_0
    assert len(m1.A)==len(m2.A)
    assert len(m1.ttable)==len(m2.ttable)

def test_string_tspda():
    """Creating string from NDFA-e"""
    m1=load_tspda(tspda)
    s=m1.to_string()
    m2=load_tspda(s)
    assert len(m1.Q)==len(m2.Q)
    assert len(m1.symbols())==len(m2.symbols())
    assert m1.q_0==m2.q_0
    assert len(m1.A)==len(m2.A)
    assert len(m1.ttable)==len(m2.ttable)

def test_string_tm():
    """Creating string from NDFA-e"""
    m1=load_tm(tm)
    s=m1.to_string()
    m2=load_tm(s)
    assert len(m1.Q)==len(m2.Q)
    assert len(m1.symbols())==len(m2.symbols())
    assert m1.q_0==m2.q_0
    assert len(m1.A)==len(m2.A)
    assert len(m1.ttable)==len(m2.ttable)


def test_load_jflap_pda():
    """Test loading jflap PDA"""
    m=load_jflap(jflap_pda, lambda x: f'{x}')
    assert len(m.Q)==5
    assert len(m.symbols())==4
    assert len(m.qsymbols())==7
    assert m.q_0=='q0'
    assert len(m.A)==1
    assert len(m.ttable)==4

def test_load_jflap_tm():
    """Test loading jflap TM"""
    m=load_jflap(jflap_tm, lambda x: f'{x}')
    assert len(m.symbols())==5
    assert len(m.tsymbols())==6
    assert m.q_0=='q0'
    assert len(m.A)==1
    assert len(m.ttable)==30


