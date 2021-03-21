from Client0 import Client
from Seq1 import Seq
PRACTICE = 2
EXERCISE= 6
print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")
IP = "192.168.1.54"
PORT =  8080
PORT_2 =  8081
c = Client(IP,PORT)
c_2=Client(IP,PORT_2)

s = Seq()
s.read_fasta('../SESSION 4/FRAT1.txt')
count=0
i =0
while i < len(s.strbases) and count < 10:
    fragment = s.strbases[i: i + 10]
    count += 1
    i += 10
    print('Fragment', count, ':', fragment)
    if count % 2 == 0:
      print(c_2.talk('Fragment ' + str(count) + ':' + fragment))
    else:
        print(c.talk('Fragment ' + str(count) + ':' + fragment))

