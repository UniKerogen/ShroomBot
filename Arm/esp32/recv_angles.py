
# this is to test for receiving angles from a website
#

import struct
import socket
import network

def recv_on(host, port):

    # initiate angles list
    #
    angles = []
    
    #
    # initiate socket 
    #
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # set timeout for socket
    #
    # sock.settimeout(30)

    # bind socket to ip and port
    #
    sock.bind((host, port))
    
    # listen to connections
    #
    sock.listen(1)
    
    while True:

        try:
            # accept incoming connection
            #
            conn, addr = sock.accept()
            # receive data while there is a connection
            #
            while True:
                data = conn.recv(4)
                
                # check if no data was sent and break
                #
                if (data == b''):
                    conn.close()
                    break
                
                # convert angles from bytes to float
                #
                data_f = struct.unpack("f", data)[0]
                angles.append(data_f)
                                
                # if no data break
                # 
                if not data:
                    conn.close()
                    break


            # close the socket
            #
            sock.close()
            
        except KeyboardInterrupt:
            sock.close()
        except OSError as err:
            print("time out!!!")
            sock.close()
            return(angles, '')
            
        return (angles, addr)
            
    
