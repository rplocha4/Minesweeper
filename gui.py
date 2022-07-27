import pygame
from main import Saper
from tkinter import *
from tkinter import messagebox
import time

TIME_START = time.time()

Tk().wm_withdraw()

pygame.init()

RECT_COLOR_1 = '#00CC66'
RECT_COLOR_2 = '#00FF66'
WINDOW_BACKGROUND_COLOR = 'grey'
SAPER_SIZE = 8
BOMBS = 10
saper = Saper(SAPER_SIZE)
saper.place_bombs(BOMBS)
saper.place_numbers()
RECT_SIZE = 400 // SAPER_SIZE

BOARD_WIDTH, BOARD_HEIGHT = RECT_SIZE * saper.get_board_size() + 1, RECT_SIZE * saper.get_board_size() + 1
WINDOW_WIDTH, WINDOW_HEIGHT = BOARD_WIDTH, BOARD_HEIGHT + RECT_SIZE

FONT = pygame.font.SysFont('indigo', RECT_SIZE + 15)

boolean_board = [[[False, False] for _ in range(saper.get_board_size())] for _ in range(saper.get_board_size())]
# [is_number, is_flag]

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
WINDOW.fill(WINDOW_BACKGROUND_COLOR)

pygame.display.set_caption("Saper")


def get_board_coords():
    board = []
    x = 0

    for i in range(0, BOARD_HEIGHT - RECT_SIZE, RECT_SIZE):
        y = 0
        for j in range(0, BOARD_WIDTH - RECT_SIZE, RECT_SIZE):
            board.append([j, j + RECT_SIZE, i, i + RECT_SIZE, [x, y]])
            y += 1
        x += 1

    return board


def draw_flag(x, y, board):
    x1, y1, board_coords = get_position(x, y, board)
    board_coords_x, board_coords_y = board_coords
    if not boolean_board[board_coords_x][board_coords_y][0]:
        if boolean_board[board_coords_x][board_coords_y][1]:
            boolean_board[board_coords_x][board_coords_y][1] = False
            rect = (x1, y1, RECT_SIZE, RECT_SIZE)
            pygame.draw.rect(WINDOW, WINDOW.get_at((x1, y1))[:3], rect)

        elif not boolean_board[board_coords_x][board_coords_y][1]:
            boolean_board[board_coords_x][board_coords_y][1] = True
            image = pygame.image.load('icons/flag.png')
            image = pygame.transform.scale(image, (RECT_SIZE - 5, RECT_SIZE - 5))
            WINDOW.blit(image, (x1 + 3, y1))


def draw_board(board):
    count = 1
    num = 1
    for i, row in enumerate(board):
        rect = (row[0], row[2], RECT_SIZE, RECT_SIZE)
        if count % 2 == 0:
            pygame.draw.rect(WINDOW, RECT_COLOR_1, rect)
        else:
            pygame.draw.rect(WINDOW, RECT_COLOR_2, rect)
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

    pygame.draw.rect(WINDOW, 'grey', rect)
    pygame.draw.rect(WINDOW, 'dimgrey', rect, width=1)

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
            pygame.draw.rect(WINDOW, 'grey', rect)

        else:
            if symbol == -1:
                return -1

            if symbol == 1:
                color = 'blue'
            elif symbol == 2:
                color = 'darkgreen'
            elif symbol == 3:
                color = 'red'
            elif symbol == 4:
                color = 'violet'
            else:
                color = 'darkviolet'

            if symbol != " ":
                rect = (board_coords_y * RECT_SIZE, board_coords_x * RECT_SIZE, RECT_SIZE, RECT_SIZE)

                pygame.draw.rect(WINDOW, 'grey', rect)
                pygame.draw.rect(WINDOW, 'dimgrey', rect, width=1)

                controls = FONT.render(str(symbol), True, color)
                WINDOW.blit(controls, (x1 + RECT_SIZE / 2 - controls.get_width() / 2, y1 + RECT_SIZE / 2 -
                                       controls.get_height() / 2))
        boolean_board[board_coords_x][board_coords_y][0] = True

        if check_for_win():
            return 1


def game_over(board):
    image = pygame.image.load('icons/mine.png')
    image = pygame.transform.scale(image, (RECT_SIZE, RECT_SIZE))
    for i, row in enumerate(saper.board):
        for j, num in enumerate(row):
            if num == -1:
                x, y, _ = get_position(j * RECT_SIZE + 1, i * RECT_SIZE + 1, board)
                rect = (x, y, RECT_SIZE, RECT_SIZE)
                pygame.draw.rect(WINDOW, 'red', rect)
                WINDOW.blit(image, (x, y))
    pygame.display.update()
    if messagebox.askyesno('You LOST!', "Wanna Play Again?"):
        return 1


def reset_game(board):
    global boolean_board
    global TIME_START
    TIME_START = time.time()
    WINDOW.fill(WINDOW_BACKGROUND_COLOR)

    saper.clear_board()
    saper.place_bombs(BOMBS)
    saper.place_numbers()
    boolean_board = [[[False, False] for _ in range(saper.get_board_size())] for _ in range(saper.get_board_size())]
    draw_board(board)


def check_for_win():
    for i, row in enumerate(saper.board):
        for j, num in enumerate(row):
            if not boolean_board[i][j][0] and num in range(1, 8):
                return False
    return True


def print_clock(time_then, start_clock):
    str_time = "000"
    if start_clock:
        time_now = int(time.time() - time_then)
        if time_now < 10:
            str_time = f"00{time_now}"
        elif time_now < 100:
            str_time = f"0{time_now}"
        else:
            str_time = f"{time_now}"

    game_time = FONT.render(str_time, True, 'black')

    pygame.draw.rect(WINDOW, WINDOW_BACKGROUND_COLOR,
                     pygame.Rect(0, BOARD_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT - BOARD_HEIGHT))
    WINDOW.blit(game_time, (WINDOW_WIDTH / 2 - game_time.get_width() / 2, WINDOW_HEIGHT - 20 -
                            game_time.get_height() / 2))


def main():
    global TIME_START
    run = True
    can_press = True
    start_clock = False
    clock = pygame.time.Clock()
    board = get_board_coords()
    draw_board(board)
    while run:
        clock.tick(999)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if pygame.mouse.get_pos()[1] < BOARD_HEIGHT:
                    TIME_START = time.time() if not start_clock else TIME_START
                    start_clock = True
                    if event.button == 1 and can_press:
                        win = draw_symbol(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], board)
                        if win == -1:
                            can_press = False
                            start_clock = False
                            if game_over(board) == 1:
                                can_press = True
                                reset_game(board)
                            else:
                                run = False
                        elif win == 1:
                            start_clock = False
                            can_press = False
                            pygame.display.update()
                            if messagebox.askyesno('You WON', "Wanna Play Again?"):
                                reset_game(board)
                                can_press = True
                            else:
                                run = False

                    if event.button == 3 and can_press:
                        draw_flag(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], board)
        print_clock(TIME_START, start_clock)
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
