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

    def movePiece(self, mover):
        if (self.board[mover.origin_row][mover.origin_column] != '--'):
            self.board[mover.origin_row][mover.origin_column] = '--'
            self.board[mover.goal_field_row][mover.goal_field_column] = mover.active_piece
            self.move_log.append(mover)
            self.white_token = not self.white_token
            self.black_token = not self.black_token
            # Update king, later with objects shifted
            if mover.active_piece == 'wK':
                self.white_king_position = (mover.goal_field_row, mover.goal_field_column)
            elif mover.active_piece == 'bK':
                self.black_king_position = (mover.goal_field_row, mover.goal_field_column)

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
                if None in moves:
                    print('CIHH')
                print('moves', moves)
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
                    print(i,len(moves))
                    print("HIER",moves[i])
                    #print(moves[i].__getattribute__(active_piece)
                    print(moves)
                    #print(moves[68])
                    print(len(moves))
                    print(moves[len(moves) - 1])
                    try:
                        print(moves[len(moves)-1].active_piece)
                    except:
                        print("JUHIGFUTFTFFZF",moves)
                        print(moves==moves[len(moves)-1])
                    print(moves[i].active_piece)
                    print(moves[i].goal_field_row)
                    print(moves[i].active_piece)
                    if moves[i].active_piece[1] != 'K':
                        if not (moves[i].goal_field_row, moves[i].goal_field_column) in valid_fields:
                            moves.remove(moves[i])
            else:
                self.calculateKing(king_row, king_column, moves)
        else:
            #print('FREI')
            moves = self.calculateEveryMove()
            #print('No-Check',moves)
        #print('out-off',moves)
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
                    if collide_piece[0] == allied_color:
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
                                (i == i and piece_type == 'P'
                                 and ((enermy_color == 'w' and 6 <= j <= 7) or
                                      (enermy_color == 'b' and 4 <= j <= 5))) or (piece_type == 'Q') or (
                                i == 1 and piece_type == 'K'):
                            if possible_pin == ():
                                in_check = True
                                print('Schachgeben',piece_type)
                                #print(self.board)
                                #print('Feind',self.board[goal_field_row+d[0]][goal_field_column+d[1]],goal_field_row,goal_field_column,d[0],d[1],goal_field_row+d[0],goal_field_column+d[1])
                                checks.append((goal_field_row, goal_field_column, d[0], d[1]))
                                break
                            else:
                                print('HU')
                                pins.append(possible_pin)
                                break
                        else:
                            break
                #else:
                 #   break
        knight_movement = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knight_movement:
            goal_field_row = origin_row + m[0]
            goal_field_column = origin_row + m[1]
            if 0 <= goal_field_row <= 7 and 0 <= goal_field_column <= 7:
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
                piece_color = self.board[row][column][0]
                #print(piece_color)
                #print(self.black_token)
                if (piece_color == 'w' and self.white_token == True) or (
                        piece_color == 'b' and self.black_token == True):
                    piece_type = self.board[row][column][1]
                    moves = self.piece_map_function[piece_type](row, column, moves)
                    #self.piece_map_function[piece_type](row, column, moves)
                    # print(moves)
                    # if len(moves)!=0:
                    #   pass
                    # print(moves[1].move_ID)
                    # print(moves[1].origin_row,moves[1].origin_column,moves[1].goal_field_row,moves[1].goal_field_column)
                    # moves.append(self.calculatePawn(row,column,moves))
        for i in range(1,len(moves)-1):
            #print("Zug",i,moves[i])
            try:
                print('Typ', moves[i].active_piece)
            #pass
            except:
                print("ZGZGZGG")
                print(moves[i])
                #print('WArning',i)

        return moves

    def calculatePawn(self, row, column, moves):
        # print(self.white_token)
        if self.white_token == True:
            test_pawn = Pieces.Pawn.Pawn(row, column, 'white', self.board)
            # print(moves)
            moves.append(test_pawn.movement(moves))
            # print(moves)
            # print("TR")
            # print(test_pawn.board)
            del test_pawn
        if self.black_token == True:
            test_pawn = Pieces.Pawn.Pawn(row, column, 'black', self.board)
            # print(moves)
            moves.append(test_pawn.movement(moves))
            # print(moves)
            # print("TR")
            # print(test_pawn.board)
            del test_pawn
        if None in moves:
            print('Bauer')
        return moves

    def calculateKnight(self, row, column, moves):
        if self.white_token == True:
            test_knight = Pieces.Knight.Knight(row, column, 'white', self.board)
            moves.append(test_knight.movement(moves))
            del test_knight
        if self.black_token == True:
            test_knight = Pieces.Knight.Knight(row, column, 'black', self.board)
            moves.append(test_knight.movement(moves))
            del test_knight
        if None in moves:
            print('Knight')
        return moves

    def calculateRook(self, row, column, moves):
        if self.white_token == True:
            test_rook = Pieces.Rook.Rook(row, column, 'white', self.board)
            moves.append(test_rook.movement(moves))
            del test_rook
        if self.black_token == True:
            test_rook = Pieces.Rook.Rook(row, column, 'black', self.board)
            moves.append(test_rook.movement(moves))
            del test_rook
        if None in moves:
            print('Turm')
        return moves

    def calculateBishop(self, row, column, moves):
        if self.white_token == True:
            test_bishop = Pieces.Bishop.Bishop(row, column, 'white', self.board)
            moves.append(test_bishop.movement(moves))
            del test_bishop
        if self.black_token == True:
            test_bishop = Pieces.Bishop.Bishop(row, column, 'black', self.board)
            moves.append(test_bishop.movement(moves))
            del test_bishop
        if None in moves:
            print('Bishop')
        return moves

    def calculateQueen(self, row, column, moves):
        if self.white_token == True:
            test_queen = Pieces.Queen.Queen(row, column, 'white', self.board)
            moves.append(test_queen.movement(moves))
            del test_queen
        if self.black_token == True:
            test_queen = Pieces.Queen.Queen(row, column, 'black', self.board)
            moves.append(test_queen.movement(moves))
            del test_queen
        if None in moves:
            print('Queen')
        return moves

    def calculateKing(self, row, column, moves):
        if self.white_token == True:
            test_king = Pieces.King.King(row, column, 'white', self.board)
            moves.append(test_king.movement(moves))
            del test_king
        if self.black_token == True:
            test_king = Pieces.King.King(row, column, 'black', self.board)
            moves.append(test_king.movement(moves))
            del test_king
        if None in moves:
            print('King')
        return moves


class MoveHandler():
    chess_row_to_base_notation_row = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
    base_notation_row_to_chess_row = {v: k for k, v in chess_row_to_base_notation_row.items()}
    chess_column_to_base_notation_column = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, }
    base_notation_column_to_chess_column = {v: k for k, v in chess_column_to_base_notation_column.items()}

    def __init__(self, origin_field, goal_field, board):
        self.origin_row = origin_field[0]
        self.origin_column = origin_field[1]
        self.goal_field_row = goal_field[0]
        self.goal_field_column = goal_field[1]
        self.active_piece = board[self.origin_row][self.origin_column]
        self.captured_piece = board[self.goal_field_row][self.goal_field_column]
        self.move_ID = self.origin_row * 1000 + self.origin_column * 100 + self.goal_field_row * 10 + self.goal_field_column

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
