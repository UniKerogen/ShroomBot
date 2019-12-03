
# this is a claas to use the Chinese servos easier
#
import struct
import machine
import time as time_mo


class Servo:
    
    # constructor
    #
    def __init__(self, TX, RX):
        self.conn = self.uart_conn(TX, RX)
  
    
    #---------------------- PUBLIC METHODS -------------------------------#
    
    # this method takes an ID
    # to get the degree mult position with 0.24
    # to get the position from the degrees  divide it  0.24 
    #
    def move(self, ID, position, time):
        start = time_mo.time()
        
        # initialize the packet
        #
        buf = [0] * 10

        # get the high and low bytes for both time and position
        #
        (pos_high, pos_low) = self.high_low_byte(position)
        (time_high, time_low) = self.high_low_byte(time)

        # setup the packet
        #
        buf[0] = b'\x55'
        buf[1] = b'\x55'
        buf[2] = bytes([ID])
        buf[3] = b'\x07'
        buf[4] = b'\x01'
        buf[5] = bytes([int(pos_low)])
        buf[6] = bytes([int(pos_high)])
        buf[7] = bytes([int(time_low)])
        buf[8] = bytes([int(time_high)])

        # calculate the checksum then assign it to the
        #
        checksum_num = [self.checksum(buf, len(buf)-1)]
        checksum_byte = bytes(checksum_num)
        buf[9] = checksum_byte

        # send the packet to the motor
        #
        self.write(buf)

        end = time_mo.time()


    # this method is used to set the ID of each servo, 
    #
    def set_id(self, ID):
        
        # initialize the packet
        #
        buf = [0] * 7

        # setup the packet
        #
        buf[0] = b'\x55'
        buf[1] = b'\x55'
        buf[2] = b'\xFE'
        buf[3] = b'\x04'
        buf[4] = b'\x0D'
        buf[5] = bytes([ID])

        # calculate the checksum then assign it to the
        #
        checksum_num = [self.checksum(buf, len(buf)-1)]
        checksum_byte = bytes(checksum_num)
        buf[6] = checksum_byte

        # send the packet to the motor
        #
        self.write(buf)


    # center the servo make it 120 degrees
    #    
    def center(self, ID):
        self.move(ID, 500, 500)
    
    
    #---------------------- PRIVATE METHODS -------------------------------#
    
    # initiate the UART connection where it takes the TX and RX pins
    #
    def uart_conn(self, TX, RX):
        return machine.UART(2, baudrate=115200, rx=RX, tx=TX, timeout=10)

    
    # calculate the checksum for the packet
    # sums all bytes from [3: LAST-1]
    # then takes the ones comp to assign it to the last byte in the packet
    #
    def checksum(self, ibuf, maxindx):

        # initialize the sum
        #
        sum = 0

        # sum the bytes except the fries two
        #
        for i in range(2, maxindx):
            byte = struct.unpack('>H', bytearray(b'\x00'+ibuf[i]))[0]
            sum += byte

        # take the one's comp of the sum and assign it to the last byte
        #
        ibuf[maxindx] = self.ones_comp(sum)
        
        return ibuf[maxindx]


    # get ones comp of an 8bit number by getting the byte
    # then XOR with 0xFF
    #
    def ones_comp(self, num):
        byte = struct.pack('<H', num)
        
        return (byte[0]^0xFF)


    # take a 16bit number and return a tuple of two bytes as high and low
    #
    def high_low_byte(self, num):
        byte = struct.pack('<H', num)
        
        return (hex(byte[1]), hex(byte[0]))
    
    
    # this method writes the buffer to the servo 
    #
    def write(self, buf):
        for i in range(0, len(buf)):
            self.conn.write(buf[i])
