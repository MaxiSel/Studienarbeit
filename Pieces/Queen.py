from Chess import ChessEngine
from Figure import ChessPiece
class Queen(ChessPiece):
    def __init__(self,row,column,color,board):
        if color == 'white':
            self.enermy_color = 'b'
        elif color == 'black':
            self.enermy_color = 'w'
        super(Queen,self).__init__(row,column,color,board)
        self.piece_is_pinned=False
        self.pin_vector=()
    def movement(self,moves):
        directions = ((1, 1), (-1, 1), (1, -1), (-1, -1),(1, 0), (-1, 0), (0, 1), (0, -1))
        # print("basis",self.row,self.column)
        for d in directions:
            for i in range(1, 8):
                goal_row = self.row + d[0] * i
                goal_column = self.column + d[1] * i
                if 0 <= goal_row < 8 and 0 <= goal_column < 8:
                    if not self.piece_is_pinned or self.pin_vector == d or self.pin_vector == (-d[0], -d[1]):
                        collide_piece = self.board[goal_row][goal_column]
                        # print(goal_row,goal_column,collide_piece)
                        if collide_piece == '--':
                            moves.append(ChessEngine.MoveHandler((self.row, self.column),
                                                                 (goal_row, goal_column), self.board))
                        elif collide_piece[0] == self.enermy_color:
                            moves.append(ChessEngine.MoveHandler((self.row, self.column),
                                                                 (goal_row, goal_column), self.board))
                            break
                        else:
                            break
                else:
                    break
        if None in moves:
            print('Queen')
        """if len(moves) != 0:
            print(" Falsche Königin")
            for i in range(0, len(moves)):
                print(moves[i])
                try:
                    print(moves[i].origin_row, moves[i].origin_column, moves[i].goal_field_row,
                          moves[i].goal_field_column)
                except:
                    print("WARNING")"""
        return moves