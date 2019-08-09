#!/usr/bin/python3

import serial
import time


serialHandle = serial.Serial("/dev/ttyAMA0", 115200) # Initialize Port

command = {"MOVE_WRITE":1, "POS_READ":28, "LOAD_UNLOAD_WRITE": 31}

##
## Sending Package
##
def servoWriteCmd(id, cmd, par1 = None, par2 = None):
    buf = bytearray(b'\x55\x55')
    try:
        len = 3   # Set Default Package Length
        buf1 = bytearray(b'')
        ## Edit Package
        if par1 is not None:
            len += 2  #Increase Package Length
            par1 = 0xffff & par1
            buf1.extend([(0xff & par1), (0xff & (par1 >> 8))])
        if par2 is not None:
            len += 2
            par2 = 0xffff & par2
            buf1.extend([(0xff & par2), (0xff & (par2 >> 8))])

        buf.extend([(0xff & id), (0xff & len), (0xff & cmd)]) #Add id, package length
        buf.extend(buf1) #Add Package

        ##Checksum Package
        sum = 0x00
        for b in buf:
            sum += b
        sum = sum - 0x55 - 0x55
        sum = ~sum
        buf.append(0xff & sum)

        serialHandle.write(buf) #Send

    except Exception as e:
        print(e)


##
## Read Position
##
def readPosition(id):
    serialHandle.flushInput() # Flush Buffer
    servoWriteCmd(id, command["POS_READ"]) # Set Port to Read
    time.sleep(0.00034) # Delay for sending
    time.sleep(0.005)  # Delay for receiving
    count = serialHandle.inWaiting() # Count reading package length
    print("inWaiting = ", serialHandle.inWaiting)
    pos = None
    print("count =", count)
    if count != 0:
        recv_data = serialHandle.read(count)
        if count == 8:
            if recv_data[0] == 0x55 and recv_data[1] == 0x55 and recv_data[4] == 0x1C :
                 pos= 0xffff & (recv_data[5] | (0xff00 & (recv_data[6] << 8)))
    return pos


servoWriteCmd(1, command["LOAD_UNLOAD_WRITE"],0)  #Decouple Servo to enable manual control
while True:
    try:
        pos = readPosition(1) # Read Servo1 Postion
        print(pos)
        time.sleep(1)
    except Exception as e:
        print(e)
        break
