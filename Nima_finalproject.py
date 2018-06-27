import sys
import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD
from time import sleep
import time;
import pyowm
import socket
import requests
GPIO.setmode(GPIO.BCM)
GPIO.setup(22,GPIO.IN,pull_up_down=GPIO.PUD_UP) #BUTTON
onOff = 1


# instantiate lcd and specify pins
lcd = LCD.Adafruit_CharLCD(rs=26, en=19,d4=13, d5=6, d6=5, d7=11,cols=16, lines=2)
lcd.clear()


#WEATHER
owm = pyowm.OWM('e90bc58e09805e568513d0b6940275ab')
observation = owm.weather_at_place('Vancouver,ca')

lcd.clear()
lcd.message("Hi, Click me!")
try:
    while True:
        input_state = GPIO.input(22)
        if input_state==False:
            sleep(1)
            
            if onOff == 1:              #TIME AND DATE
                for x in range(0, 16):
                    lcd.move_right()
                    sleep(.1)      
                lcd.clear()
                for x in range(0, 16):
                    lcd.move_right()                
                ts = time.localtime()
                theTime = (time.strftime("%Y-%m-%d\n%I:%M %p", ts))
                lcd.message(theTime)
                sleep(1)
                for x in range(0, 16):
                    lcd.move_left()
                    sleep(.1)
                print(onOff)
            elif onOff == 2:            #Weather
                for x in range(0, 16):
                    lcd.move_right()
                    sleep(.1)
                lcd.clear()
                for x in range(0, 16):
                    lcd.move_right() 
                w = observation.get_weather()
                wTemp = str(w.get_temperature('celsius'))
                wTempArray = wTemp.split(",")
                wTempMsg = wTempArray[0].strip("{}").replace("'", "")
                wDetail = str(w.get_status())
                wMsg = (wTempMsg.strip() +" C\n"+wDetail)
                lcd.message(wMsg)
                sleep(1) 
                for x in range(0, 16):
                    lcd.move_left()
                    sleep(.1)                
                print(onOff)
            else:                       #IP-ADDRESSES
                for x in range(0, 16):
                    lcd.move_right()
                    sleep(.1)
                lcd.clear()
                for x in range(0, 16):
                    lcd.move_right()
                localIP = socket.gethostbyname(socket.gethostname())
                globalIP = requests.get('http://ip.42.pl/raw').text
                ip = (localIP + "\n" + globalIP)
                lcd.message(ip)
                sleep(1) 
                for x in range(0, 16):
                    lcd.move_left()
                    sleep(.1)                
                print(onOff)
                onOff=0
            onOff+=1
except KeyboardInterrupt:
    GPIO.cleanup()
finally:
    lcd.clear()
