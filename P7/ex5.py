import http.client
import json
import Seq1

def print_colored(message, data, color):
    from termcolor import cprint, colored
    print(colored(message,color), end="")
    print(data)

DICT_GENES = {
    'FRAT1': 'ENSG00000165879',
    'ADA': 'ENSG00000196839',
    'FXN': 'ENSG00000165060',
    'RNU6_269P': 'ENSG00000212379',
    'MIR633': 'ENSG00000207552',
    'TTTY4C': 'ENSG00000228296',
    'RBMY2YP': 'ENSG00000227633',
    'FGFR3': 'ENSG00000068078',
    'KDR': 'ENSG00000128052',
    'ANK2': 'ENSG00000145362'
}

SERVER = 'rest.ensembl.org'
ENDPOINT = '/sequence/id/'
PARAMETERS = '?content-type=application/json'

connection = http.client.HTTPConnection(SERVER)
try:
    for key, id in DICT_GENES.items():
        connection.request('GET',ENDPOINT + id + PARAMETERS)
        response = connection.getresponse()
        if response.status == 200:
            response_dict=json.loads(response.read().decode())
            #print(json.dumps(response, indent=4, sort_keys=True))
            sequence = Seq1.Seq(response_dict['seq'])
            s_length = sequence.len()
            percentages = sequence.percentage_base(sequence.count_base(),s_length)
            most_frequent_base=sequence.frequent_base(sequence.count())
            print_colored('GENE ', key, 'yellow')
            print_colored('Total length ',s_length, 'yellow')
        for value in percentages.items():
            print_colored(key + ":", value, 'blue')
        print_colored('Most frequent base ',most_frequent_base, 'yellow')
except KeyError:
    print('The gene is not nt inside our dictionary.Choose one od the following: ', list(DICT_GENES.keys()))