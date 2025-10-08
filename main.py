import asyncio
from app.gpio import GPIO
from app.led import LedController, LedPattern
from app.state_machine import StateMachine

def print_help():
    print("Comandos disponibles:")
    print("  GET STATE                  # Estado actual")
    print("  GET IO                     # Estado de PILOT_OK, FAULT, BTN, CONTACTOR, LED")
    print("  SET LED <OFF|SLOW|FAST|FAULT>   # Forzar patrón LED")
    print("  SET IN <PILOT_OK|FAULT|BTN> <0|1>   # Simular entradas")
    print("  HELP")
    print("  EXIT")

async def cli(sm, gpio, led):
    print_help()
    loop = asyncio.get_event_loop()
    while True:
        line = await loop.run_in_executor(None, input, "> ")
        cmd = line.strip().split()
        if not cmd:
            continue
        if cmd[0].upper() == "HELP":
            print_help()
        elif cmd[0].upper() == "EXIT":
            break
        elif cmd[0].upper() == "GET" and len(cmd) > 1 and cmd[1].upper() == "STATE":
            print(f"STATE: {sm.state.name}")
        elif cmd[0].upper() == "GET" and len(cmd) > 1 and cmd[1].upper() == "IO":
            io = {
                "PILOT_OK": gpio.read_pilot_ok(),
                "FAULT": gpio.read_fault(),
                "BTN": gpio.read_btn_raw(),
                "CONTACTOR": gpio.contactor,
                "LED": led.pattern.name
            }
            print("IO:", io)
        elif cmd[0].upper() == "SET" and len(cmd) > 2 and cmd[1].upper() == "LED":
            try:
                led.force = LedPattern[cmd[2].upper()]
                print(f"LED patrón forzado a {cmd[2].upper()}")
            except Exception:
                print("Patrón LED no válido.")
        elif cmd[0].upper() == "SET" and len(cmd) > 3 and cmd[1].upper() == "IN":
            name = cmd[2].upper()
            val = int(cmd[3])
            if name in ("PILOT_OK", "FAULT", "BTN"):
                gpio.set_input(name, val)
                print(f"Entrada {name} = {val}")
            else:
                print("Entrada no válida.")
        else:
            print("Comando no reconocido. Escribe HELP.")

async def mainloop(sm, gpio, led):
    # Tick del sistema cada 10 ms
    while True:
        sm.tick()
        led_state = led.update()
        gpio.write_led(led_state)
        await asyncio.sleep(0.01)

async def main():
    gpio = GPIO()
    led = LedController()
    sm = StateMachine(gpio, led)
    await asyncio.gather(
        mainloop(sm, gpio, led),
        cli(sm, gpio, led)
    )

if __name__ == "__main__":
    asyncio.run(main())
