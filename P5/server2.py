import http.server
import socketserver
import termcolor
import pathlib
from jinja2 import Template
def read_html_file(filename):
    content = pathlib.Path(filename).read_text()
    return content
def read_template_html(filename):
    content = Template(pathlib.Path(filename).read_text())
    return content
# Define the Server's port
PORT = 8080
BASES_INFORMATION = {
    "A": {"link": "https://en.wikipedia.org/wiki/Adenine",
          "formula": "C5H5N5",
          "name": "ADENINE",
          'color':'green'
    },
    "C": {"link": "https://en.wikipedia.org/wiki/Cytosine",
          "formula": "C4H5N3O",
          "name": "CYTOSINE",
           'color':'yellow'
          },
    "G": {"link": "https://en.wikipedia.org/wiki/Guanine",
          "formula": "C5H5N5O",
          "name": "GUANINE",
            'color':'lightskyblue'

          },
    "T": {"link": "https://en.wikipedia.org/wiki/Thymine",
          "formula": "C5H6N2O2",
          "name": "THYMINE",
          'color':'pink'
          }
}


# -- This is for preventing the error: "Port already in use"
socketserver.TCPServer.allow_reuse_address = True


# Class with our Handler. It is a called derived from BaseHTTPRequestHandler
# It means that our class inheritates all his methods and properties
class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""

        # Print the request line
        termcolor.cprint(self.requestline, 'green')
        termcolor.cprint(self.path, 'blue')
        # IN this simple server version:
        # We are NOT processing the client's request
        # It is a happy server: It always returns a message saying
        # that everything is ok


        if self.path == '/':
            contents = read_html_file('html/INDEX.html')

        elif '/info/' in self.path:
          try:
            base = self.path.split('/')[-1]
            context = BASES_INFORMATION[base]
            context['letter']=base
            contents = read_template_html('./html/info/general.html').render(base_information = context)
          except KeyError:
              contents = read_html_file('html/ERROR.html')

        elif self.path.endswith('.html'):
            try:
                contents = read_html_file('./html' + self.path)
            except FileNotFoundError:
                contents = read_html_file('html/ERROR.html')

        else:
            contents = read_html_file('html/ERROR.html')




        # Generating the response message
        self.send_response(200)  # -- Status line: OK!

        # Define the content-type header:
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(contents.encode()))

        # The header is finished
        self.end_headers()

        # Send the response message
        self.wfile.write(contents.encode())

        return


# ------------------------
# - Server MAIN program
# ------------------------
# -- Set the new handler
Handler = TestHandler

# -- Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:

    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stoped by the user")
        httpd.server_close()