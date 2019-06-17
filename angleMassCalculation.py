##############################################################
#   Libraries
##############################################################
import multiprocessing as mp
import threading as td
import math
import datetime

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
#   Class Prototype
##############################################################
class CoreThread(td.Thread):
    def __init__(self, threadid, name, low_end, high_end):
        td.Thread.__init__(self)
        self.threadid = threadid
        self.name = name
        self.low_end = low_end
        self.high_end = high_end

    def run(self):
        print("Starting ", self.name)
        calculation(self.low_end, self.high_end, GAP_VALUE)
        print("Exiting ", self.name)


##############################################################
#   Function Prototype
##############################################################
# Generating a list based on boundaries and differences
def list_generator(low_end, high_end, gap):
    result_list = []
    attach_value = low_end
    while attach_value != high_end:
        result_list.append(attach_value)
        attach_value += gap
    return result_list


# Calculation main function
def calculation(low_end, high_end, gap):
    # Establish Degree Array of 5 Different Servos
    A1 = list_generator(low_end, high_end, gap)
    A2 = list_generator(RANGE_LOW, RANGE_HIGH, gap)
    A3 = list_generator(RANGE_LOW, RANGE_HIGH, gap)
    A4 = list_generator(RANGE_LOW, RANGE_HIGH, gap)
    A5 = list_generator(RANGE_LOW, RANGE_HIGH, gap)

    # Full Calculation Method
    for a in range(len(A1)):
        print(" * Current working on ", A1[a])
        for b in range(len(A2)):
            for c in range(len(A3)):
                for d in range(len(A4)):
                    for e in range(len(A5)):
                        y = L1 * math.cos(math.radians(A1[a])) + \
                            L2 * math.cos(math.radians(A1[a] + A2[b])) + \
                            L3 * math.cos(math.radians(A1[a] + A2[b] + A3[c])) + \
                            L4 * math.cos(math.radians(A1[a] + A2[b] + A3[c] + A4[d])) + \
                            L5 * math.cos(math.radians(A1[a] + A2[b] + A3[c] + A4[d] + A5[e]))
                        # Once Height Matches, Calculate Reach
                        if y == DESIRED_HEIGHT:
                            x = L1 * math.sin(math.radians(A1[a])) + \
                                L2 * math.sin(math.radians(A1[a] + A2[b])) + \
                                L3 * math.sin(math.radians(A1[a] + A2[b] + A3[c])) + \
                                L4 * math.sin(math.radians(A1[a] + A2[b] + A3[c] + A4[d])) + \
                                L5 * math.sin(math.radians(A1[a] + A2[b] + A3[c] + A4[d] + A5[e]))
                            # Save the Combination for Servo Angles
                            if x == DESIRED_REACH:
                                COMBO_RESULT.append([A1[a], A2[b], A3[c], A4[d], A5[e], '\n'])


# Core1 Function
def core1(low_end, high_end):
    core1threads = []
    midpoint = (low_end + high_end)/2
    # Initialize Threads
    thread1 = CoreThread(1, "Thread1", low_end, midpoint)
    thread2 = CoreThread(2, "Thread2", midpoint, high_end)
    # Try to Start All Threads
    try:
        thread1.start()
        core1threads.append(thread1)
        thread2.start()
        core1threads.append(thread2)

        # Wait Till Both Threads are Finished
        for t in core1threads:
            t.join()
    # Catch Exceptions in All Condition
    except:
        print("Unable to start Thread in Core 1")


# Core2 Function
def core2(low_end, high_end):
    core2threads = []
    midpoint = (low_end + high_end) / 2
    # Initialize Threads
    thread3 = CoreThread(3, "Thread3", low_end, midpoint)
    thread4 = CoreThread(4, "Thread4", midpoint, high_end)
    # Try to Start All Threads
    try:
        thread3.start()
        core2threads.append(thread3)
        thread4.start()
        core2threads.append(thread4)

        # Wait Till Both Threads are Finished
        for t in core2threads:
            t.join()
    # Catch Exceptions in All Condition
    except:
        print("Unable to start Thread in Core 2")


##############################################################
#   Main Function
##############################################################
def main():
    print("Hello World!")
    print("Starting Process ... ", datetime.datetime.now())
    # Initialize Cores
    p1 = mp.Process(target=core1, args=(-90, 0,))
    p2 = mp.Process(target=core2, args=(0, 90,))
    # Start Cores
    p1.start()
    p2.start()
    # Wait Till all Cores are Finished
    p1.join()
    p2.join()
    # Exiting
    print("Ending Process ... ", datetime.datetime.now())
    print(COMBO_RESULT)


##############################################################
#    Main Function Runner
##############################################################
if __name__ == "__main__":
    main()











