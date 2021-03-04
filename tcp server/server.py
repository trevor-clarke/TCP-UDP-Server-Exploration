import socket
import base64

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 8888))
s.listen(1)

#####
## HELPER FUNCTIONS
#####

def log(message):
    print("[Client]: ", message)

def merge_byte_array(data):
        # output = b''
        # cnt = 0
        # for x in arr:
        #     if cnt%100 == 0:
        #         log("Merged " + str(cnt) )
        #     output = b''.join([output, x])
        #     cnt += 1


    output_b = b''.join(data)

    # print(output)
    # print("ahhh")
    # print(output_b)
    # print("ahhhh")
    # print(output == output_b)
    return output_b


#given a file name, and the bytes for that file, save it
def bytes_to_file(file_name, packets):
    packets_to_decode = packets + b'==='
    decoded_file = base64.decodebytes(packets_to_decode)
    image_result = open("downloads/" + file_name, 'wb')
    image_result.write(decoded_file)
    image_result.close()

def data_recieve_complete(file_name, packets):
    log("Merging array into a single byte object.")
    packets = merge_byte_array(packets)
    log("Merging complete. Saving file.")
    # print("raw data")
    # print(packets)
    bytes_to_file(file_name, packets)
    log("File saving complete.")


#####
## MAIN SERVER LOOP
#####
while True:
    conn, addr = s.accept()

    packets_expected = 0
    packets_recieved = 0
    packets = []
    file_name = ""

    while True:
        data = conn.recv(4096)

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
            if packets_recieved%1 == 0:
                log("Recived: " + str(packets_recieved) + " out of " + str(packets_expected) + " size: " +  str(len(data)))
            # print("data", data)
            packets.append(data)
            packets_recieved += 1
