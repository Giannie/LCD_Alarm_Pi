#!/bin/sh

### BEGIN INIT INFO
# Provides:          lcd_start.sh
# Required-Start:
# Required-Stop:
# Should-Start:
# Should-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: lcd_start
# Description:       Starts the LCD for the alarm
#
### END INIT INFO

start() {
	if [ -z "$(pgrep -f lcd_alarm)" ]; then
		/usr/bin/python /home/pi/Adafruit-Raspberry-Pi-Python-Code/Adafruit_CharLCDPlate/lcd_alarm.py 2>> /home/pi/logs/lcd/lcd_error.log 1>> /home/pi/logs/lcd/out_lcd.log &
	fi
	}

stop() {
	a="$(pgrep -f lcd_alarm)" 
	if [ $a ]; then
		pgrep -f lcd_alarm | while read line
			do sudo kill $line
		done
	fi
	/usr/bin/python /home/pi/Adafruit-Raspberry-Pi-Python-Code/Adafruit_CharLCDPlate/off_lcd.py
	}

case "$1" in
  start)
        start
        ;;
  stop)
        stop
        ;;
  status)
	a="$(pgrep -f lcd_alarm)"
        if [ $a ]; then
		echo "Process running as"
		echo $a
	fi
	if [ -z "$(pgrep -f lcd_alarm)" ]; then
		echo "Process not running"
	fi
        ;;
  restart|reload|condrestart)
        stop
        start
        ;;
  *)
        echo $"Usage: $0 {start|stop|restart|reload|status}"
        exit 1
esac
exit 0