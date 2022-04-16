import socket
from struct import pack
import struct
from time import sleep
import uuid

PORT = -9
HOST = "127.0.0.1"

SEGMENT_BITS = 0x7F
CONTINUE_BIT = 0x80

class Offline:
    bytes = b"OfflineClient:"

def read_varint(b):
    value = 0
    position = 0
    currentByte = 0

    byte = 0
    while True:
        currentByte = b[byte]
        value |= (currentByte & SEGMENT_BITS) << position

        if ((currentByte & CONTINUE_BIT) == 0): 
            print("BYTE: ", byte)
            break

        position += 7
        byte += 1

    return value

def pack_string(s):
    encoded = bytes(s, encoding="utf-8")

    return pack_varint(len(s)) + encoded

def pack_varint(value):


    out = b""

    while (True):
        if ((value & ~SEGMENT_BITS) == 0):
          out += struct.pack("B", value)
          return out
        
        out += struct.pack("B", (value & SEGMENT_BITS) | CONTINUE_BIT)
       
        value >>= 7
  
    

def login():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

# HANDSHAKE
        data = pack_varint(758) + pack_string("127.0.0.1") + struct.pack("H",25565) + pack_varint(2)
        id = pack_varint(0)
        l = pack_varint(len(data + id))
        s.send(l + id + data)


        id = pack_varint(0)
        data = pack_string("steph")
        l = pack_varint(len(data + id))
        s.send(l + id + data)

        # s.send(pack_string("no_name") )
        data = s.recv(1024)
        print(data)

        # print(read_varint(data))
        # set compression
        # id = pack_varint(3)
        # data = pack_varint(0)
        # l = pack_varint(len(data + id))
        # s.send(l + id + data)

        data = s.recv(1024)
        print(data)
        bts = (read_varint(data))
        print(bts)
        id = read_varint(data[2:])
        print(id)
        name = str(data[2 + 2 + 16:])
        uid = uuid.uuid3(Offline(), "steph")
        # length = read_varint(data)
        print(uid, name)

       

if __name__ == "__main__":
    login()