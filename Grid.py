from collections import OrderedDict


class Grid:
    def __init__(self, filename):
        self.tiles = self.read_board(filename)
        self.start = self.find("A")
        self.goal = self.find("B")
        self.width, self.height = self.get_w_and_h()
        self.path = []

    def read_board(self, filename):
        """
        Reads board from file

        :return: Dictionary with position tuples (x,y) as keys and board symbol as values
        """
        f = open("boards/" + filename)
        board = OrderedDict()
        x = 0
        y = 0
        while True:
            c = f.read(1)  # read one character at a time
            if not c:
                break  # stop if there are no more characters
            if c == "\n":
                x = 0
                y += 1  # start next row if newline
                c = f.read(1)  # to avoid writing the newline
            board[(x, y)] = c
            x += 1
        del board[next(reversed(board))]  # deletes last element because it is a newline from the text file
        return board

    def get_w_and_h(self):
        """
        :return: width and height of board
        """
        last_elem = next(reversed(self.tiles))
        return last_elem[0]+1,last_elem[1]+1

    def find(self,search_symbol):
        for pos, val in self.tiles.items():
            if val == search_symbol:
                return pos

    def in_bounds(self, pos):
        """
        Checks if a position is inside the board

        :return: True if within bounds, False if not
        """

        (x, y) = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, pos):
        """
        Checks if a position can be passed (if it is # or not)

        :return: True if tile can be passed, False if not
        """
        return self.tiles.get(pos) != "#"

    def neighbors(self, pos):
        """
        :return: Neigbors to the north, south, west and east that we can move to
        """
        (x, y) = pos
        results = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]
        results = filter(self.in_bounds, results)       #remove neighbors outside the board
        results = filter(self.passable, results)        #remove neighbors that are walls
        return results

    def set_path(self,path):
        self.path = path

    def prettyprint(self):
        for y in range(self.height):
            s = ""
            for x in range(self.width):
                s += self.tiles.get((x, y))
            if s:
                print(s)

    def cost(self, pos):
        """
        Cost function
        :param pos: a position on the board
        :return: the cost it takes to move to this position
        """
        value = self.tiles[pos]
        if value == ".":        #empty
            return 1
        elif value == "A":      #start
            return 1
        elif value == "B":      #goal
            return 1
        elif value == "w":      #water
            return 100
        elif value == "m":      #mountain
            return 50
        elif value == "f":      #forest
            return 10
        elif value == "g":      #grass
            return 5
        elif value == "r":      #road
            return 1