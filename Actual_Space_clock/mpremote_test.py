from machine import Pin 
import neopixel
np = neopixel.NeoPixel(Pin(13), 35)
np.fill((100, 100, 100))
np.write()