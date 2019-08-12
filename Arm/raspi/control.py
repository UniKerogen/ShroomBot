##############################################################
#   Libraries
##############################################################
import sys
import getopt
import serial
import time


##############################################################
#   Initialization
##############################################################
serialHandle = serial.Serial("/dev/ttyAMA0", 115200)  # Initialize Port


##############################################################
#   Function Prototype
##############################################################
def print_help():  # PASS
    print("USAGE: python test.py -[command] (id)")
    print("    [-a aid]    servo action with action id")
    print("    [-h]        print this help message")
    print("    [-r rid]    reset with reset id")
    print("    [-s sid]    spin with spin id")
    print("    [-t tid]    test with test id")
    sys.exit(1)


def servo_write_cmd(servo_id, cmd, par1=None, par2=None):  # PASS
    buf = bytearray(b'\x55\x55')
    try:
        length = 3   # Set Default Package Length
        buf1 = bytearray(b'')

    # Edit Data Package
        if par1 is not None:
            length += 2
            buf1.extend([(0xff & par1), (0xff & (par1 >> 8))])
        if par2 is not None:
            length += 2
            buf1.extend([(0xff & par2), (0xff & (par2 >> 8))])
        buf.extend([(0xff & servo_id), (0xff & length), (0xff & cmd)])
        buf.extend(buf1)

    # CheckSum Reference Point
        check_sum = 0x00
        for b in buf:
            check_sum += b
        check_sum = check_sum - 0x55 - 0x55
        check_sum = ~check_sum
        buf.append(0xff & check_sum)
        serialHandle.write(buf)
    except Exception as e:
        print(e)


def test(test_id):  # PASS
    while True:
        try:
            servo_write_cmd(int(test_id), 1, 0, 1000)
            # ServoID=1 CMD=1 Position=0 Time=1000
            time.sleep(1.1)
            servo_write_cmd(int(test_id), 1, 1000, 1000)
            time.sleep(2.1)
        except Exception as e:
            print(e)
            break


def test_all():  # PASS
    print("test servos for 5 cycles")
    run_num = 1
    while run_num <= 5:
        try:
            print("run #", run_num)
            print("testing servo 1")
            servo_write_cmd(1, 1, 0, 1000)
            time.sleep(1.1)
            servo_write_cmd(1, 1, 1000, 1000)
            time.sleep(2.1)
            print("testing servo 2")
            servo_write_cmd(2, 1, 0, 1000)
            time.sleep(1.1)
            servo_write_cmd(2, 1, 1000, 1000)
            time.sleep(2.1)
            print("testing servo 3")
            servo_write_cmd(3, 1, 0, 1000)
            time.sleep(1.1)
            servo_write_cmd(3, 1, 1000, 1000)
            time.sleep(2.1)
            print("testing servo 4")
            servo_write_cmd(4, 1, 0, 1000)
            time.sleep(1.1)
            servo_write_cmd(4, 1, 1000, 1000)
            time.sleep(2.1)
            print("testing servo 5")
            servo_write_cmd(5, 1, 0, 1000)
            time.sleep(1.1)
            servo_write_cmd(5, 1, 1000, 1000)
            time.sleep(2.1)
            run_num += 1
        except Exception as e:
            print(e)
            break

    
def reset(reset_id):  # PASS
    try:
        servo_write_cmd(int(reset_id), 1, 500, 1000)
        time.sleep(1.1)
        print("reset servo", reset_id, "complete")
    except Exception as e:
        print(e)


def reset_all():  # PASS
    print("resetting all servos")
    while True:
        try:
            print("resetting servo 1")
            servo_write_cmd(1, 1, 500, 1000)
            time.sleep(2.1)
            print("resetting servo 2")
            servo_write_cmd(2, 1, 500, 1000)
            time.sleep(2.1)
            print("resetting servo 3")
            servo_write_cmd(3, 1, 500, 1000)
            time.sleep(2.1)
            print("resetting servo 4")
            servo_write_cmd(4, 1, 500, 1000)
            time.sleep(2.1)
            print("resetting servo 5")
            servo_write_cmd(5, 1, 500, 1000)
            time.sleep(2.1)
            print("reset completed")
            break
        except Exception as e:
            print(e)
            break


def spin(spin_id, spin_angle):
    arrival = spin_angle/240*1000
    while True:
        try:
            servo_write_cmd(int(spin_id), 1, int(arrival), 1000)
            time.sleep(2.1)
            print("servo", spin_id, "arrived at", spin_angle, "degree")
            break
        except Exception as e:
            print(e)
            break


def action1():
    try:
        servo_write_cmd(1, 1, 300, 1000)
        time.sleep(2.1)
        servo_write_cmd(2, 1, 800, 1000)
        time.sleep(2.1)
        servo_write_cmd(3, 1, 600, 1000)
        time.sleep(2.1)
        servo_write_cmd(4, 1, 900, 1000)
        time.sleep(2.1)
        servo_write_cmd(5, 1, 200, 1000)
        time.sleep(2.1)
        print("action 1 completed")
    except Exception as e:
        print(e)


##############################################################
#   Main Function
##############################################################
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hr:s:a:t:", ["rid=", "sid=", "aid=", "tid="])
    except getopt.GetoptError as err:
        print("Error 2: Arguments Fault ->", err)
        print_help()
    for opt, arg in opts:
        # Sub Command -h
        if opt == '-h':
            print_help()
        # Sub Command -r
        elif opt in ("-r", "--rid"):
            reset_id = arg
            if str(1) <= str(reset_id) <= str(5):
                print("reset servo", reset_id, "to default position")
                reset(reset_id)
            elif str(reset_id) == 'a':
                print("reset all servo")
                reset_all()
            else:
                print("Error 3: Unknown Argument for -r")
        # Sub Command -s
        elif opt in ("-s", "--sid"):
            spin_id = arg
            arrival_angle = int(input("Enter Arriving Angle (degree) >> "))
            if 0 < int(arrival_angle) < 240:
                print("spinning servo", spin_id, "to angle", arrival_angle)
                spin(spin_id, arrival_angle)
            else:
                print("Error 4: Arriving Angle Not Valid")
        # Sub Command -a
        elif opt in ("-a", "--aid"):
            action_id = arg
            print("moving servos with action", action_id)
            action1()
        # Sub Command -t
        elif opt in ("-t", "--tid"):
            test_id = arg
            if str(1) <= str(test_id) <= str(5):
                print("testing servo", test_id)
                test(test_id)
            elif str(test_id) == 'a':
                print("test all servos")
                test_all()
            else:
                print("Error 5: Unknown Argument for -t")


##############################################################
#    Main Function Runner
##############################################################
if __name__ == "__main__":
    if len(sys.argv[1:]) == 0:
        print("Error 1: Not Enough Argument")
        print_help()
    else:
        main(sys.argv[1:])
