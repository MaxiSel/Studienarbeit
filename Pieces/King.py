from Chess import ChessEngine
from Figure import ChessPiece
class King(ChessPiece):
    def __init__(self,row,column,color,board):
        if color == 'white':
            self.enermy_color = 'b'
        elif color == 'black':
            self.enermy_color = 'w'
        super(King,self).__init__(row,column,color,board)
    def movement(self,moves):
        if(self.row-1>=0)and(self.column-1>=0):
            if (self.board[self.row -1][self.column - 1] == '--') or (
                    self.board[self.row -1][self.column - 1][0] == self.enermy_color):
                moves.append(ChessEngine.MoveHandler((self.row, self.column), (self.row - 1, self.column - 1), self.board))

        if (self.row - 1 >= 0):
            if (self.board[self.row - 1][self.column] == '--') or (
                    self.board[self.row - 1][self.column][0] == self.enermy_color):
                moves.append(
                    ChessEngine.MoveHandler((self.row, self.column), (self.row - 1, self.column), self.board))
        if (self.row - 1 >= 0) and (self.column + 1 <= 7):
            if (self.board[self.row - 1][self.column + 1] == '--') or (
                    self.board[self.row - 1][self.column + 1][0] == self.enermy_color):
                moves.append(
                    ChessEngine.MoveHandler((self.row, self.column), (self.row - 1, self.column + 1), self.board))

        if  self.column + 1 <= 7:
            if (self.board[self.row][self.column + 1] == '--') or (
                    self.board[self.row][self.column + 1][0] == self.enermy_color):
                moves.append(ChessEngine.MoveHandler((self.row, self.column), (self.row, self.column + 1), self.board))

        if (self.row + 1 <= 7) and (self.column + 1 <= 7):
            if (self.board[self.row + 1][self.column + 1] == '--') or (
                    self.board[self.row + 1][self.column + 1][0] == self.enermy_color):
                moves.append(
                    ChessEngine.MoveHandler((self.row, self.column), (self.row + 1, self.column + 1), self.board))

        if (self.row + 1 <= 7):
            if (self.board[self.row + 1][self.column] == '--') or (
                    self.board[self.row + 1][self.column][0] == self.enermy_color):
                moves.append(
                    ChessEngine.MoveHandler((self.row, self.column), (self.row + 1, self.column), self.board))
        if (self.row + 1 <= 7) and (self.column - 1 >= 0):
            if (self.board[self.row + 1][self.column - 1] == '--') or (
                    self.board[self.row + 1][self.column - 1][0] == self.enermy_color):
                moves.append(
                    ChessEngine.MoveHandler((self.row, self.column), (self.row + 1, self.column - 1), self.board))

        if self.column - 1 >= 0:
            if (self.board[self.row][self.column - 1] == '--') or (
                    self.board[self.row][self.column - 1][0] == self.enermy_color):
                moves.append(
                    ChessEngine.MoveHandler((self.row, self.column), (self.row, self.column - 1), self.board))
        if None in moves:
            print('König')
        return moves
