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
sleep 3600
string="$(mpc | grep playing)"
if [ "$string" ]; then
	mpc idle
fi
mpc random off
mpc stop
mpc clear
/usr/local/bin/plug_off.sh
/usr/local/bin/plug_off.sh