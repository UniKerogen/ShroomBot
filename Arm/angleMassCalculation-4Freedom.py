# Estimate 33 hrs on 8950HK for Single Stream
# Run-Time of 6.5 minutes with hexa core 30 threads of 2073071593 calculation @ 3.9GHz on 8750H
# Run-Time of 9 minutes with quad core 16 threads of 1073741824 calculation @ 4.29GHz on 8700K
# Run-Time of 10 minutes with hexa core 24 threads of 2073071593 calculation @ 3.5GHz on 8750H
# Run-Time of 13 minutes with quad core 16 threads of 1073741824 calculation @ 3.10GHz on 8750H
# Run-Time of 39 minutes with single core 4 threads of 1073741824 calculation @ 3.8GHz~ on 8750H
# Run-Time of 16 minutes with dual core 4 threads of 1073741824 calculation @ 4.34GHz on 8700K

##############################################################
#   Libraries
##############################################################
import multiprocessing as mp
import threading as td
import os
import numpy as np
import math
import datetime
import timeit
import time

##############################################################
#   Variable Definition
##############################################################
SLEEP_TIME = 1.4  # Second
CORE_NUMBER = 10  # Cores
THREAD_NUMBER = 1  # Threads
DESIRED_HEIGHT = 3  # cm from Base Point
DESIRED_REACH = 3  # cm from Base Point
# Measurement Taken from the object #
# L1 = 9 inches, L2 = 2.5 inches, L3 = 9.1 Inches, L4 = 5.15 Inches, L5 = 1 Inches #
L0 = 3  # Raise of Shoulder - Straight up
L1 = 22.86  # Humerus Length in cm
L2 = 6.35  # Elbow Length in cm
L3 = 23.11  # Radius Length in cm
L4 = 13.08  # Metacarpi Length in cm
L5 = 2.5  # Section Cup in cm - Straight Down
GAP_VALUE = 180/(2*CORE_NUMBER*THREAD_NUMBER)  # The Difference between Two Selected Angle
RANGE_LOW = -100  # Maximum Rotation to the Left
RANGE_HIGH = 100  # Maximum Rotation to the Right
SAVE_RANGE_LOW = 5
SAVE_RANGE_HIGH = 40
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


# Calculation test function for data assignment
def calculation_test(low_end, high_end, gap, time, thread_info):
    # Establish Degree Array of 5 Different Servos
    a1 = list_generator(low_end, high_end, gap)
    a2 = list_generator(RANGE_LOW, RANGE_HIGH, gap)
    a3 = list_generator(RANGE_LOW, RANGE_HIGH, gap)
    # print(thread_info[0], thread_info[1], "completed list generation with ", timeit.timeit()-time, "seconds")

    print(thread_info[0], "thread", thread_info[1], "will work on", [items for items in a1])


# Calculation main function
def calculation(low_end, high_end, gap, time, thread_info):
    # Establish Degree Array of 5 Different Servos
    A1 = list_generator(low_end, high_end, gap)
    A2 = list_generator(RANGE_LOW, RANGE_HIGH, gap)
    A3 = list_generator(RANGE_LOW, RANGE_HIGH, gap)
    A4 = list_generator(RANGE_LOW, RANGE_HIGH, gap)
    # print(thread_info[0], thread_info[1], "completed list generation with ", timeit.timeit()-time, "seconds")

    # Full Calculation Method
    print(thread_info[0], "thread", thread_info[1], "will work on", [items for items in A1])
    calculation_file_generation(action="w", x=0, y=0, a1=0, a2=0, a3=0, a4=0,
                                file_name=str(thread_info[0]) + "thread" + str(thread_info[1]))

    for a in range(len(A1)):
        print(" * ", thread_info[0], "thread", thread_info[1], "is current working on ", A1[a])
        for b in range(len(A2)):
            for c in range(len(A3)):
                for d in range(len(A4)):
                    if RANGE_LOW <= 180-A1[a]-A2[b]-A3[c]-A4[d] <= RANGE_HIGH:
                        y = L0 * math.cos(math.radians(0)) + \
                            L1 * math.cos(math.radians(A1[a])) + \
                            L2 * math.cos(math.radians(A1[a] + A2[b])) + \
                            L3 * math.cos(math.radians(A1[a] + A2[b] + A3[c])) + \
                            L4 * math.cos(math.radians(A1[a] + A2[b] + A3[c] + A4[d])) + \
                            L5 * math.cos(math.radians(180))
                    # Once Height Matches, Calculate Reach
                    # if y == DESIRED_HEIGHT:
                        x = L0 * math.sin(math.radians(0)) + \
                            L1 * math.sin(math.radians(A1[a])) + \
                            L2 * math.sin(math.radians(A1[a] + A2[b])) + \
                            L3 * math.sin(math.radians(A1[a] + A2[b] + A3[c])) + \
                            L4 * math.sin(math.radians(A1[a] + A2[b] + A3[c] + A4[d])) + \
                            L5 * math.sin(math.radians(180))
                            # Save the Combination for Servo Angles
                            # if x == DESIRED_REACH:
                            #     COMBO_RESULT.append([A1[a], A2[b], A3[c], 180-A1[a]-A2[b]-A3[c], '\n'])
                        if SAVE_RANGE_LOW < x < SAVE_RANGE_HIGH:
                            calculation_file_generation(action="a", x=x, y=y, a1=A1[a], a2=A2[b], a3=A3[c], a4=A4[d],
                                                        file_name=str(thread_info[0]) + "thread" + str(thread_info[1]))
                # print(thread_info[0], thread_info[1], "completed one 3rd-level iteration with ", timeit.timeit()-time)
            # print(thread_info[0], thread_info[1], "completed one 2nd-level iteration with ", timeit.timeit()-time)
        # print(thread_info[0], thread_info[1], "completed one 1st-level iteration with ", timeit.timeit()-time)


def calculation_file_generation(action, x, y, a1, a2, a3, a4, file_name):
    file_name = file_name + ".txt"
    # Determine Action Type
    if action == "w":
        # Clear file
        file = open(file_name, "w")
        # file.write("xLocation yLocation Angle1 Angle2 Angle3 Angle4 Angle5\n")
        file.write("\n")
        file.close()
    else:
        # Write file
        file = open(file_name, "a")
        info = [x, y, a1, a2, a3, a4, 180-a1-a2-a3-a4]
        write_info = " ".join(str(x) for x in info)
        write_info = write_info + "\n"
        # print(write_info)
        file.write(write_info)
        file.close()


# Core0 Kernel Function - 4 thread core
def core0(low_end, high_end, core_info):
    print("Starting Core0 for testing purposes at", datetime.datetime.now())
    print(core_info)
    # Initialize Cores
    core0_start_time = timeit.timeit()
    core0threads = []
    separation_gap = (high_end - low_end) / 4
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


# Core1 Kernel Function - 2 thread core
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


# Core2 Kernel Function - User Determined Thread Number
def core2(low_end, high_end, core_info, thread_number):
    # Core Configuration
    core2_start = datetime.datetime.now()
    core2threads = []
    # Task Separation
    gaps = []
    end_point = low_end
    while end_point <= high_end:
        gaps.append(end_point)
        end_point += (high_end - low_end) / thread_number
    # Initialize Threads
    try:
        for index in range(0, len(gaps)-1):
            thread_temp = CoreThread(index, gaps[index], gaps[index+1], core2_start, core_info)
            thread_temp.start()
            core2threads.append(thread_temp)
            time.sleep(0.2)  # Sleep for terminal id output
        # Wait till all finish
        for t in core2threads:
            t.join()
    # Catch exception that stop Core2 Kernel from starting
    except:
        print("Unable to start Thread in Core 2 Kernel")
    # Print Elapse Time
    print("Core 2 Kernel finished in", datetime.datetime.now()-core2_start)


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
    time.sleep(SLEEP_TIME)  # Sleep for terminal id output
    p1.start()
    time.sleep(SLEEP_TIME)  # Sleep for terminal id output
    p2.start()
    time.sleep(SLEEP_TIME)  # Sleep for terminal id output
    p3.start()
    time.sleep(SLEEP_TIME)  # Sleep for terminal id output
    # Wait for all cores to finish
    p0.join()
    p1.join()
    p2.join()
    p3.join()
    # Exiting
    print("Ending Process ...", datetime.datetime.now())


# Application 3 Function - User Defined Core User Defined Threads
def application3(core_number, thread_number):
    # Core Configuration
    print("Starting Process ...", datetime.datetime.now())
    processor_core = []
    # Task Separation
    tasks = []
    end_point = RANGE_LOW
    while end_point <= RANGE_HIGH:
        tasks.append(end_point)
        end_point += (abs(RANGE_LOW) + abs(RANGE_HIGH)) / core_number
    # Initialize Cores
    for index in range(0, core_number):
        p_temp = mp.Process(target=core2, args=(tasks[index], tasks[index+1], "core"+str(index), thread_number))
        processor_core.append(p_temp)
        p_temp.start()
        time.sleep(SLEEP_TIME)
    # Wait for core to finish
    for c in processor_core:
        c.join()
    # Exiting
    print("Ending Process ...", datetime.datetime.now())


# Concentrate All File to One
def file_concentrate(core_number, thread_number, file_name):
    print("Concentrating files")
    # Generate File Name List
    text_file = ["None"] * (core_number * thread_number)
    loop0 = 0
    for loop1 in range(0, core_number):
        for loop2 in range(0, thread_number):
            text_file[loop0] = "core" + str(loop1) + "thread" + str(loop2) + ".txt"
            loop0 += 1
    # print(text_file)
    # Concentrate Files
    with open(file_name, 'w') as outfile:
        for name in text_file:
            if os.path.exists(name):
                with open(name) as infile:
                    for line in infile:
                        if not len(line.strip()) == 0:
                            outfile.write(line)
    # Remove Previously Generated File
    for name in text_file:
        if os.path.exists(name):
            os.remove(name)


##############################################################
#   Main Function
##############################################################
def main():
    print("Hello World!")
    time_start = datetime.datetime.now()
    # application0()
    # application1()
    # application2(THREAD_NUMBER)
    application3(CORE_NUMBER, THREAD_NUMBER)
    print("File generation Completed")
    time.sleep(1)
    print("File generation Elapse", datetime.datetime.now()-time_start)
    file_concentrate(core_number=CORE_NUMBER, thread_number=THREAD_NUMBER, file_name='MassResult4D-Short.txt')
    print("Total Elapse", datetime.datetime.now()-time_start)


##############################################################
#    Main Function Runner
##############################################################
if __name__ == "__main__":
    main()
