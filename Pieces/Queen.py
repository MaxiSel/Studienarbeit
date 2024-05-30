from Chess import ChessEngine
from Figure import ChessPiece
class Queen(ChessPiece):
    def __init__(self,row,column,color,board):
        if color == 'white':
            self.enermy_color = 'b'
        elif color == 'black':
            self.enermy_color = 'w'
        super(Queen,self).__init__(row,column,color,board)
    def movement(self,moves):
        row_counter = self.row
        column_counter = self.column
        while (row_counter <= 6):
            row_counter += 1
            #print(row_counter, column_counter)
            if self.board[row_counter][column_counter] == '--':
                moves.append(
                    ChessEngine.MoveHandler((self.row, self.column), (row_counter, column_counter), self.board))
            elif self.board[row_counter][column_counter][0] == self.enermy_color:
                moves.append(
                    ChessEngine.MoveHandler((self.row, self.column), (row_counter, column_counter), self.board))
                break
        row_counter = self.row
        while (row_counter >= 1):
            row_counter -= 1
            if self.board[row_counter][column_counter] == '--':
                moves.append(
                    ChessEngine.MoveHandler((self.row, self.column), (row_counter, column_counter), self.board))
            elif self.board[row_counter][column_counter][0] == self.enermy_color:
                moves.append(
                    ChessEngine.MoveHandler((self.row, self.column), (row_counter, column_counter), self.board))
                break
        row_counter = self.row
        while (column_counter >= 1):
            column_counter -= 1
            if self.board[row_counter][column_counter] == '--':
                moves.append(
                    ChessEngine.MoveHandler((self.row, self.column), (row_counter, column_counter), self.board))
            elif self.board[row_counter][column_counter][0] == self.enermy_color:
                moves.append(
                    ChessEngine.MoveHandler((self.row, self.column), (row_counter, column_counter), self.board))
                break
        column_counter = self.column
        while column_counter <= 6:
            column_counter += 1
            if self.board[row_counter][column_counter] == '--':
                moves.append(
                    ChessEngine.MoveHandler((self.row, self.column), (row_counter, column_counter), self.board))
            elif self.board[row_counter][column_counter][0] == self.enermy_color:
                moves.append(
                    ChessEngine.MoveHandler((self.row, self.column), (row_counter, column_counter), self.board))
                break
        row_counter = self.row
        column_counter = self.column
        while (row_counter <= 6) and (column_counter <= 6):
            row_counter += 1
            column_counter += 1
            #print(row_counter, column_counter)
            if self.board[row_counter][column_counter] == '--':
                moves.append(
                    ChessEngine.MoveHandler((self.row, self.column), (row_counter, column_counter), self.board))
            elif self.board[row_counter][column_counter][0] == self.enermy_color:
                moves.append(
                    ChessEngine.MoveHandler((self.row, self.column), (row_counter, column_counter), self.board))
                break
        row_counter = self.row
        column_counter = self.column
        while (row_counter >= 1) and (column_counter >= 1):
            row_counter -= 1
            column_counter -= 1
            if self.board[row_counter][column_counter] == '--':
                moves.append(
                    ChessEngine.MoveHandler((self.row, self.column), (row_counter, column_counter), self.board))
            elif self.board[row_counter][column_counter][0] == self.enermy_color:
                moves.append(
                    ChessEngine.MoveHandler((self.row, self.column), (row_counter, column_counter), self.board))
                break
        row_counter = self.row
        column_counter = self.column
        while (row_counter <= 6) and (column_counter >= 1):
            row_counter += 1
            column_counter -= 1
            if self.board[row_counter][column_counter] == '--':
                moves.append(
                    ChessEngine.MoveHandler((self.row, self.column), (row_counter, column_counter), self.board))
            elif self.board[row_counter][column_counter][0] == self.enermy_color:
                moves.append(
                    ChessEngine.MoveHandler((self.row, self.column), (row_counter, column_counter), self.board))
                break
        row_counter = self.row
        column_counter = self.column
        while (row_counter >= 1) and (column_counter <= 6):
            row_counter -= 1
            column_counter += 1
            if self.board[row_counter][column_counter] == '--':
                moves.append(
                    ChessEngine.MoveHandler((self.row, self.column), (row_counter, column_counter), self.board))
            elif self.board[row_counter][column_counter][0] == self.enermy_color:
                moves.append(
                    ChessEngine.MoveHandler((self.row, self.column), (row_counter, column_counter), self.board))
                break

        return moves