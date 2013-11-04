#!/bin/bash

if [ "$(pwd)" != "/home/pi" ]; then
        echo "Run script from home directory"
        exit 0
fi
if [ -z "$(crontab -l | grep Alarm)" ]; then
	line="# 0 7 * * * sh /usr/local/bin/alarmcron.sh > ~/cron.txt # Alarm"
	(crontab -l; echo "$line" ) | crontab -
fi
if [ -z "$(crontab -l | grep "LCD Logging")" ]; then
	line="0 17 * * 0 sudo /usr/local/bin/lcd_logging.sh # LCD Logging"
	(crontab -l; echo "$line" ) | crontab -
fi
if [ -z "$(crontab -l | grep "Check WiFi")" ]; then
	line="* * * * * sudo /usr/local/bin/check-wifi.sh # Check WiFi"
	(crontab -l; echo "$line" ) | crontab -
fi
sudo modprobe i2c-bcm2708 
sudo modprobe i2c-dev
if [ -z "$(grep i2c-bcm2708 /etc/modules)" ]; then
	sudo sh -c "echo i2c-bcm2708 >> /etc/modules"
fi
if [ -z "$(grep i2c-dev /etc/modules)" ]; then
	sudo sh -c "echo i2c-dev >> /etc/modules"
fi
sudo apt-get install mpd mpc python-dev python-rpi.gpio python-pip python-smbus i2c-tools
sudo pip install python-crontab
sudo pip install wiringpi
git clone https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code
git clone https://github.com/dmcg/raspberry-strogonanoff
mkdir logs
mkdir logs/lcd
mkdir logs/cron

cp /home/pi/LCD_Alarm_Pi/LCD/* /home/pi/Adafruit-Raspberry-Pi-Python-Code/Adafruit_CharLCDPlate
# sudo cp /home/pi/LCD_Alarm_Pi/etc\ logrotate.d/* /etc/logrotate.d/
sudo cp /home/pi/LCD_Alarm_Pi/etc\ init.d/* /etc/init.d/
sudo cp /home/pi/LCD_Alarm_Pi/usr\ local\ bin/* /usr/local/bin/
sudo cp /home/pi/LCD_Alarm_Pi/etc/* /etc
sudo update-rc.d lcd_start.sh defaults 100

sudo chown mpd /etc/mpd.conf
sudo chgrp audio /etc/mpd.conf

sudo mkdir /mnt/raspbmc
if [ -z "$(grep "192.168.0.18/devices /mnt/raspbmc" /etc/fstab)" ]; then
	sudo sh -c "echo \"//192.168.0.18/devices /mnt/raspbmc cifs credentials=/home/pi/.raspbmc_auth,nofail,nolock,uid=1000,gid=1000 0 0\" >> /etc/fstab"
fi
a="$(grep password .raspbmc_auth)"
if [ ${#a} -lt 10 ]; then
	echo "Enter samba password:"
	read -s pass
	printf username=pi'\n'password=$pass > .raspbmc_auth
fi
sudo service rpcbind start
sudo update-rc.d rpcbind defaults
sudo mount -a
sudo service lcd_start.sh restart
sudo service mpd restart