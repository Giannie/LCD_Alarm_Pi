#!/bin/sh

if [ "$(pwd)" != "/home/pi" ]; then
        echo "Run script from home directory"
        exit 0
fi
if [ -z "$(crontab -l | grep Alarm)" ]; then
	line="# 0 7 * * * sh /usr/local/bin/alarmcron.sh > ~/cron.txt # Alarm"
	(crontab -l; echo "$line" ) | crontab -
fi
sudo modprobe i2c-bcm2708 
sudo modprobe i2c-dev
sudo sh -c "echo i2c-bcm2708 >> /etc/modules"
sudo sh -c "echo i2c-dev >> /etc/modules"
sudo apt-get install mpd mpc python-dev python-rpi.gpio python-pip python-smbus i2c-tools
sudo pip install python-crontab
sudo pip install wiringpi
git clone https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code
git clone https://github.com/dmcg/raspberry-strogonanoff
mkdir logs
mkdir logs/lcd
mkdir logs/cron

sudo mv /home/pi/LCD_Alarm_Pi/etc\ init.d/* /etc/init.d/
mv /home/pi/LCD_Alarm_Pi/home/* /home/pi
mv /home/pi/LCD_Alarm_Pi/LCD/* /home/pi/Adafruit-Raspberry-Pi-Python-Code/Adafruit_CharLCDPlate
sudo mv /home/pi/LCD_Alarm_Pi/usr\ local\ bin/* /usr/local/bin/
sudo mv /home/pi/LCD_Alarm_Pi/etc/* /etc
sudo update-rc.d lcd_start.sh defaults 100

sudo sh -c "echo \"//192.168.0.18/devices /mnt/raspbmc cifs credentials=/home/pi/.raspbmc_auth,nofail\" >> /etc/fstab"
echo "Enter samba password:"
read pass
printf username=pi'\n'password=$pass > .raspbmc_auth
sudo mount -a
sudo service lcd_start.sh start