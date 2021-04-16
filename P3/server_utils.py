from Seq1 import Seq

def print_colored(message,colour):
    import termcolor
    import colorama
    colorama.init(strip='false')
    print('To server : ',"\n",  end='')
    print(termcolor.colored(message,colour))


def format_command(command):
    return command.replace('\n', '').replace('\r','')
def ping(cs):
    response = 'OK!'
    cs.send(str(response).encode())
    print_colored(response, 'green')
def get(cs,list_sequences,argument):
    response = list_sequences[int(argument)]
    print_colored(response,'yellow')
    cs.send(str(response).encode())

def info(cs,argument):
    seq_info = Seq(argument)
    count_bases_string = ""
    for base, count in seq_info.count().items():
        s_base = str(base) + ": " + str(count) + " (" + str(
            round(count / seq_info.len() * 100, 2)) + "%)" + "\n"
        count_bases_string += s_base
    response = ("Sequence: " + "\n" + str(seq_info) + "\n" +
                "Total length: " + str(seq_info.len()) + "\n" +
                count_bases_string)
    print_colored(response,'blue')
    cs.send(str(response).encode())
def comp(cs,argument):
    seq_comp = argument
    response = ("Sequence: " +  "\n" + str(seq_comp) + "\n" +
                "Complement sequence: " + str(Seq.complement(seq_comp)))
    print_colored(response, 'blue')
    cs.send(str(response).encode())
def rev(cs,argument):
    seq_rev = argument
    response = ("Sequence: " +  "\n" + str(seq_rev) + "\n" +
                "Reverse sequence: " + str(Seq.reverse(seq_rev)))
    print_colored(response,'yellow')
    cs.send(str(response).encode())
def gene(cs,argument):
    seq_gene = argument
    response = ("Gene: " +  "\n"+ argument + str(Seq.read_fasta(seq_gene)) + "\n")
    print_colored(response, 'blue')
    cs.send(str(response).encode())




