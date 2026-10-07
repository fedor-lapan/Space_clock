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
from machine import  RTC
import time
import network      # wifi connection
import urequests    # api requests
import neopixel     # neopixel 
import gc           # memory optimaser
import random       # random pixel optimisation
import json
from micro_bit import *

"""
The color groups determine what color wil be displayed for specific siruations.
COLORS_DAY = The colors for each area for day lightning
COLORS_NIGHT = The colors for each area for night lightning
COLOR_GROUPS = The pixel areas as an arey with pixel.

"""
"""
COLORS_DAY = [(0, 0, 30),(30, 0, 0),(0, 30, 0),(0, 30, 30)]         # !!! set by json file
COLORS_NIGHT =  [(0, 0, 1),(1, 0, 0),(0, 1, 0),(0, 1, 1)]           # !!! set by json file
COLOR_GROUPS = [                                                    # !!! set by json file
            [0, 17, 18],
            [1, 2, 3, 14, 15, 16, 19, 20, 21],
            [4, 5, 12, 13, 22, 23],
            [6, 7, 8, 9, 10, 11, 24, 25, 26]
            ]
"""

with open('config.json', 'r', encoding='utf-8') as file:
    loaded_data = json.load(file)

COLORS_DAY = loaded_data["colors"]["day_structure"]
COLORS_NIGHT = loaded_data["colors"]["night_structure"]
COLOR_GROUPS = loaded_data["colors"]["structure"]
converter = {
    0: (0, 0),  1: (1, 0),  2: (2, 0),  3: (3, 0),  4: (4, 0),
    5: (4, 1),  6: (3, 1),  7: (2, 1),  8: (1, 1),  9: (0, 1),
    10: (0, 2), 11: (1, 2), 12: (2, 2), 13: (3, 2), 14: (4, 2),
    15: (4, 3), 16: (3, 3), 17: (2, 3), 18: (1, 3), 19: (0, 3),
    20: (0, 4), 21: (1, 4), 22: (2, 4), 23: (3, 4), 24: (4, 4)
}
class Time:
    def __init__(self, ssid: str, pas_code: str, api: str, rtc: RTC, url_weather : str):
        self.ssid = ssid                # !!! set by json file
        self.pas_code = pas_code        # !!! set by json file
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
        self.np_pin = 13 # 2 if the espc3 seed studio xio is used

        #self.pixel_start = 36
        self.url = api
        self.pixel_start = 36
        self.url_w = url_weather
    """
    def np_connect(self):
        self.np = neopixel.NeoPixel(Pin(self.np_pin), 60)
        self.np.fill((0, 0, 0))
        self.np.write()
        print("Neopixels initzilized\n\t;")
    """
    def network_connection(self):
        """
        Checks the nethwork connection 
        """
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
                print("Connected to networks succesfully\n\t;")
                return True
                
            else:
                return False
    
    def device_connection(self):
        rate = 20
        while self.network_connection() is not True and rate > 0:
            time.sleep(2)
            rate -= 1
        with open("debug.txt", "a") as f:
            if rate > 0:
                print("Device connection suceeded\n\t;")
                f.write("Connecton to network completed\n")
                return True
            else:
                f.write("Connection to network was not complited\n")
                return False
        

    
    def testing(self)-> None:
        # Function which tests all the colors ( light all LED's in  specific colors)
        count = 1
        print("at start")
        for group in COLOR_GROUPS:
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

    

    def rtc_tupple(self):# -> Tupple
        """"
        Requests the time data from an api and saves it as an rtc tupple
        """
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
        #print("Time set as: ", end = "")
        print("Time set in rtc\n\t;")
        return (year, mounth, day, 0, hour, minute, seconds, 0)
    def recive_time(self):
        """
        Converts the output tupple of the rtc.datetime command  to a smaller one ( hour, minute )
        """
        time = self.rtc.datetime()
        hours = time[4]
        minutes = time[5]
        #print(hours, minutes)
        
        return (str(hours), str(minutes))
    
    def random_generation(self):
        """
        Converts the time into a better format from a sring to array.
        """
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
        #print(f"Time converted into {usage_array}")

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
        #print(f"Random pixels were selected\n\t;")
        return output
    def weather_app(self):
        """
        Requeasts the weather data from an api. Important:
        Replace the cordinates fron a json file
        """
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
            #f.write(f"Sunshine: {sun}, Rain amount: {rain}, Temperature: {temp}\n")
        #print(f"Weather recived\n\t;")
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
        #print(f"Modified weather for pixel showcase done \n\t;")
        return res
    def draw_time(self, pixels)-> None:
        """
        Displays the valus from the generation, also changes mod from 21 to 7 o'clock
        """
        for i in range(0, 35):
            self.np[i] = (0, 0, 0)
            self.np.write()
        #self.np.fill((0, 0, 0))
        time = self.recive_time()
        #print(time)
        is_datetime = ( 21 > int(time[0]) > 7)
        if is_datetime :
            #print("hi")
            pattern = pixels
            for group in pattern:
                for pixel in group:
                    value = converter[pixel]
                    value_1 = value[0]
                    value_2 = value[1]
                    display.set_pixel(value_1, value_2, 9)
            self.np.write()
        else:
            pattern = pixels
            for group, color in zip(pattern, COLORS_NIGHT):
                for pixel in group:
                    self.np[pixel] = color
    def draw_weather(self, data):
        print("Received Weather Data\n\t;" )
        
        time_data = self.recive_time() 
        hour = int(time_data[0])
        is_daytime = (21 > hour > 7)
        print(is_daytime)
        if is_daytime :
            pixel_point = self.pixel_start
            print(data)
            for index, group in enumerate(data):
                #print("IN LOOP")
                for i in range(3):
                    if index == 0:
                        self.np[pixel_point+i] = (group[i], group[i], 0)
                        #print(f"Just wrote at {pixel_point+i}")
                    elif index == 1:
                        #print(f"I am going to write into pixel{pixel_point+i}this data: {group[i]//dim_factor}")
                        self.np[pixel_point+i] = (0, 0, group[i])
                    else:
                        if group[i] < 0:
                            self.np[pixel_point+i] = (0, 0, group[i])
                        elif group[i] == 0:
                            self.np[pixel_point+i] = (100, 100, 100)
                        else:
                            self.np[pixel_point+i] = (group[i], 0, 0)
                        
                    #print(f"Just wrote at {pixel_point+i}")
                
                    #self.np[pixel_point + i] = infill
                    #self.np.write()
                pixel_point += 3
                    #self.np[pixel_point] = (10, group[i], 0)
            self.np.write()
            print("Writing completed")
        else:
            pass
            starting_pix = self.pixel_start
            for pixel in range(9):
                self.np[starting_pix] = (0, 0, 0)
                starting_pix += 1
            self.np.write()
            print("Didn't write anything")

            

    def cycle(self):
        try:
            self.np_connect()

            if self.device_connection():
                pass
            else:
                return False
            self.rtc_tupple()
            #weather = self.set_weather()
            #self.draw_weather(weather)
            
            #print(weather)
            #self.testing()
            #time.sleep(300)
            time_show = self.random_generation()
            refresh_rate = 1440

            while True:
                time_show = self.random_generation()
                refresh_rate -= 1
                if refresh_rate == 0:
                    print("THE WEATHER JUST GOT UPDATED !!!")
                    with open("debug.txt", "a++")as f:
                        f.write("Weather tool clalled")
                    #weather = self.set_weather()
                    self.rtc_tupple()
                    #self.draw_weather(weather)
                    refresh_rate = 1440
                    
                #self.np.fill((0, 0, 0))
                self.draw_time(time_show)
                #self.draw_weather(weather)
                self.np.write()
                time.sleep(30)
        except Exception as e:
            print(e)
            return False

            

rtc= RTC() 
t = Time(loaded_data["personal_data"]["network"], loaded_data["personal_data"]["password"], loaded_data["overall_data"]["URL_TIME"], rtc, loaded_data["overall_data"]["URL_WEATHER"])
t.cycle()