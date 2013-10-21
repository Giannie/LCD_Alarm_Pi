#!/usr/bin/python

from crontab import CronTab
import sys
cron = CronTab('pi')
job = cron.find_comment('Alarm')[0]

info = []

for line in sys.stdin:
    line = line.replace('\n','')
    info.append(line)

hour = int(info[0])
minute = int(info[1])

if str(hour) != str(job.hour) or str(minute) != str(job.minute):
    job.clear()
    job.hour.on(hour)
    job.minute.on(minute)

if info[2] == "on":
    job.enable()
elif info[2] == "off":
    job.enable(False)

cron.write()