import http.server
import socketserver
import termcolor
import colorama
import server_utils as su
import s2 as s_u
from urllib.parse import urlparse, parse_qs
import http.client
import json



# Define the Server's port
PORT =8080

HTML_ASSETS = "./HTML/"
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
        if path_name == "/":
            contents = su.read_template_html_file("./html/INDEX.html").render(context=context)
        elif path_name == "/test": # when working with forms my self.path always comes with a question mark at the end
            contents = su.read_template_html_file("Ctest.html").render()
        elif path_name =='/listSpecies':
            end = '/html/species'
            contents = s_u.list_seqs(connection, end, Parameters, arguments, context)

        elif path_name == '/operation':
            sequence = arguments['sequence'][0]
            operation = arguments['operation'][0]
            if operation=='Info':
                contents=su.info(sequence)
            elif operation=='Rev':
                contents = su.rev(sequence)
            elif operation == 'Comp':
                contents = su.comp(sequence)

        elif path_name =='/gene':
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