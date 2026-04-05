from device import runtime_data

_print = print

def print(*args, sep = ' ', end = '\n'):
    data = ''
    for arg in args:
        data = data + str(arg) + str(sep)

    data = data[:-len(sep)]

    data = data + str(end)

    _print({'type': 'output', 'value': data})

def input():
    data = runtime_data['program_input']
    try:
        index = data.index('\n')
    except:
        return
    
    inp_data = data[:index]
    runtime_data['program_input'] = data[index + 1:]
    return inp_data

def getch():
    data = runtime_data['program_input']
    if len(data) > 0:
        ch = data[0]
        runtime_data['program_input'] = data[1:]
        return ch

def getall():
    data = runtime_data['program_input']
    runtime_data['program_input'] = ''
    return data

def input_avail():
    return len(runtime_data['program_input']) > 0

