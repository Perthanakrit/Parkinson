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
        port='/dev/ttyUSB0',
        baudrate = 115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

df = pd.read_csv('trainDataTest.csv')
x = df[['x1', 'y1', 'z1', 'x2', 'y2', 'z2']]
y = df['par_state']
model = svm.SVC(kernel = 'linear')
model.fit(x,y)

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
    dt = datetime.now()
    num += 1
    if(num >= 10):
        running = False
    
    x=ser.readline()
    #print(x)
    #print(type(x))
    strX = x.decode('UTF-8') 
    #print(type(strX))
    #print('string is',strX)
    strX = strX.replace("\r\n", "")
    #print(strX)

    listX = strX.split('_')
    #listX[2] = listX[2].replace("\r\n", "")
    #print(type(listX))
    #print(listX)

    '''x1 = accelerometer.acceleration[0]
    y1 = accelerometer.acceleration[1]
    z1 = accelerometer.acceleration[2]'''
    x1 = accelerometer.acceleration[0]
    y1 = accelerometer.acceleration[1]
    z1 = accelerometer.acceleration[2]
    x2 = float(listX[0])
    y2 = float(listX[1])
    z2 = float(listX[2])
    

    groveData = []
    groveData.append(x1)
    groveData.append(y1)
    groveData.append(z1)
    groveData.append(x2)
    groveData.append(y2)
    groveData.append(z2)
    groveData.append('normal')
    groveData.append(dt)

    print(groveData)
    time.sleep(1)

    with open('trainData_normal.csv', 'a', newline='') as f_object:  
            # Pass the CSV  file object to the writer() function
            writer_object = writer(f_object)
            # Result - a writer object
            # Pass the data in the list as an argument into the writerow() function
            writer_object.writerow(groveData)  
            # Close the file object
            f_object.close()
    
    answer = model.predict([[x1, y1, z1, x2, y2, z2]])
    answerStr = answer[0]
    print(answerStr)

    answerTest.append(answer[0])
    if answer[0] == 'par':
        numtest1 += 1
    elif answer[0] == 'normal':
        numtest2 += 1
    #line notify
if numtest1 >= 3:
    t = requests.post(url, headers=headers, data = {'message':par})
    print(t.text)
else:
    f = requests.post(url, headers=headers, data = {'message':normal})
    print(f.text)
