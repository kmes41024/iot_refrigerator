import Adafruit_DHT
import RPi.GPIO as GPIO
import urllib.request as ur
import time

sensor = Adafruit_DHT.DHT22

pin = 27        
flag = 0
orignalTemp = 0

GPIO.setmode(GPIO.BOARD)
BUZZ_PIN = 36
GPIO.setup(BUZZ_PIN, GPIO.OUT)
pwm_B=GPIO.PWM(BUZZ_PIN, 50)
pwm_B.start(0)

result = ur.urlopen('http://192.124.20.184/iot/updateTemperature.php?isHot=0')

def warn():
    global orignalTemp, flag
    print('warn')
    pwm_B.ChangeDutyCycle(100)
    pwm_B.start(50)
    pwm_B.ChangeFrequency(262)
    time.sleep(20)
    orignalTemp = 0
    flag = 0

while True:
    hu, temp = Adafruit_DHT.read_retry(sensor, pin)
    print("Temp={0:0.2f}".format(temp))
    if temp is not None and flag == 0:
        if temp > 15.0:
            orignalTemp = temp
            flag = 1
            print("Original-Temp={0:0.2f}".format(orignalTemp))
            result = ur.urlopen('http://192.124.20.184/iot/updateTemperature.php?isHot=0')
    elif temp is not None and flag == 1:
        if temp - orignalTemp > 0.2:
            warn()
            result = ur.urlopen('http://192.124.20.184/iot/updateTemperature.php?isHot=1')
        elif temp - orignalTemp <= 0.2:
            pwm_B.stop()
GPIO.cleanup()
