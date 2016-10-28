from socketIO_client import SocketIO, LoggingNamespace
import sys
myId=1
kmap={"UP":38,"DOWN":40,"LEFT":37,"RIGHT":39}

def algorithm(data):
    print(data)
    dir=int(input(":"))



    socketIO.emit("aiwrite",dir)
    socketIO.wait(seconds=10)

socketIO = SocketIO('localhost', 5000, LoggingNamespace)

socketIO.on('airead', algorithm)

socketIO.emit("aictl",myId)
socketIO.wait(seconds=10)
