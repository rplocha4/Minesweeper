import pygame
from main import Saper

pygame.init()
SAPER_SIZE = 10
saper = Saper(SAPER_SIZE)
saper.place_bombs(10)
saper.place_numbers()
RECT_SIZE = 400 // SAPER_SIZE
RECT_BORDER = 2
WIDTH, HEIGHT = RECT_SIZE * saper.get_board_size() + 2, RECT_SIZE * saper.get_board_size() + 2

boolean_board = [[[False, False] for x in range(saper.get_board_size())] for y in range(saper.get_board_size())]

FONT = pygame.font.SysFont('indigo', RECT_SIZE)

window = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Saper")


def get_board_coords():
    board = []
    x = 0

    for i in range(0, HEIGHT - RECT_SIZE, RECT_SIZE):
        y = 0

        for j in range(0, WIDTH - RECT_SIZE, RECT_SIZE):
            board.append([j, j + RECT_SIZE, i, i + RECT_SIZE, [x, y]])
            y += 1
        x += 1

    return board


def draw_image(x, y, board, image):
    x1, y1, board_coords = get_position(x, y, board)
    board_coords_x, board_coords_y = board_coords
    if not boolean_board[board_coords_x][board_coords_y][0]:

        if boolean_board[board_coords_x][board_coords_y][1]:
            boolean_board[board_coords_x][board_coords_y][1] = False
            rect = (x1, y1, RECT_SIZE, RECT_SIZE)
            pygame.draw.rect(window, window.get_at((x1, y1))[:3], rect)

        elif not boolean_board[board_coords_x][board_coords_y][1]:
            boolean_board[board_coords_x][board_coords_y][1] = True
            window.blit(image, (x1+10, y1+10))


def draw_board(board):
    count = 1
    num = 1
    for i, row in enumerate(board):
        rect = (row[0], row[2], RECT_SIZE, RECT_SIZE)
        if count % 2 == 0:
            pygame.draw.rect(window, 'green', rect)
        else:
            pygame.draw.rect(window, 'forestgreen', rect)

        if num % SAPER_SIZE != 0:
            count += 1
        num += 1


def get_position(x, y, board):
    for coords in board:
        if coords[0] <= x <= coords[1] and coords[2] <= y <= coords[3]:
            return coords[0], coords[2], coords[4]


def empty(x, y, board):
    if saper.board[x][y] != 0:
        draw_symbol(y * RECT_SIZE + 1, x * RECT_SIZE + 1, board)
        return 0

    saper.board[x][y] = " "
    rect = (y * RECT_SIZE, x * RECT_SIZE, RECT_SIZE, RECT_SIZE)
    pygame.draw.rect(window, 'grey', rect)

    neighbours = saper.get_neighbours(x, y)

    for neighbour in neighbours:
        empty(neighbour[0], neighbour[1], board)


def draw_symbol(x, y, board):
    x1, y1, board_coords = get_position(x, y, board)

    board_coords_x = board_coords[0]
    board_coords_y = board_coords[1]

    if not boolean_board[board_coords_x][board_coords_y][0] and not boolean_board[board_coords_x][board_coords_y][1]:
        symbol = saper.board[board_coords_x][board_coords_y]
        if symbol == 0:
            empty(board_coords_x, board_coords_y, board)
            saper.board[board_coords_x][board_coords_y] = " "
            rect = (x1 * RECT_SIZE, y1 * RECT_SIZE, RECT_SIZE, RECT_SIZE)
            pygame.draw.rect(window, 'grey', rect)

        else:
            if symbol == -1:
                return -1
            elif symbol == 1:
                color = 'blue'
            elif symbol == 2:
                color = 'navy'
            else:
                color = 'indigo'

            if symbol != " ":
                controls = FONT.render(str(symbol), True, color)
                window.blit(controls, (x1 + RECT_SIZE / 2 - controls.get_width() / 2, y1+ RECT_SIZE / 2 - controls.get_height() / 2))
        boolean_board[board_coords_x][board_coords_y][0] = True


def game_over(board):
    image = pygame.image.load('mine.png')
    image = pygame.transform.scale(image, (RECT_SIZE - 20, RECT_SIZE - 20))

    for i, row in enumerate(saper.board):

        for j, num in enumerate(row):
            if num == -1:
                x, y, _ = get_position(j*RECT_SIZE+1, i*RECT_SIZE+1, board)
                rect = (x, y, RECT_SIZE, RECT_SIZE)
                pygame.draw.rect(window, 'red', rect)
                window.blit(image, (x + 10, y + 10))


def main():
    run = True
    press = True
    clock = pygame.time.Clock()
    board = get_board_coords()
    draw_board(board)
    while run:
        clock.tick(120)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and press:
                    if draw_symbol(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], board) == -1:
                        press = False
                        game_over(board)
                if event.button == 3 and press:
                    image = pygame.image.load('flag.png')
                    image = pygame.transform.scale(image, (RECT_SIZE-20, RECT_SIZE-20))
                    draw_image(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], board, image)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
