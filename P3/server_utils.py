def print_colored(message,colour):
    import termcolor
    import colorama
    colorama.init(strip='false')
    print('to server : ', end='')
    print(termcolor.colored(message,colour))
def format_command(command):
    return command.replace('\n', ' ').replace('\r',' ')
def ping(cs):
    print_colored('PING command', 'green')
def get(cs):
    response = [int(argument)]
    print(response)
    cs.send(response.encode())

