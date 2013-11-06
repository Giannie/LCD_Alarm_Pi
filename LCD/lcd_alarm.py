#!/usr/bin/python

from time import sleep
import time
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from alarm_time import *
import subprocess
import os
import sys
import string
import BBC_playlist

select = 1
right = 2
down = 4
up = 8
left = 16

FNULL = open(os.devnull, 'w')

lcd = Adafruit_CharLCDPlate()

lcd_string_prev = ''
wait_time = 1
alph = list(string.ascii_uppercase)
alph.append("Other")
type_choice = ["Artist","Playlist"]
ip_settings = ["Wifi","Ethernet"]
settings = ["Set hour:","Set minute:", "On or Off?"]
mpc_settings = ["Play","Pause","Stop","Next","Prev","Sleep","Cancel Sleep","Load"]
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
lcd_string = alarm_time(crontab,alarm)
press_before = 0
mpc = False
while True:
    try:
        lcd.i2c.bus.read_byte_data(lcd.i2c.address,lcd.MCP23017_GPIOA)
        n = lcd.buttons()
        if lcd_on and mpc:
            mpc_string_prev = ''
            mpc_setting = 0
            while mpc:
                n = lcd.buttons()
                mpc_string = mpc_settings[mpc_setting] + ' '*(16 - len(mpc_settings[mpc_setting])) + '\n' + ' '*16
                if mpc_string != mpc_string_prev:
                    message_return(lcd,mpc_string)
                    mpc_string_prev = mpc_string
                if time.time() - press_before > 30:
                    mpc = False
                    lcd_string_prev = ''
                    break
                elif button_test(n) and time.time() - press_before > wait_time/2.0:
                    press_before = time.time()
                    if n == up:
                        mpc_setting = (mpc_setting + 1) % len(mpc_settings)
                    elif n == down:
                        mpc_setting = (mpc_setting - 1) % len(mpc_settings)
                    elif n == left or n == right:
                        mpc = False
                        lcd_string_prev = ''
                        n = 0
                        break
                    elif n == select and mpc_setting < 5:
                        subprocess.call(["mpc",mpc_settings[mpc_setting].lower()])
                        if mpc_settings[mpc_setting].lower() == "stop":
                            subprocess.call(["mpc","clear"])
                        lcd_string_prev = ''
                        mpc = False
                        n = 0
                    elif n == select and mpc_setting == 5:
                        n = 0
                        sleep_time = 0
                        sleep_string_prev = ''
                        line1 = "Sleep after"
                        while True:
                            n = lcd.buttons()
                            sleep_string = line1 + ' '*(16-len(line1)) + '\n' + str(sleep_time) + " minutes" + ' '*(16 - len(str(sleep_time) + " minutes"))
                            if sleep_string != sleep_string_prev:
                                message_return(lcd,sleep_string)
                                sleep_string_prev = sleep_string
                            if time.time() - press_before > 30:
                                mpc = False
                                lcd_string_prev = ''
                                break
                            elif button_test(n) and time.time() - press_before > wait_time/2.0:
                                press_before = time.time()
                                if n == up:
                                    sleep_time += 5
                                elif n == down:
                                    sleep_time -= 5
                                elif n == select:
                                    if sleep_time != 0:
                                        subprocess.Popen(["/usr/local/bin/music_sleep.sh",str(60*sleep_time)])
                                    mpc = False
                                    lcd_string_prev = ''
                                    break
                            sleep(0.1)
                            n = 0
                    elif n == select and mpc_setting == 6:
                        mpc = False
                        lcd_string_prev = ''
                        n=0
                        proc = subprocess.Popen(["pgrep","-f","sleep"], stdout=subprocess.PIPE)
                        output = proc.stdout.read()
                        output = output.replace('\n',' ')[:-1]
                        output = output.split(' ')
                        command = ["kill"] + output
                        subprocess.call(command)
                    elif n == select and mpc_setting == 7:
                        stay = True
                        n = 0
                        type_set = 0
                        type_set_prev = ''
                        line1 = "Media Type:"
                        while stay:
                            n = lcd.buttons()
                            if type_set != type_set_prev:
                                type_string = line1 + ' '*(16 - len(line1)) + '\n' + type_choice[type_set] + ' '*(16 - len(type_choice[type_set]))
                                message_return(lcd,type_string)
                                type_set_prev = type_set
                            if time.time() - press_before > 30:
                                stay = False
                                mpc = False
                                break
                            elif button_test(n) and time.time() - press_before > wait_time/2.0:
                                press_before = time.time()
                                if n == up:
                                    type_set = (type_set + 1) % len(type_choice)
                                elif n == down:
                                    type_set = (type_set - 1) % len(type_choice)
                                elif n == left or n == right:
                                    lcd_string_prev = ''
                                    stay = False
                                    mpc = False
                                    break
                                elif n == select:
                                    if type_set == 1:
                                        n = 0
                                        play_set = 0
                                        play_set_prev = ''
                                        line1 = "Choose Playlist:"
                                        playlists = mpc_playlists()
                                        while True:
                                            n = lcd.buttons()
                                            if play_set != play_set_prev:
                                                play_string = line1 + ' '*(16 - len(line1)) + '\n' + playlists[play_set] + ' '*(16 - len(playlists[play_set]))
                                                message_return(lcd,play_string)
                                                play_set_prev = play_set
                                            if time.time() - press_before > 30:
                                                stay = False
                                                mpc = False
                                                break
                                            elif button_test(n) and time.time() - press_before > wait_time/2.0:
                                                press_before = time.time()
                                                if n == up:
                                                    play_set = (play_set + 1) % len(playlists)
                                                elif n == down:
                                                    play_set = (play_set - 1) % len(playlists)
                                                elif n == right or n == left:
                                                    stay = False
                                                    mpc = False
                                                    lcd_string_prev = ''
                                                    break
                                                elif n == select:
                                                    if playlists[play_set][0:3] == "BBC":
                                                        BBC_playlist.generate()
                                                        subprocess.call("cp /home/pi/radio/* /var/lib/mpd/playlists",shell=True)
                                                        subprocess.call("chown mpd:audio /var/lib/mpd/playlists/BBC*",shell=True)
                                                    mpc_load(playlists[play_set])
                                                    mpc_play()
                                                    stay = False
                                                    mpc = False
                                                    lcd_string_prev = ''
                                                    break
                                            n = 0
                                            sleep(0.1)
                                    elif type_set == 0:
                                        n = 0
                                        let_set = 0
                                        let_set_prev = ''
                                        line1 = "First letter:"
                                        stay_again = True
                                        while stay_again:
                                            n = lcd.buttons()
                                            if let_set != let_set_prev:
                                                let_string = message_gen(line1,alph[let_set])
                                                let_set_prev = let_set
                                                message_return(lcd,let_string)
                                            if time.time() - press_before > 30:
                                                stay = False
                                                mpc = False
                                                stay_again = False
                                                lcd_string_prev = ''
                                                break
                                            elif button_test(n) and time.time() - press_before > wait_time/2.0:
                                                press_before = time.time()
                                                if n == up:
                                                    let_set = (let_set + 1) % len(alph)
                                                elif n == down:
                                                    let_set = (let_set - 1) % len(alph)
                                                elif n == left or n == right:
                                                    stay = False
                                                    mpc = False
                                                    stay_again = False
                                                    lcd_string_prev = ''
                                                    n = 0
                                                    break
                                                elif n == select:
                                                    n = 0
                                                    art_set = 0
                                                    art_set_prev = ''
                                                    line1 = "Choose artist:"
                                                    artists = mpc_artists()[let_set]
                                                    stay3 = True
                                                    while stay3:
                                                        n = lcd.buttons()
                                                        if art_set != art_set_prev:
                                                            art_string = message_gen(line1,artists[art_set])
                                                            message_return(lcd,art_string)
                                                            art_set_prev = art_set
                                                        if time.time() - press_before > 30:
                                                            stay = False
                                                            mpc = False
                                                            stay_again = False
                                                            stay3 = False
                                                            lcd_string_prev = ''
                                                            n = 0
                                                            break
                                                        elif button_test(n) and time.time() - press_before > wait_time/2.0:
                                                            press_before = time.time()
                                                            if n == up:
                                                                art_set = (art_set + 1) % len(artists)
                                                            elif n == down:
                                                                art_set = (art_set - 1) % len(artists)
                                                            elif n == right or n == left:
                                                                stay = False
                                                                mpc = False
                                                                stay_again = False
                                                                stay3 = False
                                                                lcd_string_prev = ''
                                                                n = 0
                                                                break
                                                            elif n == select:
                                                                n = 0
                                                                alb_set = 0
                                                                alb_set_prev = ''
                                                                line1 = "Choose album:"
                                                                fun = mpc_albums(artists[art_set])
                                                                albums = fun[0]
                                                                paths = fun[1]
                                                                while True:
                                                                    n = lcd.buttons()
                                                                    if alb_set != alb_set_prev:
                                                                        alb_string = message_gen(line1,albums[alb_set])
                                                                        message_return(lcd,alb_string)
                                                                        alb_set_prev = alb_set
                                                                    if time.time() - press_before > 30:
                                                                        stay = False
                                                                        mpc = False
                                                                        stay_again = False
                                                                        stay3 = False
                                                                        lcd_string_prev = ''
                                                                        n = 0
                                                                        break
                                                                    elif button_test(n) and time.time() - press_before > wait_time/2.0:
                                                                        press_before = time.time()
                                                                        if n == up:
                                                                            alb_set = (alb_set + 1) % len(albums)
                                                                        elif n == down:
                                                                            alb_set = (alb_set - 1) % len(albums)
                                                                        elif n == left or n == right:
                                                                            stay = False
                                                                            mpc = False
                                                                            stay_again = False
                                                                            stay3 = False
                                                                            lcd_string_prev = ''
                                                                            n = 0
                                                                            break
                                                                        elif n == select:
                                                                            mpc_add(paths[alb_set])
                                                                            mpc_play()
                                                                            mpc = False
                                                                            stay = False
                                                                            stay_again = False
                                                                            stay3 = False
                                                                            lcd_string_prev = ''
                                                                            n = 0
                                                                            break
                                                                    n = 0
                                                                    sleep(0.1)
                                                    n = 0
                                                    sleep(0.1)
                                        n = 0
                                        sleep(0.1)
                                        
                        n = 0
                        sleep(0.1)
                    n = 0
                sleep(0.1)
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
                mpc = True
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
                            elif menu == 1:
                                setting = colour_def
                                set_string_prev = ''
                                while True:
                                    n = lcd.buttons()
                                    set_string = col_string[setting] + ' '*(16 - len(col_string[setting])) + '\n' + ' '*16
                                    if set_string != set_string_prev:
                                        message_return(lcd,set_string)
                                        lcd.backlight(colours[setting])
                                        set_string_prev = set_string
                                    if time.time() - press_before > 30:
                                        lcd_string_prev = ''
                                        stay = False
                                        break
                                    elif button_test(n) and time.time() - press_before > wait_time/2.0 and time.time() - press_before < 30:
                                        press_before = time.time()
                                        if n == up:
                                            setting = (setting + 1) % len(col_string)
                                        elif n == down:
                                            setting = (setting - 1) % len(col_string)
                                        elif n == select:
                                            colour = setting
                                            lcd_string_prev = ''
                                            stay = False
                                            break
                                    n = 0
                                    sleep(0.1)
                            elif menu == 2:
                                stay_again = True
                                setting = 0
                                set_string_prev = ''
                                while stay_again:
                                    n = lcd.buttons()
                                    set_string = pow_string[setting] + ' '*(16 - len(pow_string[setting])) + '\n' + ' '*16
                                    if set_string != set_string_prev:
                                        message_return(lcd,set_string)
                                        set_string_prev = set_string
                                    if time.time() - press_before > 30:
                                        stay = False
                                        lcd_string_prev = ''
                                        break
                                    elif button_test(n) and time.time() - press_before > wait_time/2.0:
                                        press_before = time.time()
                                        if n == up:
                                            setting = (setting + 1) % len(pow_string)
                                        elif n == down:
                                            setting = (setting - 1) % len(pow_string)
                                        elif setting == 2 and n == select:
                                            lcd_string_prev = ''
                                            stay = False
                                            break
                                        elif n == select:
                                            setting_confirm = 0
                                            set_string_prev = ''
                                            set_string = con + ' '*(16 - len(con)) + '\n' + confirm[setting_confirm] + ' '*(16-len(confirm[setting]))
                                            while True:
                                                n = lcd.buttons()
                                                set_string = con + ' '*(16 - len(con)) + '\n' + confirm[setting_confirm] + ' '*(16-len(confirm[setting]))
                                                if set_string != set_string_prev:
                                                    message_return(lcd,set_string)
                                                    set_string_prev = set_string
                                                if time.time() - press_before > 30:
                                                    stay = False
                                                    stay_again = False
                                                    lcd_string_prev = ''
                                                    break
                                                elif button_test(n) and time.time() - press_before > wait_time/2.0:
                                                    press_before = time.time()
                                                    if n == up:
                                                        setting_confirm = (setting_confirm + 1) % len(confirm)
                                                    elif n == down:
                                                        setting_confirm = (setting_confirm - 1) % len(confirm)
                                                    elif n == select and setting_confirm != 1:
                                                        if setting == 0:
                                                            subprocess.call("poweroff")
                                                        elif setting == 1:
                                                            subprocess.call("reboot")
                                                    elif n == select and setting_confirm == 1:
                                                        lcd_string_prev = ' '
                                                        stay = False
                                                        stay_again = False
                                                        break
                                                n = 0
                                                sleep(0.1)
                            elif menu == 3:
                                stay_again= True
                                ip_set = 0
                                ip_set_prev = ''
                                while stay_again:
                                    if ip_set != ip_set_prev:
                                        n = lcd.buttons()
                                        if ip_set == 0:
                                            p1 = subprocess.Popen(["ifconfig","wlan0"],stdout=subprocess.PIPE)
                                        elif ip_set == 1:
                                            p1 = subprocess.Popen(["ifconfig","eth0"],stdout=subprocess.PIPE)
                                        p2 = subprocess.Popen(["grep","inet"],stdin=p1.stdout,stdout=subprocess.PIPE)
                                        ip_addr = p2.stdout.read()
                                        if len(ip_addr) == 0:
                                            ip_addr = "Not connected"
                                        else:
                                            ip_addr = ip_addr.split(' ')
                                            ip_addr = ip_addr[11][5:]
                                        ip_str = ip_settings[ip_set] + ' '*(16 - len(ip_settings[ip_set])) + '\n' + ip_addr + ' '*(16 - len(ip_addr))
                                        message_return(lcd,ip_str)
                                    if time.time() - press_before > 30:
                                        stay = False
                                        stay_again = False
                                        lcd_string_prev = ''
                                        break
                                    elif button_test(n) and time.time() - press_before > wait_time/2.0:
                                        press_before = time.time()
                                        if n == up:
                                            ip_set = (ip_set + 1) % len(ip_settings)
                                        elif n == down:
                                            ip_set = (ip_set - 1) % len(ip_settings)
                                        elif n == select or n == left or n == right:
                                            stay = False
                                            stay_again = False
                                            lcd_string_prev = ''
                                            break
                                    n = 0
                                    sleep(0.1)
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
        subprocess.call(["sh","/usr/local/bin/detect_screen.sh"])
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



