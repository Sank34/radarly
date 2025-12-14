# radarly
Radarly is an arduino radar created for one of my assignments in physics class. Its purpose was to demonstrate how the reflected ultrasonic sounds can allow us to measure the distance between a **source** *(the arduino sensor)* and an **object**.

## App Preview
Here is the interface of the application:

![img](./assets/appUI.png)

## Tech Stack
In order to implement this app, i've used the following tech stack: <br>
**Frontend** <br>
- Pygame (Python library)

**Backend** <br>
- Serial (Python library)
- Math, deque (Standard py libraries)
- Arduino Servo Library <br>

**Languages** <br>
- Python
- C++ (ino)

## Setting up the project
In order to run the project on your local machine, you'll first need to clone it:
```bash
git clone https://github.com/Sank34/radarly.git
```
Inside the **interface** directory you'll find the python script. You can configure your variables or leave it as is.
- ``PORT``: your serial communication port.
- ``BAUD``: do NOT modify, it's the serial communication frequency.
- ``WIDTH; HEIGHT``: the resolution of your radar's window.
- ``FPS``: the refresh rate of your radar's window.
- ``MAX_CM``: the maximum width of your radar. Keep in mind that the HC-SR04 can measure up to 400 cm, so that's the maximum value. (Recommended to not modify it over 100 cm)
- ``SWEEP_WIDTH``: the width of your radar's sweep.
- ``POINT_MEMORY``: how many points the radar should keep in memory (aka how fast they dissapear).

Now let's setup the hardware! Here is the hardware's diagram:
![hardware](./assets/radarHardware.png)

You'll find the arduino code inside the **arduino** directory. You shouldn't modify anything, except if you have a different hardware setup for your desired ports.

Now you can upload the code on your arduino UNO/NANO board, run the python app and see the magic happen!

## How does it work?
Ofcourse , in order to make the project run we've had to come up with some formulas. Here you'll find each formula we have used in this project:

(...)

