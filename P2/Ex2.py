from Client0 import Client

PRACTICE = 2
EXERCISE= 2
print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")
IP = "192.168.1.54"
PORT = 4890
c = Client(IP,PORT)
print(c)