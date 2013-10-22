#!/usr/bin/python

from crontab import CronTab
import sys
cron = CronTab('pi')
job = cron.find_comment('Alarm')[0]

hour = int(sys.argv[1])
minute = int(sys.argv[2])

if str(hour) != str(job.hour) or str(minute) != str(job.minute):
    job.clear()
    job.hour.on(hour)
    job.minute.on(minute)

if sys.argv[3] == "on":
    job.enable()
elif sys.argv[3] == "off":
    job.enable(False)

cron.write()
