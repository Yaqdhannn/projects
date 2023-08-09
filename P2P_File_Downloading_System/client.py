import sys
import socket
import threading
import os
import time

SERVER = socket.gethostbyname(socket.gethostname())
HEADER = 1024
MAX_THREADS = 10
# latencies in format: [[port1,latency1][port2,latency2]...]
LATENCIES = []
LOAD = 0
DISCONNECT = False

# my path example:
# /home/almaa009/c1/
# /home/almaa009/c2/
# /home/almaa009/c3/

# credit: https://github.com/mdelatorre/checksum/blob/master/ichecksum.py
# An Internet checksum algorithm using Python.
# This program is licensed under the GPL; see LICENSE for details.
# This procedure can be used to calculate the Internet checksum of
# some data.  It is adapted from RFC 1071:
#
# ftp://ftp.isi.edu/in-notes/rfc1071.txt
#
# See also:
#
# http://www.netfor2.com/ipsum.htm
# http://www.netfor2.com/checksum.html
def ichecksum(data, sum=0):
    """ Compute the Internet Checksum of the supplied data.  The checksum is
    initialized to zero.  Place the return value in the checksum field of a
    packet.  When the packet is received, check the checksum, by passing
    in the checksum field of the packet and the data.  If the result is zero,
    then the checksum has not detected an error.
    """
    # make 16 bit words out of every two adjacent 8 bit words in the packet
    # and add them up
    for i in range(0,len(data),2):
        if i + 1 >= len(data):
            sum += ord(data[i]) & 0xFF
        else:
            w = ((ord(data[i]) << 8) & 0xFF00) + (ord(data[i+1]) & 0xFF)
            sum += w

    # take only 16 bits out of the 32 bit sum and add up the carries
    while (sum >> 16) > 0:
        sum = (sum & 0xFFFF) + (sum >> 16)

    # one's complement the result
    sum = ~sum

    return sum & 0xFFFF

# send message to server function
def send_msg(client, msg):
    msg = msg.encode("utf-8")
    msg_len = len(msg)

    # send msg of size HEADER giving the length of upcoming msg
    send_len = str(msg_len).encode("utf-8")
    offset = HEADER - len(send_len)
    # add offset as bytes
    send_len += b" " * offset

    # send length first, then actual message
    client.send(send_len)
    client.send(msg)

# return load of this client
def current_load():
    return (threading.activeCount()-2)

# pick client port with minimum load    
def get_minimum_load(lst):
    minimum_port = lst[0][0]
    minimum_val = lst[0][1]
    for i in range(len(lst)):
        if lst[i][1] < minimum_val:
            minimum_val = lst[i][1]
            minimum_port = lst[i][0]
    
    return minimum_port

# select peer/client taking load and latency in account
def select_peer(clients_with_file):
    algo = []
    for i in range(len(clients_with_file)):    
        port = int(clients_with_file[i])
        latency = 0
        # check if ports exist in latency list
        port_exist = False
        for j in range(len(LATENCIES)):
            if int(LATENCIES[j][0]) == port:
                port_exist = True
                latency = int(LATENCIES[j][1])

        # return -1 if port not in latency list
        if(port_exist == False):
            return -1
        
        load = get_load_specific(port)
        # algorithm will be latency*load for each client port
        lst = [port, (latency*load)]
        algo.append(lst)

    client = get_minimum_load(algo)
    return client

# let program sleep depending on client latency to emulate delay
def emulate_latency(port):
    latency = 0
    for i in range(len(LATENCIES)):
        if int(LATENCIES[i][0]) == port:
            latency = int(LATENCIES[i][1])
    
    # convert from ms to s
    latency *= 0.001
    time.sleep(latency)

# get load of a specific client
def get_load_specific(client_port):
    # connect to client
    port = client_port
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((SERVER, port))

    # send "GetLoad" command to client
    send_msg(client_sock, "GetLoad")
    msg_recv = int((client_sock.recv(4)).decode("utf-8"))

    client_sock.close()
    return msg_recv

# get load of any active client
def get_load(sock):
    send_msg(sock, "GetLoad")

    # recieve nodes in format: "port1,port2,port3,..."
    msg_recv = sock.recv(4096).decode("utf-8")


    print("current active client(s) port number: ")
    print(f"{msg_recv}\n")

    lst = msg_recv.split(",")
    port = input("type port number of client you want the load of: ")
    if port not in lst:
        print("port does not exist..")
        return -1
    
    # connect to client
    port = int(port)
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((SERVER, port))

    # send "GetLoad" command to client
    send_msg(client_sock, "GetLoad")
    msg_recv = int((client_sock.recv(4)).decode("utf-8"))

    print(f"Load for chosen client is: {msg_recv}")
    client_sock.close()
    return msg_recv

# loop through latencies.txt and import latency for port 3000 to 3100
def import_latencies(directory_path):
    #file_path = directory_path + "latencies.txt"
    filename = "latencies.txt"
    file1 = ""
    try:
        file1 = open(filename, 'r')
    except FileNotFoundError as e:
        print(f"latency file does not exist in folder\n")
        return -1
          
    Lines = file1.readlines()
    
    for line in Lines:
        lst = line.split(",")
        # remove whitespace
        lst[1] = lst[1].replace("\n", "")
        LATENCIES.append(lst)

# download file from client
def download(sock, directory_path, client_port):
    lst = find(sock)
    if(lst == -1):
        return -1

    filename = lst[0]
    clients_with_file = lst[1]

    # client cant download from themselves
    if str(client_port) in clients_with_file:
        clients_with_file.remove(str(client_port))
    
    if(clients_with_file == []):
        print(f"file {filename} only exists in current machine.. can't download")
        return -1

    port = select_peer(clients_with_file)
    if(port == -1):
        print(f"client port does not exist in latency file...")
        print(f"port number should be 3000-3100 for client")
        return -1

    print(f"port selected with minimum load and latency: {port}\n")

    # connect to client
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((SERVER, port))

    # send file name to client
    send_msg(client_sock, filename)

    # create and write data to file
    file_path = directory_path + filename
    file = open(file_path, "w")
    
    # store data of file while reading
    data = ""
    while(True):
        msg_len = int(client_sock.recv(HEADER).decode("utf-8"))
        msg_recv = (client_sock.recv(msg_len)).decode("utf-8")

        # if reached end of file
        if("[ENDOFFILE]" in msg_recv):
            # write last line without [ENDOFFILE]
            file.write(msg_recv[:-11])
            data += msg_recv[:-11]
            break

        file.write(msg_recv)
        data += msg_recv

    # emulate the latency delay
    print("\ndownloading...")
    emulate_latency(port)

    # GET CHECKSUM OF FILE
    msg_len = int(client_sock.recv(HEADER).decode("utf-8"))
    checksum_of_sender = int((client_sock.recv(msg_len)).decode("utf-8"))

    # data += "testing" #TEST: checksum will detect error if data is wrong

    # compare checksum and data, if result not 0 then error
    val = ichecksum(data,checksum_of_sender)

    # if error, delete file and return
    if(val != 0):
        print('--checksum has detected an error--')
        print('--download failed--')
        os.remove(file_path)
        file.close()
        client_sock.close()
        return -1
    
    print('--download complete--')
    file.close()
    client_sock.close()

    # send files update to tracking server
    files =  os.listdir(directory_path)
    msg = str(client_port) + "," + ",".join(files)

    send_msg(sock, "UpdateList")
    send_msg(sock, msg)

# communicate with server to return a nodes that store a specific file
def find(sock):
    filename = input("name of file you want to find/download (with file extention): ")

    # send filename to tracking server
    send_msg(sock, "Find")
    send_msg(sock, filename)

    # recieve nodes in format: "port1,port2,port3,..."
    msg_recv = sock.recv(4096).decode("utf-8")

    if msg_recv == "NOTFOUND":
        print("file is not found\n")
        return -1
    else:
        print("client(s) port number with that file: ")
        print(f"{msg_recv}\n")
        lst = msg_recv.split(",")
        return [filename,lst]

# print options to the user
def options():
    print("1. Find: will returns the list of nodes which store a file")
    print("2. Download: will download a given file; once downloaded it becomes shareable from that peer")
    print("3. GetLoad: returns the load at a given peer requested from another peer")
    print("4. UpdateList: provides the list of files stored at a given peer to the server")
    print("5. disconnect: disconnect from server\n")

# listen thread handler that checks client's commands
def listening_handler(conn, addr, directory_path):
    print(f"\nnew connection from {addr}")

    while True:
        msg_len = conn.recv(HEADER).decode("utf-8")
        if msg_len:
            # get length of msg to be recieved
            msg_len = int(msg_len)
            # get message
            msg = conn.recv(msg_len).decode("utf-8")

            if msg == "GetLoad":
                load = str(current_load())
                conn.send((load).encode("utf-8"))
                break
            else:
                # msg will be the filename
                file_path = directory_path + msg
                file = open(file_path, 'r')
                data = ""
                line = file.read(1024)
                data += line

                # send data to client in a loop
                while(line):
                    send_msg(conn, line)
                    line = file.read(1024)
                    data += line
                
                # send msg to show end of file
                send_msg(conn, "[ENDOFFILE]")
                file.close()
                # send checksum
                checksum = ichecksum(data)
                send_msg(conn, str(checksum))
                print('--file transfer complete--')
                print("type command: ")
                break

    conn.close()
    return

# listen thread that listens for clients connections
def listen(sock, client_port, directory_path):
    # tcp connection to listen for requests from other clients
    sock.bind((SERVER, client_port))
    sock.listen()
    print(f"client listening on PORT: {client_port}")
    while True:
        # stop listening if client wants to disconnect
        if(DISCONNECT):
            sock.close()
            return
        # only accept request if active clients less than MAX_THREADS
        if(threading.activeCount()-1 < MAX_THREADS):
            conn, addr = sock.accept()
            # create a thread for each connection
            thread = threading.Thread(target=listening_handler, args=(conn, addr, directory_path))
            thread.start()
        
# connect thread that connects to tracking server and takes commands from user
def connect(sock, trackingserver_port, client_port, directory_path):
    # tcp connection to tracking server
    sock.connect((SERVER, trackingserver_port))
    print(f"connected to tracking server on PORT: {trackingserver_port}")

    # send files to tracking server
    files =  os.listdir(directory_path)
    msg = str(client_port) + "," + ",".join(files)

    send_msg(sock, "UpdateList")
    send_msg(sock, msg)

    # import latency from latencies.txt to program
    if(import_latencies(directory_path) == -1):
        return -1

    # print options to client
    options()

    while True:
        command = input("type command: ")
        if command == "UpdateList":
            # send files to tracking server
            files =  os.listdir(directory_path)
            msg = str(client_port) + "," + ",".join(files)

            send_msg(sock, command)
            send_msg(sock, msg)

        elif command == "Find":
            find(sock)
        
        elif command == "Download":
            download(sock, directory_path, client_port)
        
        elif command == "GetLoad":
            get_load(sock)

        elif command == "disconnect":
            send_msg(sock, command)
            send_msg(sock, str(client_port))
            DISCONNECT = True
            sock.close()
            return

        else:
            # if command is wrong
            print("unknown command\n")
            options()

if __name__=="__main__":
    # arguments format: [TRACKINGSERVER_PORT][DIRECTORY_PATH][CLIENT_PORT]
    # check if not all arguments entered
    if(len(sys.argv) < 4):
        print(f"expected 3 arguments, recieved {len(sys.argv) -1}... exiting program")
        sys.exit(-1)
    # check if client port is incorrect
    if(int(sys.argv[3]) > 3100 or int(sys.argv[3]) < 3000):
        print(f"client port should be 3000-3100, recieved {sys.argv[3]}... exiting program")
        sys.exit(-1)

    trackingserver_port = int(sys.argv[1])
    directory_path = str(sys.argv[2])
    client_port = int(sys.argv[3])

    sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # two threads: listen and connect
    threading.Thread(target=connect, args=(sock1, trackingserver_port, client_port, directory_path)).start()
    threading.Thread(target=listen, args=(sock2, client_port, directory_path)).start()
