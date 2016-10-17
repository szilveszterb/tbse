from socketIO_client import SocketIO, LoggingNamespace
import sys
import time

myId = "admin"

kmap = {"UP": 38, "DOWN": 40, "LEFT": 37, "RIGHT": 39}


def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
             for i in range(wanted_parts) ]

def merge(line):
    """
    Function that merges a single row or column in 2048
    """
    length = len(line)
    result = [0] * length
    last_index = 0

    for current_index in range(length):
        if line[current_index] != 0:
            result[last_index] = line[current_index]
            last_index += 1

    for key in range(length - 1):
        if result[key] is result[key + 1]:
            result[key] = result[key] * 2
            result.pop(key + 1)
            result.append(0)

    return result

def step_right(data):
    new_gamestate = []
    for row in data:
        new_gamestate.append(list(reversed(merge(list(reversed(row))))))

    return new_gamestate

def step_left(data):
    new_gamestate = []
    for row in data:
        new_gamestate.append(merge(row))

    return new_gamestate

def step_up(data):
    new_gamestate = []
    for i in range(4):
        column = []
        for j in range(4):
            column.append(data[j][i])
        new_gamestate.append(merge(column))

    row_gamestate = []

    for i in range(4):
        row = []
        for j in range(4):
            row.append(new_gamestate[j][i])
        row_gamestate.append(row)

    return row_gamestate

def step_down(data):
    new_gamestate = []
    for i in range(4):
        column = []
        for j in range(4):
            column.append(data[j][i])
        new_gamestate.append(list(reversed(merge(list(reversed(column))))))

    row_gamestate = []

    for i in range(4):
        row = []
        for j in range(4):
            row.append(new_gamestate[j][i])
        row_gamestate.append(row)

    return row_gamestate


def contra(data):
    print(data)
    game_contra = 0
    for i in range(4):
        for j in range(4):
            if j-1 < 0:
                c_l = data[i][j]
            elif data[i][j-1] == 0:
                c_l = 1
            else:
                c_l = data[i][j-1]

            if j+1 > 3:
                c_r = data[i][j]
            elif data[i][j+1] == 0:
                c_r = 1
            else:
                c_r = data[i][j+1]

            if i-1 < 0:
                c_u = data[i][j]
            elif data[i-1][j] == 0:
                c_u = 1
            else:
                c_u = data[i-1][j]

            if i+1 > 3:
                c_d = data[i][j]
            elif data[i+1][j] == 0:
                c_d = 1
            else:
                c_d = data[i+1][j]

            x = data[i][j]
            con = abs(x - c_r) + abs(x - c_l) + abs(x - c_u) + abs(x - c_d)
            game_contra += con

    return game_contra

prev = []
prev_step = 0
def algorithm(data):
    global prev, prev_step
    print(data)
    data = data.split(" ")
    if prev_step and prev:
        games = []
        for p in prev:
            row = ','.join(map(str, p))
            games.append(row)
        games = ','.join(games)
        games = games + "," + str(prev_step) + "," + data[0] + "\n"
        with open("test.txt", "a") as myfile:
            myfile.write(games)

    int_data = []
    data.pop(0)
    for i in data:
        int_data.append(int(i))
    print(int_data)
    game_state = split_list(int_data, wanted_parts=4)

    up_state = step_up(game_state)
    down_state = step_down(game_state)
    left_state = step_left(game_state)
    right_state = step_right(game_state)

    steps = {}
    if up_state != prev:
        steps['UP'] = contra(up_state)

    if down_state != prev:
        steps['DOWN'] = contra(down_state)

    if left_state != prev:
        steps['LEFT'] = contra(left_state)

    if right_state != prev:
        steps['RIGHT'] = contra(right_state)

    s = sorted(steps)
    prev = game_state
    prev_step = kmap[s[0]]
    dir = kmap[s[0]]
    socketIO.emit("aiwrite", dir)


def error(msg):
    print(msg)
    SocketIO.disconnect()
    sys.exit()

socketIO = SocketIO('localhost', 5000, LoggingNamespace)

socketIO.on("airead", algorithm)
socketIO.on("error", error)

socketIO.emit("login", myId, "admin")
socketIO.emit("connect")
socketIO.emit("aictl", myId)
socketIO.wait()
