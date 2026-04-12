import pygame as pg
import random
import os

from pygame.locals import (
    QUIT,
    KEYDOWN,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    MOUSEMOTION,
    K_ESCAPE
)

os.chdir(r"C:\Users\joaop\.vscode\dot.py_files\jogo_do_livro")

BOARD_LENGH = 9

N_OF_SLAVES = BOARD_LENGH*2
N_OF_SOLDIERS = BOARD_LENGH
N_OF_ARCHERS = BOARD_LENGH // 2
N_OF_CALVARY = BOARD_LENGH // 2
N_OF_CATAPULTS = BOARD_LENGH // 4
N_OF_GENERALS = BOARD_LENGH // 5
N_OF_KINGS = 1

WHITE_PIECE_LIST = ['e', 's', 'a', 'c', 't', 'g']
BLACK_PIECE_LIST = ['E', 'S', 'A', 'C', 'T', 'G']

TILE_SIZE = 600//BOARD_LENGH

LIGHT = (255,210,140)
DARK = (90,40,0)

black_pieces = [['E' for _ in range(N_OF_SLAVES)], ['S' for _ in range(N_OF_SOLDIERS)], ['A' for _ in range(N_OF_ARCHERS)], ['C' for _ in range(N_OF_CALVARY)], ['T' for _ in range(N_OF_CATAPULTS)], ['G' for _ in range(N_OF_GENERALS)]]
white_pieces = [['e' for _ in range(N_OF_SLAVES)], ['s' for _ in range(N_OF_SOLDIERS)], ['a' for _ in range(N_OF_ARCHERS)], ['c' for _ in range(N_OF_CALVARY)], ['t' for _ in range(N_OF_CATAPULTS)], ['g' for _ in range(N_OF_GENERALS)]]

placed_black_pieces = [[] for _ in range(7)]
placed_white_pieces = [[] for _ in range(7)]

board = [[' ' for _ in range(BOARD_LENGH)] for _ in range(BOARD_LENGH)]

# print(board)
# print(black_pieces)
# print(white_pieces)

def print_board():
    print(' '+' | '.join([str(i) for i in range(BOARD_LENGH)]))
    print('-'+'--' * (BOARD_LENGH * 2 - 1)+'|')
    i = 0
    for row in board:
        print(' '+' | '.join(row)+f' | {i}')
        print('-'+'--' * (BOARD_LENGH * 2 - 1)+'|')
        i += 1
    print(' ' + ' | '.join([str(i) for i in range(BOARD_LENGH)]))
# print_board()
def place_piece(piece, position):
    row, col = position
    if 0 <= row < BOARD_LENGH and 0 <= col < BOARD_LENGH:
        if board[row][col] == ' ':
            board[row][col] = piece
            return True
        else:
            print("Position already occupied.")
            return False
    else:
        print("Invalid position.")
        return False

place_piece('K', (0,BOARD_LENGH//2))
place_piece('k', (BOARD_LENGH-1,BOARD_LENGH//2))

pg.init()

screen = pg.display.set_mode((BOARD_LENGH * TILE_SIZE + TILE_SIZE*2, BOARD_LENGH * TILE_SIZE), pg.SCALED | pg.FULLSCREEN)
pg.display.set_caption("(Nome do Jogo) - Jogo Livro")


def draw_board():
    for row in range(BOARD_LENGH):
        for col in range(BOARD_LENGH):
            if (row + col) % 2 == 0:
                color = LIGHT  # Light color
            else:
                color = DARK  # Dark color
            pg.draw.rect(screen, color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if board[row][col] != ' ':
                piece = board[row][col]
                if piece.islower():
                    if piece == 'k':
                        image = pg.image.load("7.png").convert()
                    elif piece == 'g':
                        image = pg.image.load("6.png").convert()
                    elif piece == 't':
                        image = pg.image.load("5.png").convert()
                    elif piece == 'c':
                        image = pg.image.load("4.png").convert()
                    elif piece == 'a':
                        image = pg.image.load("3.png").convert()
                    elif piece == 's':
                        image = pg.image.load("2.png").convert()
                    elif piece == 'e':
                        image = pg.image.load("1.png").convert()
                else:
                    piece = piece.lower()
                    if piece == 'k':
                        image = pg.image.load("7.png").convert()
                    elif piece == 'g':
                        image = pg.image.load("6.png").convert()
                    elif piece == 't':
                        image = pg.image.load("5.png").convert()
                    elif piece == 'c':
                        image = pg.image.load("4.png").convert()
                    elif piece == 'a':
                        image = pg.image.load("3.png").convert()
                    elif piece == 's':
                        image = pg.image.load("2.png").convert()
                    elif piece == 'e':
                        image = pg.image.load("1.png").convert()
                    arr = pg.surfarray.pixels3d(image)
                    arr[:] = 255 - arr
                    del arr
                    piece = board[row][col]
                image.set_colorkey((0,255,0) if not piece.isupper() else (255,0,255))
                screen.blit(pg.transform.scale(image, (TILE_SIZE, TILE_SIZE)), (col*TILE_SIZE, row*TILE_SIZE), )

def draw_available_pieces():
    font = pg.font.Font(None, TILE_SIZE//2-1)
    y_offset = 10
    for i, pieces in enumerate(white_pieces):
        text = font.render(f"{WHITE_PIECE_LIST[i]}: {len(pieces)}", True, (255, 255, 255))
        pg.draw.rect(screen, LIGHT, (BOARD_LENGH * TILE_SIZE, y_offset-10, TILE_SIZE+5, TILE_SIZE))
        screen.blit(text, (BOARD_LENGH * TILE_SIZE + (TILE_SIZE//5), y_offset))
        y_offset += TILE_SIZE
    y_offset = 10
    for i, pieces in enumerate(black_pieces):
        text = font.render(f"{BLACK_PIECE_LIST[i]}: {len(pieces)}", True, (0, 0, 0))
        pg.draw.rect(screen, DARK, (BOARD_LENGH * TILE_SIZE + TILE_SIZE, y_offset-10, TILE_SIZE+5, TILE_SIZE))
        screen.blit(text, (BOARD_LENGH * TILE_SIZE+(TILE_SIZE+TILE_SIZE//5), y_offset))
        y_offset += TILE_SIZE

def available_moves(input):
    if input[0] == 'M':
        row_from = int(input[1])
        col_from = int(input[2])
        piece = board[row_from][col_from]
        if piece == ' ':
            pass
        if piece.lower() == 'e':
            for i in range(-2,3):
                for j in range(-2,3):
                    if (0 <= row_from + i < BOARD_LENGH) and (0 <= col_from + j < BOARD_LENGH):
                        if (i == 0 or j == 0) and (i != j) and is_path_clear((row_from, col_from), (row_from + i, col_from + j)):
                            if board[row_from + i][col_from + j] == ' ':
                                pg.draw.circle(screen, (0,255,0), ((col_from+j) * TILE_SIZE + TILE_SIZE//2, (row_from+i) * TILE_SIZE + TILE_SIZE//2), TILE_SIZE//4)
                                possible_moves.append((row_from + i, col_from + j))
                        elif (i == -1 or i == 1) and (j == -1 or j == 1):
                            if (board[row_from + i][col_from + j].islower() and piece.isupper()) or (board[row_from + i][col_from + j].isupper() and piece.islower()):
                                pg.draw.circle(screen, (255,0,0), ((col_from+j) * TILE_SIZE + TILE_SIZE//2, (row_from+i) * TILE_SIZE + TILE_SIZE//2), TILE_SIZE//4)
                                possible_moves.append((row_from + i, col_from + j))
        elif piece.lower() == 's':
            for i in range(-2,3):
                for j in range(-2,3):
                    if (0 <= row_from + i < BOARD_LENGH) and (0 <= col_from + j < BOARD_LENGH):
                        if (i == 0 or j == 0) and (i != j):
                            if board[row_from + i][col_from + j] == ' ' and is_path_clear((row_from, col_from), (row_from + i, col_from + j)):
                                pg.draw.circle(screen, (0,255,0), ((col_from+j) * TILE_SIZE + TILE_SIZE//2, (row_from+i) * TILE_SIZE + TILE_SIZE//2), TILE_SIZE//4)
                                possible_moves.append((row_from + i, col_from + j))
                            elif (board[row_from + i][col_from + j].islower() and piece.isupper()) or (board[row_from + i][col_from + j].isupper() and piece.islower()) and is_path_clear((row_from, col_from), (row_from + i, col_from + j)):
                                pg.draw.circle(screen, (255,0,0), ((col_from+j) * TILE_SIZE + TILE_SIZE//2, (row_from+i) * TILE_SIZE + TILE_SIZE//2), TILE_SIZE//4)
                                possible_moves.append((row_from + i, col_from + j))
        elif piece.lower() == 'a':
            for i in range(-5,6):
                for j in range(-5,6):
                    if (0 <= row_from + i < BOARD_LENGH) and (0 <= col_from + j < BOARD_LENGH):
                        if (i == 0 or j == 0) and (i != j):
                            if board[row_from + i][col_from + j] == ' ':
                                pg.draw.circle(screen, (0,255,0), ((col_from+j) * TILE_SIZE + TILE_SIZE//2, (row_from+i) * TILE_SIZE + TILE_SIZE//2), TILE_SIZE//4)
                                possible_moves.append((row_from + i, col_from + j))
                            elif (board[row_from + i][col_from + j].islower() and piece.isupper()) or (board[row_from + i][col_from + j].isupper() and piece.islower()):
                                pg.draw.circle(screen, (255,0,0), ((col_from+j) * TILE_SIZE + TILE_SIZE//2, (row_from+i) * TILE_SIZE + TILE_SIZE//2), TILE_SIZE//4)
                                possible_moves.append((row_from + i, col_from + j))
                        elif i == j or i == -j:
                            if board[row_from + i][col_from + j] == ' ':
                                pg.draw.circle(screen, (0,255,0), ((col_from+j) * TILE_SIZE + TILE_SIZE//2, (row_from+i) * TILE_SIZE + TILE_SIZE//2), TILE_SIZE//4)
                                possible_moves.append((row_from + i, col_from + j))
                            elif (board[row_from + i][col_from + j].islower() and piece.isupper()) or (board[row_from + i][col_from + j].isupper() and piece.islower()):
                                pg.draw.circle(screen, (255,0,0), ((col_from+j) * TILE_SIZE + TILE_SIZE//2, (row_from+i) * TILE_SIZE + TILE_SIZE//2), TILE_SIZE//4)
                                possible_moves.append((row_from + i, col_from + j))
        elif piece.lower() == 'c':
            for i in range(-5,6):
                for j in range(-5,6):
                    if (0 <= row_from + i < BOARD_LENGH) and (0 <= col_from + j < BOARD_LENGH):
                        if (i == 0 or j == 0) and (i != j):
                            if board[row_from + i][col_from + j] == ' ' and is_path_clear((row_from, col_from), (row_from + i, col_from + j)):
                                pg.draw.circle(screen, (0,255,0), ((col_from+j) * TILE_SIZE + TILE_SIZE//2, (row_from+i) * TILE_SIZE + TILE_SIZE//2), TILE_SIZE//4)
                                possible_moves.append((row_from + i, col_from + j))
                            elif (board[row_from + i][col_from + j].islower() and piece.isupper()) or (board[row_from + i][col_from + j].isupper() and piece.islower()) and is_path_clear((row_from, col_from), (row_from + i, col_from + j)):
                                pg.draw.circle(screen, (255,0,0), ((col_from+j) * TILE_SIZE + TILE_SIZE//2, (row_from+i) * TILE_SIZE + TILE_SIZE//2), TILE_SIZE//4)
                                possible_moves.append((row_from + i, col_from + j))
                        elif i == j or i == -j:
                            if board[row_from + i][col_from + j] == ' ':
                                pg.draw.circle(screen, (0,255,0), ((col_from+j) * TILE_SIZE + TILE_SIZE//2, (row_from+i) * TILE_SIZE + TILE_SIZE//2), TILE_SIZE//4)
                                possible_moves.append((row_from + i, col_from + j))
                            elif (board[row_from + i][col_from + j].islower() and piece.isupper()) or (board[row_from + i][col_from + j].isupper() and piece.islower()):
                                pg.draw.circle(screen, (255,0,0), ((col_from+j) * TILE_SIZE + TILE_SIZE//2, (row_from+i) * TILE_SIZE + TILE_SIZE//2), TILE_SIZE//4)
                                possible_moves.append((row_from + i, col_from + j))
        elif piece.lower() == 't':
            for i in range(-BOARD_LENGH,BOARD_LENGH+1):
                for j in range(-BOARD_LENGH,BOARD_LENGH+1):
                    if (0 <= row_from + i < BOARD_LENGH) and (0 <= col_from + j < BOARD_LENGH):
                        if (i == 0 or j == 0) and (i != j):
                            if board[row_from + i][col_from + j] == ' ' and (-2 < j < 2 and -2 < i < 2):
                                pg.draw.circle(screen, (0,255,0), ((col_from+j) * TILE_SIZE + TILE_SIZE//2, (row_from+i) * TILE_SIZE + TILE_SIZE//2), TILE_SIZE//4)
                                possible_moves.append((row_from + i, col_from + j))
                            elif ((board[row_from + i][col_from + j].islower() and piece.isupper()) or (board[row_from + i][col_from + j].isupper() and piece.islower())) and ((i > 2 or i < -2) or (j > 2 or j < -2)):
                                pg.draw.circle(screen, (255,0,0), ((col_from+j) * TILE_SIZE + TILE_SIZE//2, (row_from+i) * TILE_SIZE + TILE_SIZE//2), TILE_SIZE//4)
                                possible_moves.append((row_from + i, col_from + j))
                        elif i == j or i == -j:
                            if board[row_from + i][col_from + j] == ' ' and (-2 < j < 2 and -2 < i < 2):
                                pg.draw.circle(screen, (0,255,0), ((col_from+j) * TILE_SIZE + TILE_SIZE//2, (row_from+i) * TILE_SIZE + TILE_SIZE//2), TILE_SIZE//4)
                                possible_moves.append((row_from + i, col_from + j))
                            elif ((board[row_from + i][col_from + j].islower() and piece.isupper()) or (board[row_from + i][col_from + j].isupper() and piece.islower())) and ((i > 2 or i < -2) or (j > 2 or j < -2)):
                                pg.draw.circle(screen, (255,0,0), ((col_from+j) * TILE_SIZE + TILE_SIZE//2, (row_from+i) * TILE_SIZE + TILE_SIZE//2), TILE_SIZE//4)
                                possible_moves.append((row_from + i, col_from + j))
        elif piece.lower() == 'g':
            for i in range(-BOARD_LENGH,BOARD_LENGH+1):
                for j in range(-BOARD_LENGH,BOARD_LENGH+1):
                    if (0 <= row_from + i < BOARD_LENGH) and (0 <= col_from + j < BOARD_LENGH):
                        if (i == 0 or j == 0) and (i != j): # check strait lines
                            if board[row_from + i][col_from + j] == ' ' and is_path_clear((row_from, col_from), (row_from + i, col_from + j)):
                                pg.draw.circle(screen, (0,255,0), ((col_from+j) * TILE_SIZE + TILE_SIZE//2, (row_from+i) * TILE_SIZE + TILE_SIZE//2), TILE_SIZE//4)
                                possible_moves.append((row_from + i, col_from + j))
                            elif ((board[row_from + i][col_from + j].islower() and piece.isupper()) or (board[row_from + i][col_from + j].isupper() and piece.islower())) and is_path_clear((row_from, col_from), (row_from + i, col_from + j)):
                                pg.draw.circle(screen, (255,0,0), ((col_from+j) * TILE_SIZE + TILE_SIZE//2, (row_from+i) * TILE_SIZE + TILE_SIZE//2), TILE_SIZE//4)
                                possible_moves.append((row_from + i, col_from + j))
                        elif i == j or i == -j: # check diagonals
                            if board[row_from + i][col_from + j] == ' ' and is_path_clear((row_from, col_from), (row_from + i, col_from + j)):
                                pg.draw.circle(screen, (0,255,0), ((col_from+j) * TILE_SIZE + TILE_SIZE//2, (row_from+i) * TILE_SIZE + TILE_SIZE//2), TILE_SIZE//4)
                                possible_moves.append((row_from + i, col_from + j))
                            elif ((board[row_from + i][col_from + j].islower() and piece.isupper()) or (board[row_from + i][col_from + j].isupper() and piece.islower())) and is_path_clear((row_from, col_from), (row_from + i, col_from + j)):
                                pg.draw.circle(screen, (255,0,0), ((col_from+j) * TILE_SIZE + TILE_SIZE//2, (row_from+i) * TILE_SIZE + TILE_SIZE//2), TILE_SIZE//4)
                                possible_moves.append((row_from + i, col_from + j))
        elif piece.lower() == 'k':
            for i in range(-2,3):
                for j in range(-2,3):
                    if (0 <= row_from + i < BOARD_LENGH) and (0 <= col_from + j < BOARD_LENGH):
                        if (i == 0 or j == 0) and (i != j):
                            if board[row_from + i][col_from + j] == ' ' and is_path_clear((row_from, col_from), (row_from + i, col_from + j)):
                                pg.draw.circle(screen, (0,255,0), ((col_from+j) * TILE_SIZE + TILE_SIZE//2, (row_from+i) * TILE_SIZE + TILE_SIZE//2), TILE_SIZE//4)
                                possible_moves.append((row_from + i, col_from + j))
                            elif (board[row_from + i][col_from + j].islower() and piece.isupper()) or (board[row_from + i][col_from + j].isupper() and piece.islower()) and is_path_clear((row_from, col_from), (row_from + i, col_from + j)):
                                pg.draw.circle(screen, (255,0,0), ((col_from+j) * TILE_SIZE + TILE_SIZE//2, (row_from+i) * TILE_SIZE + TILE_SIZE//2), TILE_SIZE//4)
                                possible_moves.append((row_from + i, col_from + j))
                        elif i == j or i == -j:
                            if board[row_from + i][col_from + j] == ' ' and is_path_clear((row_from, col_from), (row_from + i, col_from + j)):
                                pg.draw.circle(screen, (0,255,0), ((col_from+j) * TILE_SIZE + TILE_SIZE//2, (row_from+i) * TILE_SIZE + TILE_SIZE//2), TILE_SIZE//4)
                                possible_moves.append((row_from + i, col_from + j))
                            elif (board[row_from + i][col_from + j].islower() and piece.isupper()) or (board[row_from + i][col_from + j].isupper() and piece.islower()) and is_path_clear((row_from, col_from), (row_from + i, col_from + j)):
                                pg.draw.circle(screen, (255,0,0), ((col_from+j) * TILE_SIZE + TILE_SIZE//2, (row_from+i) * TILE_SIZE + TILE_SIZE//2), TILE_SIZE//4)
                                possible_moves.append((row_from + i, col_from + j))            
    elif input[0] == 'P':
        for i in range(BOARD_LENGH):
            if turns % 2 == 0:
                for j in range(BOARD_LENGH-BOARD_LENGH//3, BOARD_LENGH):
                    if board[j][i] == ' ':
                        pg.draw.circle(screen, (0,0,255), (i * TILE_SIZE + TILE_SIZE//2, j * TILE_SIZE + TILE_SIZE//2), TILE_SIZE//4)
                        possible_moves.append((j, i))
            elif turns % 2 != 0:
                for j in range(0, BOARD_LENGH//3):
                    if board[j][i] == ' ':
                        pg.draw.circle(screen, (0,0,255), (i * TILE_SIZE + TILE_SIZE//2, j * TILE_SIZE + TILE_SIZE//2), TILE_SIZE//4)
                        possible_moves.append((j, i))

def is_path_clear(from_pos, to_pos):
    row1, col1 = from_pos
    row2, col2 = to_pos
    dr = row2 - row1
    dc = col2 - col1

    steps = max(abs(dr), abs(dc))
    if steps == 0:
        return False  # Same square

    step_r = (dr // steps) if dr != 0 else 0
    step_c = (dc // steps) if dc != 0 else 0

    r, c = row1 + step_r, col1 + step_c
    for _ in range(steps - 1):  # Exclude destination
        if board[r][c] != ' ':
            return False
        r += step_r
        c += step_c
    return True

def check_winner():
    a = 0
    for i in range(len(board)):
        if 'k' in board[i]:
            a += 1
        if 'K' in board[i]:
            a -= 1
    
    #print(a)

    if a != 0:
        if a > 0:
            return True, 'White'
        elif a < 0:
            return True, 'Black'
    else:
        return False

class Bot():
    def bot_move(pieces):
        all_available_moves = []
        placed_pieces = []
        PorM = random.choice(['P', 'M'])
        print(PorM)
        if PorM == 'P':
            choosed_piece = random.choice(pieces)
            for i in range(BOARD_LENGH//3):
                for j in range(BOARD_LENGH):
                    if board[i][j] == ' ':
                        all_available_moves.append((i, j))
            choosed_position = random.choice(all_available_moves)
            # print([PorM, choosed_piece.lower(), '-', str(choosed_position[0]), str(choosed_position[1])])
            return [PorM, choosed_piece.lower(), '-', str(choosed_position[0]), str(choosed_position[1])]
        else:
            for i in range(len(board)):
                for j in range(len(board[i])):
                    if board[i][j] != ' ' and board[i][j].isupper():
                        placed_pieces.append((i,j))
            initial_position = random.choice(placed_pieces)
            initial_choice = [PorM, str(initial_position[0]), str(initial_position[1]), '-', '-']
            available_moves(initial_choice)
            final_position = random.choice(possible_moves)
            return [PorM, str(initial_position[0]), str(initial_position[1]), str(final_position[0]), str(final_position[1])]

turns = 0
clicks = 0
user_input = ['-']*5

clock = pg.time.Clock()

font = pg.font.Font(None, 50)

print(BOARD_LENGH//3)
print(BOARD_LENGH - BOARD_LENGH//3)

while True:
    possible_moves = []
    player = ['-']*5

    if turns%2 == 0:
        screen.fill((255,255,255))
    else:
        screen.fill((0,0,0))
        # player = Bot.bot_move(BLACK_PIECE_LIST)
        # print(player)

    draw_board()
    draw_available_pieces()
    available_moves(user_input)

    if check_winner():
        winner_message = font.render(f"{check_winner()[1]} Wins!", True, (0,0,0) if check_winner()[1] == "White" else (255,255,255))
        pg.draw.rect(screen, (255,255,255) if check_winner()[1] == "White" else (0,0,0), (((BOARD_LENGH * TILE_SIZE)//2 - len(f"{check_winner()[1]} Wins!")*8)-10, ((BOARD_LENGH * TILE_SIZE)//2-10)-5, 220, 40))
        screen.blit(winner_message, ((BOARD_LENGH * TILE_SIZE)//2 - len(f"{check_winner()[1]} Wins!")*8, (BOARD_LENGH * TILE_SIZE)//2-10))

    pg.display.flip()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pg.quit()
                exit()

    if pg.mouse.get_pressed()[0]: # Left mouse button pressed
        #print(possible_moves)
        mouse_x, mouse_y = pg.mouse.get_pos()
        row = mouse_y // TILE_SIZE
        col = mouse_x // TILE_SIZE
        if (0 <= row < BOARD_LENGH and 0 <= col < BOARD_LENGH) and clicks == 0:
            user_input = ['-']*5
            user_input[0] = 'M'  # Set the action to move
            user_input[1] = str(row)
            user_input[2] = str(col)
            clicks += 1
            #print(user_input, clicks)
            pg.time.delay(250)  # Delay to allow the user to see the selection
        elif (0 <= row < BOARD_LENGH and 0 <= col < BOARD_LENGH) and clicks == 1 and (row,col) in possible_moves:
            user_input[3] = str(row)
            user_input[4] = str(col)
            player = user_input
            user_input = ['-']*5
           # print(player)
            clicks = 0
            pg.time.delay(250)
        elif (row >= BOARD_LENGH or col >= BOARD_LENGH) and clicks == 0:
            user_input = ['-']*5
            user_input[0] = 'P'
            if mouse_x < BOARD_LENGH * TILE_SIZE + 90:
                user_input[1] = WHITE_PIECE_LIST[row]
            else:
                user_input[1] = BLACK_PIECE_LIST[row]
            clicks += 1
            #print(user_input, clicks)
            pg.time.delay(250)
        else:
            user_input = ['-'*5]
            clicks = 0
    # player = str(input())
    # for i in range(len(white_pieces)):
    #     print(f"{['e', 's', 'a', 'c', 't', 'g', 'k'][i]}: {len(white_pieces[i])}")
    # for i in range(len(black_pieces)):
    #     print(f"{['E', 'S', 'A', 'C', 'C', 'G', 'K'][i]}: {len(black_pieces[i])}")
    
    if player[0] == 'P':
        if player[1].upper() in ['E', 'S', 'A', 'C', 'T', 'G'] and (player[4].isdigit() and player[4].isdigit()):
            piece = player[1]
            position = (int(player[3]), int(player[4]))
            if turns % 2 == 0 and int(player[3]) >= BOARD_LENGH-BOARD_LENGH//3:
                if place_piece(piece.lower(), position) and len(white_pieces[['e', 's', 'a', 'c', 't', 'g'].index(piece.lower())]) > 0:
                    white_pieces[['e', 's', 'a', 'c', 't', 'g'].index(piece)].remove(piece.lower())
                    placed_white_pieces[['e', 's', 'a', 'c', 't', 'g'].index(piece)].append(piece.lower())
                    #print("Piece placed successfully.")
                    turns += 1
            elif turns % 2 != 0 and int(player[3]) <= BOARD_LENGH//3:
                if place_piece(piece.upper(), position) and len(black_pieces[['E', 'S', 'A', 'C', 'T', 'G'].index(piece.upper())]) > 0:
                    black_pieces[['E', 'S', 'A', 'C', 'T', 'G'].index(piece.upper())].remove(piece.upper())
                    placed_black_pieces[['E', 'S', 'A', 'C', 'T', 'G'].index(piece.upper())].append(piece.upper())
                   # print("Piece placed successfully.")
                    turns += 1
            else:
                pass
               # print("Invalid move: You cannot place a piece in the opponent's territory.")
        else:
            pass
            #print("Invalid input. Please use the format 'P<Piece><Row><Column>' (e.g., Pk23 for placing a king at row 2, column 3).")
        #print_board()
    elif player[0] == 'M':
        if player[1].isdigit() and player[2].isdigit() and player[3].isdigit() and player[4].isdigit():
            from_position = (int(player[1]), int(player[2]))
            to_position = (int(player[3]), int(player[4]))
            piece = board[from_position[0]][from_position[1]]
            if piece != ' ':
                if turns % 2 != 0 and piece.islower():
                    pass
                   # print("Invalid move: You cannot move a opponent's piece.")
                elif turns % 2 == 0 and piece.isupper():
                    pass
                  #  print("Invalid move: You cannot move a opponent's piece.")
                elif from_position == to_position:
                    pass
                elif (board[from_position[0]][from_position[1]].islower() and board[to_position[0]][to_position[1]].islower()) or (board[from_position[0]][from_position[1]].isupper() and board[to_position[0]][to_position[1]].isupper()):
                    pass
                else:
                    board[to_position[0]][to_position[1]] = piece
                    board[from_position[0]][from_position[1]] = ' '
                    turns += 1
            else:
                pass
              #  print("Invalid move: No piece at the specified position.")
        else:
            pass
           # print("Invalid input. Please use the format 'M<RowFrom><ColumnFrom><RowTo><ColumnTo>' (e.g., M12 for moving a piece from row 1, column 2 to row 1, column 2).")
        #print_board()