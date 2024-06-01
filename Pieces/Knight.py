from Chess import ChessEngine
from Figure import ChessPiece
class Knight(ChessPiece):
    def __init__(self,row,column,color,board):
        if color == 'white':
            self.enermy_color = 'b'
        elif color == 'black':
            self.enermy_color = 'w'
        super(Knight,self).__init__(row,column,color,board)
    def movement(self,moves):
        if(self.row-2>=0) and (self.column-1>=0):
            if(self.board[self.row-2][self.column-1]=='--') or (self.board[self.row-2][self.column-1][0]==self.enermy_color):
                moves.append(ChessEngine.MoveHandler((self.row, self.column), (self.row-2, self.column-1), self.board))
        if(self.row-2>=0) and (self.column+1<=7):
            if(self.board[self.row-2][self.column+1]=='--') or (self.board[self.row-2][self.column+1][0]==self.enermy_color):
                moves.append(ChessEngine.MoveHandler((self.row, self.column), (self.row-2, self.column+1), self.board))
        if(self.row+2<=7) and (self.column-1>=0):
            if(self.board[self.row+2][self.column-1]=='--') or (self.board[self.row+2][self.column-1][0]==self.enermy_color):
                moves.append(ChessEngine.MoveHandler((self.row, self.column), (self.row+2, self.column-1), self.board))

        if(self.row+2<=7) and (self.column+1<=7):
            if(self.board[self.row+2][self.column+1]=='--') or (self.board[self.row+2][self.column+1][0]==self.enermy_color):
                moves.append(ChessEngine.MoveHandler((self.row, self.column), (self.row+2, self.column+1), self.board))

        if(self.row-1>=0) and (self.column-2>=0):
            if(self.board[self.row-1][self.column-2]=='--') or (self.board[self.row-1][self.column-2][0]==self.enermy_color):
                moves.append(ChessEngine.MoveHandler((self.row, self.column), (self.row-1, self.column-2), self.board))

        if(self.row+1<=7) and (self.column-2>=0):
            if(self.board[self.row+1][self.column-2]=='--') or (self.board[self.row+1][self.column-2][0]==self.enermy_color):
                moves.append(ChessEngine.MoveHandler((self.row, self.column), (self.row+1, self.column-2), self.board))
        if(self.row-1>=0) and (self.column+2<=7):
            if(self.board[self.row-1][self.column+2]=='--') or (self.board[self.row-1][self.column+2][0]==self.enermy_color):
                moves.append(ChessEngine.MoveHandler((self.row, self.column), (self.row-1, self.column+2), self.board))

        if(self.row+1<=7) and (self.column+2<=7):
            if(self.board[self.row+1][self.column+2]=='--') or (self.board[self.row+1][self.column+2][0]==self.enermy_color):
                moves.append(ChessEngine.MoveHandler((self.row, self.column), (self.row+1, self.column+2), self.board))
        """if None in moves:
            print('Pferd')
        if len(moves)!=0:
            print(" Falscher Ritter")
            for i in range(0, len(moves)):
                print(moves[i])
                try:
                    print(moves[i].origin_row, moves[i].origin_column, moves[i].goal_field_row,
                          moves[i].goal_field_column)
                except:
                    print("WARNING")"""
        return moves