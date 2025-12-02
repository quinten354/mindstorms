from time import sleep as wait
import hub

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

class Print_hub_matrix:
    def __init__(self, text, spaces_before_start = True, loop = True):
        self.text = text
        self.count = 0
        self.loop = loop
        list_pixels = []
        if spaces_before_start:
            for _ in range(5):
                list_pixels.append([0, 0, 0, 0, 0])

        for char in text:
            if char == 'A':
                list_pixels.append([0, 1, 1, 1, 1])
                list_pixels.append([1, 0, 1, 0, 0])
                list_pixels.append([1, 0, 1, 0, 0])
                list_pixels.append([0, 1, 1, 1, 1])
            if char == 'a':
                list_pixels.append([0, 0, 1, 1, 0])
                list_pixels.append([0, 1, 0, 0, 1])
                list_pixels.append([0, 1, 0, 0, 1])
                list_pixels.append([0, 1, 1, 1, 1])
                list_pixels.append([0, 0, 0, 0, 1])
            if char == 'B':
                list_pixels.append([1, 1, 1, 1, 1])
                list_pixels.append([1, 0, 1, 0, 1])
                list_pixels.append([1, 0, 1, 0, 1])
                list_pixels.append([0, 1, 0, 1, 0])
            if char == 'b':
                list_pixels.append([1, 1, 1, 1, 1])
                list_pixels.append([0, 0, 1, 0, 1])
                list_pixels.append([0, 0, 1, 1, 1])
            if char == 'C':
                list_pixels.append([0, 1, 1, 1, 0])
                list_pixels.append([1, 0, 0, 0, 1])
                list_pixels.append([1, 0, 0, 0, 1])
                list_pixels.append([1, 0, 0, 0, 1])
            if char == 'c':
                list_pixels.append([0, 0, 1, 1, 0])
                list_pixels.append([0, 1, 0, 0, 1])
                list_pixels.append([0, 1, 0, 0, 1])
            if char == 'D':
                list_pixels.append([1, 1, 1, 1, 1])
                list_pixels.append([1, 0, 0, 0, 1])
                list_pixels.append([1, 0, 0, 0, 1])
                list_pixels.append([0, 1, 1, 1, 0])
            if char == 'd':
                list_pixels.append([0, 0, 1, 1, 1])
                list_pixels.append([0, 0, 1, 0, 1])
                list_pixels.append([1, 1, 1, 1, 1])
            if char == 'E':
                list_pixels.append([1, 1, 1, 1, 1])
                list_pixels.append([1, 0, 1, 0, 1])
                list_pixels.append([1, 0, 1, 0, 1])
            if char == 'e':
                list_pixels.append([0, 1, 1, 1, 0])
                list_pixels.append([1, 0, 1, 0, 1])
                list_pixels.append([1, 1, 1, 0, 1])
            if char == 'F':
                list_pixels.append([1, 1, 1, 1, 1])
                list_pixels.append([1, 0, 1, 0, 0])
                list_pixels.append([1, 0, 1, 0, 0])
            if char == 'f':
                list_pixels.append([0, 0, 1, 0, 0])
                list_pixels.append([0, 1, 1, 1, 1])
                list_pixels.append([1, 0, 1, 0, 0])
            if char == 'G':
                list_pixels.append([0, 1, 1, 1, 0])
                list_pixels.append([1, 0, 0, 0, 1])
                list_pixels.append([1, 0, 1, 0, 1])
                list_pixels.append([1, 0, 1, 1, 0])
            if char == 'g':
                list_pixels.append([0, 1, 0, 0, 1])
                list_pixels.append([1, 0, 1, 0, 1])
                list_pixels.append([1, 1, 1, 1, 1])
            if char == 'H':
                list_pixels.append([1, 1, 1, 1, 1])
                list_pixels.append([0, 0, 1, 0, 0])
                list_pixels.append([0, 0, 1, 0, 0])
                list_pixels.append([1, 1, 1, 1, 1])
            if char == 'h':
                list_pixels.append([1, 1, 1, 1, 1])
                list_pixels.append([0, 0, 1, 0, 0])
                list_pixels.append([0, 0, 0, 1, 1])
            if char == 'I':
                list_pixels.append([1, 0, 0, 0, 1])
                list_pixels.append([1, 1, 1, 1, 1])
                list_pixels.append([1, 0, 0, 0, 1])
            if char == 'i':
                list_pixels.append([1, 0, 1, 1, 1])
            if char == 'J':
                list_pixels.append([1, 0, 0, 1, 0])
                list_pixels.append([1, 0, 0, 0, 1])
                list_pixels.append([1, 1, 1, 1, 0])
            if char == 'j':
                list_pixels.append([0, 0, 1, 0, 1])
                list_pixels.append([1, 0, 1, 1, 0])
            if char == 'K':
                list_pixels.append([1, 1, 1, 1, 1])
                list_pixels.append([0, 0, 1, 0, 0])
                list_pixels.append([0, 1, 0, 1, 0])
                list_pixels.append([1, 0, 0, 0, 1])
            if char == 'k':
                list_pixels.append([1, 1, 1, 1, 1])
                list_pixels.append([0, 0, 1, 0, 0])
                list_pixels.append([0, 1, 0, 1, 0])
                list_pixels.append([0, 0, 0, 0, 1])
            if char == 'L':
                list_pixels.append([1, 1, 1, 1, 1])
                list_pixels.append([0, 0, 0, 0, 1])
                list_pixels.append([0, 0, 0, 0, 1])
            if char == 'l':
                list_pixels.append([0, 1, 1, 1, 0])
                list_pixels.append([0, 0, 0, 0, 1])
            if char == 'M':
                list_pixels.append([1, 1, 1, 1, 1])
                list_pixels.append([0, 1, 0, 0, 0])
                list_pixels.append([0, 0, 1, 0, 0])
                list_pixels.append([0, 1, 0, 0, 0])
                list_pixels.append([1, 1, 1, 1, 1])
            if char == 'm':
                list_pixels.append([1, 1, 1, 1, 1])
                list_pixels.append([0, 1, 0, 0, 0])
                list_pixels.append([0, 1, 1, 1, 1])
                list_pixels.append([0, 1, 0, 0, 0])
                list_pixels.append([0, 0, 1, 1, 1])
            if char == 'N':
                list_pixels.append([1, 1, 1, 1, 1])
                list_pixels.append([0, 1, 0, 0, 0])
                list_pixels.append([0, 0, 1, 0, 0])
                list_pixels.append([0, 0, 0, 1, 0])
                list_pixels.append([1, 1, 1, 1, 1])
            if char == 'n':
                list_pixels.append([0, 1, 1, 1, 1])
                list_pixels.append([0, 0, 1, 0, 0])
                list_pixels.append([0, 0, 1, 1, 1])
            if char == 'O':
                list_pixels.append([0, 1, 1, 1, 0])
                list_pixels.append([1, 0, 0, 0, 1])
                list_pixels.append([1, 0, 0, 0, 1])
                list_pixels.append([0, 1, 1, 1, 0])
            if char == 'o':
                list_pixels.append([0, 0, 1, 1, 0])
                list_pixels.append([0, 1, 0, 0, 1])
                list_pixels.append([0, 1, 0, 0, 1])
                list_pixels.append([0, 0, 1, 1, 0])
            if char == 'P':
                list_pixels.append([1, 1, 1, 1, 1])
                list_pixels.append([1, 0, 1, 0, 0])
                list_pixels.append([1, 1, 0, 0, 0])
            if char == 'p':
                list_pixels.append([0, 1, 1, 1, 1])
                list_pixels.append([0, 1, 0, 1, 0])
                list_pixels.append([0, 1, 1, 0, 0])
            if char == 'Q':
                list_pixels.append([0, 1, 1, 0, 0])
                list_pixels.append([1, 0, 0, 1, 0])
                list_pixels.append([1, 0, 0, 1, 1])
                list_pixels.append([0, 1, 1, 0, 1])
            if char == 'q':
                list_pixels.append([0, 1, 1, 0, 0])
                list_pixels.append([0, 1, 0, 1, 0])
                list_pixels.append([0, 1, 1, 1, 1])
            if char == 'R':
                list_pixels.append([1, 1, 1, 1, 1])
                list_pixels.append([1, 0, 1, 0, 0])
                list_pixels.append([0, 1, 1, 0, 0])
                list_pixels.append([0, 0, 0, 1, 1])
            if char == 'r':
                list_pixels.append([0, 1, 1, 1, 1])
                list_pixels.append([0, 1, 0, 0, 0])
            if char == 'S':
                list_pixels.append([0, 1, 1, 0, 1])
                list_pixels.append([1, 0, 1, 0, 1])
                list_pixels.append([1, 0, 1, 1, 0])
            if char == 's':
                list_pixels.append([0, 0, 0, 0, 1])
                list_pixels.append([0, 0, 1, 0, 1])
                list_pixels.append([0, 1, 0, 1, 0])
                list_pixels.append([0, 1, 0, 0, 0])
            if char == 'T':
                list_pixels.append([1, 0, 0, 0, 0])
                list_pixels.append([1, 1, 1, 1, 1])
                list_pixels.append([1, 0, 0, 0, 0])
            if char == 't':
                list_pixels.append([0, 0, 1, 0, 0])
                list_pixels.append([0, 1, 1, 1, 1])
                list_pixels.append([0, 0, 1, 0, 1])
            if char == 'U':
                list_pixels.append([1, 1, 1, 1, 0])
                list_pixels.append([0, 0, 0, 0, 1])
                list_pixels.append([0, 0, 0, 0, 1])
                list_pixels.append([1, 1, 1, 1, 0])
            if char == 'u':
                list_pixels.append([0, 1, 1, 1, 1])
                list_pixels.append([0, 0, 0, 0, 1])
                list_pixels.append([0, 1, 1, 1, 1])
            if char == 'V':
                list_pixels.append([1, 1, 1, 0, 0])
                list_pixels.append([0, 0, 0, 1, 0])
                list_pixels.append([0, 0, 0, 0, 1])
                list_pixels.append([0, 0, 0, 1, 0])
                list_pixels.append([1, 1, 1, 0, 0])
            if char == 'v':
                list_pixels.append([0, 1, 1, 0, 0])
                list_pixels.append([0, 0, 0, 1, 1])
                list_pixels.append([0, 1, 1, 0, 0])
            if char == 'W':
                list_pixels.append([1, 1, 1, 0, 0])
                list_pixels.append([0, 0, 0, 1, 1])
                list_pixels.append([0, 0, 1, 0, 0])
                list_pixels.append([0, 0, 0, 1, 1])
                list_pixels.append([1, 1, 1, 0, 0])
            if char == 'w':
                list_pixels.append([0, 1, 1, 0, 0])
                list_pixels.append([0, 0, 0, 1, 1])
                list_pixels.append([0, 0, 1, 0, 0])
                list_pixels.append([0, 0, 0, 1, 1])
                list_pixels.append([0, 1, 1, 0, 0])
            if char == 'X':
                list_pixels.append([1, 1, 0, 1, 1])
                list_pixels.append([0, 0, 1, 0, 0])
                list_pixels.append([0, 0, 1, 0, 0])
                list_pixels.append([1, 1, 0, 1, 1])
            if char == 'x':
                list_pixels.append([0, 1, 0, 0, 1])
                list_pixels.append([0, 0, 1, 1, 0])
                list_pixels.append([0, 0, 1, 1, 0])
                list_pixels.append([0, 1, 0, 0, 1])
            if char == 'Y':
                list_pixels.append([1, 0, 0, 0, 0])
                list_pixels.append([0, 1, 0, 0, 0])
                list_pixels.append([0, 0, 1, 1, 1])
                list_pixels.append([0, 1, 0, 0, 0])
                list_pixels.append([1, 0, 0, 0, 0])
            if char == 'y':
                list_pixels.append([0, 1, 1, 0, 1])
                list_pixels.append([0, 0, 0, 1, 0])
                list_pixels.append([0, 1, 1, 0, 0])
            if char == 'Z':
                list_pixels.append([1, 0, 0, 1, 1])
                list_pixels.append([1, 0, 1, 0, 1])
                list_pixels.append([1, 1, 0, 0, 1])
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
            if char == '_':
                list_pixels.append([0, 0, 0, 0, 1])
                list_pixels.append([0, 0, 0, 0, 1])
                list_pixels.append([0, 0, 0, 0, 1])
            if char == '.':
                list_pixels.append([0, 0, 0, 0, 1])
            if char == ',':
                list_pixels.append([0, 0, 0, 0, 1])
                list_pixels.append([0, 0, 0, 1, 0])
            if char == '-':
                list_pixels.append([0, 0, 1, 0, 0])
                list_pixels.append([0, 0, 1, 0, 0])

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

def image(list_pixels):
    for y in range(5):
        for x in range(5):
            hub.display.pixel(x, y, list_pixels[y][x] * 100)

def clear():
    hub.display.clear()

def get_pixel(x, y):
    return hub.display.pixel(x, y)

def set_pixel(x, y, brightness):
    hub.display.pixel(x, y, brightness * 9)

