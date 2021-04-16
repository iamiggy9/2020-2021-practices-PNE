
from Client0 import Client
list_sequences = ['ACTGGATAGCA','AACTCCCCCCCCCCCC','ACTGG', 'ATGGGGGCA', 'TTTGAAAAAGGTA']
print('-----| Practice 3, Exercise 7 |------')
IP = "127.0.0.1"
PORT = 8080
c = Client(IP,PORT)
msg = input('Enter your command : ')
print(' * Testing ' + msg + '...')
if msg == 'GET':
    print(c.talk(msg + ' 0'))
    print(c.talk(msg + ' 1'))
    print(c.talk(msg + ' 2'))
    print(c.talk(msg + ' 3'))
    print(c.talk(msg + ' 4'))
elif msg == 'INFO':
    print(c.talk(msg + ' ' + list_sequences[0]))
elif msg == 'COMP':
    print(c.talk(msg + ' ' + list_sequences[0]))
elif msg == 'REV':
    print(c.talk(msg + ' ' + list_sequences[0]))
else:
    print(c.talk(msg))
