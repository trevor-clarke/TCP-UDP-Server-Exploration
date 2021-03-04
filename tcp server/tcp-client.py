import socket
import base64
import math
import time
import struct


UDP_IP = "127.0.0.1"
UDP_PORT = 8888

MAX_SIZE = 4096

def log(message):
    print("[Client]: ", message)

def send_file_details(s, file_name, packets_expected):
        message = "a1a1"
        message += str(packets_expected)
        message += "a1a1"
        print("this is just before", file_name)
        message += str(file_name)
        message += "a1a1"


        byte_message = message.encode('latin-1')

        send_msg(s, byte_message)

def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def send_file(file_name, data):
    log("Starting process. Converting file to Base 64.")
    data_b64 = base64.encodebytes(data)

    # print("full data")
    # print(data)

    log("Calculating expected number of packets:")
    packets_expected = math.ceil(len(data_b64)/MAX_SIZE)
    log(packets_expected)

    log("Establishing connection with the server.")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((UDP_IP, UDP_PORT))

    #Let the server know how many packets we are about to send
    send_file_details(s, file_name, packets_expected)

    #log(data_b64)

    i = 0
    count = 0
    while i + MAX_SIZE <= MAX_SIZE * packets_expected:

        current_packet = data_b64[i:i + MAX_SIZE]
        send_msg(s,current_packet)

        # Move the current window over, so we send next chunk of data
        i += MAX_SIZE
        if packets_recieved%max(1,packets_expected/100.0) == 0:
            log(i/MAX_SIZE)
        count += 1
    #log(count)
    log("All " + str(packets_expected) + " packets sent.")
    s.close()


def send(file_path):
    #Load file into variable, initiate transfer
    image = open(file_path, 'rb')
    img_read = image.read()
    file_name = file_path.split("/")[-1]
    log("File name extracted as " + file_name)
    send_file(file_name, img_read)
    #log("Message sent!")


file_path = input("Full relative path: ")
send(file_path)
