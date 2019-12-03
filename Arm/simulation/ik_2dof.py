from math import *
from numpy import rad2deg

# length of each segments 
#
a1 = 13
a2 = 3

# the desired point 
# 
x = float(input("enter x: "))
y = float(input("enter y: "))


#
#
r = sqrt(x**2 + y**2)

phi1 = atan(y/x)
phi2 = acos((a2**2 - a1**2 - r**2)/ (-2 * a1 * r))
theta1 = phi1 -  phi2

theta1_deg = rad2deg(theta1)

#
#
phi3 = acos((r**2 - a2**2 - a1**2) / (-2 * a2 * a1))

theta2 = 180 - rad2deg(phi3)
theta2_deg = rad2deg(theta2)

# TODO: clean this make one loop or no loop do mAtH maybe
#
while(theta2_deg  > 360 or theta1_deg  > 360):
    if(theta2_deg > 360):
        theta2_deg -=  360
    elif(theta1_deg > 360):
        theta1_deg -= 360
    



# while(theta2_deg < 0 or theta1_deg  < 0):
#     if(theta2_deg < 0):
#         theta2_deg +=  360
#     elif(theta1_deg < 0):
#         theta1_deg += 360


print("theta1: {}".format(theta1_deg ))
print("theta2: {}".format(theta2_deg)) 


# add some stuff to only on the last quarter 
#
servo1_pos = abs(theta1_deg) / 0.24
servo2_pos = abs(theta2_deg) / 0.24 

if(servo1_pos > 1000):
    servo1_pos -= 500
if(servo2_pos > 1000):
    servo2_pos -= 500
    
if(servo1_pos < 500):
    servo1_pos += 500
if(servo2_pos < 500):
    servo2_pos += 500

print("first servo put: {}".format(int(servo1_pos)))
print("second servo put: {}".format(int(servo2_pos)))
