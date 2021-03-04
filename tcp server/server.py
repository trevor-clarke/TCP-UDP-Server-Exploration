import socket
import base64
import struct

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 8888))
s.listen(1)

#####
## HELPER FUNCTIONS
#####

def log(message):
    print("[Client]: ", message)

#given a file name, and the bytes for that file, save it
def bytes_to_file(file_name, packets):

    packets_to_decode = b''.join([packets,b'==='])
    decoded_file = base64.decodebytes(packets_to_decode)
    image_result = open("downloads/" + file_name, 'wb')
    image_result.write(decoded_file)
    image_result.close()

def data_recieve_complete(file_name, packets):
    log("Merging array into a single byte object.")
    packets = bytes(packets)
    log("Merging complete. Saving file.")

    bytes_to_file(file_name, packets)
    log("File saving complete.")

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

#####
## MAIN SERVER LOOP
#####
while True:
    conn, addr = s.accept()

    packets_expected = 0
    packets_recieved = 0
    packets = bytearray()
    file_name = ""

    while True:
        data = recv_msg(conn)

        # Once all data has been sent
        if not data:
            data_recieve_complete(file_name, packets)
            conn.close()
            break

        # Assuming data is sent, check for starting header 'a1a1'
        IDENTIFIER = b'a1a1'
        if IDENTIFIER in data[0:4]:

            log("Recieving new file.")

            data = data.decode('latin-1')

            # print("full data")
            # print(data)
            split_data = data.split("a1a1")

            packets_expected = int(split_data[1])
            file_name = split_data[2]

            log(str(packets_expected)  + " " +file_name)

            #Reset other values from previous time
            packets_recieved = 0
            packets = []

        #If not packet details, must be part of a file we are recieving
        else:
            # print("data", data)
            packets.extend(data)
            packets_recieved += 1
            if packets_recieved%math.max(1,packets_expected/100) == 0:
                log("Recived: " + str(packets_recieved) + " out of " + str(packets_expected) + " size: " +  str(len(data)))
