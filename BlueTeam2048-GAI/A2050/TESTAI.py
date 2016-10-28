from socketIO_client import SocketIO, LoggingNamespace
import sys

myId="my-login-name" #Put your login name here
kmap={"UP":38,"DOWN":40,"LEFT":37,"RIGHT":39}

def algorithm(data):
    """Write your code here"""
    dir=kmap["UP"]

    socketIO.emit("aiwrite",dir) #Don't remove this line


"""Do not remove the lines below"""
def error(msg):
    print(msg)
    socketIO.disconnect()
    sys.exit()

socketIO = SocketIO('diosd', 5000, LoggingNamespace)

socketIO.on('airead', algorithm)
socketIO.on('error', error)

socketIO.emit("aictl",myId)
socketIO.wait()
