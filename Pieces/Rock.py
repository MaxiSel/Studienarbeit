from Figure import ChessPiece
class Rock(ChessPiece):
    def __init__(self,row,column,color):
        super(Rock,self).__init__(row,column,color)
    def movement(self):
        pass