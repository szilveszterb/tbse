import sys

import numpy as np
from socketIO_client import SocketIO, LoggingNamespace

import neuralnet as nn


socketIO = None
model = None
host = 'server'
user = 'blue'
password = 'blue'

direction_map = {
    0: (38, 'UP'),
    1: (40, 'DOWN'),
    2: (37, 'LEFT'),
    3: (39, 'RIGHT'),
}


def main():
    global socketIO
    global model
    model = nn.load_model('models/004.txt')
    socketIO = SocketIO(host, 5000, LoggingNamespace)
    socketIO.on('airead', algorithm)
    socketIO.on('error', error)
    socketIO.emit('aictl', user)
    socketIO.wait()


step_count = 0
noop_count = 0
prev_data = None
def algorithm(data):
    global step_count
    global noop_count
    global prev_data
    step_count += 1

    print()
    inputs = data.split()
    score, board = inputs[0], inputs[1:]
    print('step: ', step_count)
    print('score: ', score)
    print('board:')
    for row in range(4):
        print(' ' + ' '.join(board[4*row:4*(row+1)]))

    dataset = np.array([np.array([np.float(cell) for cell in data.split()[1:]])])
    features = nn.get_features(dataset)
    prob = model.predict(features)[0]
    direction = int(np.argmax(prob))
    if data == prev_data:
        noop_count += 1
        for i in range(noop_count):
            prob[direction] = 0
            direction = int(np.argmax(prob))
    else:
        noop_count = 0
        prev_data = data
    print('move:', direction_map[direction][1])

    socketIO.emit('aiwrite', direction_map[direction][0])


def error(msg):
    print(msg)
    socketIO.disconnect()
    sys.exit()


if __name__ == '__main__':
    main()
