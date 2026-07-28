import hub
import os

def get_volume():
    return hub.sound.volume()

def set_volume(volume):
    hub.sound.volume(volume)

def beep(freq = 1000, time = 0.2):
    hub.sound.beep(freq, round(time * 1000))

def play(name):
    played = False
    if 'extra_files' in os.listdir('/'):
        if name in os.listdir('/extra_files/'):
            hub.sound.play('/extra_files/' + name)
            played = True

    if 'sounds' in os.listdir('/'):
        if name in os.listdir('/sounds/'):
            hub.sound.play('/sounds/' + name)
            played = True

    if not played:
        raise ValueError('Sound not found.')

def play_file(path):
    hub.sound.play(path)

