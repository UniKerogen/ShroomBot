
from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
from ikpy import plot_utils
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
import math


SCALER = 10

# TODO: check length of each link could be wrong
#
arm = Chain(name="arm", links= [
    # base servo
    #
    URDFLink(
        name = "base servo",
        translation_vector = [0, 0, 0], # location 
        orientation = [ 0, 0, 0],
        rotation = [0, 0, 1],
        bounds = (math.radians(0), math.radians(192))
        # bounds = (math.radians(-192), math.radians(0))
        ),
    
    URDFLink(
        name = "elbow low",
        translation_vector = [0, 0, 0.95 * SCALER], # location
        orientation = [0, 0, 0],
        rotation = [0, 1, 0],
        bounds = (math.radians(120), math.radians(144))
        # bounds = (math.radians(-144), math.radians(36))

        ),
    
    URDFLink(
        name = "elbow hight",
        translation_vector = [0.25 * SCALER, 0, 0], # location
        orientation = [-1, -1, -1],
        rotation = [0, 1, 0],
        bounds = (math.radians(0), math.radians(144)) 
        # bounds = (math.radians(-28), math.radians(0))

        ),

    URDFLink(
        name = "middle",
        translation_vector = [0.9 * SCALER, 0, 0], # location
        orientation = [-.7, -.7, -.7],
        rotation = [0, 1, 0],
        # maybe set the lower bound to 120 so that it doesn't point up
        #
        bounds = (math.radians(0), math.radians(240)) 
        # bounds = (math.radians(-144), math.radians(240))
        
        ),

    URDFLink(
        name = "wrist",
        translation_vector = [0.55 * SCALER, 0, 0], # location
        orientation = [0, 0, 0],
        rotation = [0, 1, 0],
        bounds = (math.radians(120), math.radians(240))
        # bounds = (math.radians(-120), math.radians(216))
        )
     
    # ,URDFLink(
    #     name = "end effector",
    #     translation_vector = [0.1 * SCALER, 0, 0], # location
    #     orientation = [0, 0, 0],
    #     rotation = [0, 1, 0])
])

# declate the axis 
#
ax = plot_utils.init_3d_figure()

#

# take the coordinate of the targer
#
x_input = float(input("X: "))
y_input = float(input("Y: "))
z_input = float(input("Z: "))

# initiate the target vector and the target frame
#
x = x_input #* SCALER
y = y_input #* SCALER
z = z_input #* SCALER
target_vector = [x, y, z]
target_frame = np.eye(4)
target_frame[:3, 3] = target_vector


angles = arm.inverse_kinematics(target_frame)
for (i, angle) in enumerate(angles):
    angles[i] = math.degrees(angle) 
    
    if (i == 0):
        angles[i] = angles[i] + 30 
        
    elif (i == 3 and angles[i] == 0):  # FIXME: try and fix this 
        angles[i] = angles[i] + 180        
        
        

    # if (angles[i] > 360 ):
    #     angles[i] = angles[i] % 360
        
    print("angle({}) = {} deg, {} pos".format(i, angles[i], int(angles[i]/0.24)))


arm.plot(arm.inverse_kinematics(target_frame), ax, target=target_vector)

# check if reached !
#
real_frame = arm.forward_kinematics(arm.inverse_kinematics(target_frame))
print("Computed position vector : %s, original position vector : %s" % (real_frame[:3, 3], target_frame[:3, 3]))

    


# plot 
#
# plt.xlim(-SCALER, SCALER)
# plt.ylim(-SCALER, SCALER)
plt.show()




# sleep(2)
# print("showing moving arm")

# new_target_vector = [x, y, 0]
# target_frame[:3, 3] = new_target_vector
# copy target vector 
#
# tmp_target_vector = target_vector

# new axis for the movement
#
# new_ax = plot_utils.init_3d_figure()


# this loop is to see the motion when moving down to pick the mushrooms
# when implementing just switch z from VALUE to zero 
#
# for i in range(int(tmp_target_vector[2]*10+1)):
#     print("z = {}".format(tmp_target_vector[2]))
#     print("The angles of each joints are : ", arm.inverse_kinematics(target_frame))
#     arm.plot(arm.inverse_kinematics(target_frame), new_ax, target=target_frame)
#     tmp_target_vector[2] -= 0.1
#     target_frame[:3, 3] = tmp_target_vector
#     print("-" * 100)

