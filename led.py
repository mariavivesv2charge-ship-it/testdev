import time
from enum import Enum

class LedPattern(Enum):
    OFF = 0
    SLOW = 1    # 1 Hz lento
    FAST = 2    # 4 Hz rápido
    FAULT = 3   # doble destello/s

class LedController:
    def __init__(self, clock=lambda: int(time.time() * 1000)):
        self.pattern = LedPattern.OFF
        self.clock = clock
        self._last_toggle = self.clock()
        self._led_on = False
        self._fault_phase = 0

    def set_pattern(self, pattern):
        self.pattern = pattern
        self._reset()

    def _reset(self):
        self._last_toggle = self.clock()
        self._led_on = False
        self._fault_phase = 0

    def update(self):
        """
       Lllamada cada < 18 
        True encendido ,Fañse mapagado.
        """
        now = self.clock()
        if self.pattern == LedPattern.OFF:
            return False
        elif self.pattern == LedPattern.SLOW:
            # 1Hz: alterna cada 500ms
            if now - self._last_toggle >= 500:
                self._led_on = not self._led_on
                self._last_toggle = now
            return self._led_on
        elif self.pattern == LedPattern.FAST:
            # 4Hz: alterna cada 125ss
            if now - self._last_toggle >= 125:
                self._led_on = not self._led_on
                self._last_toggle = now
            return self._led_on
        elif self.pattern == LedPattern.FAULT:
            # Doble destello por segundo: ONx2  off x2 cada 250ms
            if now - self._last_toggle >= 250:
                self._fault_phase = (self._fault_phase + 1) % 4
                self._last_toggle = now
            return self._fault_phase in (0,1)
        else:
            return False
