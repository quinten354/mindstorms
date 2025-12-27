_print = print

class Io:
    def __init__(self, events):
        self.events = events

    def print(self, *args, sep = ' ', end = '\\n'):
        data = ''
        for arg in args:
            data = data + arg + sep

        data = data[:-len(sep)]

        data = data + end

        _print({'type': 'output', 'value': data})

    def input(self):
        data = self.events['program_input']
        try:
            index = data.index('\\n')
        except:
            return
        
        inp_data = data[:index]
        self.events['program_input'] = data[index + 1:]
        return inp_data

    def getch(self):
        data = self.events['program_input']
        if len(data) > 0:
            ch = data[0]
            self.events['program_input'] = data[1:]
            return ch

    def getall(self):
        data = self.events['program_input']
        self.events['program_input'] = ''
        return data

    def input_avail(self):
        return len(self.events['program_input']) > 0

