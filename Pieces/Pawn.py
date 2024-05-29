from Figure import ChessPiece
from Chess import ChessEngine
class Pawn(ChessPiece):
    def __init__(self,row,column,color,board):
        super(Pawn,self).__init__(row,column,color,board)
    def movement(self,moves):
        if self.color=='white':
            if self.board[self.row,self.column]=='--':
                moves.append(ChessEngine.MoveHandler((self.row,self.column),(self.row-1,self.column),self.board))
                if self.row == 6 and self.board[self.row-2][self.column]:
                    moves.append(ChessEngine.MoveHandler((self.row,self.column),(self.row-2,self.column),self.board))

        elif self.color=='black':
            pass
        else:
            raise ValueError('undefinied Chess piece color')