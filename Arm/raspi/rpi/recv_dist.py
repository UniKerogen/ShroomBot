
# this method receives the z from the esp
#

import socket
import struct
import sys

def recv_dist(host="172.20.10.3", port=5002):
    #
    #
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

        sock.bind((host, port))
        sock.listen(1)
        
        #sock.settimeout(30)

        # initiate z distance 
        # 
        dist = 0
    
        while True:

            try:
                #accept connection
                #
                conn, addr = sock.accept()
                

                # verify connection
                #
                print("{} is connected".format(addr))
                
                while True:
                    
                    
                    # receive data
                    #
                    data = conn.recv(1024)
                    
                    # check if no data was sent and exit
                    #
                    if (data == b''):
                        conn.close()
                        sock.close()
                        break
                    
                    # convert distance from bytes to float
                    #
                    dist = struct.unpack("f", data)[0]
                    
                    # if no data break
                    # 
                    if not data:
                        conn.close()
                        sock.close()
                        break
                    
            except OSError as err:
                print(err)
                sock.close()
                break
                
    return dist