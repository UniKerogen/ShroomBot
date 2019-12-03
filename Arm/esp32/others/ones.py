import struct

def onescomp(num):
   mm=struct.pack('<H', num)
   return (mm[0]^0xFF) 

def highlowbyte(num):
   mm=struct.pack('<H', num)
   return (hex(mm[1]), hex(mm[0]))


def takesum(buf):
   tmp=0
   for i in range(2, len(buf)):
       print(buf[i])
       p=struct.unpack('>H', bytearray(b'\x00'+buf[i]))[0]
#       p=struct.unpack('>H', buf[i])[0]
       tmp+=p
   return tmp

if __name__ == '__main__':
    buf = [0]*7
    buf[0] = b'\x55'
    buf[1]=b'\x55'
    buf[2]=b'\xFE'
    buf[3]=b'\x04'
    buf[4]=b'\x0D'
    buf[5]=b'\x01'
    aa=takesum(buf[0:6])
    buf[6]=onescomp(aa)
    print(buf)

    pos=1000
    tim=1000
    buf=[0]*10
    buf[0]=b'\x55'
    buf[1]=b'\x55'
    buf[2]=b'\x01'
    buf[3]=b'\x07'
    buf[4]=b'\x01'
    (hb,lb)=highlowbyte(pos)
    buf[5]=lb
    buf[6]=hb
    (hb,lb)=highlowbyte(tim)
    buf[7]=lb
    buf[8]=hb
    aa=takesum(buf[0:9])
    buf[9]=onescomp(aa)
    print(buf)


