from Figure import ChessPiece
class King(ChessPiece):
    def __init__(self,row,column,color,board):
        super(King,self).__init__(row,column,color,board)
    def movement(self,moves):
        pass