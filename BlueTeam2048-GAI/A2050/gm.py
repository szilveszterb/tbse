from config import keymap

def printBoard(game,includeid=True):
    if includeid:
        rtv=str(game.uid)
        rtv+=" "+str(game.game.score)
    else:
        rtv=str(game.game.score)
    for line in game.game.board._board:
        for tile in line:
            rtv+=" "+str(tile)
    return rtv

outputFolder="files/"

class cGame:
    def __init__(self,game,uid,nick):
        self.game=game
        self.uid=uid
        self.nick=nick
        self.last=str()
        self.times=0

class GameManager:
    def __init__(self):
        self.games=list()

    def addTable(self,game):
        self.games.append(game)

    def removeTable(self,uid):
        for x,game in enumerate(self.games):
            if game.uid==uid:
                del self.games[x]

    def hasGameWithId(self,id):
        for game in self.games:
            if game.uid==id:
                return game
        return None

    def getGames(self,id):
        rtv=list()
        for game in self.games:
            if game.uid!=id:
                rtv.append((printBoard(game),game.nick))
        return rtv

    def genOutput(self,id):
        for game in self.games:
            if game.uid==id:
                with open(outputFolder+"out"+str(id),"w") as f:
                    f.write(printBoard(game,includeid=False))

    def shift(self,id,ev):
        for game in self.games:
            if game.uid==id:
                game.game.shift(keymap[ev])
                return

    def gameOver(self,id):
        for game in self.games:
            if game.uid==id:
                return game.game.game_over

    def getHightile(self,id):
        for game in self.games:
            if game.uid==id:
                max=2
                for line in game.game.board._board:
                    for tile in line:
                        if tile>max:
                            max=tile
                return int(pow(2,max))

    def getPoints(self,id):
        for game in self.games:
            if game.uid==id:
                return int(game.game.score)

    def get(self,id):
        for game in self.games:
            if game.uid==id:
                return game
