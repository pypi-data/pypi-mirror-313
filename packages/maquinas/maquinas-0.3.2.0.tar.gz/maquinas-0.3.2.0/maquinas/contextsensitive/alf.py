# Base class for Finite Machines
from maquinas.exceptions import *
from ordered_set import OrderedSet
import re
import tempfile
import os
from collections import defaultdict
import time

from PIL import Image, ImageDraw, ImageFont

from PIL import Image
from IPython.display import display, HTML
from graphviz import Digraph

re_tape = re.compile(r'(\[B\]|epsilon|"[^"]+"|\w)')


class Alf:
    """Automata lineal con frontera """

    def __init__(
        self, Q=[], sigma=[], gamma=[], B="𝖁", q_0=None, A=[], delta={}, force=False,
    start_ = "<",end_ = ">"):
        """Common class for Turing Machine

        :param Q: Ordered set of states (default is empty).
        :param sigma: Ordered set of terminal symbols (default is empty).
        :param gamma: Ordered set of tape symbols (default is empty).
        :param B: Blank symbol (default 𝖁).
        :param q_0: Initial state (default None).
        :param A: Set of acceptor states (default is empty).
        :param delta: List of transitions with the form tupla of tupla of q_i and a, and the list of q_f, a symbol and direction (default is empty).
        :param force: If True and states or symbols do not exists create them (default is False).
        :type force: bool
        """
        self.sigma = OrderedSet()
        self.B = B
        self.start_symbol = start_ 
        self.end_symbol =  end_
        self.i = 0
        self.gamma = OrderedSet()
        self.gamma.add(self.B)
        self.gamma.add(self.start_symbol)
        self.gamma.add(self.end_symbol)
        self.gamma.update([self._filter(g) for g in gamma])
        self.gamma.update(sigma)
        self.sigma.update(sigma)
        self.Q = OrderedSet(Q)
        self.set_initial_state(q_0)
        self.set_aceptors(A, force=force)
        self.ttable = {} #Documentar 
        
        for (q_i, a), qs in delta:
            self.add_transition(
                q_i,
                self._filter(a),
                [(q_f, self._filter(a), self._ndir(Dir)) for q_f, a, Dir in qs],
            )

        #self.curr = 0
        #self.tape = []
        self.tape = None
        self.tape_lenght =  0 
        self.w_in_tape =  False 
        #enums ---> 
        self.w_initial_pos =  1  #Por default la cadena va a posicionarse en medio

    
    def print_transition_table(self):
        print("Printing Transition table")
        if self.ttable :
            for key in self.ttable.keys():
                print(key,self.ttable[key])
        return self.ttable
    

    #documentar en texto
    def length_memory(self,w,param = 3 ):  # De 4 a 2 para que los visuales sean mas entendibles 
        return len(w) *  param
    
    def __getitem__(self, key):
        q, a = key
        return self.get_transition(q, a)

    def _nstate(self, q):
        return self.Q.index(q)

    def _nsymbol(self, a):
        return self.sigma.index(a)

    def _filter(self, t):
        return self.B if t == "[B]" or t.lower() == "blank" else t

    

#######Checar 
    def _dir(self, d):
        if d == 1:
            return "R"
        elif d == -1:
            return "L"
        else:
            return "N"

    def _ndir(self, d):
        if d == "R":
            return 1
        elif d == "L":
            return -1
        else:
            return 0

    def _ntsymbol(self, t):
        try:
            return self.gamma.index(self._filter(t))
        except KeyError as c:
            raise DoesNotExistsSymbol(c)

    def _state(self, nq):
        return self.Q.items[nq]

    def _symbol(self, na):
        return self.sigma.items[na]

    def _tsymbol(self, nz):
        return self.gamma.items[nz]

    def _status(self, status, states={}, symbols={}):
        return "|".join(f"{states.get(s,s)}" for s, _, _, _ in status)

    def states(self):
        """Gets states

        :returns: States of machine
        :rtype: list"""
        return list(self.Q)

    def symbols(self):
        """Gets terminal symbols

        :returns: Terminal symbols of machine
        :rtype: list"""
        return list(self.sigma)

    def tsymbols(self):
        """Gets tape symbols

        :returns: Tape symbols of machine
        :rtype: list"""
        return list(self.gamma)

    def tokens(self, r):
        """Gets  tokens for tape

        :returns: Tape symbols for machine
        :rtype: list"""
        return re_tape.findall(r)

    def _transition(self, nq_i, nt, nq_f, nt_, Dir):
        return (self._state(nq_i), self._tsymbol(nt)), (
            self._state(nq_f),
            self._tsymbol(nt_),
            Dir,
        )


    def __setitem__(self, key, value):
        q, t = key
        q_f, t_, Dir = value
        return self.add_transition(q, t, q_f, t_, Dir)

    def _get_transition(self, nq, nt): 
        try:
            return self.ttable[nq][nt]   
        except KeyError:
            return set()


#TODO: MOdificar delta 
#Consideraciones 

    def delta(self, states):

        """Applies delta function for Linearly Bounded Automaton."""
        states_ = set()
        for nq, tape, (c, a) in states:
            # Ensure the head does not exceed tape boundaries
            #if c == -1 or c >= len(self.tape):
             #   raise ValueError("Head is at the boundary and cannot move further.")
            try:
                na =  tape[c]
            except IndexError:
                raise ValueError("Head is at the boundary and cannot move further.")

            qs = self._get_transition(nq, na)
            tape = list(tape)
            for nq_f, t_, Dir in qs:
                                
                tape[c] = t_
                c = c + Dir  # Move head
                if c < 0 or c >= self.tape_lenght :
                    raise ValueError("Head moved out of bounds in the LBA.")
                states_.add((nq_f, tuple(tape), (c, tape[c])))  
        
        
        self.tape =  list(tape)
        return states_


    #TODO: 
    #def _tape(self, nt, pt):
     #   


    def delta_stepwise(self, w, q=None, max_steps=0,memory_function=None,most_left=1):
        """Applies a step of delta extended function

        :param w: String
        :param q: Internal state where to start (default is initial state)
        :param max_steps: Maximun number of steps to consider

        :returns: Tuple with state of precessing at step, consisting of: state, left tape, right tape, (position, processed string)"""
        if not self.tape :
            self.tape_init(w,memory_function)

        if q is None:
            states = self.create_initial_istate(w,most_left)
            yield self._index2label(states)

        steps = 0
        A = set(self._nstate(a) for a in self.A)
        while len(states):  
            
            final_states = set([q for q, _, _ in states])

            if final_states.intersection(A):    
                break
            try:
                states = self.delta(states)
            except:
                raise Exception("\nDelta stepwise failed")

            steps += 1
            yield self._index2label(states)
            #if set([s for s, _, _, _ in states]).intersection(A):
                #break
            if max_steps and steps >= max_steps:
                break
    
    def total_step_by_step(self, w, q=None, max_steps=0,memory_function=None,most_left=1,t=.25,function = None):
        self.clean()
        if not function:
            function =  self.states2string_q

        for states in self.delta_stepwise(w,q,max_steps,memory_function,most_left):
            if states:
                print(f"⊢ {function(states)}",end="\n")
                res=states
                time.sleep(t)
            else:
                print("Halts, no transition defined")


    def tape_init(self,w,memory_function = None):
        
       
        adjust = 0 

        if len (w) % 2 != 0 :
            adjust =  1

        if memory_function is None :
            memory_function = self.length_memory(w) 
            
            
            self.tape = [self._ntsymbol(self.B)] * ( memory_function +  2 +  adjust + 2)
            
            
        else:

            if not isinstance(memory_function(w), int):  # Verify the return type
                raise TypeError("Provided memory function must return an int")

            if memory_function(w) < len(w):
                raise Exception("Memory Function value is not correct")

            extra_space = 4

            if memory_function(w) <= (len(w) + 2):
                extra_space =  6
                
            if (memory_function(w) % 2 != 0  and adjust == 0) or (memory_function(w) % 2 == 0  and adjust != 0):
                extra_space += 1 
                
            self.tape = [self._ntsymbol(self.B)] * ( memory_function(w) + extra_space + adjust)

        self.tape_lenght =  len(self.tape)

        self.tape[0] =  self._ntsymbol(self.start_symbol)
        self.tape[len(self.tape)-1] =  self._ntsymbol(self.end_symbol)
        
 

    def first_write(self,w,start):
        

        if self.w_in_tape is False :
           
            for symbol in w :
                self.tape[start]  = self._ntsymbol(symbol)
                
                start += 1 
            self.w_in_tape = True 
    
    def inital_w_position(self,pos):
        #Definir un array de posiciones 
        ##Recibir como parametro el lugar a activar
        # pos = 0 Left
        # pos = 1 center 
        # pos = 2 rigth  , special case  
        for p in self.w_initial_pos:
            if p  ==  1 :
                raise Exception("w already in position")

        self.w_initial_pos[pos] =  1 
  


    def clean (self):

         self.tape = None 
         self.tape_lenght = 0 
         self.w_in_tape =  False 
         self.w_initial_pos =  None


    def create_initial_istate(self, w,most_left =  1):
        """Creates the initial internal state with the input string placed in the middle of the tape.

        :param w: Input string
        :return: Initial state with tape and position"""

        setted = False 

        if most_left == 0 :
                start_pos =  2
                #print("Left Most")

        elif most_left == 1:
            start_pos =  ((( (len(self.tape)-2) - len(w)))//2) +1 
            #print("Center ")

        elif most_left == 2:
            start_pos = len(self.tape) - (len(w) + 3)
            #print("Right most")
        
        elif len(self.tape)- len(w)  <= 4 and most_left == 1:
            start_pos = 3

        else:
            raise Exception ("No valid w position")

        self.first_write(w,start_pos)
        self.w_initial_pos = start_pos
        s = set( [(self._nstate(self.q_0), tuple(self.tape), (start_pos, self.tape[start_pos]) )]  )  
        #print("Create initial ",s)
        return s  

#***********************************************************************************
    def delta_extended(self, states, w,max_steps=None,memory_function = None,most_left=1):
        """Applies delta extended function.

        :param states: Internal states (initial state set if None).
        :param w: Input string to be processed.
        :param max_steps: Maximum number of steps to execute.
        :return: Returns final internal state after processing the string."""

        if not self.tape :
                self.tape_init(w,memory_function)

        if states is None:
            states = self.create_initial_istate(w,most_left)
        tests_=False 
        steps = 0
        final_states = set()
        i = 0 
        A = set(self._nstate(a) for a in self.A)
        # Continue processing until we reach an accept state or run out of steps
        
        #while len(states) > 0 and not final_states.intersection(self.A):
        while len(states):
            #print("Iterations: ",i)
            #print("STATES DELTA ITERATIONS:",states)

            final_states = set([q for q, _, _ in states])
            if final_states.intersection(A):
                
                break


            try:
                states = self.delta(states)  # Apply delta stepwise
            except:
                raise Exception("\nDelta extended Failed")
            
            steps += 1
            i += 1

            # If maximum steps are reached, return empty (no solution)
            if max_steps and steps >= max_steps:
                print("Maximu steps are reached\n")
                return []
        
        return self._index2label(states)
            

        # Return the state labels for the final configuration



    def _index2label(self, states_):
        """Converts index-based states into a readable string format.

        :param states_: Set of states in index form.
        :return: Readable states with tape and head position."""
        
        # Convert each state to its string label representation
        return [
            (
                self._state(q),  # Convert state index to state name
                tuple(self._tsymbol(s) for s in tape),  # Convert tape symbols
                (pos, self._tsymbol(tape[pos]))  # Position of head and symbol under head
            )
            for q, tape, (pos, _) in states_
        ]


    def _label2index(self, states):
        return [
            (
                self._nstate(q),
                tuple(self._ntsymbol(s) for s in tape),
                (pos, self._ntsymbol(tape[pos]))
            )
            for q, tape, c in states
        ]

    def items(self):
        """Iterator over the transitions

        :returns: Yeilds a tuple transition"""
        for nq_i, val in self.ttable.items():
            for nt, nq_fs in val.items():
                for (nq_f, nt_, Dir) in nq_fs:
                    yield self._transition(nq_i, nt, nq_f, nt_, Dir) ##Checar 

    def step(self, states):
        return self._index2label(self.delta(states))

    def get_transition(self, q, a):
        """Gets the destintion state or states for state, terminal symbol and stack symbol

        :param q: Source state
        :param a: Terminal symbol
        :returns: Destination state or states"""

        qs = self._get_transition(self._nstate(q), self._nsymbol(a))
        return [(self._state(s), self.tsymbol(a), d) for s, a, d in qs]

    def add_transition(self, q_i, t, qs, force=False, update=False):
        """Adds a transition

        :param q_i: Source state
        :param t: Tape symbol
        :param q_s: Destination state (q_f,t_2,dir)
        :param force: Force creation of elements
        :returns: None"""
        try:
            nq_i = self.add_state(q_i)
        except AlreadyExistsState:
            nq_i = self._nstate(q_i)
        try:
            nt = self.add_tsymbol(t)
        except AlreadyExistsSymbol:
            nt = self._ntsymbol(t)

        #TODO: Differenciate among sigma and gamma

        if force:
            for q_f, a_, _ in qs:
                try:
                    self.add_state(q_f)
                except AlreadyExistsState:
                    pass
                try:
                    self.add_tsymbol(a_)
                except AlreadyExistsSymbol:
                    pass

        qs = [(self._nstate(q), self._ntsymbol(t), Dir) for q, t, Dir in qs]  ##Actualizar 

        ##RELLENO DE TTABLE ***************

        if nq_i in self.ttable and nt in self.ttable[nq_i]:
            if update:
                self.ttable[nq_i][nt].update(qs)
            else:
                raise AlreadyExistsTMTransition(q_i, t, self)
        else:
            if not nq_i in self.ttable:   
                self.ttable[nq_i] = {}
            if not nt in self.ttable[nq_i]:
                self.ttable[nq_i][nt] = set()
            self.ttable[nq_i][nt].update(qs)

    def add_state(self, q, initial=False):
        """Adds a state

        :param q: State or states
        :param initial: Set state as a initial
        :returns: Indixes of state or states"""
        if initial:
            self.q_0 = q
        if q in self.Q:
            raise AlreadyExistsState(q)
        if isinstance(q, (set, list)):
            return set(self.Q.add(q_) for q_ in q)
        else:
            return self.Q.add(q)

    def add_next_state(self, initial=False):
        """Adds a state with a infered name based on the number of states q_max. If the name state is already defined it looks the following integer available.

        :param q: State or states
        :param initial: Set state as a initial
        :returns: Next state generated and integer"""
        max_ix = len(self.Q)
        while f"q_{max_ix}" in self.Q:
            max_ix += 1
        q = f"q_{max_ix}"
        self.Q.add(q)
        if initial:
            self.q_0 = q
        return q, max_ix

    def add_symbol(self, a):
        """Adds a symbol

        :param a: Symbol
        :returns: Indixes of symbol"""
        if a in self.gamma:
            raise AlreadyExistsSymbol(a)
        return self.sigma.add(a)
        return self.gamma.add(a)

    def add_tsymbol(self, t):
        """Adds a tape symbol

        :param t: Tape xymbol
        :returns: Indixes of symbol"""
        if t in self.gamma:
            raise AlreadyExistsSymbol(t)
        return self.gamma.add(t)

    def set_initial_state(self, q, force=False):
        """Sets an initial state

        :param q: State
        :param force: If not defined it creates it (default is False)
        :returns: None"""
        if q is None:
            self.q_0 = None
            return None
        if not q in self.Q:
            if force:
                self.add_state(q)
            else:
                raise DoesNotExistsState(q)
        self.q_0 = q

    def get_initial_state(self):
        """Gets an initial state

        :returns: State"""
        return self.q_0

    def set_aceptors(self, A, force=False):
        """Sets aceptors states

        :param A: States
        :param force: If not defined it creates it (default is False)
        :returns: None"""
        if force:
            self.add_state(A)
        self.A = set(A)

    def stepStatus(self, status,most_left=1):
        """Gives a step and calculates new status for Simulation

        :param Status: Status
        :returns: None"""
        if status.state is None:
            states = self._index2label(self.create_initial_istate(status.string,most_left))
        else:
            states = status.state
        states = self.step(self._label2index(states))
        status.position += 1
        status.step += 1
        status.state = states

    def accepts(self, w, max_steps=0,memory_function = None,most_left=1):
        """Checks if string is accepted

        :param w: String
        :returns: None"""   
        
        self.tape_init(w,memory_function)
        try:

            res = self.acceptor(self.delta_extended(None, w, max_steps=max_steps,most_left=most_left))
            return res 
        except:
            return False

    def acceptor(self, states):
        """Checks if state is an acceptor state

        :param states: State or states
        :type: Set

        :returns: None"""
        try:
            final = set([q for q, _, _ in states])  # Extract state indices
        except ValueError as e:
            raise ValueError(f"Invalid state structure in acceptor: {states}") from e

        if bool(final.intersection(self.A)):
            return True
        return False
   
    
    def render_step(self, tape, state, pos, step_number, save_path="step.png"):
        # Settings
        cell_width, cell_height = 60, 60
        tape_len = len(tape)
        img_width = cell_width * tape_len
        img_height = cell_height * 3
        
        # Create image
        img = Image.new("RGB", (img_width, img_height), "white")
        draw = ImageDraw.Draw(img)
        
        # Load a font that supports Unicode
        try:
            font = ImageFont.truetype("DejaVuSansMono.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        # Draw tape
        for i, symbol in enumerate(tape):
            x = i * cell_width
            draw.rectangle([x, cell_height, x + cell_width, 2 * cell_height], outline="black", width=2)
            draw.text((x + cell_width // 3, cell_height + cell_height // 3), str(symbol), fill="black", font=font)
        
        # Highlight tape head
        head_x = pos * cell_width
        draw.rectangle([head_x, cell_height, head_x + cell_width, 2 * cell_height], outline="blue", width=4)

        # Draw state above tape
        state_text = f"State: {state} | Step: {step_number}"
        draw.text((cell_width, cell_height // 4), state_text, fill="blue", font=font)

        # Save the image
        img.save(save_path)


    
    def generate_steps(self, w, output_prefix="step", delay=0.15,q=None,max_steps=0,memory_function=None,most_left=1):
        """
        Generates a sequence of images representing each step of the automaton.

        :param automaton: The automaton object.
        :param input_string: The input string to process.
        :param output_prefix: Prefix for output image filenames.
        :param delay: Time delay (in seconds) between steps.
        """
        step_number = 0

        self.clean()
        print("Making gif...")
        for step in self.delta_stepwise(w,q,max_steps,memory_function,most_left):
            # Extract tape, state, and position from the step
            for state, tape, (pos, _) in step:
                '''
                self.render_step(
                    tape,
                    state,
                    pos,
                    step_number,
                    save_path=f"{output_prefix}_{step_number}.png"
                )
                '''
                #print(f"Step: {step_number}, State: {state}, Tape: {tape}, Head Pos: {pos}")
                
                self.render_step(tape, state, pos, step_number, save_path=f"{output_prefix}_{step_number}.png")
                step_number += 1
                time.sleep(delay)
        print("Done")


    def create_gif(self,output_prefix, num_steps, gif_name="automaton.gif", duration=500):
        """
        Combines step images into an animated GIF.

        :param output_prefix: Prefix of the step images.
        :param num_steps: Total number of steps.
        :param gif_name: Name of the output GIF file.
        :param duration: Duration between frames in milliseconds.
        """
        images = []
        for i in range(num_steps):
            img_path = f"{output_prefix}_{i}.png"
            images.append(Image.open(img_path))
        
        images[0].save(
            gif_name,
            save_all=True,
            append_images=images[1:],
            duration=duration,
            loop=0
        )



    def save_img(
        self,
        filename,
        q_c=set(),
        a_c=set(),
        q_prev=set(),
        symbols={},
        states={},
        format="svg",
        dpi="60.0",
        string=None,
        status=None,
    ):
        """Saves machine as an image

        :param filename: Filename of image
        :param q_c: Set of current states to be highlited (default is empty)
        :param a_c: Set of current symbols to be highlited (default is empty)
        :param q_prev: Set of previos states to be highlited (default is empty)
        :param symbols: Replacements of the symbols to show (default is empty)
        :param states: Replacements of the states to show (default is empty)
        :param format: Format of image (default is svg)
        :param dpi: Resolution of image (default is "90.0")
        :param string: Label of string being analysed (default is None)
        :param stack: Status of the stack (default is None)
        :param status: Status of the TM (default is None)

        :returns: None"""
        dot = self.graph(
            q_c=q_c,
            a_c=a_c,
            q_prev=q_prev,
            symbols=symbols,
            states=states,
            format=format,
            dpi=dpi,
            string=string,
            status=status,
        )
        dot.render(filename, format="png", cleanup=True)

    
    #ARREGLAR 
    def states2string(self, states):
        """Renders srting with the state of the Alf

        :returns: String tiwh the states of the ALF"""
        res = []
        for q, tape, (c, a) in states:
            colored_symbol = f"\033[32m_{tape[c]}_\033[0m" #Verde
            #f"\033[1;31m_{tape[c]}_\033[0m" #Rojo
            res.append(      #Cambiar por arreglo
                "{},  {} _{}_ {} ".format(
                    q,
                    " ".join([t for t in tape[:c]]),
                    colored_symbol,#tape[c],
                    " ".join([t for t in tape[c + 1 :]]),
                )
            )
        return "|".join(res)

    def states2string_q(self, states):
        """Renders srting with the state of the Alf

        :returns: String tiwh the states of the ALF"""
        #print("States to convert : ",states)
        res = []
        for q, tape, (c, a) in states:
            #tape = self.tape
            #print("TAPE IN CYCLE: ",tape)
            colored_symbol = f"\033[32m_{tape[c]}_\033[0m" #Verde
            colored_state =  f"\033[1;34m{q}\033[0m"  #Azul
            #f"\033[1;31m_{tape[c]}_\033[0m" #Rojo
            res.append(      #Cambiar por arreglo
                "  {} {} {} {} ".format(
                    " ".join([t for t in tape[:c]]),colored_state,
                    colored_symbol,#tape[c],
                    " ".join([t for t in tape[c + 1 :]]),
                )
            )
        return "|".join(res)

    def to_string(self, order_Q=None, order_gamma=None): ###
        """Creates a string

        :param order_Q: Order to print states
        :param order_sigma: Order to print alphabet
        :param order_gamma: Order to print stack alphabet

        :returns: None
        """
        largest_q = max([len(q) for q in self.Q])
        largest_q += 3
        largest_cell = {a: 2 for a in self.gamma}
        ttable = defaultdict(list)
        ttable_ = defaultdict(list)
        for (q_i, a), (q_f, a_, Dir) in self.items():
            ttable[(q_i, a)].append(f"{a}/{a_}→{q_f}:{self._dir(Dir)}")

        for (q_i, a), elements_cell in ttable.items():
            largest_cell[a] = max(largest_cell[a], len(",".join(elements_cell)))
        order_Q = list(self.Q) if not order_Q else order_Q
        order_gamma = list(self.gamma) if not order_gamma else order_gamma
        strings = []
        # Alphabet line
        strings.append(
            " " * (largest_q + 2)
            + "|"
            + "|".join(
                " {: ^{width}} ".format(a, width=l)
                for a in order_gamma
                if (l := largest_cell[a])
            )
            + "|"
        )
        # Printing states
        for q_i in order_Q:
            q_l = q_i
            if q_i == self.q_0:
                q_l = f"->{q_i}"
            if q_i in self.A:
                q_l = f"{q_l}]"
            if q_i == self.q_0:
                strings.append(" {: <{width}}|".format(q_l, width=largest_q + 1))
            else:
                strings.append("   {: <{width}}|".format(q_l, width=largest_q - 1))
            line = []
            for a in order_gamma:
                e = ttable[(q_i, a)]
                line.append(",".join(e))
            r = "|".join(
                " {: ^{width}} ".format(c, width=l)
                for c, a in zip(line, order_gamma)
                if (l := largest_cell[a])
            )
            strings[-1] += r + "|"
        return "\n".join(strings)

    def save_file(
        self, filename="machine.txt", order_Q=None, order_gamma=None
    ):
        """Saves a file

        :param filename: Name of filename (default is machine.txt)
        :param order_gamma: Order to print stack alphabet

        :returns: None
        """
        string = self.to_string(
            order_Q=order_Q, order_gamma=order_gamma
        )
        with open(filename, "w") as f:
            f.write(string)


    def summary(self):
        """Producrs summary of the PDA
        :returns: List with summary"""
        info = [
            "States  : " + ", ".join(self.states()),
            "Sigma   : " + ", ".join(self.symbols()),
            "Gamma   : " + ", ".join(self.tsymbols()),
            "Initial : " + self.q_0,
            "Aceptors: " + ", ".join(self.A),
            "Transitions:\n"
            + "\n".join(
                f" {q_i},{t}/{t_} → {q_f}:{self._dir(Dir)}"
                for (q_i, t), (q_f, t_, Dir) in self.items()
            ),
        ]
        return "\n".join(info)

    def print_summary(self):
        """Prints a summary of the PDA"""
        print(self.summary())

    def graph(
        self,
        q_c=set(),
        a_c=set(),
        q_prev=set(),
        symbols={},
        states={},
        format="svg",
        dpi="60.0",
        string=None,
        status=None,
        one_arc=True,
        finished=False,
    ):
        """Graphs TM

            :param q_c: Set of current states to be highlited (default is empty)
            :param a_c: Set of current symbols to be highlited (default is empty)
            :param q_prev: Set of previos states to be highlited (default is empty)
            :param symbols: Replacements of the symbols to show (default is empty)
            :param states: Replacements of the states to show (default is empty)
            :param format: Format of image (default is svg)
        :param dpi: Resolution of image (default is "60.0")
            :param string: Label of string being analysed (default is None)
            :param status: Status of the TM (default is None)
            :param one_arc: Graph one arc in case of multiple transitions (default is True)
            :param finished: If has pass through final state (default is False)

            :returns: Returns Digraph object from graphviz"""
        if len(q_c) == 0:
            states_ = [(self._nstate(self.q_0), (), (0, ""))]  
        else:
            states_ = q_c
            

        f = Digraph(comment="Alf", format=format)
        f.attr(rankdir="LR", dpi=dpi)
        #print("STATES_:, ",states_)

        for i, (q_c_, tape, (c, a)) in enumerate(states_):
            if len(q_c) > 0:
                q_c_ = set([q_c_])
            else:
                q_c_ = []
            with f.subgraph(name=f"cluster_{i}") as f_:
                self._graph(
                    f_,
                    i=i,
                    q_c=q_c_,
                    a_c=set([a]),
                    q_prev=q_prev,
                    symbols=symbols,
                    states=states,
                    tape=self.tape,
                    #pos=c + len(nt),
                    pos=c,
                    dpi=dpi,
                    format=format,
                    status=status,
                    string=string,
                    one_arc=one_arc,
                )
        return f

    def _graph(
        self,
        f,
        i=0,
        q_c=set(),
        a_c=set(),
        q_prev=set(),
        states={},
        symbols={},
        format="svg",
        dpi="60.0",
        string=None,
        tape=None,
        status=None,
        one_arc=True,
        pos=None,
        finished=False,
    ):
        label_tape = None
        if len(self.A.intersection(q_c)) > 0:
            color_state = "limegreen"
        else:
            if status == None:
                color_state = "lightblue2"
            else:
                color_state = "orangered"

        f.attr(style="invis", labelloc="b")

        if tape:
            cells = []
            for i, c in enumerate(tape):
                if i == pos:
                    cells.append(f'<TD BGCOLOR="{color_state}">{symbols.get(c,c)}</TD>')
                else:
                    cells.append(f"<TD>{symbols.get(c,c)}</TD>")
            label_tape = f"< <TABLE BORDER='0' CELLBORDER='1' SIDES='TBRL'><TR>{' '.join(cells)}</TR></TABLE> >"

        if label_tape:
            f.attr(label=label_tape)

        for q, _ in self.Q.map.items():
            if q in self.A:
                shape = "doublecircle"
            else:
                shape = "circle"
            if q in q_c:
                f.node(
                    name=f"{q}_{i}",
                    label=states.get(q, q),
                    shape=shape,
                    color=color_state,
                    style="filled",
                )
            else:
                f.node(name=f"{q}_{i}", label=states.get(q, q), shape=shape)

        edges = defaultdict(list)
        for e, info in enumerate(self.items()):
            (q_i, a), (q_f, a_, Dir) = info
            if (q_f in q_c and q_i in q_prev) and (a in a_c):
                edges[(f"{q_i}_{i}", f"{q_f}_{i}")].append(
                    (f"{symbols.get(a,a)}/{symbols.get(a_,a_)},{self._dir(Dir)}", True)
                )
            else:
                edges[(f"{q_i}_{i}", f"{q_f}_{i}")].append(
                    (f"{symbols.get(a,a)}/{symbols.get(a_,a_)},{self._dir(Dir)}", False)
                )

        for (q_i, q_f), labels in edges.items():
            if one_arc:
                tags = []
                colored_ = False
                for label, colored in labels:
                    if colored:
                        colored_ = True
                        tags.append(f'<FONT color="{color_state}">{label}</FONT>')
                    else:
                        tags.append(f"{label}")
                tags = f'< {"<BR/>".join(tags)} >'
                if colored_:
                    f.edge(q_i, q_f, label=tags, labelloc="b", color=color_state)
                else:
                    f.edge(q_i, q_f, label=tags, labelloc="b")
            elif not one_arc:
                for label, colored in labels:
                    if colored:
                        f.edge(
                            q_i,
                            q_f,
                            label=label,
                            labelloc="b",
                            color=color_state,
                            fontcolor=color_state,
                        )
                    else:
                        f.edge(q_i, q_f, label=label, labelloc="b")
        return f

    def table(
        self,
        symbols={},
        states={},
        q_order=None,
        s_order=None,
        color_final="#32a852",
        empty_symbol="∅",
    ):
        """Creates an HTML object for the table of the PDA

        :param symbols: Replacements of the symbols to show (default is empty)
        :param states: Replacements of the states to show (default is empty)
        :param  q_order: Order to use for states
        :param  s_order: Order to use for symbols
        :param color_final: RGB string for color of final state (default is "#32a852")

        :returns: Display object for IPython"""
        if not s_order:
            s_order = list(self.gamma)
            s_order.sort()
        if not q_order:
            q_order = list(self.Q)
            q_order.sort()
        symbs_h = "</strong></td><td><strong>".join(
            [symbols.get(q, q) for q in s_order]
        )
        table = f"<table><tr><td></td><td><strong>{symbs_h}</strong></td></tr>"
        for q_i in q_order:
            vals = []
            initial = "⟶" if q_i == self.q_0 else ""
            final = f'bgcolor="{color_final}"' if q_i in self.A else ""
            vals.append(f"<strong>{initial}{states.get(q_i,q_i)}</strong>")
            for a in s_order:
                try:
                    labels = []
                    for q_f, r, Dir in self.ttable[self._nstate(q_i)][
                        self._ntsymbol(a)
                    ]:
                        labels.append(
                            f"/{symbols.get(self._tsymbol(r),self._tsymbol(r))}→{self._state(q_f)},{self._dir(Dir)}"
                        )
                    vals.append("<br/>".join(labels))
                except KeyError:
                    vals.append(empty_symbol)
            row = "</td><td>".join(vals)
            table += f"<tr><td {final}>{row}</td></tr>"
        table += "</table>"
        return display(HTML(table))

    def save_gif(
        self,
        w,
        filename="alf.gif",
        symbols={},
        states={},
        dpi="90",
        show=True,
        loop=0,
        duration=500,
        max_steps=1000,
    ):
        """Saves an animation of  machine

        :param w: String to analysed during animation
        :param filename: Name of gif (default is tm.gif")
        :param symbols: Replacements of the symbols to show (default is empty)
        :param states: Replacements of the states to show (default is empty)
        :param dpi: Resolution of image (default is "90.0")
        :param show: In interactive mode return gif
        :param loop: Number of loops in annimation, cero is forever (default is 0)
        :param duration: Duration in msegs among steps (default is 500)
        :param max_steps: Maximum number of steps to consider (default is 1000)
        :returns: None or HTML for Ipython"""
        dirpath = tempfile.mkdtemp()
        i = 0
        images = []
        q_prev = set()
        max_images_height = 1
        status = None
        for ii, q in enumerate(self.delta_stepwise(w)):
            if len(q) == 0:
                status = self.accept(q_prev)
                if status:
                    break
                q = q_prev
                q_prev = set()
            if ii >= max_steps:
                break
            filename_ = os.path.join(dirpath, f"{i}")
            g = self.save_img(
                filename_,
                q_c=q,
                q_prev=set([q_c for q_c, _, _, _ in q]),
                symbols=symbols,
                states=states,
                status=status,
                dpi=dpi,
                format="png",
            )
            q_prev = q
            im = Image.open(filename_ + ".png")
            width, height = im.size
            max_images_height = max(max_images_height, height)
            images.append(im)
            i += 1
            filename_ = os.path.join(dirpath, f"{i}")
            g = self.save_img(
                filename_,
                q_c=q,
                status=status,
                symbols=symbols,
                states=states,
                dpi=dpi,
                format="png",
            )
            im = Image.open(filename_ + ".png")
            images.append(im)
            i += 1
        images.append(im)
        images.append(im)
        images.append(im)
        images.append(im)

        for i, im in enumerate(images):
            im2 = Image.new("RGB", (width, max_images_height), (255, 255, 255))
            width, height = im.size
            im2.paste(im)
            images[i] = im2

        images[0].save(
            filename,
            save_all=True,
            append_images=images[1:],
            optimize=False,
            duration=500,
            loop=loop,
        )
        if show:
            return HTML(f'<img src="{filename}">')
        else:
            return
