from machine import ADC, Pin
from time import sleep_ms
from micropython import const

class Joystick:
    MaxRaw = const(65535)
    def __init__(self, PinX, PinY, PinButton=None, *, CalValues=10):
        self._jx = ADC(Pin(PinX))
        self._jy = ADC(Pin(PinY))

        try:
            self._jx.width(ADC.WIDTH_12BIT)
            self._jy.width(ADC.WIDTH_12BIT)
            self._jx.atten(ADC.ATTN_11DB)
            self._jy.atten(ADC.ATTN_11DB)
        except AttributeError:
            raise RuntimeError("ADC width/atten not supported on this platform.")
        
        if PinButton:
            self._jb = Pin(PinButton, Pin.IN, Pin.PULL_UP)
        else:
            self._jb = None

        # Initial calibration
        if CalValues > 0:
            self._x_center, self._y_center = self.calibrate_center(CalValues)

    def calibrate_center(self, num_samples=10, delay_ms=1):
        """
        Calibrates the center value for both ADC pins.
        
        Args:
            num_samples (int): The number of samples to average for calibration.
        
        Returns:
            tuple: The calibrated center values for x and y axes.
        """
        total_x = 0
        total_y = 0
        for _ in range(num_samples):
            total_x += self._jx.read_u16()
            total_y += self._jy.read_u16()
            if delay_ms > 0:
                sleep_ms(delay_ms)
        center_x = total_x // num_samples
        center_y = total_y // num_samples
        return center_x, center_y
    
    @micropython.native
    def _scale_value(self, reading, center):
        """Scales the raw ADC value to a range of -100 to 100."""
        delta = reading - center
        if center == 0:
            return 0  # Prevent division by zero
        if delta >= 0:
            return (delta * 100) // (self.MaxRaw - center)
        else:
            return (delta * 100) // center
        
    @property
    @micropython.native
    def x(self):
        """Return x-axis value from -100 to 100."""
        return self._scale_value(self._jx.read_u16(), self._x_center)

    @property
    @micropython.native
    def y(self):
        """Return y-axis value from -100 to 100."""
        return self._scale_value(self._jy.read_u16(), self._y_center)

    @property
    @micropython.native
    def b(self):
        """Return button state, True if pressed, False otherwise."""
        if self._jb:
            return not self._jb.value()
        else:
            return None

if __name__ == "__main__":
    J = Joystick(1, 2, 3, CalValues=100)
    import time
    n = 1000
    t0 = time.ticks_us()
    for _ in range(n):
        J.x
        J.y
        J.b
    t1 = time.ticks_us()
    dt = time.ticks_diff(t1, t0)
    print(f'Getting Samples at {n/dt*1e3:2.2f} kHz')
    while True:
        print("X: {}, Y: {}, Button: {}".format(J.x, J.y, J.b))
        time.sleep_ms(250)  # Sleep for 250 milliseconds
