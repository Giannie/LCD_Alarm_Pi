#!/usr/bin/python

from time import sleep
import datetime
import time
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import alarm_time
import subprocess
import os
import sys
import string

select = 1
right = 2
down = 4
up = 8
left = 16

FNULL = open(os.devnull, 'w')

lcd = Adafruit_CharLCDPlate()
play_char = [0b10000,0b11000,0b11100,0b11000,0b10000,0b0,0b0,0b0]
rand_char = [0b0,0b0,0b0,0b0,0b111,0b101,0b110,0b101]
pr_char = []
arrow = [0b100,0b1110,0b11111,0b0,0b0,0b11111,0b1110,0b100]
for i in range(8):
    pr_char.append(play_char[i] | rand_char[i])

lcd.createChar(0,play_char)
lcd.createChar(1,rand_char)
lcd.createChar(2,pr_char)
lcd.createChar(3,arrow)

lcd_string_prev = ''
wait_time = 1
alph = list(string.ascii_uppercase)
alph.append("Other")
type_choice = ["Artist","Playlist"]
ip_settings = ["Wifi","Ethernet"]
settings = ["Set hour:","Set minute:"]
mpc_settings = ["Play","Pause","Stop","Next","Prev","Random","Sleep","Cancel Sleep","Load"]
menus = ["Set Alarm","Set Backlight","Power Management","IP Addresses"]
col_string = ['Red','Yellow','Green','Teal','Blue','Violet']
pow_string = ['Shutdown','Reboot','Cancel']
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
play_state_prev = ''
time_date = alarm_time.cur_time()
fun = alarm_time.alarm_time(crontab,alarm)
crontab = fun[0]
alarm = fun[1]
lcd_string = time_date + '\n' + alarm
press_before = 0
mpc = False
while True:
    while True:
#    try:
        lcd.i2c.bus.read_byte_data(lcd.i2c.address,lcd.MCP23017_GPIOA)
        n = lcd.buttons()
        if lcd_on and time.time() - before > 5:
            play_state = alarm_time.check_playing()
            time_date = alarm_time.cur_time()
            fun = alarm_time.alarm_time(crontab,alarm)
            crontab = fun[0]
            alarm = fun[1]
            lcd_string = alarm_time.message_gen(time_date,alarm)
            before = time.time()
        if lcd_string != lcd_string_prev or play_state != play_state_prev:
            alarm_time.main_screen(lcd,lcd_string,play_state)
            lcd_string_prev = lcd_string
            play_state_prev = play_state
        if colour != colour_prev:
            lcd.backlight(colours[colour])
            colour_prev = colour
        if lcd_on != lcd_on_prev:
            if lcd_on:
                before = 0
                lcd_string_prev = ''
                colour = colour_def
                lcd.backlight(colours[colour])
            else:
                lcd.backlight(lcd.OFF)
                lcd.clear()
            lcd_on_prev = lcd_on
        if lcd_on and alarm_time.button_test(n) and time.time() - press_before > wait_time/4.0 and time.time() - press_before < 30:
            press_before = time.time()
            if n == right:
                alarm_time.mpc_screen(lcd)
                lcd_string_prev = ''
                before = 0
                press_before = time.time() + 0.5
            elif n == left:
                alarm_time.cur_track_screen(lcd)
                lcd_string_prev = ''
                before = 0
                press_before = time.time() + 0.5
            elif n == up:
                lcd_on = not(lcd_on)
            elif n == down:
                new_setting = alarm_time.get_time()
                alarm_time.set_alarm(new_setting[0],new_setting[1],new_setting[2])
                fun = alarm_time(crontab,alarm)
                crontab = fun[0]
                alarm = fun[1]
                lcd_string = time_date + '\n' + alarm
                press_before = time.time()
            elif n == select:
                alarm_time.main_menu(lcd,colour)
                lcd_string_prev = ''
                before = 0
                press_before = time.time() + 0.5
        elif lcd_on and time.time() - press_before > 30 and n == up:
            press_before = time.time()
        elif not(lcd_on) and n == up and time.time() - press_before > wait_time/4.0:
            lcd_on = not(lcd_on)
            press_before = time.time()
        n = 0
        sleep(0.1)
#    except:
#        now = datetime.datetime.now()
#        hour = str(now.hour)
#        minute = str(now.minute)
#        day = str(now.day)
#        month = str(now.month)
#        date_log = hour + ":" + minute + ' ' + day + "/" + month
#        print >> sys.stderr, date_log
#        print >> sys.stderr, "There is something wrong with the screen, hopefully it hasn't broken."
#        count = True
#        sleep(5)
#        subprocess.call(["sh","/usr/local/bin/detect_screen.sh"])
#        while True:
#            try:
#                lcd.i2c.bus.read_byte_data(lcd.i2c.address,lcd.MCP23017_GPIOA)
#                break
#            except:
#                if count:
#                    count = not(count)
#                    print >> sys.stderr, "I can't access the screen yet."
#                else:
#                    pass
#                sleep(10)
#        try:
#            if lcd_on:
#                lcd.backlight(colours[colour])
#            else:
#                lcd.backlight(lcd.OFF)
#                lcd.clear()
#        except:
#            pass
#        lcd_string_prev = ''
#        print >> sys.stderr, "I've accessed the screen, hopefully it will work now."
#
#
#
