_print = print

class io:
    def __init__(self, location):
        self.location = location

    def print(self, *args, sep = ' '):
        data = ''
        for arg in args:
            data = data + arg + sep

        data = data[:-1]

        _print({'type': 'output', 'value': data})

    def get_input(self):
        if len(location) > 0:
            return location[0]
            del location[0]
        else:
            return None

    def input_avail(self):
        return len(location) > 0

def print(*args, sep = ' '):
    data = ''
    for arg in args:
        data = data + str(arg) + str(sep)

    data = data[:-1]

    _print({'type': 'output', 'value': data})

def get_input(location):
    if len(location) > 0:
        return location[0]
        del location[0]
    else:
        return None

def input_avail(location):
    return len(location) > 0

