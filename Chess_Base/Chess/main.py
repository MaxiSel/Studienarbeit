"""
Main file to handle Input and Basic GUI for the user or testing
"""
import pygame as p
from Chess import ChessEngine
WIDTH = HEIGHT = 1024
DIMENSION = 8
SQUARE_Size=HEIGHT//DIMENSION
Max_FPS=24
IMAGES={}
p.init()

"""
Init global Image dic. Only onetime execution in main
"""
def imageLoader():
    pieces={'wP','wR','wN','wB','wQ','wK','bP','bN','bR','bB','bQ','bK'}
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('images/'+piece+'.png'),(SQUARE_Size,SQUARE_Size))



"""
Main Handler
"""
def main():
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock= p.time.Clock()
    screen.fill(p.Color('lightblue'))
    gameStatus= ChessEngine.GameState()
    imageLoader()
    game_runs = True

    while game_runs:
        for e in p.event.get():
            if e.type == p.QUIT:
                game_runs= False
        drawGameState(screen,gameStatus)
        clock.tick(Max_FPS)
        p.display.flip()
"""
Draw the GUI for the chess board
"""
def drawGameState(screen, gameStatus):
    drawBoard(screen)
    drawPieces(screen,gameStatus.board)

def drawBoard(screen):
    colors= p.Color('white'), p.Color('lightgray')
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color=colors[((row+column)%2)]
            p.draw.rect(screen,color,p.Rect(column*SQUARE_Size,row*SQUARE_Size,SQUARE_Size,SQUARE_Size))


def drawPieces(screen, board):
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece!='--':
                screen.blit(IMAGES[piece],p.Rect(column*SQUARE_Size,row*SQUARE_Size,SQUARE_Size,SQUARE_Size))


if __name__ == '__main__':
    main()
