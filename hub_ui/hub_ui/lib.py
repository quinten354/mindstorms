from time import sleep as wait
import hub

from .constants import *

class EndOfLoopError:
    def __init__(self, message = ''):
        super().__init__(message)
        self.message = message

class Picture:
    def __init__(self, list_pixels):
        self.list_pixels = list_pixels
        self.count = 0

    def show_next(self):
        for y in range(5):
            for x in range(5):
                hub.display.pixel(x, y, self.list_pixels[self.count][y][x] * 100)
        self.count = self.count + 1
        if self.count >= len(self.list_pixels):
            self.count = 0

def image(list_pixels):
    for y in range(5):
        for x in range(5):
            hub.display.pixel(x, y, list_pixels[y][x] * 100)

class Print_hub_matrix:
    def __init__(self, text, spaces_before_start = True, loop = False):
        self.text = text
        self.count = 0
        self.loop = loop
        text.lower()
        list_pixels = []
        if spaces_before_start:
            for _ in range(5):
                list_pixels.append([0, 0, 0, 0, 0])

        for char in text:
            if char == 'a':
                list_pixels.append([1, 0, 1, 1, 1])
                list_pixels.append([1, 0, 1, 0, 1])
                list_pixels.append([1, 1, 1, 1, 1])
            if char == 'b':
                list_pixels.append([1, 1, 1, 1, 1])
                list_pixels.append([0, 0, 1, 0, 1])
                list_pixels.append([0, 0, 1, 1, 1])
            if char == 'c':
                list_pixels.append([0, 1, 1, 1, 1])
                list_pixels.append([0, 1, 0, 0, 1])
                list_pixels.append([0, 1, 0, 0, 1])
            if char == 'd':
                list_pixels.append([0, 0, 1, 1, 1])
                list_pixels.append([0, 0, 1, 0, 1])
                list_pixels.append([1, 1, 1, 1, 1])
            if char == 'e':
                list_pixels.append([1, 1, 1, 1, 1])
                list_pixels.append([1, 0, 1, 0, 1])
                list_pixels.append([1, 1, 1, 0, 1])
            if char == 'f':
                list_pixels.append([0, 0, 1, 0, 0])
                list_pixels.append([1, 1, 1, 1, 1])
                list_pixels.append([1, 0, 1, 0, 0])
            if char == 'g':
                list_pixels.append([1, 1, 1, 1, 1])
                list_pixels.append([1, 0, 0, 0, 1])
                list_pixels.append([1, 0, 1, 0, 1])
                list_pixels.append([1, 0, 1, 1, 1])
            if char == 'h':
                list_pixels.append([1, 1, 1, 1, 1])
                list_pixels.append([0, 0, 1, 0, 0])
                list_pixels.append([0, 0, 1, 1, 1])
            if char == 'i':
                list_pixels.append([1, 0, 1, 1, 1])
            if char == 'j':
                list_pixels.append([0, 0, 1, 0, 1])
                list_pixels.append([1, 0, 1, 1, 1])
            if char == 'k':
                list_pixels.append([1, 1, 1, 1, 1])
                list_pixels.append([0, 0, 1, 0, 0])
                list_pixels.append([0, 1, 0, 1, 0])
                list_pixels.append([1, 0, 0, 0, 1])
            if char == 'l':
                list_pixels.append([1, 1, 1, 1, 1])
                list_pixels.append([0, 0, 0, 0, 1])
            if char == 'm':
                list_pixels.append([1, 1, 1, 1, 1])
                list_pixels.append([0, 1, 0, 0, 0])
                list_pixels.append([0, 1, 1, 1, 1])
                list_pixels.append([0, 1, 0, 0, 0])
                list_pixels.append([0, 1, 1, 1, 1])
            if char == 'n':
                list_pixels.append([1, 1, 1, 1, 1])
                list_pixels.append([0, 1, 0, 0, 0])
                list_pixels.append([0, 1, 1, 1, 1])
            if char == 'o':
                list_pixels.append([0, 0, 1, 1, 0])
                list_pixels.append([0, 1, 0, 0, 1])
                list_pixels.append([0, 1, 0, 0, 1])
                list_pixels.append([0, 0, 1, 1, 0])
            if char == 'p':
                list_pixels.append([1, 1, 1, 1, 1])
                list_pixels.append([1, 0, 1, 0, 0])
                list_pixels.append([1, 1, 1, 0, 0])
            if char == 'q':
                list_pixels.append([1, 1, 1, 0, 0])
                list_pixels.append([1, 0, 1, 0, 0])
                list_pixels.append([1, 1, 1, 1, 1])
            if char == 'r':
                list_pixels.append([0, 1, 1, 1, 1])
                list_pixels.append([0, 1, 0, 0, 0])
            if char == 's':
                list_pixels.append([0, 1, 1, 0, 1])
                list_pixels.append([1, 0, 1, 0, 1])
                list_pixels.append([1, 0, 1, 1, 0])
            if char == 't':
                list_pixels.append([0, 0, 1, 0, 0])
                list_pixels.append([0, 1, 1, 1, 1])
                list_pixels.append([0, 0, 1, 0, 1])
            if char == 'u':
                list_pixels.append([0, 1, 1, 1, 1])
                list_pixels.append([0, 0, 0, 0, 1])
                list_pixels.append([0, 1, 1, 1, 1])
            if char == 'v':
                list_pixels.append([0, 1, 1, 0, 0])
                list_pixels.append([0, 0, 0, 1, 1])
                list_pixels.append([0, 1, 1, 0, 0])
            if char == 'w':
                list_pixels.append([0, 1, 1, 0, 0])
                list_pixels.append([0, 0, 0, 1, 1])
                list_pixels.append([0, 1, 1, 0, 0])
                list_pixels.append([0, 0, 0, 1, 1])
                list_pixels.append([0, 1, 1, 0, 0])
            if char == 'x':
                list_pixels.append([0, 1, 0, 0, 1])
                list_pixels.append([0, 0, 1, 1, 0])
                list_pixels.append([0, 0, 1, 1, 0])
                list_pixels.append([0, 1, 0, 0, 1])
            if char == 'y':
                list_pixels.append([0, 1, 1, 0, 1])
                list_pixels.append([0, 0, 0, 1, 1])
                list_pixels.append([0, 1, 1, 0, 0])
            if char == 'z':
                list_pixels.append([0, 1, 0, 1, 1])
                list_pixels.append([0, 1, 1, 1, 1])
                list_pixels.append([0, 1, 1, 0, 1])
            if char == '0':
                list_pixels.append([1, 1, 1, 1, 1])
                list_pixels.append([1, 0, 0, 0, 1])
                list_pixels.append([1, 1, 1, 1, 1])
            if char == '1':
                list_pixels.append([0, 1, 0, 0, 1])
                list_pixels.append([1, 1, 1, 1, 1])
                list_pixels.append([0, 0, 0, 0, 1])
            if char == '2':
                list_pixels.append([1, 0, 0, 1, 1])
                list_pixels.append([1, 0, 1, 0, 1])
                list_pixels.append([1, 1, 0, 0, 1])
            if char == '3':
                list_pixels.append([1, 0, 1, 0, 1])
                list_pixels.append([1, 0, 1, 0, 1])
                list_pixels.append([1, 1, 1, 1, 1])
            if char == '4':
                list_pixels.append([0, 0, 1, 1, 0])
                list_pixels.append([1, 1, 0, 1, 0])
                list_pixels.append([1, 1, 1, 1, 1])
                list_pixels.append([0, 0, 0, 1, 0])
            if char == '5':
                list_pixels.append([1, 1, 1, 0, 1])
                list_pixels.append([1, 0, 1, 0, 1])
                list_pixels.append([1, 0, 0, 1, 0])
            if char == '6':
                list_pixels.append([1, 1, 1, 1, 1])
                list_pixels.append([1, 0, 1, 0, 1])
                list_pixels.append([1, 0, 1, 1, 1])
            if char == '7':
                list_pixels.append([1, 0, 0, 1, 1])
                list_pixels.append([1, 0, 1, 0, 0])
                list_pixels.append([1, 1, 0, 0, 0])
            if char == '8':
                list_pixels.append([1, 1, 1, 1, 1])
                list_pixels.append([1, 0, 1, 0, 1])
                list_pixels.append([1, 1, 1, 1, 1])
            if char == '9':
                list_pixels.append([1, 1, 1, 0, 1])
                list_pixels.append([1, 0, 1, 0, 1])
                list_pixels.append([1, 1, 1, 1, 1])
            if char == ' ':
                list_pixels.append([0, 0, 0, 0, 0])
                list_pixels.append([0, 0, 0, 0, 0])
                list_pixels.append([0, 0, 0, 0, 0])

            list_pixels.append([0, 0, 0, 0, 0])

        for _ in range(5):
            list_pixels.append([0, 0, 0, 0, 0])

        self.list_pixels = list_pixels

    def show_next(self):
        list_current_pixels = self.list_pixels[self.count:self.count + 5]
        for number_x in range(5):
            for number_y in range(5):
                try:
                    hub.display.pixel(number_x, number_y, list_current_pixels[number_x][number_y] * 100)
                except IndexError:
                    if self.loop:
                        self.count = 0
                        return self.show_next()
                    else:
                        raise EndOfLoopError('Youre at the end of the text.')

        self.count = self.count + 1
        return self.count

    def start(self, interval):
        try:
            while True:
                self.show_next()
                wait(interval)
        except:
            return ''

def show_error():
    hub.led(colors.RED)
    wait(0.2)
    hub.led(colors.WHITE)

def sync_programs():
    listdir = os.listdir('/programs')
    programs = []
    for item in listdir:
        programs.append({'name': item.split('.py')[0], 'nickname': item.split('.py')[0]})

    file = open('/.program_info')
    try:
        data = eval(file.read()
    except:
        data = []

    file.close()

    for item in data:
        exist = False
        for program in programs:
            if item['name'] == program['name']:
                exist = True

        if not exist:
            data.remove(item)

    for program in programs:
        exist = False
        for item in data:
            if item['name'] == program['name']:
                exist = True

        if not exist:
            data.append(program)

    file = open('/.program_info', mode = 'w')
    file.write(str(data))
    file.close()

