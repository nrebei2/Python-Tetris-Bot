import random
import copy
import time
import numpy as np

class Tetromino():
    def __init__(self, state):
        self.state = state

    def __str__(self):
        return "\n".join(["".join(x) for x in self.state])

    @staticmethod
    def ITetromino():
        return Tetromino(
            [
                ['I', 'I', 'I', 'I']
            ]
        )

    @staticmethod
    def OTetromino():
        return Tetromino(
            [
                ['O', 'O'],
                ['O', 'O']
            ]
        )

    @staticmethod
    def TTetromino():
        return Tetromino(
            [
                [' ', 'T', ' '],
                ['T', 'T', 'T']
            ]
        )

    @staticmethod
    def STetromino():
        return Tetromino(
            [
                [' ', 'S', 'S'],
                ['S', 'S', ' ']
            ]
        )

    @staticmethod
    def ZTetromino():
        return Tetromino(
            [
                ['Z', 'Z', ' '],
                [' ', 'Z', 'Z']
            ]
        )

    @staticmethod
    def JTetromino():
        return Tetromino(
            [
                ['J', ' ', ' '],
                ['J', 'J', 'J']
            ]
        )

    @staticmethod
    def LTetromino():
        return Tetromino(
            [
                [' ', ' ', 'L'],
                ['L', 'L', 'L']
            ]
        )
        
    def rotate_right(self):
        self.state = list(zip(*self.state[::-1]))
        return self

    def rotate_left(self):
        self.state = list(reversed(list(zip(*self.state))))
        return self

    def flip(self):
        self.state = [row[::-1] for row in self.state[::-1]]
        return self
    
class Board():
    def __init__(self, board=None):
        self.WIDTH = 10
        self.HEIGHT = 20
        if board:
            self.board = board
        else:
            self.board = [ [' ']*self.WIDTH for i in range(self.HEIGHT)]


    def copy(self):
        return Board([row[:] for row in self.board])

    def printBoard(self):
        board = "    0 1 2 3 4 5 6 7 8 9 \n"
        for i in range(self.HEIGHT):
            board += " " * (len(str(self.HEIGHT)) - len(str(i+1))) + str(i+1) + " |"
            for j in range(self.WIDTH):
                if self.board[i][j] == ' ':
                    board += (" " if j == self.WIDTH - 1 else "  ")
                else:
                    board += (self.board[i][j] if j == self.WIDTH - 1 else self.board[i][j] + " ")
            board += "| \n"
        board += "    0 1 2 3 4 5 6 7 8 9 "
        print(board)

    def checkRow(self, piece, row, column):
        for j in reversed(range(len(piece.state))):
            for k in range(len(piece.state[j])):
                if self.board[row-(len(piece.state)-j-1)][k+column] != " " and piece.state[j][k] != " ":
                    return "bad"                  
        return "good"

    def placePiece(self, piece, row, column):
         for j in reversed(range(len(piece.state))):
            for k in range(len(piece.state[j])):
                if piece.state[j][k] != " ":
                    self.board[row-(len(piece.state)-j-1)][k+column] = piece.state[j][k]

    def clearLines(self):
        rlines = []
        for i in range(len(self.board)):
            if ' ' not in self.board[i]:
                rlines.append(i)
        y = []

        for i in range(len(rlines)):
            y.append([' ']*10)

        for v in range(len(self.board)):
            if v not in rlines:
                y.append(self.board[v])
        
        self.board = y
        return

    def drop(self, piece, column):
        #self.board[row][column]
        try:
            for row in reversed(range(self.HEIGHT)):
                if self.checkRow(piece, row, column) == "good":
                    self.placePiece(piece, row, column)
                    self.clearLines()
                    return row
        except:
            return "Invalid column"
        return
    
    def attributes(self):
        heights = []
        for i in range(self.WIDTH):
            colH = 0
            for j in reversed(range(self.HEIGHT)):
                if self.board[j][i] != " ":
                    colH = self.HEIGHT-j
            heights.append(colH)

        gaps = 0
        for i in range(self.WIDTH):
            for j in reversed(range(self.HEIGHT - heights[i], self.HEIGHT)):
                if self.board[j][i] == " ":
                    gaps += 1

        return {"height diff": max(heights) - min(heights), "gaps": gaps, "mean": np.mean(heights), "std": np.std(heights), "consec": np.ediff1d(heights).max()}


