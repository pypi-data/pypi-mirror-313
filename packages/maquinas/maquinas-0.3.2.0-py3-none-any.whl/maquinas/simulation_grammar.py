# Código de simulación
import ipywidgets as widgets
from IPython.core.display import display, HTML, Markdown, clear_output
from maquinas.status import Status


class SimulationGrammar:
    def __init__(self, grammar, string="", speed=1, symbols={}, states={}):
        self.speed = speed
        self.symbols = symbols
        self.states = states
        self.input_string = widgets.Text(
            value=string,
            description="Cadena",
        )
        self.button_load_string = widgets.Button(description="⏎")
        self.string = widgets.HBox([self.input_string, self.button_load_string])
        self.button_forward = widgets.Button(description="▶️")
        self.button_reverse = widgets.Button(description="◀️")
        self.controls = widgets.HBox([self.button_reverse, self.button_forward])
        self.output = widgets.Output()
        self.button_forward.on_click(self._next)
        self.button_load_string.on_click(self._load_string)

    def reset(self, strin=""):
        self.status = Status(self.status.machine)

    def display(self):
        with self.output:
            clear_output()
            display(
                HTML(self.status.tape2html(symbols=self.symbols, states=self.states))
            )
            display(
                self.status.machine.graph(
                    self.status.state, symbols=self.symbols, states=self.states
                )
            )

    def _load_string(self, b):
        self.reset()
        self.status.tape = self.input_string.value
        self.display()

    def _next(self, b):
        self.status.next()
        self.display()

    def run(self, text=None):
        self.status.tape = self.input_string.value
        self.display()
        return display(widgets.VBox([self.string, self.controls, self.output]))
