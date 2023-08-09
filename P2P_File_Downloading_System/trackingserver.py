import sys
import socket
import threading

SERVER = socket.gethostbyname(socket.gethostname())
HEADER = 1024
MAX_THREADS = 10

# each client server array in the format: [Client ID, Port, [file1, file2, ...]]
CLIENTS = []
id_counter = 1

# generate an id for each client
def create_id():
    global id_counter

    id = id_counter
    # increment id
    id_counter += 1

    return id

# return port number of all active clients
def all_clients():
    lst = []
    for i in range(len(CLIENTS)):
        lst.append(str(CLIENTS[i][1]))
    
    return lst

# check if client port exists
def client_exists(port):
    exists = False
    for i in range(len(CLIENTS)):
        # if port num exists in CLIENTS array
        if(CLIENTS[i][1] == port):
            exists = True
    
    return exists

# remove client from clients list
def disconnect_client(port):
    for i in range(len(CLIENTS)):
        # remove client from list
        if(CLIENTS[i][1] == int(port)):
            CLIENTS.remove(CLIENTS[i])
            break

# update clients list
def update_list(msg_list):
    client_port = int(msg_list[0])
    updated_files = msg_list[1:]

    if(client_exists(client_port)):
        # loop through client list and update client files
        for i in range(len(CLIENTS)):
            if(CLIENTS[i][1] == client_port):
                CLIENTS[i][2] = updated_files
                break
    else:
        # create new client element
        new_client = [create_id(), client_port, updated_files]
        CLIENTS.append(new_client)

# find a specific file from clients list
def find_file(file):
    nodes_list = []
    # loop through client list and find file
    for i in range(len(CLIENTS)):
        for j in range(len(CLIENTS[i][2])):
            if(CLIENTS[i][2][j] == file):
                # append client port num to list
                nodes_list.append(str(CLIENTS[i][1]))
    
    return nodes_list

# handle each client connection
def handler(conn, addr):
    print(f"new connection from {addr}")
    
    while True:
        msg_len = conn.recv(HEADER).decode("utf-8")
        if msg_len:
            # get length of msg to be recieved
            msg_len = int(msg_len)
            # get message
            msg = conn.recv(msg_len).decode("utf-8")

            if msg == "disconnect":
                # get length of msg to be recieved
                msg_len = int(conn.recv(HEADER).decode("utf-8"))
                # get message
                msg = conn.recv(msg_len).decode("utf-8")
                # msg will be client port number
                disconnect_client(msg)

                print(f"client {addr} {msg} disconnected")
                print(f"Client list updated. Current active clients: ")
                print(all_clients())
                break

            elif msg == "UpdateList":
                # get length of msg to be recieved
                msg_len = int(conn.recv(HEADER).decode("utf-8"))
                # get message
                msg = conn.recv(msg_len).decode("utf-8")
                
                # msg list will be in format: [client_port, file1, file2, file3, ...]
                msg_list = msg.split(",")
                update_list(msg_list)

                print(f"Client list updated. Current active clients: ")
                print(all_clients())
            
            elif msg == "Find":
                # get length of msg to be recieved
                msg_len = int(conn.recv(HEADER).decode("utf-8"))
                # get message
                msg = conn.recv(msg_len).decode("utf-8")
                
                nodes_list = find_file(msg)
                msg = ",".join(nodes_list)

                # send back node list to client
                if(nodes_list == []):
                    conn.send("NOTFOUND".encode("utf-8"))
                else:
                    conn.send(msg.encode("utf-8"))
            
            elif msg == "GetLoad":
                lst = all_clients()
                msg = ",".join(lst)
                conn.send(msg.encode("utf-8"))           
    
    # close connection
    conn.close()

if __name__=="__main__":
    # check if port num not entered
    if(len(sys.argv) < 2):
        print("PORT not entered as argument... exiting program")
        sys.exit(-1)

    PORT = int(sys.argv[1])

    # tcp connection
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER, PORT))

    print(f"tracking server starting on PORT: {PORT}")

    # listen for a connection
    server.listen()
    print(f"tracking server listening on IP: {SERVER}")
    while True:
        # only accept request if active clients less than MAX_THREADS
        if(threading.activeCount()-1 < MAX_THREADS):
            conn, addr = server.accept()
            # create a thread for each connection
            thread = threading.Thread(target=handler, args=(conn, addr))
            thread.start()

            print(f"{threading.activeCount()-1} active connection(s)")
