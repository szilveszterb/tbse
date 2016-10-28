#!/usr/bin/env python3
import sys
from socketIO_client import SocketIO, LoggingNamespace


my_id = 'Blue Team'
d = dict(UP=38, DOWN=40, LEFT=37, RIGHT=39)
d_order = {
    0: ['UP', 'LEFT', 'RIGHT', 'DOWN'],
    1: ['UP', 'RIGHT', 'LEFT', 'DOWN'],
}

prev_data = []
move_counter = 0


def algorithm(data):
    global prev_data
    global move_counter

    if data == prev_data:
        print('board unchanged')
        move_counter += 1
        if move_counter == 4:
            sys.exit()
    else:
        print(prev_data)
        print(data)
        move_counter = 0
    prev_data = data

    data = list(map(int, data.split()))
    score = int(data.pop(0))
    print('score', score)

    board = []
    print('board')
    for row in range(4):
        board.append(data[:4])
        print(board[row])
        data = data[4:]

    rows_filled = 0
    for i in range(4):
        if all(cell > 0 for cell in board[i]):
            rows_filled += 1
        else:
            break
    print('rows filled', rows_filled)

    direction = d_order[rows_filled % 2][move_counter]
    print('direction', direction)
    direction = d[direction]

    socketIO.emit('aiwrite', direction)


def error(msg):
    print(msg)
    socketIO.disconnect()
    sys.exit()


socketIO = SocketIO('diosd', 5000, LoggingNamespace)
socketIO.on('airead', algorithm)
socketIO.on('error', error)
socketIO.emit('aictl', my_id)
socketIO.wait()
