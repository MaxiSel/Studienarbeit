"""
Handles the status of the game and the processing for the initial
phase. Includes later a PGN (Portable Game Notation)
"""

class GameState():
    def __init__(self):
        self.whiteToken=True
        self.blackToken=False
        self.whiteRochadeToken=True
        self.BlackRochadeToken=True
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
        self.moveLog=[]

