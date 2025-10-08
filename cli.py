import sys
import asyncio
from app.state_machine import StateMachine, IO, LedPattern

io = IO()
sm = StateMachine(io)

def print_help():
    print("GET STATE")
    print("GET IO")
    print("SET LED <OFF|SLOW|FAST|FAULT>")
    print("SET IN <PILOT_OK|FAULT|BTN> <0|1>")
    print("HELP")

async def main():
    print_help()
    while True:
        # Ejecutar tick cada 10ms
        sm.tick()
        await asyncio.sleep(0.01)
        # Procesar input usuario si hay
        if sys.stdin in asyncio.select([sys.stdin], [], [], 0)[0]:
            line = sys.stdin.readline().strip()
            if line.upper() == "GET STATE":
                print(sm.get_state())
            elif line.upper() == "GET IO":
                print(sm.get_io())
            elif line.upper().startswith("SET LED"):
                _, _, led = line.split()
                sm.force_led(LedPattern[led.upper()])
            elif line.upper().startswith("SET IN"):
                _, _, inp, val = line.split()
                setattr(io, inp, int(val))
            elif line.upper() == "HELP":
                print_help()
            else:
                print("Comando desconocido.")

if __name__ == "__main__":
    asyncio.run(main())
