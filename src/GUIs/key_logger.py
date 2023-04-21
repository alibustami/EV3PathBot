"""Key logger."""
from pynput import keyboard


def keylogger():
    """Key logger."""
    events = []

    def on_press(key):
        try:
            events.append(key.char)
            if key.char == "q":
                return False
        except AttributeError:
            events.append(format(key))

    with keyboard.Listener(on_press=on_press) as _:
        while True:
            try:
                event = events.pop(0)
                yield event
                if "q" in event:
                    break
            except IndexError:
                pass
            except KeyboardInterrupt:
                break
