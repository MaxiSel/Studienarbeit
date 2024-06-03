from Figure import ChessPiece
from Chess import ChessEngine
class Pawn(ChessPiece):
    def __init__(self,row,column,color,board,enpassant_possible_field):
        if color == 'white':
            self.enermy_color = 'b'
        elif color == 'black':
            self.enermy_color = 'w'
        super(Pawn,self).__init__(row,column,color,board)
        self.piece_is_pinned=False
        self.pin_vector=()
        self.enpassant_possible_field=enpassant_possible_field
    def movement(self,moves):
        #print("Anfang",moves)
        if self.color=='white':
            #print("ENPAS",self.enpassant_possible_field)
            if self.board[self.row-1][self.column]=='--':

                if not self.piece_is_pinned or self.pin_vector==(-1,0):
                    #print(ChessEngine.MoveHandler((self.row,self.column),(self.row-1,self.column),self.board))
                    moves.append(ChessEngine.MoveHandler((self.row,self.column),(self.row-1,self.column),self.board))

                    if (self.row == 6) and (self.board[self.row-2][self.column]=='--'):
                        moves.append(ChessEngine.MoveHandler((self.row,self.column),(self.row-2,self.column),self.board))
            if (self.column-1>=0) :
                if self.board[self.row-1][self.column-1][0]==self.enermy_color:
                    if not self.piece_is_pinned or self.pin_vector == (-1, -1):
                        moves.append(ChessEngine.MoveHandler((self.row,self.column),(self.row-1,self.column-1),self.board))
                elif (self.row-1,self.column-1)==self.enpassant_possible_field:
                    if not self.piece_is_pinned or self.pin_vector == (-1, -1):
                    #print('HIER')
                        moves.append(
                        ChessEngine.MoveHandler((self.row, self.column), (self.row - 1, self.column - 1), self.board,move_is_enpassant_move=True))



            if (self.column+1<=7):
                if self.board[self.row-1][self.column+1][0]==self.enermy_color:
                    if not self.piece_is_pinned or self.pin_vector == (-1, 1):
                        moves.append(
                        ChessEngine.MoveHandler((self.row , self.column), (self.row - 1, self.column + 1),self.board))
                elif (self.row - 1, self.column + 1) == self.enpassant_possible_field:
                    if not self.piece_is_pinned or self.pin_vector == (-1, 1):
                    #print('DORT')
                        moves.append(ChessEngine.MoveHandler((self.row, self.column), (self.row - 1, self.column + 1),self.board, move_is_enpassant_move=True))

            if len(moves) != 0:
                #print("Weißer Bauer")
                #print("Raus",moves)
                """
                test2 = [i for i in moves if i not in test]
                for i in range(0, len(test2) - 1):
                    print(test2)
                    try:
                        print(test2[i].origin_row, test2[i].origin_column, test2[i].goal_field_row,
                              test2[i].goal_field_column)
                    except:
                        print("WARNING")
                """




        elif self.color=='black':
            if self.board[self.row + 1][self.column] == '--':
                if not self.piece_is_pinned or self.pin_vector == (-1, 0):
                    # print(ChessEngine.MoveHandler((self.row,self.column),(self.row-1,self.column),self.board))
                    moves.append(ChessEngine.MoveHandler((self.row, self.column), (self.row + 1, self.column), self.board))
                #print(moves)
                    if (self.row == 1) and (self.board[self.row + 2][self.column]=='--'):
                        moves.append(ChessEngine.MoveHandler((self.row, self.column), (self.row + 2, self.column), self.board))
            if (self.column-1>=0) :
                if self.board[self.row+1][self.column-1][0]==self.enermy_color:
                    if not self.piece_is_pinned or self.pin_vector == (1, -1):
                        moves.append(ChessEngine.MoveHandler((self.row,self.column),(self.row+1,self.column-1),self.board))
                elif (self.row + 1, self.column - 1) == self.enpassant_possible_field:
                    if not self.piece_is_pinned or self.pin_vector == (1, -1):
                        moves.append(
                            ChessEngine.MoveHandler((self.row, self.column), (self.row + 1, self.column - 1),
                                                    self.board, move_is_enpassant_move=True))

            if (self.column+1<=7):
                if self.board[self.row+1][self.column+1][0]==self.enermy_color:
                    if not self.piece_is_pinned or self.pin_vector == (1, 1):
                        moves.append(
                        ChessEngine.MoveHandler((self.row , self.column), (self.row + 1, self.column + 1),self.board))
                elif (self.row - 1, self.column - 1) == self.enpassant_possible_field:
                    if not self.piece_is_pinned or self.pin_vector == (1, 1):
                        moves.append(
                            ChessEngine.MoveHandler((self.row, self.column), (self.row + 1, self.column + 1),
                                                    self.board, move_is_enpassant_move=True))
            """if len(moves) != 0:
                print("Schwarzer Bauer")
                for i in range(0,len(moves)-1):
                    print(moves[i])
                    try:
                        print(moves[i].origin_row,moves[i].origin_column,moves[i].goal_field_row,moves[i].goal_field_column)
                    except:
                        print("WARNING")"""

        #else:
            #raise ValueError('undefinied Chess piece color')
        """if None in moves:
            print('Bauer')
        #print(("bauer"),moves[len(moves)-1])
        if len(moves)!=0:
            print(len(moves))
            print("Letzer",moves)
            for i in range(len(moves)):
                print(i)
                print(moves[i])
                try:
                    print(moves[i].origin_row, moves[i].origin_column, moves[i].goal_field_row, moves[i].goal_field_column)
                except:
                    print("WARNING")"""
        """if len(moves) != 0:
            for i in range(len(moves)):
                print(moves[i].origin_row, moves[i].origin_column, moves[i].goal_field_row, moves[i].goal_field_column,
                      moves[i].move_is_enpassant_move)"""
        return moves