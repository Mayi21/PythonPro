import getopt
import sys
import uuid



def main(argv):
    bootstrap_servers = None
    try:
        opts, argvs = getopt.getopt(argv, "hs:", ["bootstrap_servers="])
    except getopt.GetoptError:
        print("test.py -s <bootstrap_servers:port>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-s':
            bootstrap_servers = arg
    print(bootstrap_servers)

if __name__ == "__main__":
   main(sys.argv[1:])