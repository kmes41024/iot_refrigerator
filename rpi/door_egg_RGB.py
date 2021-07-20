import time
import RPi.GPIO as GPIO
import os
import urllib.request as ur

GPIO.setmode(GPIO.BOARD)

LED1_G_PIN = 12
LED1_R_PIN = 18
EGG1_OUT = 16

LED2_G_PIN = 40
LED2_R_PIN = 7
EGG2_OUT = 22

TRIGGER1_PIN = 32
ECHO1_PIN = 24

TRIGGER2_PIN = 29
ECHO2_PIN = 26

BUZZ_PIN = 36
GPIO.setup(BUZZ_PIN, GPIO.OUT)
pwm_B=GPIO.PWM(BUZZ_PIN, 50)
pwm_B.start(0)

GPIO.setup(EGG1_OUT,GPIO.IN)
GPIO.setup(LED1_G_PIN, GPIO.OUT)
GPIO.output(LED1_G_PIN, GPIO.LOW)
GPIO.setup(LED1_R_PIN, GPIO.OUT)
GPIO.output(LED1_R_PIN, GPIO.LOW)

GPIO.setup(EGG2_OUT,GPIO.IN)
GPIO.setup(LED2_G_PIN, GPIO.OUT)
GPIO.output(LED2_G_PIN, GPIO.LOW)
GPIO.setup(LED2_R_PIN, GPIO.OUT)
GPIO.output(LED2_R_PIN, GPIO.LOW)

GPIO.setup(TRIGGER1_PIN, GPIO.OUT)
GPIO.setup(ECHO1_PIN, GPIO.IN)
GPIO.output(TRIGGER1_PIN, GPIO.LOW)

GPIO.setup(TRIGGER2_PIN, GPIO.OUT)
GPIO.setup(ECHO2_PIN, GPIO.IN)
GPIO.output(TRIGGER2_PIN, GPIO.LOW)

Egg1Time = 0
Egg2Time = 0

doorOpenTime = 0

result = ur.urlopen('http://192.124.20.184/iot/updateEgg.php?eggPos=1&isExpired=0&putInTime=0')
result = ur.urlopen('http://192.124.20.184/iot/updateEgg.php?eggPos=2&isExpired=0&putInTime=0')

def doorOpen1():
	GPIO.output(TRIGGER1_PIN, GPIO.HIGH)
	time.sleep(0.00001)
	GPIO.output(TRIGGER1_PIN, GPIO.LOW)
	while GPIO.input(ECHO1_PIN) == 0:
		start_time = time.time()
	while GPIO.input(ECHO1_PIN) == 1:
		end_time = time.time()
	etime = end_time - start_time
	distance = 17150 * etime
	if distance > 5.0 and distance < 500.0:
		return True
	else:
		return False
		
def doorOpen2():
	GPIO.output(TRIGGER2_PIN, GPIO.HIGH)
	time.sleep(0.00001)
	GPIO.output(TRIGGER2_PIN, GPIO.LOW)
	while GPIO.input(ECHO2_PIN) == 0:
		start_time = time.time()
	while GPIO.input(ECHO2_PIN) == 1:
		end_time = time.time()
	etime = end_time - start_time
	distance = 17150 * etime
	if distance > 5.0 and distance < 500.0:
		return True
	else:
		return False

def bright1(): #亮綠燈表示先拿 紅燈表示過期
	nowTime = time.time()
	if nowTime - Egg1Time > 30:
		GPIO.output(LED1_G_PIN,GPIO.LOW)
		GPIO.output(LED1_R_PIN,GPIO.HIGH)
		result = ur.urlopen('http://192.124.20.184/iot/updateEgg.php?eggPos=1&isExpired=1&putInTime='+str(Egg1Time))
	elif Egg1Time < Egg2Time or Egg2Time == 0:
		GPIO.output(LED1_G_PIN,GPIO.HIGH)
		GPIO.output(LED1_R_PIN,GPIO.LOW)

def bright2(): #亮綠燈表示先拿 紅燈表示過期
	nowTime = time.time()
	if nowTime - Egg2Time > 30:				#過期
		GPIO.output(LED2_G_PIN,GPIO.LOW)
		GPIO.output(LED2_R_PIN,GPIO.HIGH)
		result = ur.urlopen('http://192.124.20.184/iot/updateEgg.php?eggPos=2&isExpired=1&putInTime='+str(Egg2Time))
		#print('222')
	elif Egg2Time < Egg1Time or Egg1Time == 0:	#沒過期
		GPIO.output(LED2_G_PIN,GPIO.HIGH)
		GPIO.output(LED2_R_PIN,GPIO.LOW)


def warn():
    print('warn')
    pwm_B.ChangeDutyCycle(100)
    pwm_B.start(50)
    pwm_B.ChangeFrequency(262)   

while True:
	if doorOpen1() == True or doorOpen2() == True:			#門開
		if doorOpenTime == 0:								#記錄開門的時間
			doorOpenTime = time.time()
		elif time.time() - doorOpenTime > 10:				#判斷門是否開超過七分鐘沒關	
			warn()
		else:												#關門
			pwm_B.stop()
		
		if GPIO.input(EGG1_OUT) == 0: 			#有蛋放置
			if Egg1Time == 0:					#首次放蛋
				Egg1Time = time.time()
				result = ur.urlopen('http://192.124.20.184/iot/updateEgg.php?eggPos=1&isExpired=0&putInTime='+str(Egg1Time))
			bright1()
		else:									#沒蛋(拿走蛋)
			GPIO.output(LED1_G_PIN,GPIO.LOW)
			GPIO.output(LED1_R_PIN,GPIO.LOW)
			if Egg1Time != 0:						#拿走蛋
				result = ur.urlopen('http://192.124.20.184/iot/updateEgg.php?eggPos=1&isExpired=0&putInTime=0')
			Egg1Time = 0
			
		if GPIO.input(EGG2_OUT) == 0: 			#有蛋放置
			if Egg2Time == 0:					#首次放蛋
				Egg2Time = time.time()
				result = ur.urlopen('http://192.124.20.184/iot/updateEgg.php?eggPos=2&isExpired=0&putInTime='+str(Egg2Time))
			bright2()
		else:									#沒蛋
			GPIO.output(LED2_G_PIN,GPIO.LOW)
			GPIO.output(LED2_R_PIN,GPIO.LOW)
			if Egg2Time != 0:					#拿走蛋
				result = ur.urlopen('http://192.124.20.184/iot/updateEgg.php?eggPos=2&isExpired=0&putInTime=0')
			Egg2Time = 0
	else:
		GPIO.output(LED2_G_PIN,GPIO.LOW)
		GPIO.output(LED1_G_PIN,GPIO.LOW)
		GPIO.output(LED1_R_PIN,GPIO.LOW)
		GPIO.output(LED2_R_PIN,GPIO.LOW)
		doorOpenTime = 0
GPIO.cleanup()
