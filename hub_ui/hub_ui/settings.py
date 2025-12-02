from device.display import image
from device.button import center

stop = center.was_pressed

def main():
    selection = 0
    while True:
        image([[0, 0, 1, 0, 0], [1, 0, 1, 0, 1], [1, 0, 1, 0, 1], [1, 0, 0, 0, 1], [0, 1, 1, 1, 0]])
        if stop():
            return

        yield

