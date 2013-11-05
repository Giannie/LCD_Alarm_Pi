#!/bin/bash

sudo cp LCD_Alarm_Pi/wifi/interfaces.txt /etc/network/interfaces
sudo chown root:root /etc/network/interfaces
sudo chmod 644 /etc/network/interfaces

sudo cp LCD_Alarm_Pi/wifi/supplicant.txt /etc/wpa_supplicant/wpa_supplicant.conf
sudo chown root:root /etc/wpa_supplicant/interfaces
sudo chmod 600 /etc/wpa_supplicant/wpa_supplicant.conf

echo "Add SSID and Password to /etc/wpa_supplicant/wpa_supplicant.conf"
