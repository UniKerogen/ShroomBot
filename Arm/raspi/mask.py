##############################################################
#   Libraries
##############################################################
import sys, getopt


##############################################################
#   Function Prototype
##############################################################
def printhelp():
    print("USAGE: python test.py -[command] (id)")
    print("    [-a aid]    servo action with action id")
    print("    [-h]        print this help message")
    print("    [-r rid]    rest with reset id")
    print("    [-s sid]    spin with spin id")
    print("    [-t tid]    test with test id")
    sys.exit(1)


##############################################################
#   Main Function
##############################################################
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hr:s:a:t:", ["rid=", "sid=", "aid=", "tid="])
    except getopt.GetoptError as err:
        print("Error 2: Arguments Fault ->", err)
        printhelp()
    for opt, arg in opts:
        if opt == '-h':
            printhelp()
        elif opt in ("-r", "--rid"):
            resetid = arg
            print("reset servo", resetid, "to default position")
        elif opt in ("-s", "--sid"):
            spinid = arg
            print("spinning servo", spinid)
        elif opt in ("-a", "--aid"):
            actionid = arg
            print("moving servos with action", actionid)
        elif opt in ("-t", "--tid"):
            testid = arg
            print("testing servo", testid)
            


##############################################################
#    Main Function Runner
##############################################################
if __name__ == "__main__":
    if len(sys.argv[1:]) == 0:
        print("Error 1: Not Enough Argument")
        printhelp()
    else:
        main(sys.argv[1:])
