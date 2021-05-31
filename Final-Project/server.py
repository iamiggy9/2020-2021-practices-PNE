import http.server
import socketserver
import termcolor
import colorama
from Seq1 import Seq
import server_utils as su
from urllib.parse import urlparse, parse_qs
import http.client
import json
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


# Define the Server's port
PORT =8080

SERVER = 'rest.ensembl.org'
Parameters = "?content-type=application/json"


# -- This is for preventing the error: "Port already in use"
socketserver.TCPServer.allow_reuse_address = True


# Class with our Handler. It is a called derived from BaseHTTPRequestHandler
# It means that our class inheritates all his methods and properties
class TestHandler(http.server.BaseHTTPRequestHandler): # this class is inside the HTTP server therefore it inherit the BaseHTTPRequestHandler methods

    def do_GET(self):
        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""
        connection = http.client.HTTPConnection(SERVER)
        # We just print a message
        print("GET received! Request line:")

        # Print the request line
        termcolor.cprint("  " + self.requestline, 'green')

        # Print the command received (should be GET)
        print("  Command: " + self.command)

        # Print the resource requested (the path)
        termcolor.cprint("  Path: " + self.path, "blue")

        # we are creating a parse object (easier way to work with the elements of the path
        o = urlparse(self.path)
        path_name = o.path
        arguments = parse_qs(o.query)
        print("Resource requested: ", path_name)
        print("Parameters: ", arguments)
        context = {}
        try:
            if path_name == "/":
                contents = su.read_template_html_file("./html/INDEX.html").render(context=context)
            elif path_name == "/listSpecies":
                ENDPOINT = "/info/species"
                connection.request("GET", ENDPOINT + Parameters)
                response = connection.getresponse()
                response_dict = json.loads(response.read().decode())
                species_list = []
                amount_species = len(response_dict["species"])
                context["amount_species"] = amount_species
                limit = int(arguments["limit"][0])
                context["limit"] = limit
                for n in range(0, limit):
                    species_list.append(response_dict["species"][n]["common_name"])
                context["names"] = species_list
                contents = su.read_template_html_file("html/LISTSPECIES.html").render(context=context)
            elif path_name == "/karyotype":
                ENDPOINT = "info/assembly/"
                specie = arguments["species"][0]
                connection.request("GET", ENDPOINT + specie + Parameters)
                response = connection.getresponse()
                response_dict = json.loads(response.read().decode())
                karyotype = response_dict["karyotype"]
                context["species"] = arguments["species"][0]
                context["karyotype"] = karyotype
                contents = su.read_template_html_file("./html/KARYOTYPE.html").render(context=context)
            elif path_name == "/chromosomeLength":
                ENDPOINT = "info/assembly/"
                specie = arguments["species"][0]
                connection.request("GET", ENDPOINT + specie + Parameters)
                response = connection.getresponse()
                response_dict = json.loads(response.read().decode())
                chromosome = arguments["chromosome"][0]
                print(response_dict['top_level_region'])
                for n in range(0, len(response_dict["top_level_region"])):
                    if chromosome == response_dict["top_level_region"][n]["name"]:
                        length = response_dict["top_level_region"][n]["length"]
                context["length"] = length
                contents = su.read_template_html_file("./html/CHROMOSOMELENGTH.html").render(context=context)
            elif path_name == "/geneSeq":
                ENDPOINT = "/sequence/id/"
                gene = arguments["gene"][0]
                id = DICT_GENES[gene]
                connection.request("GET", ENDPOINT + id + Parameters)
                response = connection.getresponse()
                response_dict = json.loads(response.read().decode())
                context["seq"] = response_dict["seq"]
                contents = su.read_template_html_file("./html/SEQGENE.html").render(context=context)
            elif path_name == "/geneInfo":
                ENDPOINT = "/sequence/id/"
                gene = arguments["gene"][0]
                id = DICT_GENES[gene]
                connection.request("GET", ENDPOINT + id + Parameters)
                response = connection.getresponse()
                response_dict = json.loads(response.read().decode())
                # print(json.dumps(response_dict, indent=4, sort_keys=True))
                info = response_dict["desc"].split(":")
                context["dict_info"] = {
                    "Name": info[1],
                    "ID": id,
                    "Start": info[3],
                    "End": info[4],
                    "Length": (int(info[4]) - int(info[3]) + 1)
                }
                contents = su.read_template_html_file("./html/INFOGENE.html").render(context=context)
            elif path_name == "/geneCalc":
                ENDPOINT = "/sequence/id/"
                gene = arguments["gene"][0]
                id = DICT_GENES[gene]
                connection.request("GET", ENDPOINT + id + Parameters)
                response = connection.getresponse()
                response_dict = json.loads(response.read().decode())
                # print(json.dumps(response_dict, indent=4, sort_keys=True))
                sequence = Seq(response_dict["seq"])
                dict_bases = Seq.count(sequence)
                percentage = Seq.percentage(sequence)
                context["length"] = Seq.len(sequence)
                context["bases"] = {
                    "A": str(dict_bases["A"]) + " (" + str(percentage[0]) + "%)",
                    "C": str(dict_bases["C"]) + " (" + str(percentage[1]) + "%)",
                    "T": str(dict_bases["T"]) + " (" + str(percentage[2]) + "%)",
                    "G": str(dict_bases["G"]) + " (" + str(percentage[3]) + "%)"
                }
                contents = su.read_template_html_file("./html/CALCGENE.html").render(context=context)
            else:
                contents = su.read_template_html_file("./html/ERROR.html").render()
        except KeyError:
            contents = su.read_template_html_file("./html/ERROR.html").render()
        except IndexError:
            contents = su.read_template_html_file("./html/ERROR.html").render()
        # Generating the response message
        self.send_response(200)  # -- Status line: OK!

        # Define the content-type header:
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(contents.encode()))

        # The header is finished
        self.end_headers() # we always need to call the end headers method which forces to create an empty line of the HTTP message

        # Send the response message
        self.wfile.write(contents.encode()) # wfile acts like a socket, its just something that we can write on

        # IN this simple server version:
        # We are NOT processing the client's request
        return


# ------------------------
# - Server MAIN program
# ------------------------
# -- Set the new handler
Handler = TestHandler # we create an instance of the child class TestHandler

# -- Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:

    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stopped by the user")
        httpd.server_close()