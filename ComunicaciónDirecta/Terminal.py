import sys
from xmlrpc.server import SimpleXMLRPCServer
from TerminalDisplayer import TerminalDisplayer


if __name__ == "__main__":
    server = SimpleXMLRPCServer(("localhost", int(sys.argv[1])), allow_none=True)  # We create the server
    terminal_displayer = TerminalDisplayer()
    server.register_instance(terminal_displayer)  # We register the server

    print("Terminal started.")
    try:
        server.serve_forever()  # We start the server
    except KeyboardInterrupt:
        print("Terminal stopped.")