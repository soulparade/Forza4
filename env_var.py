import pygame
pygame.font.init()
FULL_COLUMN = 6
WINNER = False
TURN = 0
COLUMN = 7
ROW = 6
SQUARE_SIZE = 100
CIRCLE_RADIUS = SQUARE_SIZE / 2 - 5
WIDTH = COLUMN * SQUARE_SIZE
HEIGHT = ( ROW + 1 ) * SQUARE_SIZE
SIZE = ( WIDTH, HEIGHT)
FONT = pygame.font.SysFont("monospace", 75)
RED = ( 255, 0, 0)
YELLOW = ( 255, 255, 0 )
BLACK = ( 0, 0, 0)
GREEN = ( 0, 255, 0)
BLUE = ( 0, 0, 200)
PLAYER1 = 1
PLAYER2 = 2