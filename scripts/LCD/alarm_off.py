from crontab import CronTab

cron = CronTab('pi')
job = cron.find_comment('Alarm')[0]

job.enable(False)

cron.write()
