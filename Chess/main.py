"""
Main file to handle Input and Basic GUI for the user or testing
"""
import pygame as p
from Chess import ChessEngine
WIDTH = HEIGHT = 512
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
    game_status= ChessEngine.GameState()
    imageLoader()
    game_runs = True
    field_selected=()
    player_clicks=[]# Stores Player Mouse Click Input


    while game_runs:
        for e in p.event.get():
            if e.type == p.QUIT:
                game_runs= False
            elif e.type == p.MOUSEBUTTONDOWN:
                mouse_pos=p.mouse.get_pos()
                mouse_x_pos= mouse_pos[0]//SQUARE_Size
                mouse_y_pos= mouse_pos[1]//SQUARE_Size
               # print(mouse_x_pos,mouse_y_pos)
                if(field_selected==(mouse_x_pos,mouse_y_pos)):
                    field_selected=()
                    player_clicks=[]
                else:
                    field_selected =(mouse_y_pos,mouse_x_pos)
                    #print(game_status.board[1][1])
                    #a=field_selected[0]
                    #k=field_selected[1]
                    #print(game_status.board[field_selected[0]][field_selected[1]])
                    if(len(player_clicks)==0):
                        if (game_status.checkField(field_selected)==True):
                            player_clicks.append(field_selected)
                        else:
                            field_selected = ()
                            player_clicks = []
                    elif(len(player_clicks)==1):
                        player_clicks.append(field_selected)

                if(len(player_clicks)==2):
                    #print(field_selected[1])
                    mover=ChessEngine.MoveHandler(player_clicks[0],player_clicks[1],game_status.board)
                    #print(mover.getChessNotation())
                    game_status.movePiece(mover)
                    field_selected=()
                    player_clicks=[]
            elif e.type==p.KEYDOWN:
                if e.key == p.K_r:
                    game_status.revertMove()

        drawGameState(screen,game_status)
        clock.tick(Max_FPS)
        p.display.flip()
"""
Draw the GUI for the chess board
"""
def drawGameState(screen, game_status):
    drawBoard(screen)
    drawPieces(screen,game_status.board)

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
