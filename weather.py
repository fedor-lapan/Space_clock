import network
import urequests
import time
import gc
from machine import Pin
import neopixel
class Weather:
    
    def __init__(self, ssid, password, update_rate, weather_url):
        self.pixel_start = 36
        self.url = weather_url
        self.np = neopixel.NeoPixel(Pin(0), 45)
        self.np.fill((0, 0, 0))
        self.np.write()
        wlan = network.WLAN(network.STA_IF)
        wlan.active(False)   
        wlan.active(True)   
        
        if not wlan.isconnected():
            wlan.connect(ssid, password)
            attempt = 0
            while not wlan.isconnected() and attempt < 10:
                time.sleep(1)
                attempt += 1
            #print(wlan.ifconfig())
            with open("debug.txt", "w") as f:
                if wlan.isconnected():
                    print("True")
                    f.write(f"Connecton to {ssid} completed\n")
                else:
                    f.write(f"Connection to {ssid} was not complited\n")
                            
                            
    def application(self):
        gc.collect()
        response = urequests.get(self.url, timeout = 10.0)
        data = response.json()
        response.close()
        gc.collect()
        sun = data['daily']['sunshine_duration']
        rain = data['daily']['rain_sum']
        temp = data['daily']['temperature_2m_max']
        del data
        with open("debug.txt", "a+") as f:
            f.write("Application completed:\n")
            f.write(f"Sunshine: {sun}, Rain amount: {rain}, Temperature: {temp}\n")
        return (sun, rain, temp)
    def converter(self, w_type, value):
        if w_type == "r":
            return round((value / 500) * 255, 0)
        if w_type == "s":
            return round((value / (12 * 60 * 60))* 255, 0)
        if w_type == "t":
            if value < 0:
                return round(-abs(abs(value) / 40 *255), 0)
            elif value == 0:
                return 0
            else:
                return round(((value / 50) * 255), 0)
    def display(self):
        #self.np[self.pixel_start] = (100, 0, 0)
        self.np.fill((0, 0, 0))
        #print(self.application())
        status_kind = ["s", "r", "t"]
        current_status = 0
        pixel_s = self.pixel_start
        for parameter in self.application():
            #print(parameter)
            #print(status_kind[current_status])
            for value in parameter:
                if status_kind[current_status] == "s":
                    #print("At sunn")
                    output = int(self.converter("s", value))
                    #print(output, value)
                    self.np[pixel_s] = (output, output, 0)
                    self.np.write()
                elif status_kind[current_status] == "r":
                    #print("At rain")
                    if int(value) == 0:
                        output = 0
                    else:
                        output = int(self.converter("r", value))
                    #print(output, value)
                    self.np[pixel_s] = (0, output, output)
                    self.np.write()
                elif status_kind[current_status] == "t":
                    #print("At temp")
                    output = int(self.converter("t", value))
                    if output < 0:
                        self.np[pixel_s] = (0, output, output)
                    else:
                        self.np[pixel_s] = (output, 0, 0)
                    self.np.write()
                    #print(output, value)
                #print(value)
                pixel_s += 1
            current_status += 1
                    
                
        
                                

w = Weather("ShmumaIoT", "BOleNetI", 10, "https://api.open-meteo.com/v1/forecast?latitude=52.21099&longitude=7.02238&daily=temperature_2m_max,rain_sum,sunshine_duration&timezone=Europe%2FBerlin&forecast_days=3")
#print(w.application())
#print(w.converter("t", 40))
timer = 3600
current = 0
w.display()
while True:
    time.sleep(1)
    if timer == current:
        print("updated")
        w.display()
        current = 0
    #print(current)
    current += 1
