#!/bin/bash

sudo mount -a
/usr/local/bin/plug_on.sh
/usr/local/bin/plug_on.sh
python ~/Adafruit-Raspberry-Pi-Python-Code/Adafruit_CharLCDPlate/alarm_off.py
mpc random on
mpc load AlarmPlaylist.m3u
sleep 5
mpc volume 80
mpc play
sleep 15
mpc volume 82
sleep 15
mpc volume 84
sleep 15
mpc volume 86
sleep 15
mpc volume 88
sleep 15
mpc volume 90
string="$(mpc | grep playing)"
if [ -z "$string" ]
    then
        mpc load AlarmPlaylist.m3u
        mpc volume 80
        mpc play
        sleep 15
        mpc volume 82
        sleep 15
        mpc volume 84
        sleep 15
        mpc volume 86
        sleep 15
        mpc volume 88
        sleep 15
        mpc volume 90
fi
sleep 240
mpc volume 85
sleep 1560
string="$(mpc | grep playing)"
if [ "$string" ]; then
	mpc idle
	mpc pause
#	sudo python /home/pi/Adafruit-Raspberry-Pi-Python-Code/Adafruit_CharLCDPlate/weather_report.py
	mpc play
fi
sleep 1800
string="$(mpc | grep playing)"
if [ "$string" ]; then
	mpc idle
fi
mpc random off
mpc stop
mpc clear
mpc volume 90
/usr/local/bin/plug_off.sh
/usr/local/bin/plug_off.sh