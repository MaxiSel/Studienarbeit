from Figure import ChessPiece
from Chess import ChessEngine
class Pawn(ChessPiece):
    def __init__(self,row,column,color,board):
        super(Pawn,self).__init__(row,column,color,board)
    def movement(self,moves):
        if self.color=='white':
            print("ra")
            if self.board[self.row-1][self.column]=='--':
                #print(ChessEngine.MoveHandler((self.row,self.column),(self.row-1,self.column),self.board))
                moves.append(ChessEngine.MoveHandler((self.row,self.column),(self.row-1,self.column),self.board))
                print(moves)
                if self.row == 6 and self.board[self.row-2][self.column]:
                    moves.append(ChessEngine.MoveHandler((self.row,self.column),(self.row-2,self.column),self.board))
            return moves
        elif self.color=='black':
            if self.board[self.row + 1][self.column] == '--':
                # print(ChessEngine.MoveHandler((self.row,self.column),(self.row-1,self.column),self.board))
                moves.append(ChessEngine.MoveHandler((self.row, self.column), (self.row + 1, self.column), self.board))
                print(moves)
                if self.row == 1 and self.board[self.row + 2][self.column]:
                    moves.append(
                        ChessEngine.MoveHandler((self.row, self.column), (self.row + 2, self.column), self.board))
        else:
            raise ValueError('undefinied Chess piece color')