AlYaqdhan Al Maawali

HOW TO RUN:
to run code, navigate through terminal the project directory and run server first by typing:
python3 trackingserver.py [server_port] 
[server_port] being the port number bigger than 2000 (or any unoccupied port). In another terminal, run the client(s) by typing:
python3 client.py [server_port] [client_shared_directory_path] [client_port]

NOTE: make sure your client_port is between 3000-3100 or the program will not run. Make sure different clients have different port numbers (including the server having a different port number). Make sure latencies.txt is in the same directory as client.py so importing latencies happen successfuly. Run the server in a seperate terminal and run each client in a seperate terminal. Make sure the client_shared_directory_path is in the same format as: /home/almaa009/c1/
c1 being the shared folder
client_shared_directory_path tested on Ubuntu only so run on Ubuntu
When running the program again, run server and client(s) using port numbers different than the one used recently.

To run the tests, type:
python3 -m unittest tests.py

After running both the server and client(s) in different terminals using different ports, you will see a message in the server terminal that there is an active connection(s). Head to the client terminal and you will see the list of options
you can type. If you type a wrong command the program will list the options again.
1. Find: program will ask you to type name of file you want to find (with extention). Example: hello.txt. The program will then print the port number(s) of the current active client(s) that share that file.
2. Download: program will ask you to type name of file you want to find (with extention). Example: hello.txt. The program will then print the port number(s) of the current active client(s) that share that file. Then, program will print the client picked taking load and latency into account. When download is complete a message stating that will be printed to the client downloaded, and a message will be printed to the client uploading the file that their is a new connection and that their file transfer is complete. If client wants to Download a file that doesn't exist a message will be printed. If a client wants to download a file that they only own then a message will also be printed. If the file is corrupted during the process then a message will be printed and the download will be unsuccessful.
3. GetLoad: program will ask you to type the port number of an active client you want to know the load of and prints the load. If client port number does not exist then a message is printed.
4. UpdateList: client will send their updated list to the server. This command is called automatically everytime a client downloads a new file. A message is printed in the server's terminal when a client updates their list.
5. disconnect: disconnect from the tracking server. A message is printed in the tracking server's terminal of the updated client list (the client that disconnected is removed from the list).

DESIGN DOC:
the server and client communicate with each other using tcp connection.
both the server and the client will be the current machine the user is using. The max threads the server will create is 10, so 10 clients maximum can connect to the server at once. if a client connected when 10 clients are already connected, their message will be blocked until one of the other clients leave. Once a connection has been established, the server will call the handler function which is a loop receiving messages from the client. the client will send the msg length first to the server then the actual message, so the server knows how much byte to expect when reading the message.
For almost each command, there is a function that is called for that command. There are also global variables in this system, such as the id_counter that tracks the next id for the next client and a clients list that stores client's information in the format: [Client ID, Port, [file1, file2, ...]]

Each client communicates with another client using tcp connection as well. When client.py is ran, two main threads are created: connect and listen. Connect is a thread that connects to the tracking server, and listen is a thread that listens for connections from other clients and when a connection is established, it deals with that connection in a new seperate thread up to MAX_THREADS. 

connect: after the connect thread connects to the tracking server, it imports latencies.txt and stores it in a global list, asks the server to UpdateList, then asks the user for a command in a loop until the user disconnects.

listen: after a connection is established between the client and another client in a new thread, the client will expect two messages: either the name of the file the other client wants to download or the load of the client. There are helper functions that the client calls to deal with each command.

GetLoad: when a client asks another client for their load, the client gets it by counting their active threads. If multiple clients are communicating with a single client at the same time then that client's load should be higher since the thread count is higher.

download: when client wants to download a file, it asks the tracking server for the clients that have that file, then for each client it multiples their load with their latency (load*latency), then the client with the minimum value is selected and communicated with. the client then will recieve the file data in a loop until the other client sends "[ENDOFFILE]" which then the client knows that they reached the end. the other client will also send their checksum value of the file and the current client compares their checksum value with the other client. If an error is detected then the file will not be downloaded. Otherwise, the download will be complete. Latency is also emulated using python's time.sleep() function. Download time difference can be observed when downloading files from different clients. 

Fault Tolerance: there are numerous error handling methods used in this program. First of all, the program is tested throughly using unit tests and manual testing that the program will not crash. Secondly, Download files corruption is detected by checksum, if corruption is found then the download will not happen successfully. if a peer disconnects, then the server is informed about that and an update to the client's list is made so that other clients do not try and download from a disconnected peer. There are also other error handling situations such as client port not being between 3000-3100, latencies.txt not existing, client wanting to download a file that does not exist, client wants a load of a client that does not exist, and more that can be observed while using the program.

E. Testing description, including a list of cases attempted (which could also include negative cases) and the results.

tests could be found at tests.py. the tests test the functions:
1. create_id()
2. all_clients()
3. client_exists()
4. disconnect_client()
5. update_list()
6. find_file()
7. ichecksum()
8. get_minimum_load()

All tests pass. Tests that are expected to return True return True, tests that should return False return False, tests that should return equal are equal, tests that should not be equal are not equal. More information about the tests could be found in the tests.py file.

Credit for checksum algo: https://github.com/mdelatorre/checksum/blob/master/ichecksum.py