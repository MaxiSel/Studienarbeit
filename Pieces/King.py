from Chess import ChessEngine
from Figure import ChessPiece
class King(ChessPiece):
    def __init__(self,row,column,color,game_status):
        if color == 'white':
            self.enermy_color = 'b'
            self.allied_color='w'
        elif color == 'black':
            self.enermy_color = 'w'
            self.allied_color = 'b'
        super(King,self).__init__(row,column,color,game_status.board)
        self.in_check=False
        self.pins=[]
        self.checks=[]
        self.game_status_obj=game_status
    def movement(self,moves):
        directions = ((1, 1), (-1, 1), (1, -1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1))
        for d in directions:
            goal_row = self.row + d[0]
            goal_column = self.column + d[1]
            if 0 <= goal_row < 8 and 0 <= goal_column < 8:
                collide_piece = self.board[goal_row][goal_column]
                if (collide_piece == '--') or (collide_piece[0]==self.enermy_color):
                    if self.allied_color=='w':
                        self.game_status_obj.white_king_position=(goal_row,goal_column)
                    elif self.allied_color=='b':
                        self.game_status_obj.black_king_position = (goal_row, goal_column)
                    in_check,pins,checks=self.game_status_obj.checkForPinsAndChecks()
                    if not in_check:
                        moves.append(ChessEngine.MoveHandler((self.row, self.column),
                        (goal_row, goal_column), self.board))
                    if self.allied_color == 'w':
                        self.game_status_obj.white_king_position = (self.row, self.column)
                    elif self.allied_color == 'b':
                        self.game_status_obj.black_king_position = (self.row, self.column)
        """if len(moves)!=0:
            for i in range(0, len(moves)):
                print(moves[i])
                try:
                    print(moves[i].origin_row, moves[i].origin_column, moves[i].goal_field_row,
                          moves[i].goal_field_column)
                except:
                    print("WARNING")"""
        #self.game_status_obj.black_king_position = (7, 7)
        return moves
