"""
Handles the status of the game and the processing for the initial
phase. Includes later a PGN (Portable Game Notation)
"""

class GameState():
    def __init__(self):
        self.white_token=True
        self.black_token=False
        self.white_rochade_token=True
        self.black_rochade_token=True
        self.board= [
            ['bR','bN','bB','bQ','bK','bB','bN','bR'],
            ['bP','bP','bP','bP','bP','bP','bP','bP'],
            ['--','--','--','--','--','--','--','--','--'],
            ['--', '--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR','wN','wB','wQ','wK','wB','wN','wR']
        ]
        self.move_log=[]
    def movePiece(self,mover):
        if (self.board[mover.origin_row][mover.origin_column]!='--'):
            self.board[mover.origin_row][mover.origin_column]='--'
            self.board[mover.goal_field_row][mover.goal_field_column] = mover.active_piece
            self.move_log.append(mover)
            self.white_token = not self.white_token
            self.black_token = not self.black_token

    def checkField(self,player_select_field):
        """
        Checks if mouse target field is empty
        """
        if self.board[player_select_field[0]][player_select_field[1]]=='--':
            return False
        return True


    def revertMove(self):
        if len(self.move_log)!=0:
            prev_move = self.move_log.pop()
            self.board[prev_move.origin_row][prev_move.origin_column] = prev_move.active_piece
            self.board[prev_move.goal_field_row][prev_move.goal_field_column] = prev_move.captured_piece
            self.white_token = not self.white_token
            self.black_token = not self.black_token

    def calculateMoves(self):
        pass

    def calculateEveryMove(self):
        """
        Includes every theoretical move, also moves which would end in a checkmate, these needs to be
        cut by the calling method
        :return:
        """
        moves =[]
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                piece_color=self.board[row][column][0]
                if(piece_color=='w' and self.white_token==True) and (piece_color=='b' and self.black_token==True):
                    piece_type = self.board[row][column][1]
                    if piece_type =='P':
                        pass
                    elif piece_type =='K':
                        pass
                    elif piece_type =='B':
                        pass
                    elif piece_type =='R':
                        pass
                    elif piece_type =='Q':
                        pass
                    elif piece_type =='K':
                        pass
        return moves

    def calculatePawn(self,row,column,moves):
        pass
    def calculateKnight(self,row,column,moves):
        pass
    def calculateRock(self,row,column,moves):
        pass
    def calculateBishop(self,row,column,moves):
        pass
    def calculateQueen(self,row,column,moves):
        pass
    def calculateKing(self,row,column,moves):
        pass


class MoveHandler():
    chess_row_to_base_notation_row ={'1':7,'2':6,'3':5,'4':4,'5':3,'6':2,'7':1,'8':0}
    base_notation_row_to_chess_row = {v:k for k,v in chess_row_to_base_notation_row.items()}
    chess_column_to_base_notation_column = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7,}
    base_notation_column_to_chess_column={v:k for k,v in chess_column_to_base_notation_column.items()}

    def __init__(self,origin_field,goal_field,board):
        self.origin_row=origin_field[0]
        self.origin_column=origin_field[1]
        self.goal_field_row=goal_field[0]
        self.goal_field_column = goal_field[1]
        self.active_piece=board[self.origin_row][self.origin_column]
        self.captured_piece=board[self.goal_field_row][self.goal_field_column]
        self.move_ID= self.origin_row*1000+self.origin_column*100+self.goal_field_row*10+self.goal_field_column


        """
        Overide ==
        """
        def __eq__(self,other):
            if isinstance(other,MoveHandler):
                return self.move_ID == other.move_ID
            return False


    def getChessNotation(self):
        # only video implemnt. Real PGN needs to be reviewed and added
        return self.getRowColumn(self.origin_row,self.origin_column) + self.getRowColumn(self.goal_field_row,self.goal_field_column)


    def getRowColumn(self,row,column):
        return self.base_notation_column_to_chess_column[column] +self.base_notation_row_to_chess_row[row]


