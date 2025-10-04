class Cell:
    def __init__(self):
        self.has_mine = False
        self.revealed = False
        self.flagged = False
        self.adjacent_mines = 0
        self.probability = None