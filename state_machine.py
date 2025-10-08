from enum import Enum, auto
import time

class State(Enum):
    IDLE = auto()
    READY = auto()
    CHARGING = auto()
    FAULT = auto()

class LedPattern(Enum):
    OFF = auto()
    SLOW = auto()
    FAST = auto()
    FAULT = auto()

class IO:
    """Simulación de entradas/salidas."""
    def __init__(self):
        self.PILOT_OK = 0
        self.FAULT = 0
        self.BTN = 0
        self.CONTACTOR = 0
        self.LED = LedPattern.OFF

class StateMachine:
    DEBOUNCE_MS = 20

    def __init__(self, io, clock=lambda: int(time.time() * 1000)):
        self.io = io
        self.clock = clock
        self.state = State.IDLE
        self.last_btn = 0
        self.last_btn_time = 0
        self.led_forzado = None

    def _debounce_btn(self):
        now = self.clock()
        changed = False
        if self.io.BTN != self.last_btn:
            if now - self.last_btn_time >= self.DEBOUNCE_MS:
                changed = self.io.BTN == 1  # Borde ascendente
                self.last_btn = self.io.BTN
                self.last_btn_time = now
        return changed

    def force_led(self, pattern):
        self.led_forzado = pattern

    def tick(self):
        # Transición a FAULT si FAULT activa
        if self.io.FAULT:
            self.state = State.FAULT
        elif self.state == State.FAULT:
            if not self.io.FAULT and self._debounce_btn():
                self.state = State.IDLE

        elif self.state == State.IDLE:
            self.io.CONTACTOR = 0
            if self.io.PILOT_OK:
                self.state = State.READY
        elif self.state == State.READY:
            if self._debounce_btn():
                self.state = State.CHARGING
            elif not self.io.PILOT_OK:
                self.state = State.IDLE
        elif self.state == State.CHARGING:
            self.io.CONTACTOR = 1
            if not self.io.PILOT_OK:
                self.state = State.IDLE

        # LED pattern según estado (si no forzado)
        if self.led_forzado is not None:
            self.io.LED = self.led_forzado
        else:
            if self.state == State.IDLE:
                self.io.LED = LedPattern.SLOW
            elif self.state == State.READY:
                self.io.LED = LedPattern.OFF
            elif self.state == State.CHARGING:
                self.io.LED = LedPattern.FAST
            elif self.state == State.FAULT:
                self.io.LED = LedPattern.FAULT

    def get_state(self):
        return self.state.name

    def get_io(self):
        return {
            "PILOT_OK": self.io.PILOT_OK,
            "FAULT": self.io.FAULT,
            "BTN": self.io.BTN,
            "CONTACTOR": self.io.CONTACTOR,
            "LED": self.io.LED.name
        }
