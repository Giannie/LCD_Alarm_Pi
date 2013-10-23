#!/usr/bin/python

from time import sleep
import time
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from alarm_time import *
import subprocess
import os
import sys

lcd = Adafruit_CharLCDPlate()

lcd.clear()
lcd.backlight(lcd.OFF)
