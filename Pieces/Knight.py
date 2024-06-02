from Chess import ChessEngine
from Figure import ChessPiece
class Knight(ChessPiece):
    def __init__(self,row,column,color,board):
        if color == 'white':
            self.enermy_color = 'b'
        elif color == 'black':
            self.enermy_color = 'w'
        super(Knight,self).__init__(row,column,color,board)
        self.piece_is_pinned=False
        self.pin_vector=()
    def movement(self,moves):
        directions = ((2, 1), (2, -1), (-2, 1), (-2, -1),(1, -2), (1, 2), (-1, 2), (-1, -2))
        for d in directions:
            goal_row = self.row + d[0]
            goal_column = self.column + d[1]
            if 0 <= goal_row < 8 and 0 <= goal_column < 8:
                collide_piece = self.board[goal_row][goal_column]
                if collide_piece == '--':
                    moves.append(ChessEngine.MoveHandler((self.row, self.column),
                                                         (goal_row, goal_column), self.board))
                elif collide_piece[0] == self.enermy_color:
                    moves.append(ChessEngine.MoveHandler((self.row, self.column),
                                                         (goal_row, goal_column), self.board))
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