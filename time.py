"""
file name = time_only.py
group = new_debug_version
description = 
A class for a neopixel binary clock with time update via wifi and rtc module
Pin_config:
In = 0
GND = GND
Vcc = 5v
"""
# Imports:
#     gc module for ram manadgement
#     network + urequests for time application
#     neopixle for neopixel
#     random for oixel generation
#     mashine for RTC and Pin conffiguration
from machine import Pin, RTC
import time
import network
import urequests
import neopixel
import gc
import random


COLORS_DAY = [(0, 0, 50),(50, 0, 0),(0, 50, 0),(0, 50, 50)]
COLORS_NIGHT =  [(0, 0, 1),(1, 0, 0),(0, 1, 0),(0, 1, 1)]
COLOR_GROUPS = [
            [0, 17, 18],
            [1, 2, 3, 14, 15, 16, 19, 20, 21],
            [4, 5, 12, 13 , 22, 23],
            [6, 7, 8, 9, 10, 11, 24, 25, 26]
            ]

class Time:
    def __init__(self, ssid: str, pas_code: int, api: str, rtc: RTC):
        self.ssid = ssid
        self.pas_code = pas_code
        """ 
        Varaible explanation:
            self.colors ( group of 2 ) -> manadge each color of evry sector
            self.rtc -> rtc module configuration
            self.groups -> list of each group ( pixels )
            self.api -> url link for time requests
            ssid + password -> wifi data
        """
        self.rtc= rtc
        self.np_pin = 0

        #self.pixel_start = 36
        self.url = api


    def np_connect(self):
        self.np = neopixel.NeoPixel(Pin(self.np_pin), 45)
        self.np.fill((0, 0, 0))
        self.np.write()
    def connect(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(False)   
        wlan.active(True)   
        
        # connecting to wifi
        if not wlan.isconnected():
            wlan.connect(self.ssid, self.pas_code)
            attempt = 0
            while not wlan.isconnected() and attempt < 10:
                time.sleep(1)
                attempt += 1
            #print(wlan.ifconfig())
            with open("debug.txt", "w") as f:
                if wlan.isconnected():
                    print("True")
                    f.write(f"Connecton to {self.ssid} completed\n")
                else:
                    f.write(f"Connection to {self.ssid} was not complited\n")

    def testing(self)-> None:
        """
        Function which tests all the colors ( light all LED's in  specific colors)
        """
        count = 1
        print("at start")
        for group in self.groups:
            for pix in group:
                if count == 1:
                    self.np[pix] = (0, 0, 100)
                elif count == 2:
                    self.np[pix] = (100, 0, 0)
                elif count == 3:
                    self.np[pix] = (0, 100, 0)
                else:
                    self.np[pix] = (0, 100, 100)
                self.np.write()
            count += 1

    def rtc_tupple(self):# -> Tupple
        """
        Recives the json pack from the api and saves it inside of the memory
        """
        response = urequests.get(self.url, timeout= 10.0)
        data = response.json()
        response.close()
        gc.collect()
        year = int(data['local_time'].split('-')[0])
        mounth = int(data['local_time'].split('-')[1])
        day = int(data['local_time'].split('-')[2].split('T')[0])
        hour = int(data['local_time'].split('-')[2].split('T')[1].split(':')[0])
        minute = int(data['local_time'].split('-')[2].split('T')[1].split(':')[1])
        seconds = int(data['local_time'].split('-')[2].split(":")[2].split(".")[0])
        self.rtc.datetime((year, mounth, day, 0, hour, minute, seconds, 0))
        return (year, mounth, day, 0, hour, minute, seconds, 0)
     
    def recive_time(self):
        """
        Converts the output tupple of the rtc.datetime command  to a smaller one ( hour, minute )
        """
        time = self.rtc.datetime()
        hours = time[4]
        minutes = time[5]
        #print(hours, minutes)
        with open("debug.txt", "a+") as f:
            f.write("Application completed:\n")
            f.write(f"{hours}:{minutes}")
        return (str(hours), str(minutes))
    
    def random_generation(self):
        time = self.recive_time()
        hours = time[0]
        """
        1 part:
            converting the tupple into a hour_1, hour_2, minute_1 ... tupple
        2 part:
            random generation of the pixel wich willl be light up in each sector
        """
        if len(hours) == 1:
            hour_1 = 0
            hour_2 = hours[0]
        else:
            hour_1 = hours[0]
            hour_2 = hours[1]
        minutes = time[1]
        if len(minutes) == 1:
            minute_1 = 0
            minute_2 = minutes[0]
        else:
            minute_1 = minutes[0]
            minute_2 = minutes[1]
        already_used = set()
        output = [[],[],[],[]]
        usage_array = [hour_1, hour_2, minute_1, minute_2]

        def random_value(group):
            return random.choice(group)
        
        for idx, (group, value) in enumerate(zip(COLOR_GROUPS, usage_array)):
                for i in range(int(value)):
                    while True:
                        pixel = random_value(group)
                        if pixel not in already_used:
                            #print(pixel)
                            already_used.add(pixel)
                            self.np[pixel] = (0, 0, 100)
                            output[idx].append(pixel)
                            break
                #print(already_used)
                already_used.clear()
        return output
    def show_values(self)-> None:
        """
        Displays the valus from the generation, also changes mod from 21 to 7 o'clock
        """
        self.np.fill((0, 0, 0))
        time = self.recive_time()     
        if int(time[0]) < 21 and int(time[0]) > 7:
            #print("hi")
            pattern = self.random_generation()
            for group, color in zip(pattern, COLORS_DAY):
                for pixel in group:
                    self.np[pixel] = color
            self.np.write()
        else:
            pattern = self.random_generation()
            for group, color in zip(pattern, COLORS_NIGHT):
                for pixel in group:
                    self.np[pixel] = color
            self.np.write()

            

rtc= RTC()
t = Time("ShmumaIoT", "BOleNetI", "https://timeapi.io/api/v1/timezone/zone?timeZone=Europe%2FBerlin", rtc)
t.connect()
t.np_connect()
#t.show_values()
#t.testing()
t.rtc_tupple()
t.show_values()
refresh_rate = 1440
timer = 0
while True:
    time.sleep(30)
    if timer == refresh_rate:
        t.rtc_tupple()
    t.show_values()