import os
from micropython import const

_ISDIR = const(0x4000)

def isdir(path):
    mode = os.stat(path)[0]
    return bool(mode & _ISDIR)

def exists(path):
    try:
        os.stat(path)
    except:
        return False
    return True

def basename(path):
    split = path.split('/')
    if split[-1] == '':
        return split[-2]
    else:
        return split[-1]

def dirname(path):
    items = path.split('/')
    if len(items[-1]) == 0:
        del items[-1]
    del items[-1]
    return '/'.join(items)

def split(path):
    return dirname(path), basename(path)

def get_size(path):
    return os.stat(path)[6]

def getctime(path):
    return os.stat(path)[7]

def getmtime(path):
    return os.stat(path)[8]

def getatime(path):
    return os.stat(path)[9]

def move(path, to):
    if to[-1] == '/':
        os.rename(path, to + basename(path))
    else:
        os.rename(path, to)

def copyfile(path, to):
    file = open(path, mode = 'br')
    data = file.read()
    file.close()
    if to[-1] == '/':
        file = open(to + basename(path), mode = 'bw')
        file.write(data)
        file.close()
    else:
        file = open(to, mode = 'bw')
        file.write(data)
        file.close()

def walk(path):
    main_list = []
    listdir = os.listdir(path)
    dirs = []
    files = []
    for item in listdir:
        if isdir(path + '/' + item):
            dirs.append(item)
        else:
            files.append(item)

    main_list.append((path, dirs, files))
    for dir in dirs:
        main_list = main_list + walk(path + '/' + dir)

    return main_list

def removetree(dir):
    paths = walk(dir)
    paths.reverse()
    for path in paths:
        for dir in path[1]:
            os.rmdir(path[0] + '/' + dir)
        for file in path[2]:
            os.remove(path[0] + '/' + file)
    os.rmdir(dir)

def copytree(dir, to):
    if to[-1] == '/':
        to = to + basename(dir)
        os.mkdir(to)
    paths = walk(dir)
    for path in paths:
        for dir in path[1]:
            os.mkdir(path[0].replace(dir, to) + '/' + path[1])
        for file in path[2]:
            copyfile(path[0] + '/' + path[2], path[0].replace(dir, to) + '/' + path[2])

