from Client0 import Client

PRACTICE = 2
EXERCISE= 2
print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")
IP = "172.18.15.194"
PORT = 4532
c = Client(IP,PORT)
print(c)