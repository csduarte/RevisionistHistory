import random


class Board(object):

    def __init__(self):
        # Creates [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.data = [[x + 3 * (i - 1) for x in xrange(1,4)] for i in xrange(1,4)]
        self.move_count = 0

    def submit_move(self, panel, value):
        panel -= 1
        column = panel % 3
        row = panel / 3
        self.data[row][column] = value
        self.move_count += 1

    def __str__(self):
        st = "\t %s | %s | %s\n" % (self.data[0][0], self.data[0][1], self.data[0][2])
        st += "\t-----------\n"
        st += "\t %s | %s | %s\n" % (self.data[1][0], self.data[1][1], self.data[1][2])
        st += "\t-----------\n"
        st += "\t %s | %s | %s\n" % (self.data[2][0], self.data[2][1], self.data[2][2])
        return st

    def has_won(self):
        return (
            self.data[0][0] == self.data[0][1] == self.data[0][2] or
            self.data[1][0] == self.data[1][1] == self.data[1][2] or
            self.data[2][0] == self.data[2][1] == self.data[2][2] or

            self.data[0][0] == self.data[1][0] == self.data[2][0] or
            self.data[0][1] == self.data[1][1] == self.data[2][1] or
            self.data[0][2] == self.data[1][2] == self.data[2][2] or

            self.data[0][0] == self.data[1][1] == self.data[2][2] or
            self.data[2][0] == self.data[1][1] == self.data[0][2]
        )

    def is_cats_eye(self):
        return self.move_count == 9 and not self.has_won()


class Player(object):

    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def __str__(self):
        return self.name


class Game(object):

    def __init__(self):
        self.player1 = None
        self.player2 = None
        self.winner = None
        self.current_move = None
        self.board = Board()
        self.turn_count = 1
        self.cats_eye = False

    def add_player(self, name=None, symbol=None):
        if self.player1 is None:
            self.player1 = Player(name or "Player 1", symbol)
        elif self.player2 is None:
            self.player2 = Player(name or "Player 2", self.opposite_symbol(self.player1.symbol))
        else:
            print "A Three player game, are you you crazy?"

    @staticmethod
    def opposite_symbol(symbol):
        if symbol == 'x' or symbol == 'X':
            return 'O'
        else:
            return 'X'

    def select_first_player(self):
        if random.randint(0, 1) == 0:
            self.current_move = self.player1
        else:
            self.current_move = self.player2
        return self.current_move

    def display_board(self):
        print "\n========================="
        print " Current Board, Move #%d " % self.turn_count
        print "========================="
        print "  %s's turn(%s)" % (self.current_move.name, self.current_move.symbol)
        print "\n"
        print self.board

    def submit_move(self, panel):
        self.board.submit_move(panel, self.current_move.symbol)

    def take_turn(self, panel):
        self.submit_move(panel)
        if self.board.has_won():
            self.winner = self.current_move
        elif self.board.is_cats_eye():
            self.cats_eye = True
        self.display_board()
        self.next_player()
        self.turn_count += 1

    def next_player(self):
        if self.current_move == self.player1:
            self.current_move = self.player2
        else:
            self.current_move = self.player1


def play():
    g = Game()

    n = raw_input("Enter Player #1 Name?\n")
    s = raw_input("X or O? ")[0:1]
    g.add_player(name=n, symbol=s)

    g.add_player(raw_input("Enter Player #2 Name?\n"))
    g.select_first_player()
    print "First Move goes to: %s" % g.current_move
    print "Game on!"

    while True:
        if g.winner is not None:
            print "And the winner is %s" % g.winner
            break
        if g.cats_eye is True:
            print "Yikes. A Tie!"
            break
        g.display_board()
        g.take_turn(int(raw_input("Where to?\n")))

    prompt_replay()


def prompt_play():
    print "Hi want to play some tic-tac-toe? Press enter"
    raw_input()
    play()


def prompt_replay():
    print "Good Game!! Play Again? (Yes or No)"
    result = raw_input()
    if result == 'Yes' or result == 'yes' or result == 'y':
        play()
    elif result == 'No' or result == 'no' or result == 'n':
        exit()
    else:
        prompt_replay()


if __name__ == "__main__":
    prompt_play()
