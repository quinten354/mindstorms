import hub
from .lib import image

def main():
    selection = 0
    while True:
        image([[0, 0, 1, 0, 0], [1, 0, 1, 0, 1], [1, 0, 1, 0, 1], [1, 0, 0, 0, 1], [0, 1, 1, 1, 0]])
        if hub.button.center.was_pressed():
            return

        yield

