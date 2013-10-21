#!/bin/bash

while true
	do a="$(pgrep python)"
	b="$(ps aux | grep "$a" | grep lcd_alarm)"
	if [ -z "$b" ]
		then
		cp /home/pi/hello.txt /home/pi/hello1.txt
		sudo /etc/init.d/lcd_start.sh
	fi
	sleep 5
done
	