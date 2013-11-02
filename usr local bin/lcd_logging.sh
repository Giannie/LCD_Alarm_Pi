#!/bin/bash

cat /home/pi/logs/lcd/lcd_error.log > /home/pi/logs/lcd/lcd_error.log1
cat /home/pi/logs/lcd/out_lcd.log > /home/pi/logs/lcd/out_lcd.log1
service lcd_start.sh restart