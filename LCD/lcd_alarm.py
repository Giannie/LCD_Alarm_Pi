#!/usr/bin/python

from time import sleep
import time
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from alarm_time import *
import subprocess
import os
import sys

select = 1
right = 2
down = 4
up = 8
left = 16

FNULL = open(os.devnull, 'w')

lcd = Adafruit_CharLCDPlate()

lcd_string_prev = ''
wait_time = 1

settings = ["Set hour:","Set minute:", "On or Off?"]
menus = ["Set Alarm","Set Backlight","Power Management","Cancel"]
confirm = ["Yes","No"]
con = "Are you sure?"

colours = [lcd.RED , lcd.YELLOW, lcd.GREEN, lcd.TEAL, lcd.BLUE, lcd.VIOLET]
colour_def = 5
colour_prev = colour_def
colour = colour_def
lcd.backlight(colours[colour])
lcd_on = True
lcd_on_prev = True
before = 0
crontab = ''
alarm = ''
lcd_string = alarm_time(crontab,alarm)
press_before = 0
while True:
    try:
        lcd.i2c.bus.read_byte_data(lcd.i2c.address,lcd.MCP23017_GPIOA)
        n = lcd.buttons()
        if lcd_on and time.time() - before > 5:
            time_date = cur_time()
            fun = alarm_time(crontab,alarm)
            crontab = fun[0]
            alarm = fun[1]
            lcd_string = time_date + '\n' + alarm
            before = time.time()
        if lcd_string != lcd_string_prev:
            message_return(lcd,lcd_string)
            lcd_string_prev = lcd_string
        if colour != colour_prev:
            lcd.backlight(colours[colour])
            colour_prev = colour
        if lcd_on != lcd_on_prev:
            if lcd_on:
                time_date = cur_time()
                fun = alarm_time(crontab,alarm)
                crontab = fun[0]
                alarm = fun[1]
                lcd_string = time_date + '\n' + alarm
                message_return(lcd,lcd_string)
                colour = colour_def
                lcd.backlight(colours[colour])
            else:
                lcd.backlight(lcd.OFF)
                lcd.clear()
            lcd_on_prev = lcd_on
        if lcd_on and button_test(n) and time.time() - press_before > wait_time/4.0 and time.time() - press_before < 30:
            if n == right:
                colour = (colour + 1) % len(colours)
                press_before = time.time()
            elif n == up:
                lcd_on = not(lcd_on)
                press_before = time.time()
            elif n == down:
                new_setting = get_time()
                set_alarm(new_setting[0],new_setting[1],new_setting[2])
                fun = alarm_time(crontab,alarm)
                crontab = fun[0]
                alarm = fun[1]
                lcd_string = time_date + '\n' + alarm
                press_before = time.time()
            elif n == left:
                subprocess.call(["mpc","stop"])
                press_before = time.time()
            elif n == select:
                sleep(wait_time/2.0)
                menu = 0
                menu_prev = ''
                press_before = time.time()
                stay = True
                while stay:
                    n = lcd.buttons()
                    if menu != menu_prev:
                        menu_string = menus[menu] + ' '*(16-len(menus[menu])) + "\n" + ' '*16
                        message_return(lcd,menu_string)
                        menu_prev = menu
                    if button_test(n) and time.time() - press_before > wait_time/4.0:
                        press_before = time.time()
                        if n == right:
                            menu = (menu + 1) % len(menus)
                        elif n == left:
                            menu = (menu - 1) % len(menus)
                        elif n == up or n == down:
                            lcd_string_prev = ''
                            break
                        elif n == select:
                            if menu == 0:
                                setting = 0
                                hour = 7
                                minute = 0
                                set_string_prev = ''
                                flash = True
                                set_bef = time.time()
                                press_before = time.time()
                                on = True
                                while True:
                                    n = lcd.buttons()
                                    if time.time() - press_before > 30:
                                        stay = False
                                        break
                                    set_string = gen_setting(settings[setting],hour,minute)
                                    if set_string != set_string_prev:
                                        message_return(lcd,set_string)
                                        set_string_prev = set_string
                                    if time.time() - set_bef > 0.5:
                                        if setting == 0:
                                            lcd.write(0xC0)
                                            if flash:
                                                message_return(lcd,'  ')
                                            else:
                                                message_return(lcd,add_zero(hour))
                                        elif setting == 1:
                                            lcd.write(0xC3)
                                            if flash:
                                                message_return(lcd,'  ')
                                            else:
                                                message_return(lcd,add_zero(minute))
                                        flash = not(flash)
                                        set_bef = time.time()
                                    if button_test(n) and time.time() - press_before > wait_time/2.0:
                                        press_before = time.time()
                                        if n == select:
                                            stay = False
                                            message_return(lcd,set_string)
                                            set_alarm(hour,minute,on)
                                            lcd_string_prev = ''
                                            before -= 5
                                            sleep(wait_time/2.0)
                                            break
                                        elif n == right:
                                            message_return(lcd,set_string)
                                            setting = (setting + 1) % 2
                                        elif n == left:
                                            message_return(lcd,set_string)
                                            setting = (setting - 1) % 2
                                        elif setting == 0:
                                            if n == up:
                                                hour = (hour + 1) % 24
                                                set_string = gen_setting(settings[setting],hour,minute)
                                                message_return(lcd,set_string)
                                                flash = not(flash)
                                                set_string_prev = set_string
                                                press_before = time.time()
                                            elif n == down:
                                                hour = (hour - 1) % 24
                                                set_string = gen_setting(settings[setting],hour,minute)
                                                message_return(lcd,set_string)
                                                flash = not(flash)
                                                set_string_prev = set_string
                                                press_before = time.time()
                                        elif setting == 1:
                                            if n == up:
                                                minute = (minute + 5) % 60
                                                set_string = gen_setting(settings[setting],hour,minute)
                                                message_return(lcd,set_string)
                                                flash = not(flash)
                                                set_string_prev = set_string
                                                press_before = time.time()
                                            elif n == down:
                                                minute = (minute - 5) % 60
                                                set_string = gen_setting(settings[setting],hour,minute)
                                                message_return(lcd,set_string)
                                                flash = not(flash)
                                                set_string_prev = set_string
                                                press_before = time.time()
                                        sleep(0.1)
                                    n = 0
                    n = 0
            n = 0
        elif lcd_on and time.time() - press_before > 30 and n == up:
            press_before = time.time()
            n=0
        elif not(lcd_on) and n == up and time.time() - press_before > wait_time/4.0:
            lcd_on = not(lcd_on)
            press_before = time.time()
            n = 0
        sleep(0.1)
    except:
        print >> sys.stderr, "There is something wrong with the screen, hopefully it hasn't broken.", datetime.datetime.now().hour, datetime.datetime.now().minute
        count = True
        sleep(5)
        subprocess.call(["sh","/home/pi/detect_screen.sh"])
        while True:
            try:
                lcd.i2c.bus.read_byte_data(lcd.i2c.address,lcd.MCP23017_GPIOA)
                break
            except:
                if count:
                    count = not(count)
                    print >> sys.stderr, "I can't access the screen yet."
                else:
                    pass
                sleep(10)
        lcd = Adafruit_CharLCDPlate()
        if lcd_on:
            lcd.backlight(colours[colour])
        else:
            lcd.backlight(lcd.OFF)
            lcd.clear()
        lcd_string_prev = ''
        print >> sys.stderr, "I've accessed the screen, hopefully it will work now."
