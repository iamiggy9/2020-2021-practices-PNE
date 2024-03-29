import socket
import termcolor
class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
    def ping(self):
        print('OK!')
    def advanced_ping(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.ip, self.port))
            print('Server is up')
        except ConnectionRefusedError:
            print('Could not correct to the server.Is it running?')
    def __str__(self):
        return "Connection to SERVER at " + self.ip + ",PORT:" + str(self.port)
    def talk(self,msg):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # establish the connection to the Server (IP, PORT)
        s.connect((self.ip, self.port))

        # Send data.
        print('To server :', msg)
        s.send(msg.encode())

        # Receive data
        response = s.recv(2048).decode("utf-8")

        # Close the socket
        s.close()

        # Return the response
        return 'From server: ' + response
    def debug_talk(self, msg):
        message = str(msg)
        response = self.talk(msg)
        termcolor.cprint(message, 'blue')
        termcolor.cprint(response, 'yellow')

