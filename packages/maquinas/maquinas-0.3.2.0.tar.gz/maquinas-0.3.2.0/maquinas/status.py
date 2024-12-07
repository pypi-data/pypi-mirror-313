# Código para Estado

from maquinas.exceptions import *
from maquinas.recursivelyenumerable.tm import TuringMachine


class Status:
    def __init__(self, machine, string="", state=None, memory=None):
        self.step = 0
        self.status = None
        self.position = 0
        self.machine = machine
        self.string = string
        if not machine is None:
            self.state = self.machine.delta_extended(None, "")
        else:
            self.state = None
        self.set_tape(string)
        self.memory = memory
        self.history = []
        self.positioncolor = "#b3e0ff"
        self.sucesscolor = "##00b300"
        self.failcolor = "#ff6666"

    def __str__(self):
        r = {
            "step": self.step,
            "tape": [_ for _ in self.tape],
            "pos": self.position,
            "state": self.state,
        }
        return str(r)

    def set_tape(self, string):
        if isinstance(self.machine, TuringMachine):
            self.tape = None
            for state in self.machine.delta_stepwise(string):
                self.state = state
                break
        else:
            self.tape = f"{string}"

    def get_symbol_tape(self):
        try:
            return self.tape[self.position]
        except IndexError:
            self.status = self.machine.accept(self.state)

    def get_memory(self):
        return self.memory

    def next(self, dir=-1):
        if not self.status is None:
            return None
        if self.step == len(self.history):
            prev = {
                "step": self.step,
                "tape": [_ for _ in self.tape] if self.tape else None,
                "pos": self.position,
                "state": self.state,
            }
            self.history.append(prev)
            try:
                self.machine.stepStatus(self)
            except DoesNotExistsSymbol:
                self.status = False
        else:
            step = self.history[self.step + 1]
            self.step = step["step"]
            self.tape = step["tape"]
            self.position = step["pos"]
            self.state = step["state"]
        if self.tape and self.position == len(self.tape):
            self.status = self.machine.acceptor(self.state)
        if not self.tape:
            if len(self.state) == 0:
                self.status = False
                self.state = self.history[-1]["state"]
            else:
                if self.machine.acceptor(self.state):
                    self.status = True

    def is_finish(self):
        if self.tape:
            return self.position == len(self.tape)
        else:
            return False

    def tape2html(self, ncols=20, symbols={}, states={}):
        if self.tape:
            tape_idx = list(enumerate(self.tape))
            tape = tape_idx[
                max(0, self.position - ncols) : min(
                    2 * ncols, self.position + ncols + 1
                )
            ]
            columns = []
            for pos, symbol in tape:
                symbol_ = symbols.get(symbol, symbol)
                if self.status is None:
                    if pos == self.position:
                        columns.append(
                            f"<td  bgcolor='{self.positioncolor}'>{symbol_}</td>"
                        )
                    else:
                        columns.append(f"<td>{symbol_}</td>")
                elif self.status:
                    columns.append(f"<td  bgcolor='{self.sucesscolor}'>{symbol_}</td>")
                else:
                    columns.append(f"<td  bgcolor='{self.failcolor}'>{symbol_}</td>")
            columns = "".join(columns)
            row = f"<tr>{columns}</tr>"
        if self.status is None:
            status = "Processing"
        elif self.status:
            status = "Accepted"
        else:
            status = "Rejected"

        state_ = self.machine._status(self.state, states=states, symbols=symbols)
        if self.tape:
            table = f"<strong>Estado actual:</strong> {state_}<br/><strong>Cadena:</strong> {status}<table>{row}</table>"
        else:
            table = f"<strong>Estado actual:</strong> {state_}<br/><strong>"
        return table
