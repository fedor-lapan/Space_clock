from machine import Pin
import neopixel 
import time

np = neopixel.NeoPixel(Pin(2), 60)


for pixel in range(60):
    np[pixel] = (100, 0, 0)
    np.write()
    time.sleep(1)
    np[pixel] = (0, 0, 0)
    np.write()
print("Neopixels connected")