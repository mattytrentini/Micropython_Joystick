# Joystick Library for MicroPython

This repository contains a simple and efficient MicroPython library for interfacing with a joystick module. The library provides calibration, scaling, and real-time value retrieval for both axes (X and Y) and an optional button.

## Features
- **X and Y Axis Support**: Reads analog joystick values and scales them to a range of -100 to 100.
- **Button Support**: Handles an optional button for input.
- **Calibration**: Automatically calibrates the joystick's center position.
- **High Performance**: Optimized for speed with native decorators and efficient sampling.

## Usage

### Initialization
```python
from joystick import Joystick

# Initialize the joystick on pin 1 for X-axes, pin 2 for Y-axes and pin 3 for the button (optional).
joystick = Joystick(1, 2, 3)
```

### Accessing Joystick Values
```python
# Get the scaled X and Y values (-100 to 100)
x_value = joystick.x
y_value = joystick.y

# Get button state (True if pressed, False otherwise)
button_state = joystick.b
```

### Example
```python
import time
from joystick import Joystick

joystick = Joystick(1, 2, 3, CalValues=20)

while True:
    print(f"X: {joystick.x}, Y: {joystick.y}, Button: {joystick.b}")
    time.sleep(0.25)
```

## Performance Benchmark
On a ESP32S3 the library can get all values together at aprox. 7.7 kHz.

## Notes
- Adjust the `CalValues` parameter for better calibration accuracy. Higher values result in more samples being averaged.
- Ensure the joystick is in the center position during calibration.
- If the button is not used, set `PinButton=None` or don't pass the argument at all.
