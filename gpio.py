
class GPIO:
    def __init__(self):
      self._pilot_ok = 0
      self._fault = 0
      self._btn_raw = 0
      self.contactor = 0
      self.led = 0
def read_pilot_ok(self) -> int: return self._pilot_ok
def read_fault(self) -> int: return self._fault
def read_btn_raw(self) -> int: return self._btn_raw
def write_contactor(self, on: int): self.contactor = 1 if on else 0
def write_led(self, on: int): self.led = 1 if on else 0
# setters para simular entradas:
def set_input(self, name: str, val: int): setattr(self, f"_{name.lower()}", 1 if val else
0)
