from Client0 import Client

PRACTICE = 2
EXERCISE= 3
print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")
IP = "192.168.1.54"
PORT =8080
c = Client(IP,PORT)
print('Response: ', c.talk('Message'))