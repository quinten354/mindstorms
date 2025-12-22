# Introduction

This package is for lego hubs, like mindstorms or spike. The app is a bit limited and if you run large programs on the hub, you wil get a MemoryError.


## What is this about?

 -  To install software on the hub (and you can also restore the lego software)
 -  To upload/download easy files to/from the hub
 -  To interact to the hub with the installed software without using the app


## What is this NOT about?

 -  To interact to the hub with the lego software
 -  To flash firmware


## What are the requirements?

Install: `pip install -r requirements.txt`

Needed:
 -  rshell
 -  serial

Optional:
 -  mpy-cross, you can compile your programs to .mpy programs to use less storage and to run faster. See link: [micropython repo on github](https://github.com/micropython/micropython)


## How to use?

### Connect with the hub

Import the library and connect with `rshell.Pyboard`.

```import mindstorms

hub = mindstorms.Hub_connect_pyboard()
```

When none parameters were given to `Hub_connect_pyboard()`, it will search to the hub with `mindstorms.find_device()`. If it can't find it, it will raise a RuntimeError.
You can add a parameter for the device node of the hub, like /dev/cuaU0 or a other device. You can use `mindstorms.Hub_connect_pyboard(device)`.

You can do:
 -  Close connection with `hub.close()`.
 -  Download/upload file with `hub.download_file(path_hub, path_computer)` or `hub.upload_file(path_computer, path_hub)`.
 -  Execute micropython code on the hub with `hub.exec(str)`.
 -  Power off or restart the hub with `hub.power_off()` or `hub.restart()`. Make sure the connection will be closed.
 -  Set power off timeout in miliseconds with `hub.set_power_off_timeout(ms)`.
 -  Install the software with `hub.install(restart_after_installing)`. If `restart_after_installing` is False, the connection will stay opened.


### Easy install the software

Install the software to use `mindstorms.install(device)`.

```import mindstorms

mindstorms.install() # does the same as mindstorms.install(mindstorms.find_device())

## add device node
device = '/dev/cuaU0'
mindstorms.install(device)
```


## Connect with the event-loop on the hub

You can only do this when the software is installed on the hub.

Use `mindstorms.Hub_connect_event_loop(device)`.

```import mindstorms

hub = mindstorms.Hub_connect_event_loop()
```

This will connect to the event loop on the hub. The event loop works with asyncio, on micropython uasyncio.

You can do:
 -  Close connection, download/upload file, power off, restart and set power off timeout on the same was as `Hub_connect_pyboard()`.
 -  Send a command to the event loop, you can only send a dict with some keywords in it, see [table for i/o to hub](notes/io.txt) for more information.
 -  Upload a user-created program to the hub. This program will be stored on /programs/NAME.
        Use `hub.upload_program(path_computer, name, animation)`.
        Only the `path_computer` parameter is required.
        You can use the `name` parameter to change the name of the program on the hub. That name will be placed on /programs/NAME.
        You can add the `animation` parameter. If it is given, the hub will show that animation instead of the program name.
        The animation must be a list with a list of 5 list of 0 or 1 (off or on).

# User programs

You can create a user program and upload it to the hub.
See more information in the [docs](docs/user_programs.md).


## Requirements

This are the requirements for a user program


### Required

 -  main function (accept one parameter, can be used to connect to a lego remote or something else)


### Optional

 -  yield in main function to continue the event loop. Use `yield` to update event loop and continue so fast as possible, or `yield SEC` and replace `SEC` for the number of seconds (may be float) to wait.


## Multi threading

A easy way to run multiple programs at the same time is to use yield, here is a example:

```import hub

def main(events):
    abc = setup_abc()
    write = setup_writer()
    while True:
        abc.__next__()
        write.__next__()
        yield

def setup_abc():
    while True:
        print('abc')
        yield

def setup_writer():
    while True:
        hub.display.show('abc')
        yield
```


## Packages

You can see here the built-in package hub and the package device.


### Hub

You can use it with `import hub`. See [docs](https://lego.github.io/MINDSTORMS-Robot-Inventor-hub-API/pkg_hub.html) for more info.


### Device

Device is a package that uses hub (see above) and it is easy to use. See [docs](docs/device.md) for more info.
            

# Links
 -  [docs hub package](https://lego.github.io/MINDSTORMS-Robot-Inventor-hub-API/pkg_hub.html)
 -  [mindstorms repo github](https://github.com/noamraph/mindstorms)
 -  [rshell github](https://github.com/dhylands/rshell)

