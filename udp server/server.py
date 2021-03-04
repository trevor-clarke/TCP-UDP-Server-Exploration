import socket
import base64

UDP_IP = "0.0.0.0"
UDP_PORT = 8888

#bind to the port
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))


def merge_byte_array(arr):
    output = b''
    for x in arr:
        output += x
    return output

#given a file name, and the bytes for that file, save it
def bytes_to_file(f_name, bytes):
    image_64_decode = base64.b64decode(bytes+ b'===')

    image_result = open("downloads/" + f_name, 'wb')
    image_result.write(image_64_decode)
    image_result.close()

pack_len = 0
pack_rec = 0
packet = []
file_name = ""

while True:

    data, addr = sock.recvfrom(65507) # buffer size is 1024 bytes

    #look for the key value 'a', this val actually needs to be more complicated TODO::::
    if b'a1a1' in data[0:4]:
        print("starting file")
        data = data.decode('latin-1')

        #Split details message
        split_data = data.split("a1a1")
        pack_len = int(split_data[1])
        file_name = split_data[2]

        #Reset other values from previous time
        pack_rec = 0
        packet = []

    #If not packet details, must be part of a file we are recieving
    elif len(data)>= 0:
        packet.append(data)
        pack_rec += 1
        if pack_rec%1 == 0:
            print(len(data), pack_len, pack_rec)
        if pack_len == pack_rec:
            print("merging array")
            packet = merge_byte_array(packet)
            print("done merging, converting and saving")
            bytes_to_file(file_name, packet)
