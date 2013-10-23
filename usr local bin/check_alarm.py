#!/usr/bin/python

from crontab import CronTab
cron = CronTab('pi')
job = cron.find_comment('Alarm')[0]

hour = str(job.hour)
minute = str(job.minute)
if job.is_enabled():
	on = 'on'
else:
	on = 'off'

print hour
print minute
print on