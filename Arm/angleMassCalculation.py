# Estimate 33 hrs on 8950HK

##############################################################
#   Libraries
##############################################################
import multiprocessing as mp
import threading as td
import math
import datetime
import timeit
import time

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
GAP_VALUE = 22.5/2  # The Difference between Two Selected Angle
RANGE_LOW = -90  # Maximum Rotation to the Left
RANGE_HIGH = 90  # Maximum Rotation to the Right
COMBO_RESULT = []  # Empty Space for Result


##############################################################
#   Class Prototype
##############################################################
# Fix Thread Operation
class CoreThread(td.Thread):
    def __init__(self, thread_id, low_end, high_end, time, core_info):
        td.Thread.__init__(self)
        self.low_end = low_end
        self.high_end = high_end
        self.time = time
        self.core_info = [core_info, thread_id]

    def run(self):
        print("Starting ", self.core_info[0], "thread", self.core_info[1])
        calculation_test(self.low_end, self.high_end, GAP_VALUE, self.time, self.core_info)
        print("Exiting ", self.core_info[0], "thread", self.core_info[1])


# User Determined Thread Operation
class CoreThread2(td.Thread):
    def __init__(self, thread_id, low_end, high_end, time, core_info):
        td.Thread.__init__(self)
        self.low_end = low_end
        self.high_end = high_end
        self.time = time
        self.core_info = [core_info, thread_id]

    def run(self):
        print("Starting ", self.core_info[0], "thread", self.core_info[1])
        calculation(self.low_end, self.high_end, GAP_VALUE, self.time, self.core_info)
        print("Exiting ", self.core_info[0], "thread", self.core_info[1])

##############################################################
#   Function Prototype
##############################################################
# Generating a list based on boundaries and differences
def list_generator(low_end, high_end, gap):
    result_list = []
    attach_value = low_end
    while attach_value < high_end:
        result_list.append(attach_value)
        attach_value += gap
    if high_end == RANGE_HIGH:
        result_list.append(RANGE_HIGH)
    return result_list


def calculation_test(low_end, high_end, gap, time, thread_info):
    # Establish Degree Array of 5 Different Servos
    A1 = list_generator(low_end, high_end, gap)
    A2 = list_generator(RANGE_LOW, RANGE_HIGH, gap)
    A3 = list_generator(RANGE_LOW, RANGE_HIGH, gap)
    A4 = list_generator(RANGE_LOW, RANGE_HIGH, gap)
    A5 = list_generator(RANGE_LOW, RANGE_HIGH, gap)
    # print(thread_info[0], thread_info[1], "completed list generation with ", timeit.timeit()-time, "seconds")

    print(thread_info[0], "thread", thread_info[1], "will work on", [items for items in A1])


# Calculation main function
def calculation(low_end, high_end, gap, time, thread_info):
    # Establish Degree Array of 5 Different Servos
    A1 = list_generator(low_end, high_end, gap)
    A2 = list_generator(RANGE_LOW, RANGE_HIGH, gap)
    A3 = list_generator(RANGE_LOW, RANGE_HIGH, gap)
    A4 = list_generator(RANGE_LOW, RANGE_HIGH, gap)
    A5 = list_generator(RANGE_LOW, RANGE_HIGH, gap)
    # print(thread_info[0], thread_info[1], "completed list generation with ", timeit.timeit()-time, "seconds")

    # Full Calculation Method
    print(thread_info[0], "thread", thread_info[1], "will work on", [items for items in A1])
    for a in range(len(A1)):
        print(" * ", thread_info[0], thread_info[1], "is current working on ", A1[a])
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
                        # print(thread_info[0], thread_info[1], "completed one fifth-degree iteration with", timeit.timeit()-time)
                # print(thread_info[0], thread_info[1], "completed one third-degree iteration with ", timeit.timeit()-time)
        # print(thread_info[0], thread_info[1], "completed one first-degree iteration with ", timeit.timeit()-time)


# Core1 Function - 2 thread core
def core1(low_end, high_end, core_info):
    core1_time_start = timeit.timeit()
    core1threads = []
    midpoint = (low_end + high_end)/2
    # Initialize Threads
    thread1 = CoreThread(1, low_end, midpoint, core1_time_start, core_info)
    thread2 = CoreThread(2, midpoint, high_end, core1_time_start, core_info)
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
    core1_time_end = timeit.timeit()
    print("Core 1 finished in", core1_time_end-core1_time_start)


# Core0 Function - 4 thread core
def core0(low_end, high_end, core_info):
    print("Starting Core0 for testing purposes at", datetime.datetime.now())
    print(core_info)
    # Initialize Cores
    core0_start_time = timeit.timeit()
    core0threads = []
    separation_gap = (abs(low_end) + abs(high_end)) / 4
    separation_point_1 = RANGE_LOW + separation_gap
    separation_point_2 = RANGE_LOW + separation_gap * 2
    separation_point_3 = RANGE_LOW + separation_gap * 3
    # Initialize Threads
    thread01 = CoreThread(1, low_end, separation_point_1, core0_start_time, core_info)
    thread02 = CoreThread(2, separation_point_1, separation_point_2, core0_start_time, core_info)
    thread03 = CoreThread(3, separation_point_2, separation_point_3, core0_start_time, core_info)
    thread04 = CoreThread(4, separation_point_3, high_end, core0_start_time, core_info)
    # Try to Start All Threads
    try:
        thread01.start()
        core0threads.append(thread01)
        time.sleep(3)
        thread02.start()
        core0threads.append(thread02)
        time.sleep(3)
        thread03.start()
        core0threads.append(thread03)
        time.sleep(3)
        thread04.start()
        core0threads.append(thread04)

        # Wait Till Both Threads are Finished
        for t in core0threads:
            t.join()
    # Catch Exceptions in All Condition
    except:
        print("Unable to start Thread in Core0")
    core0_end_time = timeit.timeit() - core0_start_time
    print("Core 0 finished in", core0_end_time - core0_start_time)


# Application1 Function - Dual Core 4 Thread
def application1():
    print("Starting Process ... ", datetime.datetime.now())
    half_process = (RANGE_LOW + RANGE_HIGH) / 2
    # Initialize Cores
    p1 = mp.Process(target=core1, args=(RANGE_LOW, half_process, "core1"))
    p2 = mp.Process(target=core1, args=(half_process, RANGE_HIGH, "core2"))
    # Start Cores
    p1.start()
    p2.start()
    # Wait Till all Cores are Finished
    p1.join()
    p2.join()
    # Exiting
    print("Ending Process ... ", datetime.datetime.now())
    print(COMBO_RESULT)


# Application 0 Function - Single Core 4 thread
def application0():
    print("Starting the test process ...", datetime.datetime.now())
    # Initialize Cores
    p0 = mp.Process(target=core0, args=(RANGE_LOW, RANGE_HIGH, "core0"))
    # Start Cores
    p0.start()
    # Wait till all cores finish
    p0.join()
    # Exiting
    print("Ending test process ...", datetime.datetime.now())


# Core2 Function - User Determined Thread Number
def core2(low_end, high_end, core_info, thread_number):
    # Core Configuration
    core2_start = datetime.datetime.now()
    core2threads = []
    # Task Separation
    gaps = []
    end_point = low_end
    while end_point <= high_end:
        gaps.append(end_point)
        end_point += (abs(low_end) + abs(high_end)) / thread_number
    # Initialize Threads
    try:
        for index in range(0, len(gaps)-1):
            thread_temp = CoreThread(index, gaps[index], gaps[index+1], core2_start, core_info)
            thread_temp.start()
            core2threads.append(thread_temp)
            time.sleep(1)
        # Wait till all finish
        for t in core2threads:
            t.join()
        print(core2threads)
    except:
        print("Unable to start Thread in Core 2 Kernel")
    # Print Elaspe Time
    print("Core 2 finished in", datetime.datetime.now()-core2_start)


# Application 2 Function - Quad Core User Defined Threads
def application2(thread_number):
    # Core Configuration
    print("Starting Process ...", datetime.datetime.now())
    # Task Separation
    tasks = []
    end_point = RANGE_LOW
    while end_point <= RANGE_HIGH:
        tasks.append(end_point)
        end_point += (abs(RANGE_LOW) + abs(RANGE_HIGH)) / 4
    # Initialize Cores
    p0 = mp.Process(target=core2, args=(tasks[0], tasks[1], "core0", thread_number))
    p1 = mp.Process(target=core2, args=(tasks[1], tasks[2], "core1", thread_number))
    p2 = mp.Process(target=core2, args=(tasks[2], tasks[3], "core2", thread_number))
    p3 = mp.Process(target=core2, args=(tasks[3], tasks[4], "core3", thread_number))
    # Start Cores
    p0.start()
    time.sleep(1)
    p1.start()
    time.sleep(1)
    p2.start()
    time.sleep(1)
    p3.start()
    time.sleep(1)
    # Wait for all cores to finish
    p0.join()
    p1.join()
    p2.join()
    p3.join()
    # Exiting
    print("Ending Process ...", datetime.datetime.now())


##############################################################
#   Main Function
##############################################################
def main():
    print("Hello World!")
    # application1()
    # application0()
    application2(4)


##############################################################
#    Main Function Runner
##############################################################
if __name__ == "__main__":
    main()
