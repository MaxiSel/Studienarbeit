from Figure import ChessPiece
class Pawn(ChessPiece):
    def __init__(self,row,column,color):
        super(Pawn,self).__init__(row,column,color)
    def movement(self):
        pass