#!/usr/bin/python3

import serial
import time


serialHandle = serial.Serial("/dev/ttyAMA0", 115200)  #Initialize Port


##
## Sending Package
##
def servoWriteCmd(id, cmd, par1 = None, par2 = None):
    buf = bytearray(b'\x55\x55')
    try:
        len = 3   # Set Default Package Length
        buf1 = bytearray(b'')

	## Edit Data Package
        if par1 is not None:
            len += 2
            buf1.extend([(0xff & par1), (0xff & (par1 >> 8))])
        if par2 is not None:
            len += 2
            buf1.extend([(0xff & par2), (0xff & (par2 >> 8))])
        buf.extend([(0xff & id), (0xff & len), (0xff & cmd)])
        buf.extend(buf1)

	## CheckSum Reference Point
        sum = 0x00
        for b in buf:
            sum += b
        sum = sum - 0x55 - 0x55
        sum = ~sum
        buf.append(0xff & sum)
        serialHandle.write(buf)
    except Exception as e:
        print(e)


while True:
    try:
        servoWriteCmd(1,1,0,1000)
        # ServoID=1 CMD=1 Position=0 Time=1000
        time.sleep(1.1)
        servoWriteCmd(1,1,1000,2000)
        time.sleep(2.1)
    except Exception as e:
        print(e)
        break
