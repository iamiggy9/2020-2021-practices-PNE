from Seq1 import Seq

def print_colored(message,colour):
    import termcolor

    print(termcolor.colored(message,colour))
def format_command(command):
    return command.replace('\n', '').replace('\r','')
def ping(cs):
    response = 'OK!'
    cs.send(str(response).encode())
    print_colored('PING command', 'green')
def get(cs,list_sequences,argument):
    response = list_sequences[int(argument)]
    print(response)
    cs.send(str(response).encode())
    print_colored('GET', 'yellow')
def info(cs,argument):
    seq_info = Seq(argument)
    count_bases_string = ""
    for base, count in seq_info.count().items():
        s_base = str(base) + ": " + str(count) + " (" + str(
            round(count / seq_info.len() * 100, 2)) + "%)" + "\n"
        count_bases_string += s_base
    response = ("Sequence: " + str(seq_info) + "\n" +
                "Total length: " + str(seq_info.len()) + "\n" +
                count_bases_string)
    print(response)
    cs.send(str(response).encode())
def comp(cs,argument):
    seq_comp = argument
    BLANK = ''
    for e in seq_comp:
        if e == "A":
            BLANK += "T"
        if e == "T":
            BLANK += "A"
        if e == "C":
            BLANK += "G"
        if e == "G":
            BLANK += "C"
            print(BLANK)
    response = ("Sequence: " + str(seq_comp) + "\n" +
                "Complement sequence: " + str(BLANK))
    print(response)
    cs.send(str(response).encode())




