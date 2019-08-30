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
DESIRED_HEIGHT = 10  # Centimeters
DESIRED_REACH = 10  # Centimeters
L1 = 10  # Humerus Length in Centimeters
L2 = 10  # Elbow Length in Centimeters
L3 = 10  # Radius Length in Centimeters
L4 = 10  # Metacarpi Length in Centimeters
L5 = 10  # Finger Length in Centimeters
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
    A4 = array_generator(RANGE_LOW, RANGE_HIGH, gap)
    A5 = array_generator(RANGE_LOW, RANGE_HIGH, gap)

    # Full Calculation Method
    for a in range(A1.shape[1]):
        print(" * Current working on ", A1[a])
        for b in range(A2.shape[1]):
            for c in range(A3.shape[1]):
                for d in range(A4.shape[1]):
                    for e in range(A5.shape[1]):
                        y = L1 * math.cos(math.radians(A1[0][a])) + \
                            L2 * math.cos(math.radians(A1[0][a] + A2[0][b])) + \
                            L3 * math.cos(math.radians(A1[0][a] + A2[0][b] + A3[0][c])) + \
                            L4 * math.cos(math.radians(A1[0][a] + A2[0][b] + A3[0][c] + A4[0][d])) + \
                            L5 * math.cos(math.radians(A1[0][a] + A2[0][b] + A3[0][c] + A4[0][d] + A5[0][e]))
                        # Once Height Matches, Calculate Reach
                        if y == DESIRED_HEIGHT:
                            x = L1 * math.sin(math.radians(A1[0][a])) + \
                                L2 * math.sin(math.radians(A1[0][a] + A2[0][b])) + \
                                L3 * math.sin(math.radians(A1[0][a] + A2[0][b] + A3[0][c])) + \
                                L4 * math.sin(math.radians(A1[0][a] + A2[0][b] + A3[0][c] + A4[0][d])) + \
                                L5 * math.sin(math.radians(A1[0][a] + A2[0][b] + A3[0][c] + A4[0][d] + A5[0][e]))
                            # Save the Combination for Servo Angles
                            if x == DESIRED_REACH:
                                COMBO_RESULT.append([A1[0][a], A2[0][b], A3[0][c], A4[0][d], A5[0][e], '\n'])


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