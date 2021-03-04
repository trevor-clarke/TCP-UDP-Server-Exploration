import socket
import base64
import math

UDP_IP = "127.0.0.1"
UDP_PORT = 8888



def send_file(name, data):
    print("converting to base 64")
    b64 = base64.encodebytes(data)

    num_pack = math.ceil(len(b64)/65507)
    print("num should be ", num_pack)
    print("packet len", ("111" + str(num_pack)).encode('latin-1'))
    send_bytes(("a1a1" + str(num_pack) + "a1a1" + name).encode('latin-1'))


    cnt = 0
    while len(b64)> 0:

        send_bytes(b64[0:65507]) # not sure if this should be :-1 less
        b64 = b64[65507:]
        cnt+=1

    print(cnt)

def send_bytes(bytes):
    print("sending bytes")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.sendto(bytes, (UDP_IP, UDP_PORT))


file_name = 'clouds.jpg'
image = open('pics/' + file_name, 'rb')
img_read = image.read()
send_file(file_name, img_read)
print("message sent")
