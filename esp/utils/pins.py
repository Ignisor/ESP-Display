from machine import I2C, Pin

from utils.display import Display


ON = 1
OFF = 0

LED = Pin(1, Pin.OUT)
DISPLAY = Display(I2C(sda=Pin(0), scl=Pin(2)))
