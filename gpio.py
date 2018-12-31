import RPi.GPIO as GPIO
from datetime import datetime

# Initialize Relaybays => run 'pinout' on PI to see pin numbering
# physical pin numbering used
gpio_map_to_relaybay1 = [38,40] # gpio 20 and 21
gpio_map_to_relaybay2 = []
gpio_map_to_relaybay3 = []
relays = [gpio_map_to_relaybay1, gpio_map_to_relaybay2, gpio_map_to_relaybay3]

# Initialize the Raspberry Board
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# change state of a relaygroup
def change(relaygroup, mode):
    for x in relaygroup:
        GPIO.setup(x, GPIO.OUT)
        #print "Set port mode: ",x,"to OUT"
        if mode=="ON":
            GPIO.output(x,GPIO.LOW)
            #print "Set port state:",x,"HIGH"
        else:
            GPIO.output(x,GPIO.HIGH)
            #print "Set port state:",x,"LOW"

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

def set_led_on():
    change(relays[0], "ON")
    print("Turn LED on")
    f=open("ledlog.txt","a+")
    f.write("On - " + get_timestamp() + "\n")
    f.close

def set_led_off():
    change(relays[0], "OFF")
    print("Turn LED off")
    f=open("ledlog.txt","a+")
    f.write("Off - " + get_timestamp() + "\n")
    f.close

def no_set_led():
    f=open("ledlog.txt","a+")
    f.write("Wrong pass - " + get_timestamp() + "\n")
    f.close

