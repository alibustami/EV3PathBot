"""Mouse logger."""
from pynput import mouse


def mouselogger():
    """Mouse logger."""
    events = []

    def on_click(x, y, button, pressed):
        if pressed:
            events.append([x, y, button, pressed])

    with mouse.Listener(on_click=on_click) as _:
        while True:
            try:
                event = events.pop(0)
                yield event
            except IndexError:
                pass
            except KeyboardInterrupt:
                break
