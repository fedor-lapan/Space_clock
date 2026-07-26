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
    def __init__(self, ssid: str, pas_code: str, api: str, rtc: RTC):
        self.ssid = ssid
        self.pas_code = pas_code
        """ 
        Varaible explanation:
            self.colors ( group of 2 ) -> manadge each color of evry sector
            self.rtc -> rtc module configuration
            self.groups -> list of each group ( pixels )
            self.api -> url link for time requests
            ssid + password -> wifi data
            np_pin -> Neopixel gpio
            pixel_start -> Starting pixel of the  weather
        """
        self.rtc= rtc
        self.np_pin = 0

        #self.pixel_start = 36
        self.url = api
        self.pixel_start = 36
        self.url_w = "https://api.open-meteo.com/v1/forecast?latitude=52.21099&longitude=7.02238&daily=temperature_2m_max,rain_sum,sunshine_duration&timezone=Europe%2FBerlin&forecast_days=3"


    def np_connect(self):
        self.np = neopixel.NeoPixel(Pin(self.np_pin), 45)
        self.np.fill((0, 0, 0))
        self.np.write()
    def network_connection(self):
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
            if wlan.isconnected():
                return True
            else:
                return False
    
    def device_connection(self):
        rate = 20
        while self.network_connection() is not True and rate > 0:
            time.sleep(2)
            rate -= 1
        with open("debug.txt", "w") as f:
            if rate > 0:
                print("True")
                f.write(f"Connecton to {self.ssid} completed\n")
                return True
            else:
                f.write(f"Connection to {self.ssid} was not complited\n")
                return False
        

    """
    def testing(self)-> None:
        #Function which tests all the colors ( light all LED's in  specific colors)
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
    """

    def rtc_tupple(self):# -> Tupple
        #Recives the json pack from the api and saves it inside of the memory
        response = urequests.get(self.url, timeout= 10.0)
        data = response.json()
        response.close()
        gc.collect()
        #print(data)
        year = int(data['datetime'].split('-')[0])
        mounth = int(data['datetime'].split('-')[1])
        day = int(data['datetime'].split('-')[2].split('T')[0])
        hour = int(data['datetime'].split('-')[2].split('T')[1].split(':')[0])
        minute = int(data['datetime'].split('-')[2].split('T')[1].split(':')[1])
        seconds = int(data['datetime'].split('-')[2].split(":")[2].split(".")[0])
        self.rtc.datetime((year, mounth, day, 0, hour, minute, seconds, 0))
        print( (year, mounth, day, 0, hour, minute, seconds, 0) )
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
            f.write(f"{hours}:{minutes}\n")
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
                            output[idx].append(pixel)
                            break
                #print(already_used)
                already_used.clear()
        return output
    def weather_app(self):
        gc.collect()
        response = urequests.get(self.url_w, timeout = 10.0)
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
            return round((value / (11 * 60 * 60))* 255, 0)
        if w_type == "t":
            if value < 0:
                return round(-abs(abs(value) / 40 *255), 0)
            elif value == 0:
                return 0
            else:
                return round(((value / 40) * 255), 0)
    def set_weather(self):
        #self.np[self.pixel_start] = (100, 0, 0)
        #self.np.fill((0, 0, 0))
        #print(self.application())
        status_kind = ["s", "r", "t"]
        res = [[],[],[]]
        current_status = 0
        pixel_s = self.pixel_start
        for parameter in self.weather_app():
            #print(parameter)
            #print(status_kind[current_status])
            for value in parameter:
                if status_kind[current_status] == "s":
                    #print("At sunn")
                    output = int(self.converter("s", value))
                    #print(output, value)
                    res[0].append(output)
                elif status_kind[current_status] == "r":
                    #print("At rain")
                    if int(value) == 0:
                        output = 0
                    else:
                        output = int(self.converter("r", value))
                    #print(output, value)
                    res[1].append(output)
                elif status_kind[current_status] == "t":
                    #print("At temp")
                    output = int(self.converter("t", value))
                    res[2].append(output)
                    #self.np.write()
                    #print(output, value)
                #print(value)
                pixel_s += 1
            current_status += 1
        return res
    def draw_time(self, pixels)-> None:
        """
        Displays the valus from the generation, also changes mod from 21 to 7 o'clock
        """
        #self.np.fill((0, 0, 0))
        time = self.recive_time()
        #print(time)
        if int(time[0]) < 21 and int(time[0]) > 7:
            #print("hi")
            pattern = pixels
            for group, color in zip(pattern, COLORS_DAY):
                for pixel in group:
                    self.np[pixel] = color
            self.np.write()
        else:
            pattern = pixels
            for group, color in zip(pattern, COLORS_NIGHT):
                for pixel in group:
                    self.np[pixel] = color
        
    def draw_weather(self, data):
        time = self.recive_time()

        temp = data[0]
        rain = data[1]
        sun = data[2]
        b_pixel = self.pixel_start
        if int(time[0]) < 21 and int(time[0]) > 7:
            for group in range(1, 4):
                for i in range(0, 3):
                    if group == 1:
                        self.np[b_pixel+i] = (sun[i], sun[i] // 2, 0)
                    if group == 2:
                        self.np[b_pixel+i] = (0, 0, rain[i])
                    if group == 3:
                        if temp[i] <= 0:
                            self.np[b_pixel+i] = (0, 0, abs(temp[i]))
                            print("HELLLOOO")
                        else:
                            print(temp[i])
                            self.np[b_pixel+i] = (temp[i], 0, 0)
                b_pixel += 3
        else:
            for group in range(1, 4):
                for i in range(1, 3):
                    if group == 1:
                        self.np[b_pixel+i] = (sun[i]//10, sun[i] // 20, 0)
                    if group == 2:
                        self.np[b_pixel+i] = (0, 0, rain[i]//10)
                    if group == 3:
                        if temp[i] <= 0:
                            self.np[b_pixel+i] = (0, 0, abs(temp[i]//10))
                        else:
                            self.np[b_pixel+i] = (temp[i]//10, 0, 0)
                b_pixel += 3



                
        

        return True
    def cycle(self):
        self.np_connect()
        self.device_connection()
        self.rtc_tupple()
        weather = self.set_weather()
        print(weather)
        time_show = self.random_generation()
        refresh_rate = 1440
        self.draw_weather(weather)
        while True:
            time_show = self.random_generation()
            refresh_rate -= 1
            if refresh_rate == 0:
                weather = self.set_weather()
                self.rtc_tupple()
                self.draw_weather(weather)
                print("Update")
            self.np.fill((0, 0, 0))
            self.draw_time(time_show)
            self.draw_weather(weather)
            self.np.write()
            time.sleep(30)

            

rtc= RTC()
t = Time("ShmumaIoT", "BOleNetI", "https://time.now/developer/api/timezone/Europe/Berlin", rtc)
t.cycle()