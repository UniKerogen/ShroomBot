####HELP####
#store to usb
#https://www.raspberrypi.org/forums/viewtopic.php?t=51967
#
#raspistill
#https://www.raspberrypi.org/documentation/usage/camera/raspicam/raspistill.md
#
#push button
#https://www.instructables.com/id/Raspberry-Pi-Tutorial-How-to-Use-Push-Button/

import RPi.GPIO  as GPIO
import os
from time import sleep, gmtime, strftime
#from picamera import PiCamera

##GPIO setup
##
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

##Old Camera setup
##
#camera = PiCamera()
##Camera resolution
#camera.resolution = (,)


##Variables
##
Button = 23
LED = 24
GPIO.setup(Button, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(LED,GPIO.OUT)

##Functions
def button_press():
    take_picture()


def take_picture():
    usb_mount()
#    output = strftime("/mnt/images/image-%d-%m %H:%M:%S.jpg",gmtime())

#    output = strftime("/home/pi/pics/image-%d-%m %H:%M:%S.jpg",gmtime())
#    output = strftime("/boot/image-%d-%m %H:%M:%S.jpg",gmtime())
    print("Taking picture!")
#    camera.capture(output)
#    print("Moving Image!")
    os.system("sudo raspistill -o /mnt/images/$(date +""%Y-%m-%d_%H%M%S"").jpg")


def usb_mount():
    try:
        os.system("sudo fdisk -l")
        os.system("sudo touch /mnt/images/")
        os.system("sudo mount /dev/sda1 /mnt/images")
        print("USB mounted")
    except:
        print("USB not mounted")



def usb_unmount():
    print("Unmounting USB")
    os.system("sudo umount /dev/sda1")

##Main Code
while True:

    button_state = GPIO.input(Button)
    if button_state == 0:
        GPIO.output(LED,GPIO.HIGH)
        button_press()
    else:
        GPIO.output(LED,GPIO.LOW)
        sleep(1)
usb_unmount()
