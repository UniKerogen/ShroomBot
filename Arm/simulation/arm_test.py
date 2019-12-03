
from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
from ikpy import plot_utils
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
import math

# create the arm using IKpy's chain constructor with URDF links
# TODO: check length of each link could be wrong
#
arm = Chain(name="arm", links= [
    URDFLink(
        name = "base servo",
        translation_vector = [0, 0, 0],
        orientation = [ 0, 0, 0],
        rotation = [0, 0, 1],
        # bounds=(math.radians(0), math.radians(180))
        ),
    URDFLink(
        name = "elbow low",
        translation_vector = [0, 0, 8],
        orientation = [0, 0, 0],
        rotation = [0, 1, 0],
        bounds=(math.radians(-25), math.radians(90))
        ),
    URDFLink(
        name = "elbow hight",
        translation_vector = [0, 0, 2.5],
        orientation = [0, 0, 0],
        rotation = [0, 1, 0],
        bounds=(math.radians(-160), math.radians(36))
        ),

    URDFLink(
        name = "middle",
        translation_vector = [9, 0, 0],
        orientation = [0, 0, 0],
        rotation = [0, 1, 0],
        bounds=(math.radians(-110), math.radians(110))
        ),

    URDFLink(
        name = "wrist",
        translation_vector = [5.25, 0, 0],
        orientation = [0, 0, 0],
        rotation = [0, 1, 0],
        bounds=(math.radians(-120), math.radians(120))
        )
     
    # ,URDFLink(
    #     name = "end effector",
    #     translation_vector = [1, 0, 0],
    #     orientation = [0, 0, 0],
    #     rotation = [0, 1, 0])
])


# declate the axis 
#
AXIS = plot_utils.init_3d_figure()

def main():

    # take the coordinate of the targer
    #
    x_input = float(input("X: "))
    y_input = float(input("Y: "))
    z_input = float(input("Z: "))

    # initiate the target vector and the target frame
    #
    x = x_input 
    y = y_input 
    z = z_input 

    # check if the X is negative then set the flag
    #
    if x_input < 0:
        x = abs(x_input)
        negX_flag = 1
    else:
        negX_flag = 0

    # compute the target frame (homogeneous matrix) where the specified point is 
    #
    target_vector = [x, y, z]
    target_frame = np.eye(4)
    target_frame[:3, 3] = target_vector

    # compute the inverse Kinematics and store the angles for each joint
    #
    angles = arm.inverse_kinematics(target_frame)

    # raw_angles = math.degrees(sum(angles)- angles[0])
    
    raw_angles = 120 - (90 + -1 * (math.degrees(angles[1]) + (math.degrees(angles[2])) + (math.degrees(angles[3]))))
    
    
    print("sum of raw angles {}".format(raw_angles))
    
    # for each angle of the arm
    #
    for (i, angle) in enumerate(angles):
        # convert the angle from radian to degrees
        #
        angles[i] = math.degrees(angle) 
                
        # remap each angle using Brandon's LoGic 
        #
        angles[i] = remap(angles=angles, id=i, negX_flag=negX_flag)

        # print each angle in degrees and position
        #
        print("angle({}) = {} deg, {} pos".format(i, angles[i], int(angles[i]/0.24)))


    # generate the simulation to see the arm
    #
    arm.plot(arm.inverse_kinematics(target_frame), AXIS, target=target_vector)

    # compare where the end effector is with where the specified point is
    # 
    real_frame = arm.forward_kinematics(arm.inverse_kinematics(target_frame))
    print("Computed position vector : %s, original position vector : %s" % (real_frame[:3, 3], target_frame[:3, 3]))

    # show the simulation plot 
    #
    plt.show()

 
# this function is to remap the coordinates using Brandon's lOgIc
#
def remap(id=0, angles=[], negX_flag=0):
        
    # reference angles for Brandon's LoGic
    # TODO: CLEAN OR FIND A WAY TO EXPLAIN
    #
    REF_ANGLES = [55, 120, 36, 120, 120, 120]

    print("{} raw: {}".format(id, angles[id]))

    if(id == 0):
        angles[id] = REF_ANGLES[id] + angles[id]
    # angles[id] = angles[id] + REF_ANGLES[id]
    if(id != 0 and angles[id] >= 0):
        angles[id] = REF_ANGLES[id] - abs(angles[id])
    elif(id != 0 and angles[id] < 0):
        angles[id] = REF_ANGLES[id] + abs(angles[id])
        

    # if (id == 0):  
    #     # FIXME: not negative but very large number becomes negative when flipping 
    #     # FIXME: not sure if that the right fix but this fixed the high too
    #     # FIXME: this works for X = 0 but X = 1 works but technically shouldn't ?
    #     #
    #     print("base: {}".format(angles[id]))      
    #     # if(angles[id] > 240):
    #     #     angles[id] = 100
        
    #     # angles[id] = angles[id] + 45
        
    #     # check if the negative flag was set
    #     #
    #     # if(negX_flag):
    #     #     print("it was negative")
    #     #     angles[id] = angles[id] + 90
        
    #     # FIXME: the angles changes here before that it's not negative
    #     # #    
    #     # if angles[id] > 270:
    #     #     angles[id] = 360 - angles[id]
            
            
    # elif (id == 1): 
    #     angles[id] = angles[id]
        
    # elif (id == 2):
    #     angles[id] = angles[id]
      
    # elif (id == 3):
    #     angles[id] = angles[id]
    
    return abs(angles[id])

if __name__ == "__main__":
    main()