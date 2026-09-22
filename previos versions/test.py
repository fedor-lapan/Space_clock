import neopixel
from machine import Pin
np = neopixel.NeoPixel(Pin(0), 45)
np.fill((0, 0, 120))
np.write()