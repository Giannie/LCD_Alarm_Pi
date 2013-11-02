#!/usr/bin/python

import datetime
import subprocess
from crontab import CronTab
from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

def button_test(n):
    if n in [1,2,4,8,16]:
        return True
    else:
        return False

def gen_setting(setting,hour,minute):
    set_string = setting + ' '*(16 - len(setting)) + '\n' + add_zero(hour) + ':' + add_zero(minute) + " "*11
    return set_string

def message_return(lcd,string):
    lcd.message(string)
    lcd.write(0x80)

def get_time():
    cron = CronTab('pi')
    job = cron.find_comment('Alarm')[0]
    alarm_hour = int(str(job.hour))
    alarm_min = int(str(job.minute))
    return [alarm_hour,alarm_min,not(job.is_enabled())]

def add_zero(time):
    if int(time) < 10:
            return "0" + str(time)
    else:
            return str(time)

def cur_time():
    weekdays = ['MON','TUE','WED','THU','FRI','SAT','SUN']
    now = datetime.datetime.now()
    
    current_hour = add_zero(str(now.hour))
    current_min = add_zero(str(now.minute))
    current_day = add_zero(str(now.day))
    current_mon = add_zero(str(now.month))

    dow = weekdays[now.weekday()]
    
    current_time = current_hour + ":" + current_min
    current_date = dow + ' ' + current_day + "/" + current_mon
    
    line1 = current_time + ' '*(16-len(current_time+current_date)) + current_date
    
    return line1


def alarm_time(crontab,line2):
    proc = subprocess.Popen(['crontab','-lu','pi'],stdout=subprocess.PIPE)
    output = proc.stdout.read()
    if output == crontab:
            return [output,line2]
    else:
            now = datetime.datetime.now()
            cron = CronTab('pi')
            job = cron.find_comment('Alarm')[0]
    
            current_hour = add_zero(str(now.hour))
            current_min = add_zero(str(now.minute))
            current_day = add_zero(str(now.day))
            current_mon = add_zero(str(now.month))
    
            alarm_hour = add_zero(str(job.hour))
            alarm_min = add_zero(str(job.minute))
            alarm_on = job.is_enabled
    
            alarm_time = alarm_hour + ':' + alarm_min
    
            current_time = current_hour + ":" + current_min
            current_date = current_day + "/" + current_mon
    
            line1 = current_time + ' '*(16-len(current_time+current_date)) + current_date
    
            if job.is_enabled():
                    line2 = "Alarm: " + alarm_time
            else:
                    line2 = "Alarm off"
    
            line2 = line2 + ' '*(16-len(line2))
    
            lcd_string = line1 + '\n' + line2
    
            return [output,line2]
	
def set_alarm(hour,minute,on):
    cron = CronTab('pi')
    job = cron.find_comment('Alarm')[0]
    
    job.clear()
    job.hour.on(hour)
    job.minute.on(minute)
    if on:
            job.enable()
    else:
            job.enable(False)
    cron.write()
    return

