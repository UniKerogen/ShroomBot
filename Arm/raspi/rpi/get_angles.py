

#
#
def compute_angles(arm, target_frame):
    from remap import remap
    import math 
    
    # compute the inverse Kinematics and store the angles for each joint
    #
    angles = arm.inverse_kinematics(target_frame)
    
    # convert the angle from radian to degrees
    #
    for (i, _) in enumerate(angles):
        angles[i] = math.degrees(angles[i])    
        
    # remap the coordinates for each servo using Brandon's lOgIc
    # remap each angle using Brandon's LoGic 
    # print each angle in degrees and position for debugging
    #
    for i in range(4, -1, -1):
        angles[i] = remap(angles=angles, id=i)
        print("angle({}) = {} deg, {} pos".format(i, angles[i], int(angles[i]/0.24)))

    return angles 