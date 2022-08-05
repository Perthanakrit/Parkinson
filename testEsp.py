import time
import serial
import requests

import board 
#import busio
#import adafruit_adxl34x

from csv import writer
from datetime import datetime

from sklearn import svm
import pandas as pd

#import RPi.GPIO as GPIO
from time import sleep




running = True

#i2c = busio.I2C(board.SCL, board.SDA)
#accelerometer = adafruit_adxl34x.ADXL345(i2c)
dt = datetime.now()

ser = serial.Serial(
        port='/devttyUSB5',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)


# LINE notify
'''url = 'https://notify-api.line.me/api/notify'
token = 'j5acxSlH6KOWBShpIvvXEjFcGtfWooMeiYNCotpjM4F'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}      
par = 'ตรวจพบอาการของโรค พาร์กินสัน'
normal = 'ไม่พบอารการของโรค พาร์กินสัน'''

answerTest = []

numtest1 = 0
numtest2 = 0
num = 0

while running:
    x=ser.readline().decode('utf-8')
    print(x)