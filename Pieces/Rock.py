from Figure import ChessPiece
class Rock(ChessPiece):
    def __init__(self,row,column,color,board):
        super(Rock,self).__init__(row,column,color,board)
    def movement(self):
        pass