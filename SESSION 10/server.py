import socket

# -- Step 1: create the socket
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# -- Optional: This is for avoiding the problem of Port already in use
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Configure the Server's IP and PORT
PORT = 8080
IP = "127.0.0.1"

# -- Step 1: create the socket
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# -- Optional: This is for avoiding the problem of Port already in use
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# -- Step 2: Bind the socket to server's IP and PORT
ls.bind((IP, PORT))

# -- Step 3: Configure the socket for listening
ls.listen()

print("The server is configured!")
count_connection=0
client_adress_list=[IP,PORT]
while True:
    # -- Waits for a client to connect
    print("Waiting for Clients to connect")
    try:
        (cs, client_ip_port) = ls.accept()
        client_adress_list.append(client_ip_port)
        count_connection += 1
        print('CONNECTION ' + str(count_connection) + ' client ip, port : ' + str(client_ip_port))
        print("A client has connected to the server!")
    except KeyboardInterrupt:
        print('Server stopped by the user')
        ls.close()
        exit()

    # -- Read the message from the client
    # -- The received message is in raw bytes
    msg_raw = cs.recv(2048)

    # -- We decode it for converting it
    # -- into a human-redeable string
    msg = msg_raw.decode()

    # -- Print the received message
    print(f"Message received: {msg}")
    try:
        response = int(msg) ** int(msg)
        print('Response', response)
        cs.send(str(response).encode())
    except ValueError:
        cs.send('We need a number'.encode())

    # -- Close the data socket
    cs.close()
    if count_connection== 5:
        for i in range(0,len(client_adress_list)):
            print('Client'+ str(i) + ':Client IP, PORT : ' + str(client_adress_list[i]))