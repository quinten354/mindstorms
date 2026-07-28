import os
import sys
import hub
from device import path
from device import system

def chsize(bytes):
    pow = 0
    while bytes >= 1024:
        bytes = bytes / 1024
        pow = pow + 1

    bytes = str(bytes)
    bytes = bytes[:4]
    if bytes[-1] == '.':
        bytes = bytes[:-1]
    size = bytes + ['', 'K', 'M', 'G', 'T'][pow]
    return size

def input():
    inp = ''
    while True:
        ch = sys.stdin.read(1)
        if ch == '\n':
            print()
            return inp

        elif ch == '\x03':
            raise KeyboardInterrupt

        elif ch == '\x7f' or ch == '\x08':
            if len(inp) > 0:
                inp = inp[:-1]
                print('\x1b[D \x1b[D', end = '')

        elif ch == '\x04' and inp == '':
            print()
            return '\x04'

        elif ch == '\x1b':
            continue

        elif ch == '\t':
            print('\\t', end = '')
            inp = inp + '\\t'

        elif ch == '\r':
            print('\\r', end = '')
            inp = inp + '\\r'

        else:
            print(ch, end = '')
            inp = inp + ch

def chtext(string):
    string = string.replace('\\\'', '\'').replace('\\\\', '\\').replace('\\ ', ' ').replace('\\t', '\t').replace('\\r', '\r').replace('\\n', '\n')
    while '\\x' in string:
        place = string.index('\\x')
        char_org = string[place + 2:place + 4]
        char_new = eval('\\x' + char)
        string.replace('\\x' + char_org, char_new)

    return string

def main():
    print()
    print('Welcome by the command shell.')
    print('Type \'help\' to view the help menu.')
    print()
    while True:
        try:
            print(os.getcwd() + '$ ', end = '')
            try:
                inp = input()
            except KeyboardInterrupt:       
                print()
                continue

            inp_old = inp
            inp = []

            quote = False
            text = ''
            backslash = False
            wait = 0
            for number in range(len(inp_old)):
                if wait:
                    wait = wait - 1
                    continue
                ch = inp_old[number]
                if backslash:
                    if ch == 't':
                        text = text + '\t'
                    elif ch == 'r':
                        text = text + '\r'
                    elif ch == 'n':
                        text = text + '\n'
                    elif ch == 'x':
                        char_hex = inp_old[number + 1] + inp_old[number + 2]
                        char_new = eval('\\x' + char_hex)
                        text = text + char_new
                        wait = 2
                    else:
                        text = text + ch
                    backslash = False
                elif ch == '\'':
                    if quote:
                        inp.append(text)
                        text = ''
                        quote = False
                    else:
                        quote = True
                elif ch == '\\':
                    backslash = True
                elif quote:
                    text = text + ch
                elif ch == ' ':
                    inp.append(text)
                    text = ''
                else:
                    text = text + ch

            inp.append(text)

            while '' in inp:
                inp.remove('')

            if len(inp) == 0:
                continue

            if inp[0] == '':
                continue

            elif inp[0] == 'help':
                if len(inp) == 1:
                    help_menu()
                else:
                    help_cmd(inp[1])

            elif inp[0] == 'exit':
                return

            elif inp[0] == '\x04':
                return

            elif inp[0] == 'ls' or inp[0] == 'dir':
                sort = True
                if '-s' in inp:
                    sort = False
                if len(inp) == 1 or (len(inp) == 2 and not sort):
                    listdir = os.listdir()
                    dir = os.getcwd() + '/'
                else:
                    listdir = os.listdir(inp[-1])
                    dir = inp[-1] + '/'

                if sort:
                    listdir.sort()

                for item in listdir:
                    if path.isdir(dir + item):
                        print(item + '/')
                    else:
                        print(item)

            elif inp[0] == 'stat':
                print('Type: ' + ('directory' if path.isdir(inp[1]) else 'file'))
                print('Size: ' + str(path.get_size(inp[1])))

            elif inp[0] == 'pwd':
                print(os.getcwd())

            elif inp[0] == 'cd':
                os.chdir(inp[1])

            elif inp[0] == 'touch':
                for file in inp[1:]:
                    open(file, mode = 'x').close()

            elif inp[0] == 'rm':
                for file in inp[1:]:
                    os.remove(inp[1])

            elif inp[0] == 'mkdir':
                for file in inp[1:]:
                    os.mkdir(inp[1])

            elif inp[0] == 'rmdir':
                for file in inp[1:]:
                    os.rmdir(inp[1])

            elif inp[0] == 'rmtree':
                path.removetree(inp[1])

            elif inp[0] == 'cat':
                numbers = False
                lines = None
                if '-n' in inp or '--numbers' in inp:
                    numbers = True
                
                if inp[-2][:3] == '-l=' or inp[-2][:8] == '--lines=':
                    lines = inp[-2].split('=')[1].split('-')

                file = open(inp[-1])
                data = file.read()
                file.close()
                data = data.split('\n')

                if lines:
                    for line in range(int(lines[0]) - 1, int(lines[1])):
                        if numbers:
                            print(line + 1, end = '')
                            print(': ', end = '')
                            print(' ' * (6 - len(str(line + 1))), end = '')
                        print(data[line])

                else:
                    for line in range(len(data)):
                        if numbers:
                            print(line + 1, end = '')
                            print(': ', end = '')
                            print(' ' * (6 - len(str(line + 1))), end = '')
                        print(data[line])

            elif inp[0] == 'cp':
                files = inp[1:][:-1]
                to = inp[-1]
                if to[-1] == '/':
                    for file in files:
                        path.copyfile(file, to)
                else:
                    path.copyfile(inp[1], to)

            elif inp[0] == 'cptree':
                path.copytree(inp[1], inp[2])

            elif inp[0] == 'mv':
                files = inp[1:][:-1]
                to = inp[-1]
                if to[-1] == '/':
                    for file in files:
                        path.move(file, to)
                else:
                    path.move(inp[1], to)

            elif inp[0] == 'statfs':
                statfs = os.statvfs('/')
                blocksize = statfs[1]
                max_filename_length = statfs[9]

                blocks_total = statfs[2]
                blocks_free = statfs[3]
                blocks_used = blocks_total - blocks_free

                total_bytes = blocksize * blocks_total
                used_bytes = blocksize * blocks_used
                free_bytes = blocksize * blocks_free

                total_size = chsize(total_bytes)
                total_used = chsize(used_bytes)
                total_free = chsize(free_bytes)

                print('Blocksize: ' + str(blocksize))
                print('Max filename size: ' + str(max_filename_length))
                print()

                print('Total blocks: ' + str(blocks_total))
                print('Used blocks:  ' + str(blocks_used))
                print('Free blocks:  ' + str(blocks_free))
                print()

                print('Total bytes: ' + str(total_bytes))
                print('Used bytes:  ' + str(used_bytes))
                print('Free bytes:  ' + str(free_bytes))
                print()

                print('Total size: ' + str(total_size))
                print('Used size:  ' + str(total_used))
                print('Free size:  ' + str(total_free))

            elif inp[0] == 'delline':
                filename = inp[1]
                lines = inp[2:]
                lines.sort()
                lines.reverse()

                file = open(filename)
                data = file.read()
                file.close()

                data = data.split('\n')

                for line in lines:
                    del data[line]

                file = open(filename, mode = 'w')
                file.write('\n'.join(data))
                file.close()

            elif inp[0] == 'insline':
                filename = inp[1]
                line = inp[2]
                text = inp[3]

                file = open(filename)
                data = file.read()
                file.close()

                data = data.split('\n')

                data.insert(int(line), text)

                file = open(filename, mode = 'w')
                file.write('\n'.join(data))
                file.close()

            elif inp[0] == 'addline':
                filename = inp[1]
                text = inp[2]

                file = open(filename, mode = 'a')
                file.write(text + '\n')
                file.close()

            elif inp[0] == 'chline':
                filename = inp[1]
                line = inp[2]
                text = inp[3]

                file = open(filename)
                data = file.read()
                file.close()

                data = data.split('\n')

                data[int(line)] = text

                file = open(filename, mode = 'w')
                file.write('\n'.join(data))
                file.close()

            elif inp[0] == 'clearfile':
                file = open(inp[1], mode = 'w')
                file.write('')
                file.close()

            elif inp[0] == 'adddata':
                data = ''
                while True:
                    try:
                        data = data + sys.stdin.read(1)
                    except KeyboardInterrupt:
                        break

                print('Saving...')

                file = open(inp[1], mode = 'a')
                file.write(data)
                file.close()

            elif inp[0] == 'clear':
                print('\x1b[H\x1b[2J\x1b[3J', end = '')

            elif inp[0] == 'python':
                if len(inp) == 2:
                    execfile(inp[1])
                else:
                    print('The python shell doesn\'t work jet...')

            elif inp[0] == 'shutdown':
                hub.power_off()

            elif inp[0] == 'reboot':
                hub.power_off(restart = True)

            else:
                print('Unknown command: ' + inp[0])

        except Exception as error:
            system.print_error(error, event_loop = False)

def help_menu():
    print('Help menu')
    print('Press exit or ctrl + D to exit.')
    print('Note: do arguments with spaces between \'.')
    print()
    print('ls/dir    Show all files and dirs in a directory.')
    print('stat      Show info of a file or directory.')
    print('pwd       Show current work directory.')
    print('cd        Change work directory.')
    print('touch     Create a file.')
    print('rm        Remove a file.')
    print('mkdir     Create a directory.')
    print('rmdir     Remove a directory.')
    print('rmtree    Remove a directory with files and sub-directories.')
    print('cat       Show the content of a file.')
    print('cp        Copy a file.')
    print('cptree    Copy a dir with all files and sub-directories.')
    print('mv        Move (rename) a file or dir.')
    print('statfs    Show the status of the file system.')
    print('delline   Delete a line in a file.')
    print('insline   Insert a line in a file.')
    print('addline   Add a line to a file.')
    print('chline    Change a line of a file.')
    print('clearfile Remove all data in a file.')
    print('adddata   Add multiple lines to a file by pasting.')
    print('clear     Clear the screen.')
    print('python    Setup a simple python shell or run a python file.')
    print('shutdown  Turn off the hub.')
    print('reboot    Reboot the hub.')
    print('exit      Return to the hub ui.')

def help_cmd(cmd):
    if cmd == 'ls' or cmd == 'dir':
        print('Show all files and dirs in the current work directory or the given directory.')
        print('It will by default sort the items. Disable this with -s.')
        print('$ ls [-s] <dir>')
        print('$ dir [-s] <dir>')

    elif cmd == 'stat':
        print('Show the status of a file or directory (file/dir, size)')
        print('$ stat path')

    elif cmd == 'pwd':
        print('Show the current work directory.')
        print('$ pwd')

    elif cmd == 'cd':
        print('Change the current work directory.')
        print('$ cd dir')

    elif cmd == 'touch':
        print('Create a new file or new files.')
        print('$ touch file <file2>')

    elif cmd == 'rm':
        print('Remove a file or files.')
        print('$ rm file <file2')

    elif cmd == 'mkdir':
        print('Create a new directory or new directories.')
        print('$ mkdir dir <dir2>')

    elif cmd == 'rmdir':
        print('Remove a empty directory or directories.')
        print('$ rmdir dir <dir2>')

    elif cmd == 'rmtree':
        print('Remove a directory with all files and sub-directories in it.')
        print('$ rmtree dir')

    elif cmd == 'cat':
        print('Show the content of a file.')
        print('-n/--numbers:       Show line numbers (begin counting with 1)')
        print('-l=B-E/--lines=B-E: Only show lines from Begin to End (both included)')
        print('$ cat [-n] [-l=] file')

    elif cmd == 'cp':
        print('Copy a file or multiple files to a file or dir.')
        print('If the to is a file, there can be only 1 from file.')
        print('$ from <from2> to')

    elif cmd == 'cptree':
        print('Copy a directory with all files and sub-directories in it.')
        print('$ from to')

    elif cmd == 'mv':
        print('Move (or rename) a file or directory.')
        print('$ from to')

    elif cmd == 'statfs':
        print('Show the status of the file system.')
        print('$ statfs')

    elif cmd == 'delline':
        print('Delete a line or lines in a file.')
        print('The first line is counted as 1.')
        print('Delete a row of lines with a - between the first and the last.')
        print('$ delline file line <line2>')

    elif cmd == 'insline':
        print('Insert a line in a file.')
        print('Place a \\ before a space, \\ or \'.')
        print('Place a \' before and after an argument if you willn\'t use \\ before spaces.')
        print('The first line is line 1, all lines after the given line (included the given line) will be moved a line.')
        print('Type \\t for a tab and \\xXX for invalid characters.')
        print('$ insline file line text')

    elif cmd == 'addline':
        print('Add a line to a file.')
        print('Place a \\ before a space, \\ or \'.')
        print('Place a \' before and after an argument if you willn\'t use \\ before spaces.')
        print('Type \\t for a tab and \\xXX for invalid characters.')
        print('$ addline file text')

    elif cmd == 'chline':
        print('Change a line of a file.')
        print('Place a \\ before a space, \\ or \'.')
        print('Place a \' before and after an argument if you willn\'t use \\ before spaces.')
        print('Type \\t for a tab and \\xXX for invalid characters.')
        print('$ chline file line text')

    elif cmd == 'clearfile':
        print('Clear a file, remove all the data in it.')
        print('$ clearfile file')

    elif cmd == 'adddata':
        print('Add data to a file.')
        print('Paste the content of a file from your computer to add it to a file.')
        print('Press ctrl + c if you are done.')
        print('The program will not echo your data.')
        print('$ adddata file')

    elif cmd == 'clear':
        print('Clear the screen.')
        print('$ clear')

    elif cmd == 'python':
        print('Setup a simple python shell or run a python (.py) file.')
        print('$ python <file>')

    elif cmd == 'shutdown':
        print('Turn off the hub.')
        print('$ shutdown')

    elif cmd == 'reboot':
        print('Restart the hub (the shell will not be started automaticly).')
        print('$ reboot')

    elif cmd == 'exit':
        print('Exit this shell (afther that, you can use the hub ui).')
        print('You can also press ctrl + D on a blank line.')
        print('$ exit')

