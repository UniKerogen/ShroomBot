##############################################################
#   Libraries
##############################################################
import os
import numpy as np
import matplotlib.pyplot as plt


##############################################################
#   Variable Definition
##############################################################


##############################################################
#   Class Prototype
##############################################################


##############################################################
#   Function Prototype
##############################################################
def reach_plot(data, scatter=True):
    if scatter:
        plt.scatter(data[:, 0], data[:, 1], linewidths=0.1)
        plt.xlabel("Horizontal Distance from Base Mount in [cm]")
        plt.ylabel("Vertical Reachable Point in [cm]")
        plt.show()


##############################################################
#   Main Function
##############################################################
def main():
    print("Hello World!")
    # Read in Data in the order of
    # Reaching x location; Reaching y location; Servo 2 angle, Servo 3 angle, Servo 4 angle, Servo 5 angle
    data = np.loadtxt(fname='MassResult4D-Short.txt', dtype=float, delimiter=" ")
    data = np.sort(data, axis=0)
    reach_plot(data)
    print("Data Loaded")


##############################################################
#    Main Function Runner
##############################################################
if __name__ == "__main__":
    main()
