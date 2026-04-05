import hub
import machine
from time import sleep as wait

import device

def main():
    options = [
            [[[0, 0, 1, 0, 0], [1, 0, 1, 0, 1], [1, 0, 1, 0, 1], [1, 0, 0, 0, 1], [0, 1, 1, 1, 0]], shutdown],
            [[[0, 0, 1, 0, 0], [0, 1, 1, 1, 0], [0, 0, 1, 0, 1], [1, 0, 0, 0, 1], [0, 1, 1, 1, 0]], restart],
            [[[0, 0, 1, 0, 0], [1, 0, 0, 0, 1], [0.8, 0, 1, 0, 0.8], [1, 0, 0, 0, 1], [0, 0, 0, 0, 0]], remote],
            [[[1, 1, 1, 1, 0], [1, 0, 0, 1, 1], [1, 0, 0, 0, 1], [1, 0, 0, 1, 1], [1, 1, 1, 1, 0]], battery],
            [[[0, 0, 1, 0, 0], [0, 1, 0, 0, 0], [1, 1, 1, 1, 1], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0]], exit]
    ]
    selection = 0
    changed = True
    mode = None
    while True:
        if mode:
            try:
                next(mode)
            except StopIteration:
                mode = None
                device.button.center.was_pressed()
            except Exception as error:
                device.system.print_error(error)
                mode = None
                device.button.center.was_pressed()
        else:
            if device.button.center.was_pressed():
                mode = options[selection][1]()
                changed = True
                continue
            if device.button.left.was_pressed():
                selection = selection - 1
                changed = True
            if device.button.right.was_pressed():
                selection = selection + 1
                changed = True
            if selection < 0:
                selection = len(options) - 1
            if selection >= len(options):
                selection = 0
            if changed:
                device.display.image(options[selection][0])
        yield

def shutdown():
    hub.power_off(fast = True)

def restart():
    machine.reset()

def remote():
    device.remote.connect(device.button.center.was_pressed)
    color = 0
    color_ch = False
    while True:
        pressed = device.remote.get_pressed()
        if pressed:
            device.display.image([[0, 0, 0, 0, 0], [1 if 'LEFT_PLUS' in pressed else 0, 0, 0, 0, 1 if 'RIGHT_PLUS' in pressed else 0], [1 if 'LEFT' in pressed else 0, 0, 1 if 'CENTER' in pressed else 0, 0, 1 if 'RIGHT' in pressed else 0], [1 if 'LEFT_MINUS' in pressed else 0, 0, 0, 0, 1 if 'RIGHT_MINUS' in pressed else 0], [0, 0, 0, 0, 0]])
        else:
            device.display.image([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])
        if device.button.left.was_pressed():
            color = color - 1
            color_ch = True
        if device.button.right.was_pressed():
            color = color + 1
            color_ch = True
        if color < 0:
            color = 10
        if color > 10:
            color = 0
        if color_ch:
            device.remote.set_color(color)
            color_ch = False
        if device.button.center.was_pressed():
            device.remote.disconnect()
            break
        yield

def battery():
    while True:
        percent = device.battery.get_current()
        if percent < 10:
            device.display.image([[1, 1, 1, 1, 0], [1, 0, 0, 1, 1], [1, 0, 0, 0, 1], [1, 0, 0, 1, 1], [1, 1, 1, 1, 0]])
        elif percent < 20:
            device.display.image([[1, 1, 1, 1, 0], [1, 0.8, 0, 1, 1], [1, 0.8, 0, 0, 1], [1, 0.8, 0, 1, 1], [1, 1, 1, 1, 0]])
        elif percent < 40:
            device.display.image([[1, 1, 1, 1, 0], [1, 1, 0, 1, 1], [1, 1, 0, 0, 1], [1, 1, 0, 1, 1], [1, 1, 1, 1, 0]])
        elif percent < 60:
            device.display.image([[1, 1, 1, 1, 0], [1, 1, 0.8, 1, 1], [1, 1, 0.8, 0, 1], [1, 1, 0.8, 1, 1], [1, 1, 1, 1, 0]])
        elif percent < 80:
            device.display.image([[1, 1, 1, 1, 0], [1, 1, 1, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 0]])
        elif percent < 100:
            device.display.image([[1, 1, 1, 1, 0], [1, 1, 1, 1, 1], [1, 1, 1, 0.8, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 0]])
        else:
            device.display.image([[1, 1, 1, 1, 0], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 0]])

        if device.button.center.was_pressed():
            break

        yield
        wait(0.5)
        yield

        charging = device.battery.get_charging()
        if charging:
            device.display.image([[0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [1, 1, 1, 1, 1], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0]])
        else:
            device.display.image([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [1, 1, 1, 1, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])

        if device.button.center.was_pressed():
            break

        yield
        wait(0.5)
        yield

