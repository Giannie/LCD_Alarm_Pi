#!/bin/sh

sudo mv etc\ init.d/* /etc/init.d/
mv home/* /home/pi
mv LCD/* ~/Adafruit-Raspberry-Pi-Python-Code/Adafruit_CharLCDPlate
sudo mv usr\ local\ bin/* /usr/local/bin/
sudo update-rc.d lcd_start.sh defaults
