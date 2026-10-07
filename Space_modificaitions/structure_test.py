import neopixel
import time
from machine import Pin
np = neopixel.NeoPixel(Pin(13), 35)

for i in range(0, 34):
    np[i] = (100, 100, 100)
    time.sleep(2)
    np.write()
