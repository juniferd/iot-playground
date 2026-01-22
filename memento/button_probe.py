import time
import board
import digitalio
import microcontroller

# Probe for pins that toggle when you press board buttons.
def is_candidate(name, pin):
    if not name.isupper():
        return False
    if "CAMERA" in name or name in {"SCL", "SDA"}:
        return False
    return isinstance(pin, microcontroller.Pin)


pins = []
for name in dir(board):
    pin = getattr(board, name)
    if is_candidate(name, pin):
        pins.append((name, pin))

inputs = {}
for name, pin in pins:
    try:
        dio = digitalio.DigitalInOut(pin)
        dio.direction = digitalio.Direction.INPUT
        dio.pull = digitalio.Pull.UP
        inputs[name] = dio
    except Exception:
        pass

print("Watching pins:", list(inputs.keys()))

last = {k: v.value for k, v in inputs.items()}

def run():
    while True:
        for name, dio in inputs.items():
            now = dio.value
            if now != last[name]:
                print(name, "->", now)
                last[name] = now
        time.sleep(0.05)
