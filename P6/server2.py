import http.server
import socketserver
import termcolor

from urllib.parse import urlparse, parse_qs
import server_utils as su
# DYNAMIC WEBPAGES, webpages where the user can interact with (provide content, post comments). And the server is providing content to the user according to certain parameters
# we will see how to send information from the server to the user (send the html information from the server. Instead of having lots of html files for each webpage we would have one html template).




# Define the Server's port
PORT = 6555
LIST_SEQUENCES = ['ACTGGATAGCA','AACTCCCCCCCCCCCC','ACTGG', 'ATGGGGGCA', 'TTTGAAAAAGGTA']
LIST_GENES=['ADA','FRAT1','FXN','RNU6_269P','U5']
HTML_ASSETS = "./HTML/"

BASES_INFORMATION = {
    "A":{"link": "https//en.wikipedia.org/wiki/Adenine",
         "formula": "C5H5N5",
         "name": "ADENINE",
         "color": "green"
         },
    "C":{"link": "https//en.wikipedia.org/wiki/Citosine",
         "formula": "C5H5N5",
         "name": "CYTOSINE",
         "color": "yellow"
         },
    "G":{"link": "https//en.wikipedia.org/wiki/Guanine",
         "formula": "C5H5N5",
         "name": "GUANINE",
         "color":"lightblue"
         },
    "T":{"link": "https//en.wikipedia.org/wiki/Thymine",
         "formula": "C5H5N5",
         "name": "THYMINE",
         "color": "lightpink"
         },
}

# -- This is for preventing the error: "Port already in use"
socketserver.TCPServer.allow_reuse_address = True


# Class with our Handler. It is a called derived from BaseHTTPRequestHandler
# It means that our class inheritates all his methods and properties
class TestHandler(http.server.BaseHTTPRequestHandler): # this class is inside the HTTP server therefore it inherit the BaseHTTPRequestHandler methods

    def do_GET(self):
        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""

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
        if self.path == "/":
            context['n_sequences']=len(LIST_SEQUENCES)
            context['list_genes'] =LIST_GENES
            contents = su.read_template_html_file("./html/INDEX.html").render(context=context)
        elif path_name == "/test": # when working with forms my self.path always comes with a question mark at the end
            contents = su.read_template_html_file("Ctest.html").render()
        elif path_name =='/ping':
            contents = su.read_template_html_file("./html/ping.html").render()
        elif path_name=='/get':
            number_sequence=arguments['sequence'][0]
            contents = su.get(LIST_SEQUENCES,number_sequence)
        elif path_name=='/gene':
            gene = arguments['gene'][0]
            contents = su.gene(gene)
        else:
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