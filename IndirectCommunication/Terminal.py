import sys
from xmlrpc.server import SimpleXMLRPCServer
from TerminalDisplayer import TerminalDisplayer
from TerminalConsumer import TerminalConsumer


if __name__ == "__main__":

    terminal = TerminalConsumer({"host": "localhost", "port": "8000"}, "Terminal", "Terminal", "Terminal-"+str(sys.argv[1]))

    print("Terminal started.")
    try:
        terminal.consume()
    except KeyboardInterrupt:
        print("Terminal stopped.")