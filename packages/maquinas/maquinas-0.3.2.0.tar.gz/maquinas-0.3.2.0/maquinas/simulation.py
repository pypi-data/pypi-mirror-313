# Código de simulación
import ipywidgets as widgets
from IPython.display import display, HTML, Markdown, clear_output
from maquinas.status import Status
from PIL import Image
import tempfile
import time


class Simulation:
    def __init__(self, machine, string="", speed=1, symbols={}, states={}):
        self.status = Status(machine)
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
        self.button_gif = widgets.Button(description="💾")
        self.controls = widgets.HBox(
            [self.button_reverse, self.button_forward, self.button_gif]
        )
        self.output = widgets.Output()
        self.button_forward.on_click(self._next)
        self.button_load_string.on_click(self._load_string)
        self.button_gif.on_click(self._create_gif)

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
                    self.status.state, symbols=self.symbols, status=self.status.status
                )
            )

    def _load_string(self, b):
        self.reset()
        self.status.set_tape(self.input_string.value)
        self.display()

    def _next(self, b):
        self.status.next()
        self.display()

    def _play(self, b):
        self.reset()
        self.status.set_tape(self.input_string.value)
        while not self.status.is_finish():
            self.display()
            time.sleep(self.speed)
            self.status.next()
        self.display()
        time.sleep(self.speed)
        self.status.next()

    def _create_gif(self, b):
        pass

    def run(self, text=None):
        self.status.set_tape(self.input_string.value)
        self.display()
        return display(widgets.VBox([self.string, self.controls, self.output]))
