# Package device

## Introduction

Device is a easy to use package for controll the hubs display, the led, motors, other devices, motion, i/o and GPIO pins.


## How to use

It's very simple, import the module: `import device`.


# Top-level

## Get led color

Get the current rgb color of the led

```device.get_led()
```


## Set led color

Set the led rgb color (must be a tuple with 3 values between 0 and 255)
See constants --> colors for prepared colors.

```device.set_led((RED, GREEN, BLUE))
```


## Temperature

Get the current temperature of the hub in °C.

```device.get_temp()
```


# Battery

## Voltage

Get the voltage of the battery in mV.

```device.battery.get_voltage()
```


## Power

Get the power of the battery in mA.

```device.battery.get_power()
```


## Current

Get the current capacity of the battery in %.

```device.battery.get_current()
```


## Temperature

Get the current temperature of the battery in °C.

```device.battery.get_temp()
```


# Button

The hub has 4 buttons: center, connect (bluetooth), left and right. For each button are these functions:


## Is pressed

Returns True if the button is pressed right now or False if it not.

```device.button.right.is_pressed()
```


## Was pressed

Returns True if the button was pressed.

```device.button.right.was_pressed()
```


## Presses

Returns the number of times the button is pressed.

```device.button.right.presses()
```


# Constants

## Colors

A lot of prepared rgb colors


# Display

## Picture

Place a animation on the hubs display

It requires a list, with a list of rows with a list of pixels (1 = on, 0 = off).


### Show next

Update the animation

```picture = device.display.Picture([
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

```animation = device.display.Print_hub_matrix('test123')

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


# Motion


# Port


# Sound


# System

