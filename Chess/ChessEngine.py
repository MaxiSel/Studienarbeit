"""
Handles the status of the game and the processing for the initial
phase. Includes later a PGN (Portable Game Notation)
"""
import sys

sys.path.append('../Pieces')
import Pieces


class GameState():
    def __init__(self):
        self.white_token = True
        self.black_token = False
        self.white_rochade_token = True
        self.black_rochade_token = True
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]
        self.piece_map_function = {'P': self.calculatePawn, 'R': self.calculateRook, 'K': self.calculateKing
            , 'Q': self.calculateQueen, 'N': self.calculateKnight, 'B': self.calculateBishop}
        self.move_log = []
        self.white_king_position = (7, 4)
        self.black_king_position = (0, 4)
        self.check_mate = False
        self.Patt = False
        self.in_check = False
        self.pins = []
        self.checks = []
        self.enpassant_move_possible_field = ()
        self.current_castle_rights=CastleRights(True,True,True,True)
        self.castle_rights_log=[CastleRights(self.current_castle_rights.w_short,
                                             self.current_castle_rights.w_long,
                                             self.current_castle_rights.b_short,
                                             self.current_castle_rights.b_long)]

    def inCheck(self):
        if self.white_token:
            return self.squareUnderAttack(self.white_king_position[0],self.white_king_position[1])
        elif self.black_token:
            return self.squareUnderAttack(self.black_king_position[0],self.black_king_position[1])

    def squareUnderAttack(self,row,column):
        self.white_token = not self.white_token
        self.black_token = not self.black_token
        enermy_moves=self.calculateMoves()
        self.white_token = not self.white_token
        self.black_token = not self.black_token
        for move in enermy_moves:
            if move.goal_field_row ==row and move.goal_field_column==column:
                return True
        return False



    def movePiece(self, mover):
        #print('POS WEIS',self.white_king_position)
        #print('POS Schwarz', self.black_king_position)
        if (self.board[mover.origin_row][mover.origin_column] != '--'):
            self.board[mover.origin_row][mover.origin_column] = '--'
            self.board[mover.goal_field_row][mover.goal_field_column] = mover.active_piece
            self.move_log.append(mover)
            if mover.move_is_enpassant_move:
                print("HGGG/(",mover.captured_piece)
            self.white_token = not self.white_token
            self.black_token = not self.black_token
            # Update king, later with objects shifted
            if mover.active_piece == 'wK':
                #print('WEIß KÖNIG')
                self.white_king_position = (mover.goal_field_row, mover.goal_field_column)
            elif mover.active_piece == 'bK':
                #print('SCHWARZ KÖNIG')
                self.black_king_position = (mover.goal_field_row, mover.goal_field_column)

            if mover.pawn_promote_move:
                promoted_piece=input("Q=Queen       N=Springer,     B=Läufer,   R=Turm")
                try:
                    self.board[mover.goal_field_row][mover.goal_field_column]=mover.active_piece[0]+promoted_piece
                except:
                    self.board[mover.goal_field_row][mover.goal_field_column] = mover.active_piece[0] + 'Q'
            print(mover.move_is_enpassant_move,mover.origin_row,mover.origin_column,mover.goal_field_row,mover.goal_field_column)
            if mover.move_is_enpassant_move==True:
                self.board[mover.origin_row][mover.goal_field_column]='--'
            if mover.active_piece[1]=='P' and abs(mover.origin_row- mover.goal_field_row)==2:
                self.enpassant_move_possible_field=((mover.origin_row+mover.goal_field_row)//2,mover.goal_field_column)
                print('ENGINE',self.enpassant_move_possible_field)
            else:
                self.enpassant_move_possible_field=()

            if mover.is_castle_move:
                if mover.goal_field_column-mover.origin_column==2:
                    self.board[mover.goal_field_row][mover.goal_field_column-1]=self.board[mover.goal_field_row][mover.goal_field_column+1]
                    self.board[mover.goal_field_row][mover.goal_field_column+1]='--'
                else:
                    self.board[mover.goal_field_row][mover.goal_field_column+1]=self.board[mover.goal_field_row][mover.goal_field_column-2]
                    self.board[mover.goal_field_row][mover.goal_field_column-2]='--'


            self.updateCastleRights(mover)
            self.castle_rights_log.append(CastleRights(self.current_castle_rights.w_short,
                                                   self.current_castle_rights.w_long,
                                                   self.current_castle_rights.b_short,
                                                   self.current_castle_rights.b_long))


    def getCastleMoves(self,row,column,moves,allied_color):
        if self.in_check:
            return
        if (self.white_token and self.current_castle_rights.w_short)\
                or (self.black_token and self.current_castle_rights.b_short):
            self.getKingsideCastleMoves(row,column,moves,allied_color)
        if (self.white_token and self.current_castle_rights.w_long)\
                or (self.black_token and self.current_castle_rights.b_long):
            self.getQueensideCastleMoves(row,column,moves,allied_color)
    def getKingsideCastleMoves(self,row,column,moves,allied_color):
        if self.board[row][column+1]=='--' and self.board[row][column+2]=='--':
            if not self.squareUnderAttack(row,column+1) and not self.squareUnderAttack(row,column+2):
                moves.append(MoveHandler((row,column),
                        (row, column+2), self.board,is_castle_move=True))


    def getQueensideCastleMoves(self,row,column,moves,allied_color):
        if self.board[row][column - 1] == '--' and self.board[row][column - 2] and self.board[row][column - 3] == '--':
            if not self.squareUnderAttack(row,column - 1) and not self.squareUnderAttack(row, column - 2):
                moves.append(MoveHandler((row, column),
                                                     (row, column - 2), self.board, is_castle_move=True))




    def updateCastleRights(self,mover):
        if mover.active_piece=='wK':
            self.current_castle_rights.w_short=False
            self.current_castle_rights.w_long=False
        elif mover.active_piece=='bK':
            self.current_castle_rights.b_short=False
            self.current_castle_rights.b_long=False
        elif mover.active_piece=='wR':
            if mover.origin_row==7:
                if mover.origin_column==0:
                    self.current_castle_rights.w_long=False
                elif mover.origin_column==7:
                    self.current_castle_rights.w_short=False
        elif mover.active_piece=='bR':
            if mover.origin_row==0:
                if mover.origin_column==0:
                    self.current_castle_rights.b_long=False
                elif mover.origin_column==7:
                    self.current_castle_rights.b_short=False


    def checkField(self, player_select_field):
        """
        Checks if mouse target field is empty
        """
        if self.board[player_select_field[0]][player_select_field[1]] == '--':
            return False
        return True

    def revertMove(self):
        if len(self.move_log) != 0:
            prev_move = self.move_log.pop()
            # print(self.black_token, self.white_token)
            self.board[prev_move.origin_row][prev_move.origin_column] = prev_move.active_piece
            self.board[prev_move.goal_field_row][prev_move.goal_field_column] = prev_move.captured_piece
            self.white_token = not self.white_token
            self.black_token = not self.black_token
            # print('black',self.black_token,'white',self.white_token)
            # Update king, later with objects shifted
            if prev_move.active_piece == 'wK':
                self.white_king_position = (prev_move.origin_row, prev_move.origin_column)
            elif prev_move.active_piece == 'bK':
                self.black_king_position = (prev_move.origin_row, prev_move.origin_column)
            if prev_move.move_is_enpassant_move:
                print("HIER",prev_move.captured_piece)
                self.board[prev_move.goal_field_row][prev_move.goal_field_column]='--'
                self.board[prev_move.origin_row][prev_move.goal_field_column]=prev_move.captured_piece
                self.enpassant_move_possible_field=(prev_move.goal_field_row,prev_move.goal_field_column)
            if prev_move.active_piece[1]=='P' and abs(prev_move.origin_row-prev_move.goal_field_row)==2:
                self.enpassant_move_possible_field=()
            self.castle_rights_log.pop()
            self.current_castle_rights=self.castle_rights_log[-1]

            if prev_move.is_castle_move:
                if prev_move.goal_field_column-prev_move.origin_column==2:
                    self.board[prev_move.goal_field_row][prev_move.goal_field_column + 1] = self.board[prev_move.goal_field_row][prev_move.goal_field_column - 1]
                    self.board[prev_move.goal_field_row][prev_move.goal_field_column - 1] = '--'
                else:
                    self.board[prev_move.goal_field_row][prev_move.goal_field_column - 2] = self.board[prev_move.goal_field_row][prev_move.goal_field_column + 1]
                    self.board[prev_move.goal_field_row][prev_move.goal_field_column + 1] = '--'




    def calculateMoves(self):
        moves = []
        self.in_check, self.pins, self.checks = self.checkForPinsAndChecks()
        print('in_checks', self.in_check, 'pins', self.pins, 'checks', self.checks)
        if self.white_token:
            king_row = self.white_king_position[0]
            king_column = self.white_king_position[1]
        elif self.black_token:
            king_row = self.black_king_position[0]
            king_column = self.black_king_position[1]
            #print("King",king_row,king_column)
        if self.in_check:
            print('Check')
            if len(self.checks) == 1:
                print('Check1')
                moves = self.calculateEveryMove()
                #print('moves', moves)
                check = self.checks[0]
                check_row = check[0]
                check_column = check[1]
                piece_check_giver = self.board[check_row][check_column]
                valid_fields = []
                if piece_check_giver[1] == 'N':
                    valid_fields = [(check_row, check_column)]
                else:
                    for i in range(1, 8):
                        valid_field = (king_row + check[2] * i, king_column + check[3] * i)
                        valid_fields.append(valid_field)
                        if valid_field[0] == check_row and valid_field[1] == check_column:
                            break
                for i in range(len(moves) - 1, -1, -1):
                    #print(i,len(moves))
                    #print("HIER",moves[i])
                    #print(moves[i].__getattribute__(active_piece)
                    #print(moves)
                    #print(moves[68])
                    #print(len(moves))
                    #print(moves[len(moves) - 1])
                    if moves[i].active_piece[1] != 'K':
                        if not (moves[i].goal_field_row, moves[i].goal_field_column) in valid_fields:
                            moves.remove(moves[i])
            else:
                moves=self.calculateKing(king_row, king_column, moves)
        else:
            #print('FREI')
            moves = self.calculateEveryMove()
            #print('No-Check',moves)
        #print('out-off',moves)
        print("ENDE")
        print(len(moves))
        #print(moves[1])
        #print(moves[5][1])
        #print(moves[3])
        """error_counter=0
        for i in range(len(moves)-1):
            print(moves[i])
            try:
                print(moves[i].active_piece)
            except:
                print("ERROR")
                error_counter+=1
        print("ERROR_Counter",error_counter)
"""
        return moves

    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        in_check = False

        #print('black_token', self.black_token)
        if self.white_token:
            enermy_color = 'b'
            allied_color = 'w'
            origin_row = self.white_king_position[0]
            origin_column = self.white_king_position[1]
        elif self.black_token:
            enermy_color = 'w'
            allied_color = 'b'
            origin_row = self.black_king_position[0]
            origin_column = self.black_king_position[1]

        #print('ORIGINS',origin_row,origin_column)

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possible_pin = ()
            for i in range(1, 8):
                goal_field_row = origin_row + d[0] * i
                goal_field_column = origin_column + d[1] * i

                if 0 <= goal_field_row < 8 and 0 <= goal_field_column < 8:
                    #print("Feld", goal_field_row, goal_field_column)
                    collide_piece = self.board[goal_field_row][goal_field_column]
                    if (collide_piece[0] == allied_color) and (collide_piece[1]!='K'):
                        #print('Allianz')
                        if possible_pin == ():
                            #print('Ally')
                            possible_pin = (goal_field_row, goal_field_column, d[0], d[1])
                        else:
                            break
                    elif collide_piece[0] == enermy_color:
                        #print('alli',allied_color)
                        #print('enermy')
                        #print(enermy_color)
                        piece_type = collide_piece[1]
                        if (0 <= j < 3 and piece_type == 'R') \
                                or (4 <= j <= 7 and piece_type == 'B') or \
                                (i == 1 and piece_type == 'P'
                                 and ((enermy_color == 'w' and 6 <= j <= 7) or
                                      (enermy_color == 'b' and 4 <= j <= 5))) or (piece_type == 'Q') or (
                                i == 1 and piece_type == 'K'):
                            if possible_pin == ():
                                in_check = True
                                print('Schachgeben',piece_type)
                                if enermy_color=='w':
                                    print('KÖNIG SCHWARZ',self.black_king_position)
                                else:
                                    print('KÖNIG WEI?',self.white_king_position)
                                #print(self.board)
                                #print('Feind',self.board[goal_field_row+d[0]][goal_field_column+d[1]],goal_field_row,goal_field_column,d[0],d[1],goal_field_row+d[0],goal_field_column+d[1])
                                checks.append((goal_field_row, goal_field_column, d[0], d[1]))
                                break
                            else:
                                pins.append(possible_pin)
                                break
                        else:
                            break
                else:
                    break
        knight_movement = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knight_movement:
            goal_field_row = origin_row + m[0]
            goal_field_column = origin_column + m[1]
            if 0 <= goal_field_row < 8 and 0 <= goal_field_column < 8:
                collide_piece = self.board[goal_field_row][goal_field_column]
                if collide_piece[0] == enermy_color and collide_piece[1] == 'N':
                    in_check = True
                    checks.append((goal_field_row, goal_field_column, m[0], m[1]))
        return in_check, pins, checks

    def calculateEveryMove(self):
        """
        Includes every theoretical move, also moves which would end in a checkmate, these needs to be
        cut by the calling method
        :return:
        """
        moves = []
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                try:
                    piece_color = self.board[row][column][0]
                except:
                    print('BOARD',row,column,self.board[row][column],self.board)
                #print(piece_color)
                #print(self.black_token)
                if (piece_color == 'w' and self.white_token == True) or (
                        piece_color == 'b' and self.black_token == True):
                    piece_type = self.board[row][column][1]
                    #print("EINS",moves)

                    moves = self.piece_map_function[piece_type](row, column, moves)
                    #print('ZWEI', moves)

                    #self.piece_map_function[piece_type](row, column, moves)
                    #print("Raus")
                    #print(len(moves),moves)
                    # if len(moves)!=0:
                    #   pass
                    # print(moves[1].move_ID)
                    # print(moves[1].origin_row,moves[1].origin_column,moves[1].goal_field_row,moves[1].goal_field_column)
                    # moves.append(self.calculatePawn(row,column,moves))
        """for i in range(1,len(moves)-1):
            #print("Zug",i,moves[i])
            try:
                print('Typ', moves[i].active_piece)
            #pass
            except:
                print("ZGZGZGG")
                print(moves[i])
                #print('WArning',i)
        """

        return moves

    def calculatePawn(self, row, column, moves):
        # print(self.white_token)
        piece_pinned=False
        pin_vector=()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0]==row and self.pins[i][1]==column:
                piece_pinned=True
                pin_vector=(self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.white_token == True:
            test_pawn = Pieces.Pawn.Pawn(row, column, 'white', self.board,self.enpassant_move_possible_field)
            test_pawn.piece_is_pinned=piece_pinned
            test_pawn.pin_vector=pin_vector
            # print(moves)
            moves=test_pawn.movement(moves)
            #print('Test',moves)
            # print("TR")
            # print(test_pawn.board)
            del test_pawn
        if self.black_token == True:
            test_pawn = Pieces.Pawn.Pawn(row, column, 'black', self.board,self.enpassant_move_possible_field)
            test_pawn.piece_is_pinned = piece_pinned
            test_pawn.pin_vector = pin_vector
            # print(moves)
            moves=test_pawn.movement(moves)
            # print(moves)
            # print("TR")
            # print(test_pawn.board)
            del test_pawn
        if None in moves:
            print('Bauer')
        return moves

    def calculateKnight(self, row, column, moves):
        piece_pinned=False
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0]==row and self.pins[i][1]==column:
                piece_pinned=True
                self.pins.remove(self.pins[i])
                break
        if self.white_token == True:
            test_knight = Pieces.Knight.Knight(row, column, 'white', self.board)
            test_knight.piece_is_pinned=piece_pinned
            moves=test_knight.movement(moves)
            del test_knight
        if self.black_token == True:
            test_knight = Pieces.Knight.Knight(row, column, 'black', self.board)
            test_knight.piece_is_pinned=piece_pinned
            moves=test_knight.movement(moves)
            del test_knight
        if None in moves:
            print('Knight')
        return moves

    def calculateRook(self, row, column, moves):
        piece_pinned=False
        pin_vector=()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0]==row and self.pins[i][1]==column:
                piece_pinned=True
                pin_vector=(self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        if self.white_token == True:
            test_rook = Pieces.Rook.Rook(row, column, 'white', self.board)
            test_rook.piece_is_pinned=piece_pinned
            test_rook.pin_vector=pin_vector
            moves=test_rook.movement(moves)
            del test_rook
        if self.black_token == True:
            test_rook = Pieces.Rook.Rook(row, column, 'black', self.board)
            test_rook.piece_is_pinned=piece_pinned
            test_rook.pin_vector=pin_vector
            moves=test_rook.movement(moves)
            del test_rook
        if None in moves:
            print('Turm')
        return moves

    def calculateBishop(self, row, column, moves):
        piece_pinned=False
        pin_vector=()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0]==row and self.pins[i][1]==column:
                piece_pinned=True
                pin_vector=(self.pins[i][2],self.pins[i][3])# sollte u.U. append sein, in Quellverwendungen aber so definiert
                self.pins.remove(self.pins[i])
                break
        if self.white_token == True:
            test_bishop = Pieces.Bishop.Bishop(row, column, 'white', self.board)
            test_bishop.piece_is_pinned=piece_pinned
            test_bishop.pin_vector=pin_vector
            moves=test_bishop.movement(moves)
            del test_bishop
        if self.black_token == True:
            test_bishop = Pieces.Bishop.Bishop(row, column, 'black', self.board)
            test_bishop.piece_is_pinned=piece_pinned
            test_bishop.pin_vector=pin_vector
            moves=test_bishop.movement(moves)
            del test_bishop
        if None in moves:
            print('Bishop')
        return moves

    def calculateQueen(self, row, column, moves):
        piece_pinned=False
        pin_vector=()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0]==row and self.pins[i][1]==column:
                piece_pinned=True
                pin_vector=(self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        if self.white_token == True:
            test_queen = Pieces.Queen.Queen(row, column, 'white', self.board)
            test_queen.piece_is_pinned=piece_pinned
            test_queen.pin_vector=pin_vector
            moves=test_queen.movement(moves)
            del test_queen
        if self.black_token == True:
            test_queen = Pieces.Queen.Queen(row, column, 'black', self.board)
            test_queen.piece_is_pinned=piece_pinned
            test_queen.pin_vector=pin_vector
            moves=test_queen.movement(moves)
            del test_queen
        if None in moves:
            print('Queen')
        return moves

    def calculateKing(self, row, column, moves):
        if self.white_token == True:
            #print(self.board)
            test_king = Pieces.King.King(row, column, 'white',self)
            moves=test_king.movement(moves)
            #print(moves)
            del test_king
            #print('Schwarzer König',self.black_king_position)
        if self.black_token == True:
            test_king = Pieces.King.King(row, column, 'black', self)
            moves=test_king.movement(moves)
            del test_king
        if None in moves:
            print('King')
        return moves


class MoveHandler():
    chess_row_to_base_notation_row = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
    base_notation_row_to_chess_row = {v: k for k, v in chess_row_to_base_notation_row.items()}
    chess_column_to_base_notation_column = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, }
    base_notation_column_to_chess_column = {v: k for k, v in chess_column_to_base_notation_column.items()}

    def __init__(self, origin_field, goal_field, board,move_is_enpassant_move=False,is_castle_move=False):
        self.origin_row = origin_field[0]
        self.origin_column = origin_field[1]
        self.goal_field_row = goal_field[0]
        self.goal_field_column = goal_field[1]
        self.active_piece = board[self.origin_row][self.origin_column]
        self.captured_piece = board[self.goal_field_row][self.goal_field_column]
        self.move_ID = self.origin_row * 1000 + self.origin_column * 100 + self.goal_field_row * 10 + self.goal_field_column
        self.pawn_promote_move=False
        if ((self.active_piece=='wP' and self.goal_field_row==0) or
                self.active_piece=='bP' and self.goal_field_row==7):
            self.pawn_promote_move=True
        self.promotion_choice=''#piece type to which to pawn should swap
        self.move_is_enpassant_move=move_is_enpassant_move
        if move_is_enpassant_move:
            self.captured_piece='wP' if self.active_piece=='bP' else 'bP'
            #print('DORT',self.captured_piece)
        self.is_castle_move = is_castle_move


    """
    Overide ==
    """
    def __eq__(self, other):
        if isinstance(other, MoveHandler):
            return self.move_ID == other.move_ID
        return False

    def getChessNotation(self):
        # only video implemnt. Real PGN needs to be reviewed and added
        return self.getRowColumn(self.origin_row, self.origin_column) + self.getRowColumn(self.goal_field_row,
                                                                                          self.goal_field_column)

    def getRowColumn(self, row, column):
        return self.base_notation_column_to_chess_column[column] + self.base_notation_row_to_chess_row[row]

class CastleRights():
    def __init__(self,w_short,w_long,b_short,b_long):
        self.w_short=w_short
        self.w_long=w_long
        self.b_short=b_short
        self.b_long=b_long

