import numpy as np
import math
import pygame
import sys
import json

from env_var import *
from websocket_main import *

def init_board():
    board = np.zeros((ROW, COLUMN))
    return board

def validation_move(board, col_selected, player):
    row = validation_row(board, col_selected)
    if row != FULL_COLUMN:
        return place_piece(board, col_selected, row, player)

def validation_row(board, col_selected):
    for r in range(ROW):
        if board[r][col_selected] == 0:
            return r
    return FULL_COLUMN

def place_piece(board, col_selected, row, player):
    board[row][col_selected] = player
    return board

def validation_winning(board, player):
    for c in range(COLUMN-3):  # -
        for r in range(ROW):
            if (board[r][c] == player and board[r][c+1] == player and 
                board[r][c+2] == player and board[r][c+3] == player):
                return True

    for c in range(COLUMN):  # |
        for r in range(ROW-3):
            if (board[r][c] == player and board[r+1][c] == player and 
                board[r+2][c] == player and board[r+3][c] == player):
                return True

    for c in range(COLUMN-3):  # /
        for r in range(ROW-3):
            if (board[r][c] == player and board[r+1][c+1] == player and 
                board[r+2][c+2] == player and board[r+3][c+3] == player):
                return True

    for c in range(COLUMN-3):  # \
        for r in range(3, ROW):
            if (board[r][c] == player and board[r-1][c+1] == player and 
                board[r-2][c+2] == player and board[r-3][c+3] == player):
                return True
    return validation_tie(board)

def validation_tie(board):
    return not np.any(board == 0)

def draw_board(board):
    for c in range(COLUMN):
        for r in range(ROW):
            pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), CIRCLE_RADIUS)

    for c in range(COLUMN):
        for r in range(ROW):
            if board[r][c] == PLAYER1:
                pygame.draw.circle(screen, RED, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), HEIGHT - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), CIRCLE_RADIUS)
            elif board[r][c] == PLAYER2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), HEIGHT - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), CIRCLE_RADIUS)
    pygame.display.update()

def player_turn(col_selected, board, player):
    if validation_row(board, col_selected) != FULL_COLUMN:
        validation_move(board, col_selected, player)

        if validation_winning(board, player):
            label = FONT.render(f"Player {player} wins", 1, GREEN)
            screen.blit(label, (40, 10))
            pygame.display.update()
            return True

        if validation_tie(board):
            label = FONT.render("Tie game", 1, GREEN)
            screen.blit(label, (40, 10))
            pygame.display.update()
            return True

    return False

def handle_message(message):
    global TURN, WINNER
    data = json.loads(message)
    col_selected = data['col_selected']
    player = data['player']
    WINNER = player_turn(col_selected, board, player)
    TURN += 1
    draw_board(board)
    if WINNER:
        pygame.time.wait(3000)

board = init_board()
pygame.init()

screen = pygame.display.set_mode(SIZE)
draw_board(board)
pygame.display.update()

ws = connect_to_websocket(ws_url)

if not ws:
    print("Impossibile connettersi al WebSocket. Verifica la connessione.")
    sys.exit()

def send_turn(col_selected, player):
    message = {
        'col_selected': col_selected,
        'player': player
    }
    send_message(ws, message)

while not WINNER:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
            pos_x = event.pos[0]
            col_selected = int(math.floor(pos_x / SQUARE_SIZE))

            if TURN % 2 == 0:
                pygame.draw.circle(screen, RED, (col_selected * SQUARE_SIZE + SQUARE_SIZE / 2, int(SQUARE_SIZE / 2)), CIRCLE_RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (col_selected * SQUARE_SIZE + SQUARE_SIZE / 2, int(SQUARE_SIZE / 2)), CIRCLE_RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if (TURN % 2 == 0 and ws.url.endswith('player1')) or (TURN % 2 != 0 and ws.url.endswith('player2')):
                pos_x = event.pos[0]
                col_selected = int(math.floor(pos_x / SQUARE_SIZE))

                if validation_row(board, col_selected) != FULL_COLUMN:
                    send_turn(col_selected, PLAYER1 if TURN % 2 == 0 else PLAYER2)

            draw_board(board)
    
    # Check for messages from WebSocket
    try:
        message = ws.recv()
        if message:
            handle_message(message)
    except websocket.WebSocketTimeoutException:
        pass
