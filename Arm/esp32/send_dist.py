
import socket
import struct
import sys
 
# this method is to send the mushroom distance to the pi
#
def send_dist(z, addr="172.20.10.3", port=5002):
    # open a socket to connect 
    #
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
    
    # connect to the given ip
    # 
    try:
        print("trying to connect to {} : {}".format(addr, port))
        sock.connect((addr, port))
        print("connected!!!!")
    
        # pack the value the send it via the socket
        #
        z_data = struct.pack("f", z)
        sock.send(z_data)
        sock.close()
        
        return 1
    except OSError as err :
        print("something went wrong {}".format(err))
        sock.close()
        return 1