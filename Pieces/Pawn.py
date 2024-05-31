from Figure import ChessPiece
from Chess import ChessEngine
class Pawn(ChessPiece):
    def __init__(self,row,column,color,board):
        if color == 'white':
            self.enermy_color = 'b'
        elif color == 'black':
            self.enermy_color = 'w'
        super(Pawn,self).__init__(row,column,color,board)
    def movement(self,moves):
        print("Anfang",moves)
        if self.color=='white':
            if self.board[self.row-1][self.column]=='--':
                #print(ChessEngine.MoveHandler((self.row,self.column),(self.row-1,self.column),self.board))
                moves.append(ChessEngine.MoveHandler((self.row,self.column),(self.row-1,self.column),self.board))
                #print('HIUGGUFG',moves)
                #print(moves)
                if self.row == 6 and self.board[self.row-2][self.column]:
                    moves.append(ChessEngine.MoveHandler((self.row,self.column),(self.row-2,self.column),self.board))
            if (self.column-1>=0) :
                if self.board[self.row-1][self.column-1][0]==self.enermy_color:
                    moves.append(ChessEngine.MoveHandler((self.row,self.column),(self.row-1,self.column-1),self.board))

            if (self.column+1<=7):
                if self.board[self.row-1][self.column+1][0]==self.enermy_color:
                    moves.append(
                        ChessEngine.MoveHandler((self.row , self.column), (self.row - 1, self.column + 1),self.board))
            if len(moves) != 0:
                print("Weißer Bauer")
                print(moves[len(moves) - 1])


        elif self.color=='black':
            if self.board[self.row + 1][self.column] == '--':
                # print(ChessEngine.MoveHandler((self.row,self.column),(self.row-1,self.column),self.board))
                moves.append(ChessEngine.MoveHandler((self.row, self.column), (self.row + 1, self.column), self.board))
                #print(moves)
            if self.row == 1 and self.board[self.row + 2][self.column]:
                moves.append(ChessEngine.MoveHandler((self.row, self.column), (self.row + 2, self.column), self.board))
            if (self.column-1>=0) :
                if self.board[self.row+1][self.column-1][0]==self.enermy_color:
                    moves.append(ChessEngine.MoveHandler((self.row,self.column),(self.row+1,self.column-1),self.board))

            if (self.column+1<=7):
                if self.board[self.row+1][self.column+1][0]==self.enermy_color:
                    moves.append(
                        ChessEngine.MoveHandler((self.row , self.column), (self.row + 1, self.column + 1),self.board))
            if len(moves) != 0:
                print("Schwarzer Bauer")
                print(moves[len(moves) - 1])
        #else:
            #raise ValueError('undefinied Chess piece color')
        if None in moves:
            print('Bauer')
        #print(("bauer"),moves[len(moves)-1])
        return moves