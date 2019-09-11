##############################################################
#   Libraries
##############################################################
from numba import cuda
import math
import numpy as np
import time
import datetime
import array


##############################################################
#   Variable Definition
##############################################################
DESIRED_HEIGHT = 3  # Inches from Base Point
DESIRED_REACH = 3  # Inches from Base Point
L1 = 9  # Humerus Length in Inches - Straight Up
L2 = 2.5  # Elbow Length in Inches
L3 = 9.1  # Radius Length in Inches
L4 = 5.15  # Metacarpi Length in Inches
L5 = 3  # Section Cup in Inches - Straight Down
GAP_VALUE = 1  # The Difference between Two Selected Angle
RANGE_LOW = -90  # Maximum Rotation to the Left
RANGE_HIGH = 90  # Maximum Rotation to the Right
COMBO_RESULT = []  # Empty Space for Result


##############################################################
#   Function Prototype
##############################################################
# Generating a list based on boundaries and differences
def array_generator(low_end, high_end, gap):
    result_list = []
    attach_value = low_end
    while attach_value != high_end + 1:
        result_list.append(attach_value)
        attach_value += gap
    result_array = np.array([result_list])
    return result_array


def calculation_file_generation(action, x, y, a1, a2, a3):
    file_name = "MassResult.txt"
    # Determine Action Type
    if action == "w":
        # Clear file
        file = open(file_name, "w")
        file.write("xLocation yLocation Angle1 Angle2 Angle3 Angle4 \n")
        file.close()
    else:
        # Write file
        file = open(file_name, "a")
        info = [x, y, a1, a2, a3, 180-a1-a2-a3, "\n"]
        write_info = " ".join(str(x) for x in info)
        file.write(write_info)
        file.close()


@cuda.jit(nopython=True, parallel=True)
def cal_kernel(input_array):
    # Establish Variables
    low_end = input_array[0]
    high_end = input_array[1]
    gap = input_array[2]
    # Establish Degree Array of 5 Different Servos
    A1 = array_generator(low_end, high_end, gap)
    A2 = array_generator(RANGE_LOW, RANGE_HIGH, gap)
    A3 = array_generator(RANGE_LOW, RANGE_HIGH, gap)

    # Full Calculation Method
    calculation_file_generation(action="w", x=0, y=0, a1=0, a2=0, a3=0)
    for a in range(A1.shape[1]):
        print(" * Current working on ", A1[a])
        for b in range(A2.shape[1]):
            for c in range(A3.shape[1]):
                if RANGE_LOW <= 180 - A1[a] - A2[b] - A3[c] <= RANGE_HIGH:
                    y = L1 * math.cos(math.radians(0)) + \
                        L2 * math.cos(math.radians(A1[0][a])) + \
                        L3 * math.cos(math.radians(A1[0][a] + A2[0][b])) + \
                        L4 * math.cos(math.radians(A1[0][a] + A2[0][b] + A3[0][c])) + \
                        L5 * math.cos(math.radians(180))

                    x = L1 * math.sin(math.radians(0)) + \
                        L2 * math.sin(math.radians(A1[0][a])) + \
                        L3 * math.sin(math.radians(A1[0][a] + A2[0][b])) + \
                        L4 * math.sin(math.radians(A1[0][a] + A2[0][b] + A3[0][c])) + \
                        L5 * math.sin(math.radians(180))
                    # Save the Combination for Servo Angles
                    if x > 0:
                        calculation_file_generation(action="a", x=x, y=y, a1=A1[a], a2=A2[b], a3=A3[c])


##############################################################
#   Main Function
##############################################################
def main():
    print("Hello World!")
    print("Starting Process ... ", datetime.datetime.now())
    c = array_generator(-10, 10, 1)
    input_array = [-90, 90, 1]
    cal_kernel(input_array)
    print("Ending Process ... ", datetime.datetime.now())


##############################################################
#    Main Function Runner
##############################################################
if __name__ == "__main__":
    main()
