import time
import sys
import urllib.request as ur
import os

EMULATE_HX711=False

result = ur.urlopen('http://192.124.20.184/iot/updateDrink.php?drinkPos=1&nowWeight=0')
result = ur.urlopen('http://192.124.20.184/iot/updateDrink.php?drinkPos=2&nowWeight=0')

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
        
    print("Bye!")
    sys.exit()

hx = HX711(5, 6)   
hx_2= HX711(12,13) 

hx.set_reading_format("MSB", "MSB")
hx_2.set_reading_format("MSB", "MSB")


hx.set_reference_unit(2031)
hx_2.set_reference_unit(433)

hx.reset()
hx_2.reset()

hx.tare()
hx_2.tare()

#start
print("Tare done! Add weight now...")
val_org = val_org_2 = -1
val = val_2 = -1
weight =  weight_2 = 0

#get origin num
val_org = max(0,int(hx.get_weight(1)))
val_org_2 = max(0,int(hx_2.get_weight(5)))
print('Zero it! val_org=' + str(val_org) +','+str(val_org_2))
time.sleep(1)
val = max(0,int(hx.get_weight(1)))
val_2 = max(0,int(hx_2.get_weight(5)))
time.sleep(1)

def get_weight_1():
    global val, val_org, weight

    val = max(0,int(hx.get_weight(1)))
    time.sleep(1)
    val = max(0,int(hx.get_weight(1)))
    if val_org > 0 and val < 10 :
        print("NO.1 take")
        weight = val
        result = ur.urlopen('http://192.124.20.184/iot/updateDrink.php?drinkPos=1&nowWeight=0')
    elif val_org == 0 and val >= 10 :
        weight = val
        print('NO.1 put, weight =' + str(weight))
        result = ur.urlopen('http://192.124.20.184/iot/updateDrink.php?drinkPos=1&nowWeight='+str(weight))
    
    val_org = val

    hx.power_down()
    hx.power_up()
    time.sleep(1)

def get_weight_2():
    global val_2, val_org_2, weight_2
    
    val_2 = max(0,int(hx_2.get_weight(5)))
    time.sleep(1)
    val_2 = max(0,int(hx_2.get_weight(5)))
    print('val_org2 ='+ str(val_org)+'val2='+str(val_2))
    if val_org_2 > 0 and val_2 < 10 :
        print("NO.2 take")
        weight_2 = val_2
        result = ur.urlopen('http://192.124.20.184/iot/updateDrink.php?drinkPos=2&nowWeight=0')
    elif val_org_2 == 0 and val_2 >= 10 :
        weight_2 = val_2
        print('NO.2 put, weight2 =' + str(weight_2))
        result = ur.urlopen('http://192.124.20.184/iot/updateDrink.php?drinkPos=2&nowWeight='+str(weight_2))

    val_org_2 = val_2

    hx_2.power_down()
    hx_2.power_up()
    time.sleep(1)

while True:
    try:
        get_weight_1()
        get_weight_2()

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
