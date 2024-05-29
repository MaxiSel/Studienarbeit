from Figure import ChessPiece
class Queen(ChessPiece):
    def __init__(self,row,column,color,board):
        super(Queen,self).__init__(row,column,color,board)
    def movement(self):
        pass