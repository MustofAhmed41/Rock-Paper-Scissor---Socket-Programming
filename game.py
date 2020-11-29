# this class will keep track of the whole game and will store all the necessary information

class Game:
    def __init__(self, id):
        self.p1Went = False  # if player 1 made a move or not
        self.p2Went = False
        self.ready = False
        self.id = id  # A game will have a unique Id, this is a game ID
        self.moves = [None, None]  # players moves will be stored here, initially there won't be any move so None
        self.wins = [0, 0]
        self.ties = 0

    def get_player_move(self, p):
        """
        :param p: [0,1]  p is in the range 0 or 1 # 0 means player 1 and 1 means player 2
        :return: Move
        """
        return self.moves[p]

    def play(self, player, move):  # when players make a move
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self):  # if the two players are connected to the game or not
        return self.ready

    def bothWent(self):  # if both player went (i am confused about this one)
        return self.p1Went and self.p2Went

    def winner(self):  # determines who won the case, there are total 9 possible cases

        p1 = self.moves[0].upper()[0]  # getting first letter only to check move
        p2 = self.moves[1].upper()[0]

        winner = -1  # winner  = 0 when player 1 wins, if players 2 wins then winner = 0, or else -1 for tie
        if p1 == "R" and p2 == "S":
            winner = 0
        elif p1 == "S" and p2 == "R":
            winner = 1
        elif p1 == "P" and p2 == "R":
            winner = 0
        elif p1 == "R" and p2 == "P":
            winner = 1
        elif p1 == "S" and p2 == "P":
            winner = 0
        elif p1 == "P" and p2 == "S":
            winner = 1

        return winner

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False
