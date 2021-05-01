from Seq1 import Seq
import pathlib
from jinja2 import Template

def print_colored(message,colour):
    import termcolor
    import colorama
    colorama.init(strip='false')
    print('To server : ',"\n",  end='')
    print(termcolor.colored(message,colour))
def read_template_html_file(filename):
    content= Template(pathlib.Path(filename).read_text())
    return content


def format_command(command):
    return command.replace('\n', '').replace('\r','')
def ping(cs):
    response = 'OK!'
    cs.send(str(response).encode())
    print_colored(response, 'green')
def get(list_sequences,seq_number):

    context={
        'number':seq_number,
        'sequence':list_sequences[int(seq_number)]
    }
    contents = read_template_html_file(('./html/get.html')).render(context=context)
    return contents


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
def gene(seq_name):
  PATH='./Sequences/'+ seq_name +'.txt'
  s1= Seq()
  s1.read_fasta(PATH)
  context={
      'gene_name':seq_name,
      'gene_contents':s1.strbases
  }
  contents = read_template_html_file('./html/gene.html').render(context=context)
  return contents






