
# this is a high level function that takes a pint (X, Y, Z)
# it then coputes the inverse kinematics to get the angle of each joint on the 
# arm those angle are then sent to the esp32 via socket
#
# TODO: look into websockets vs sockets ?
#

import sys

# 
#
def main():
  
    while True:
        try:
            # take the coordinate of the targer
            #
            x_input = float(input("X: "))
            y_input = float(input("Y: "))

            # ip of esp and port for the socket connection
            #
            ip = "10.42.0.102"
            port = 5001
            
            # 
            #
            move_arm(x = x_input, y = y_input, ip = ip, port = port)
        
        except KeyboardInterrupt:
            sys.exit()
        except ValueError:
            print("please enter a number")
            continue 

# this is the function to be coppied to the Rpi
#
def move_arm(x, y, ip, port):
   
    # load modules 
    #
    import arm_chain
    from send_angles_sockets import send_angles
    from recv_dist import recv_dist
    from get_angles import compute_angles
    from angles_no_repl import no_repl
    import numpy as np
    import math
    import time
    # import socket
    import netifaces as ni


    # get the local ip address of the machine running the script
    #
    if('en1' in ni.interfaces()):
        local_ip = ni.ifaddresses('en1')[ni.AF_INET][0]['addr']
    else:
        local_ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
        
    print("ip is {}".format(local_ip))

    # initiate the arm chain object
    #
    arm = arm_chain.arm
    
    Z_HIGH = 10.5
    
    # compute the target frame (homogeneous matrix) where the specified point is 
    #
    target_vector = [x, y, Z_HIGH]
    target_frame = np.eye(4)
    target_frame[:3, 3] = target_vector

    # compute the required angles to get to the target vector
    #
    angles = compute_angles(arm, target_frame)

    # uncomment to repl
    #
    # angles = no_repl()
    
    # compare where the end effector is with where the specified point is
    # 
    real_frame = arm.forward_kinematics(arm.inverse_kinematics(target_frame))
    print("Computed position vector : %s, original position vector : %s"\
         % (real_frame[:3, 3], target_frame[:3, 3]))

    
    # send the angles to the esp32 via socket
    #
    send_angles(angles=angles, ip=ip, port=port)
    
    # wait some time ? 
    #
    time.sleep(1)
    
    # rcv distance from esp
    #
    dist = recv_dist(host=local_ip, port=6666)
    
    # compute the z value from current hight
    # then add 0.5 inches to give space
    #
    z = Z_HIGH - dist
    z = z + 0.5
    
    print("this is the new z value {}".format(z))
    
    # recompute the angles with the new z
    #
    new_target_vector = [x, y, z]
    new_target_frame = np.eye(4)
    new_target_frame[:3, 3] = new_target_vector
    new_angles = compute_angles(arm, new_target_frame)

    time.sleep(1)

    # compare where the end effector is with where the specified point is
    # 
    real_frame = arm.forward_kinematics(arm.inverse_kinematics(new_target_frame))
    print("Computed position vector : %s, original position vector : %s" \
        % (real_frame[:3, 3], new_target_frame[:3, 3]))


    new_coordinates = real_frame[:3, 3]
    THRESHOLD = 0.10
    
    # check if the new computed coordinates are within the desired threshold 
    #
    if (((abs(new_coordinates[0]) < (abs(x) * (1+THRESHOLD))) and abs(new_coordinates[0]) > (abs(x) * (1-THRESHOLD))) and
        ((abs(new_coordinates[1]) < (abs(y) * (1+THRESHOLD))) and abs(new_coordinates[1]) > (abs(y) * (1-THRESHOLD))) #and
        #((new_coordinates[2] < (z * (1+THRESHOLD))) and new_coordinates[2] > (z * (1-THRESHOLD)))
        ):
        
        # send the angles to the esp32 via socket
        #
        send_angles(angles=new_angles, ip=ip, port=port)
    
    else:
        # send old angles
        #
        send_angles(angles=angles, ip=ip, port=port)
        print("staying in old...")


    # TODO: find a way to know that the arm is now at drop!
    #
    time.sleep(10)



if __name__ == "__main__":
    main()
