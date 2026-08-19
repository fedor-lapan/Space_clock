from machine import Pin
import neopixel
import time

# Teste Pin 3 (C3) oder Pin 2 (S3)
np = neopixel.NeoPixel(Pin(2), 60) 

print("Sende Test-Signal an die Matrix...")
# Schalte alle 60 LEDs auf ein schwaches, sicheres Rot
np.fill((10, 0, 0)) 
np.write()
print("Signal gesendet!")
