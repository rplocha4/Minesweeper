from random import randint


class Saper:
    def __init__(self, board_size):
        self.board_size = board_size
        self.board = [[0 for x in range(board_size)] for y in range(board_size)]

    def get_board_size(self):
        return self.board_size

    def place_bombs(self, num):
        i = 0
        if num > self.board_size * self.board_size:
            print("Too much bombs")
            return
        while i < num:
            bomb_x = randint(0, self.board_size - 1)
            bomb_y = randint(0, self.board_size - 1)
            if self.board[bomb_x][bomb_y] == 0:
                self.board[bomb_x][bomb_y] = -1  # -1 = bomb
                i += 1

    def place_numbers(self):
        for i, b in enumerate(self.board):
            for j, c in enumerate(b):
                if c != -1:  # -1 = bomb
                    self.board[i][j] = self.check_for_bombs(i, j)

    def get_neighbours(self, x, y):
        possible_neighbours = [[x, y+1], [x, y-1], [x+1, y], [x-1, y], [x+1, y+1], [x+1, y-1], [x-1, y+1], [x-1, y-1]]
        neighbours = []
        for neighbour in possible_neighbours:
            try:
                if neighbour[0] < 0 or neighbour[1] < 0:  # to prevent '-1' index
                    raise IndexError
                _ = self.board[neighbour[0]][neighbour[1]]  # check if coords are in board range if not IndexError occurs
                neighbours.append([neighbour[0], neighbour[1]])
            except IndexError:
                continue

        return neighbours

    def check_for_bombs(self, x, y):
        n_bombs = 0

        neighbours = self.get_neighbours(x, y)

        for neighbour in neighbours:
            if self.board[neighbour[0]][neighbour[1]] == -1:  # -1 = bomb
                n_bombs += 1

        return n_bombs


if __name__ == "__main__":
    saper = Saper(8)
    saper.place_bombs(10)
    saper.place_numbers()

    for b in saper.board:
        print(b)
