#!/bin/sh

if [ "$(pwd)" != "/home/pi" ]; then
        echo "Run script from home directory"
        exit 0
fi
if [ -z "$(crontab -l | grep Alarm)" ]; then
	line="# 0 7 * * * sh /usr/local/bin/alarmcron.sh > ~/cron.txt # Alarm"
	(crontab -l; echo "$line" ) | crontab -
fi
sudo apt-get install mpd mpc python-pip
sudo pip install python-crontab
sudo pip install wiringpi
git clone https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code
git clone https://github.com/dmcg/raspberry-strogonanoff
mkdir logs
mkdir logs/lcd
mkdir logs/cron

sudo mv /home/pi/LCD_Alarm_Pi/etc\ init.d/* /etc/init.d/
mv /home/pi/LCD_Alarm_Pi/home/* /home/pi
mv /home/pi/LCD_Alarm_Pi/LCD/* ~/Adafruit-Raspberry-Pi-Python-Code/Adafruit_CharLCDPlate
sudo mv /home/pi/LCD_Alarm_Pi/usr\ local\ bin/* /usr/local/bin/
sudo mv /home/pi/LCD_Alarm_Pi/etc/* /etc
sudo update-rc.d lcd_start.sh defaults 100

sudo sh -c "echo \"//192.168.0.18/devices /mnt/raspbmc cifs credentials=/home/pi/.raspbmc_auth,nofail\" >> /etc/fstab"