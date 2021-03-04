import socket
import base64
import math
import time

UDP_IP = "174.91.123.117"
UDP_PORT = 8888
file_name = input("Filename: ")

def send_file(name, data):
    print("Converting to base 64")
    b64 = base64.encodebytes(data)

    num_pack = math.ceil(len(b64)/65507)
    print("num should be", num_pack)
    print("packet len", ("111" + str(num_pack)).encode('latin-1'))
    send_bytes(("a1a1" + str(num_pack) + "a1a1" + name).encode('latin-1'))

    count = 0
    max_size = 65507
    i = 0
    while i <= len(b64):
        send_bytes(b64[i:i + max_size]) # not sure if this should be :-1 less
        time.sleep(5 / 1000)
        i += max_size
        count += 1
        print(count)

    print("Total sent:", count)

def send_bytes(bytes):
    print("sending bytes...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.sendto(bytes, (UDP_IP, UDP_PORT))

image = open(file_name, 'rb')
img_read = image.read()
send_file(file_name, img_read)
print("Message sent!")