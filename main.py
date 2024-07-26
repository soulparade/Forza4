import numpy as np
import math
import pygame
import sys

from env_var import *

def init_board():
    board = np.zeros(( ROW, COLUMN ))
    return board

def validation_move( board, col_selected, player ):

    if board[ validation_row( board, col_selected ) ][col_selected] == 0:
        return place_piece( board, col_selected, player )

def validation_row( board, col_selected ):

    for r in range(ROW):
        if board[r][col_selected] == 0:
            return r
    return FULL_COLUMN

def place_piece( board, col_selected, player ):

    board[ validation_row( board, col_selected ) ][col_selected] = player
    return board

def validation_winning( board, player ):
    for c in range( COLUMN-3 ):   # -
        for r in range( ROW ):
            if board[r][c] == player and board[r][c+1] == player and board[r][c+2] == player and board[r][c+3] == player:
                return True

    for c in range( COLUMN ): # |
        for r in range( ROW-3 ):
            if board[r][c] == player and board[r+1][c] == player and board[r+2][c] == player and board[r+3][c] == player:
                return True

    for c in range( COLUMN-3 ):   # /
        for r in range( ROW-3 ):
            if board[r][c] == player and board[r+1][c+1] == player and board[r+2][c+2] == player and board[r+3][c+3] == player:
                return True

    for c in range( COLUMN-3 ):   # \
        for r in range( 2, ROW ):
            if board[r][c] == player and board[r-1][c+1] == player and board[r-2][c+2] == player and board[r-3][c+3] == player:
                return True
    validation_tie( board )

def validation_tie( board):
    return not np.any(board == 0)


def draw_board( board ):
    for c in range( COLUMN ):
        for r in range ( ROW ):
            pygame.draw.rect( screen, BLUE, ( c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE ))
            pygame.draw.circle( screen, BLACK, ( int (c * SQUARE_SIZE + SQUARE_SIZE / 2), int( r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2 )), CIRCLE_RADIUS )

    for c in range(COLUMN):
        for r in range(ROW):
            if board[r][c] == PLAYER1:
                pygame.draw.circle( screen, RED, ( int (c * SQUARE_SIZE + SQUARE_SIZE / 2), HEIGHT - int( r * SQUARE_SIZE + SQUARE_SIZE / 2 )), CIRCLE_RADIUS )
            if board[r][c] == PLAYER2:
                pygame.draw.circle( screen, YELLOW, ( int (c * SQUARE_SIZE + SQUARE_SIZE / 2), HEIGHT - int( r * SQUARE_SIZE + SQUARE_SIZE / 2 )), CIRCLE_RADIUS )
    pygame.display.update()

def player_turn( event, board, player, color ):
    
    pos_x = event.pos[0]
    col_selected = int( math.floor( pos_x / SQUARE_SIZE ) )

    while True:
        if validation_row(board, col_selected ) != FULL_COLUMN:
            validation_move(board, col_selected, player)
            break

    if validation_winning(board, player):
        label = FONT.render( f"Player {player} wins", 1, GREEN)
        screen.blit( label, ( 40, 10 ) )
        WINNER = True
        return WINNER

    if validation_tie( board ):
        label = FONT.render("Tie game", 1, GREEN )
        screen.blit( label, ( 40, 10 ) )
        WINNER = True 
        return WINNER

board = init_board()
pygame.init()

screen = pygame.display.set_mode( SIZE )
draw_board( board )
pygame.display.update()

while not WINNER:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect( screen, BLACK, ( 0, 0, WIDTH, SQUARE_SIZE ) )
            pos_x = event.pos[0]
            col_selected = int( math.floor( pos_x / SQUARE_SIZE ) )

            if TURN % 2 == 0:
                pygame.draw.circle( screen, RED, ( col_selected * SQUARE_SIZE + SQUARE_SIZE / 2, int( SQUARE_SIZE / 2 ) ), CIRCLE_RADIUS )
                pygame.display.update()

            if TURN % 2 != 0:
                pygame.draw.circle( screen, YELLOW, ( col_selected * SQUARE_SIZE + SQUARE_SIZE / 2, int(SQUARE_SIZE / 2 ) ), CIRCLE_RADIUS )
                pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if TURN % 2 == 0:
                player_turn( event, board, PLAYER1, RED )
                WINNER = validation_winning( board, PLAYER1 )

            if TURN % 2 != 0:
                player_turn( event, board, PLAYER2, YELLOW )
                WINNER = validation_winning( board, PLAYER2 )

            TURN += 1
            draw_board( board ) 

            if WINNER:
                pygame.time.wait( 3000 )
                break