from arm import Arm
from time import sleep
import math


arm = Arm()
sleep(1)

def move(angles=[]):



    # if angle > 240 set to 240
    # if angle < 0 take the abs(angle) 
    #
    for (i, angle) in enumerate(angles):
        if angles[i] < 0:
            angles[i] = abs(angle)
        
        if angle > 240:
            angles[i] = 240
            
        print("{}th angle is {}".format(i, angles[i]))
        
    arm.moveJoints(angles)




