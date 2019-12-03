
# this is a class represents the arm
#

from servo import Servo as servo
from time import sleep
from machine import Pin


# class as a struct for joint names
#
class Joints():
    base = 0 
    lower_elbow = 1
    higher_elbow = 2
    mid_arm = 3
    wrist = 4
    
    
    
# this is The arm class
#
class Arm():

    # initiate used variables
    #
    
    # connections
    #
    TX_PIN = 16
    RX_PIN = 17
    SUCTION_PIN= 33
    DROP_ANGLES = [1.87, 145, 47.62, 10, 103.38]

    
    # objects
    #
    CONNECTION = servo(TX_PIN, RX_PIN)
    JOINTS = Joints()
    SUCTION = Pin(SUCTION_PIN, Pin.OUT) 

    #
    #
    def __init__(self):
        sleep(0.5)
        self.IDLE()
    
    
    #
    #
    def IDLE(self):
       self.drop()

        
    # TODO: reorder joint movements 
    #
    def moveJoints(self, angles=[]):
        pass        
        # if no angles ware passed set to IDLE
        # 
        if len(angles) == 0:
            self.IDLE()
            return
        
        # send each joint the corresbonding angle
        # 
        for (id,angle) in enumerate(angles):
            position = self.conv_angle(angle)
            self.CONNECTION.move(ID=id, position=position, time=500)
            sleep(0.5)
            
        return 1
            
    
    
    # this function converts angles to possitoins 
    #
    def conv_angle(self, angle):
        CONV = .240
        pos = angle / .240
        return int(pos)
   

    # turn on the suction cup  
    #
    def pick(self, angles):
        
        # move the middle joint to make the suction on top of the mushrom
        #
        
        # turn on the pump
        #
        self.SUCTION.value(0)

        # move elevate arm to z=10.5
        #
        self.moveJoints(angles=angles)


    # move to drop basket and turn off the suction cup
    #
    def drop(self):
        
        # move the arm to go on top of the basket
        #   
        self.moveJoints(self.DROP_ANGLES)
        
        # turn off suction
        #
        self.SUCTION.value(1)

    

    # this method was for demo purposes in the first presentation
    #
    def demo(self):
        self.CONNECTION.move(self.JOINTS.higher_elbow, 0, 500)
        self.CONNECTION.move(self.JOINTS.mid_arm, 600,  500)
        self.CONNECTION.move(self.JOINTS.wrist, 700, 500)
        self.CONNECTION.move(self.JOINTS.base, 1000, 500)
        sleep(1)
        self.CONNECTION.move(self.JOINTS.base, 600, 500)
        sleep(1)
        
        self.IDLE()
        sleep(2)

        self.CONNECTION.move(self.JOINTS.higher_elbow, 300, 500)
        self.CONNECTION.move(self.JOINTS.mid_arm, 500,  500)
        self.CONNECTION.move(self.JOINTS.wrist, 500, 500)
        self.CONNECTION.move(self.JOINTS.base, 1000, 500)
        sleep(1)
        self.CONNECTION.move(self.JOINTS.base, 600, 500)
        sleep(1)
        
        self.IDLE()
        sleep(2)
        
        self.CONNECTION.move(self.JOINTS.lower_elbow, 350, 500)
        self.CONNECTION.move(self.JOINTS.higher_elbow, 150, 500)
        self.CONNECTION.move(self.JOINTS.mid_arm, 830,  500)
        self.CONNECTION.move(self.JOINTS.wrist, 550, 500)
        self.CONNECTION.move(self.JOINTS.base, 1000, 500)
        sleep(1)
        self.CONNECTION.move(self.JOINTS.base, 600, 500)
        sleep(1)
        
        self.IDLE()  
        sleep(2)

        
        
    
