# Package device

## Introduction

Device is a easy to use package for controll the hubs display, the led, motors, other devices, motion, i/o and GPIO pins.


## How to use

It's very simple, import the module: `import device`.


# Top-level

## Get led color

Get the current rgb color of the led

```import device
device.get_led()
```


## Set led color

Set the led rgb color (must be a tuple with 3 values between 0 and 255)
See constants --> colors for prepared colors.

```import device
device.set_led((RED, GREEN, BLUE))
```


## Temperature

Get the current temperature of the hub in °C.

```import device
device.get_temp()
```


# Battery

## Voltage

Get the voltage of the battery in mV.

```import device
device.battery.get_voltage()
```


## Power

Get the power of the battery in mA.

```import device
device.battery.get_power()
```


## Current

Get the current capacity of the battery in %.

```import device
device.battery.get_current()
```


## Temperature

Get the current temperature of the battery in °C.

```import device
device.battery.get_temp()
```


# Button

The hub has 4 buttons: center, connect (bluetooth), left and right. For each button are these functions:


## Is pressed

Returns True if the button is pressed right now or False if it not.

```import device
device.button.right.is_pressed()
```


## Was pressed

Returns True if the button was pressed.

```import device
device.button.right.was_pressed()
```


## Presses

Returns the number of times the button is pressed.

```import device
device.button.right.presses()
```


# Constants

## Rgb colors

Here do you find a lot of prepared RGB colors.
Use `device.constants.rgb_colors.COLOR` with color is one of WHITE, BLACK, RED, ORANGE, YELLOW, GREEN, PETROL, BLUE or PURPLE.


## Light matrix

Here can you find a lot of prepared colors for the 3x3 light matrix device.
Availeble colors: OFF, WHITE, GREY, RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE and PINK.


## Colors

Here can you find some colors from color-sensors.
Availeble colors: WHITE, RED, YELLOW, GREEN, CYAN, BLUE, BLACK and NONE.


# Display

## Picture

Place a animation on the hubs display

It requires a list, with a list of rows with a list of pixels (1 = on, 0 = off).


### Show next

Update the animation

```import device
picture = device.display.Picture([
    [[1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1],
    [0, 0, 0, 0, 0],
    [1, 0, 0, 0, 1],
    [0, 1, 1, 1, 0]],

    [[1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [1, 0, 0, 0, 1]]])

while True:
    picture.show_next()
    yield 0.2
```
This example shows a animation with a happy smile and a angry smale.


## Print hub matrix

This place text on the display. Parameters: text: str, spaces_before_start: bool = True, loop: bool = True.


### Show next

Update the animation


### Start

Start the animation and stops if it is done. Parameters: interval: float.

```import device
animation = device.display.Print_hub_matrix('test123')

while True:
    animation.show_next()
    yield 0.2
```
This example shows repeatly 'test123' on the display.


### Image

Shows a image on the display
Works the same as picture, but this is 1 frame of the animation.


### Clear

Clear the display


### Get pixel

Get if the pixel is on (1) or off (0)


### Set pixel

Set a pixel on (1) or off (0)


# I/O

This module can read and write data from/to the computer.

To use it, you must first initialise the class device/io/Io:

```import device.io

def main(events):
    io = device.io.Io(events)
    print = io.print
    input = io.input
    getch = io.getch
    getall = io.getall
```

## print

Send data to the computer. You can give more parameters. They will be added by sep (default a space), and end (default a newline) will be added to the datastring.
Example:

```print = device.io.Io(events).print
print('test1', 'test2', 'test3', sep = ', ')
```
Output: 'test1, test2, test3\n'


## input

Read all data from the computer and stops by the first newline. Accepts 0 parameters.


## getch

Read 1 character from the computer. Accepts 0 parameters.


## getall

Read all availeble data from the computer. Accepts 0 parameters.


# Motion

## Get motion values

```import device.motion
acceleration = device.motion.get_acceleration(filtered = False)
gyroscope = device.motion.get_gyroscope(filtered = False)
yaw = device.motion.get_yaw(filtered = False)
pitch = device.motion.get_pitch(filtered = False)
roll = device.motion.get_roll(filtered = False)
```

Acceleration and gyroscope returns a tuple with 3 values: x, y and z, yaw, pitch and roll returns 1 interger.


## Set yaw value

Reset the yaw value, the current yaw is now the given value.

```import device.motion
device.motion.set_yaw(0)
```

## Get gesture events

```import device.motion
tapped = device.motion.was_tapped()
double_tapped = device.motion.was_double_tapped()
shaked = device.motion.was_shaked()
freefall = device.motion.was_freefall()
```

# Path

Here can you find functions like os.path.

## Isdir

Use `device.path.isdir(PATH)` with PATH is a string to a file or directory.


# Port

Here can you find functions for lego sensors, motors and more.

```import device.port
#########
# Motor #
#########

# Get current speed of motor connected to port A
speed = device.port.motor.get_speed('A')

# Get relative position
rel_pos = device.port.motor.get_rel_pos('A')

# Set relative position (second argument isn't required)
device.port.motor.set_rel_pos('A', 100)

# Get abs position
abs_pos = device.port.motor.get_abs_pos('A')

# Float motor (you can easyally move the motor)
device.port.motor.float('A')

# Break motor (you can't move easyally the motor)
device.port.motor.break('A')

# Hold the motor (if you move the motor, it goes back to his old position)
device.port.motor.hold('A')

# Get if the motor is busy with a action (bool)
busy = device.port.motor.get_busy('A')

# Run motor at a speed
device.port.motor.run_speed('A', 75)

# Run the motor for a time (sec)
device.port.motor.run_for_sec('A', 5, speed = 75)

# Run the motor for a number of degrees
device.port.motor.run_for_degrees('A', 360, speed = 75)

# Run the motor to relative position
device.port.motor.run_to_rel_position('A', 0, speed = 75)

# Run the motor to abs position
# Choose direction between fastest (default), right or left.
device.port.motor.run_to_abs_position('A', 0, 'right')

# Set default of the motor, use default(speed = 75) 1 time instead of everytime add a keyword speed = 75.
# Choose keywords: speed, max_power, acceleration, deceleration, stop, pid and stall.
# You can add this keywords also by all other functions.
device.port.motor.default('A', KEYWORD)

###################
# Distance sensor #
###################

# Get distance
cm = device.port.devices.distance_sensor.get_cm('B')
inch = device.port.devices.distance_sensor.get_inch('B')

# Set light
# Values 0 --> 100, left-up, right-up, left-down, right-down
device.port.devices.distance_sensor.set_light('B', 100, 100, 100, 100)

# Get light
light = device.port.devices.distance_sensor.get_light('B')
# licht = [100, 100, 100, 100]

################
# Color sensor #
################

# Turn light on
device.port.devices.color_sensor.on('C')

# Turn light off
device.port.devices.color_sensor.off('C')

# Get color (see constants.colors)
color = device.port.devices.color_sensor.get_color('C')

# Get reflection
ref = device.port.devices.color_sensor.get_reflection('C')

# Get rgb
rgb = device.port.devices.color_sensor.get_rgb('C')
# rgb = [r, g, b]

################
# Light matrix #
################

# the 3x3 light matrix

# Clear, set all pixels off
device.port.devices.light_matrix.clear('D')

# Set color (see constants.light_matrix)
device.port.devices.light_matrix.set_color('D', 'abcdefghi')
device.port.devices.light_matrix.set_color('D', device.constants.light_matrix.YELLOW * 9)

#########################
# Color-distance sensor #
#########################

# Set color of light
device.port.devices.color_distance_sensor.red('E')
device.port.devices.color_distance_sensor.green('E')
device.port.devices.color_distance_sensor.blue('E')
device.port.devices.color_distance_sensor.white('E')
device.port.devices.color_distance_sensor.off('E')

# Get color (see constants.colors)
color = device.port.devices.color_distance_sensor.get_color('E')

# Get reflection
ref = device.port.devices.color_distance_sensor.get_reflection('E')

# Get rgb
rgb = device.port.devices.color_distance_sensor.get_rgb('E')

# Get cm
cm = device.port.devices.color_distance_sensor.get_cm('E')

# Get inch
inch = device.port.devices.color_distance_sensor.get_inch('E')

# Get counted
counted = device.port.devices.color_distance_sensor.get_counted('E')

#########
# Other #
#########

# Get type
type = get_type('F')
```

For device types, see [table for devices](../notes/devices.txt)


# Remote

With this module, you can connect with the lego powerd up remote 88010.

## Connect

Connect to the remote. This does the same as pressing the connect button

```import device.remote
device.remote.connect(events)
```

## Is connected

Check if the remote is connected. `device.remote.is_connected(events)`


## Disconnect (not working)

Disconnect: `device.remote.disconnect(events)`


## Get remote

Get the remote class: `device.remote.get_remote(events)`


## Get pressed

Get buttons there are pressed: `device.remote.get_pressed(events)`


## Is pressed

Get if the given button is pressed: `device.remote.is_pressed(events, button)`


## Get value (not good working)

Get the value (left, right): `device.remote.get_value(events)`


# Sound

## Get volume

Get the current volume: `device.sound.get_volume()`


## Set volume

Set the volume: `device.sound.set_volume(volume)`


## Beep

Beep: `device.sound.beep(freq = 1000, time = 0.2)`


## Play

Requires a string: `device.sound.play('Damage')`


## Play a file

Play a sound from a file: `device.sound.play_file('/extra_files/Damage')`

