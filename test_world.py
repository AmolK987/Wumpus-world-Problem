# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 18:55:55 2021

@author: 987am

This file builds a model board as a 2D list of Tile objects based off a
text file of a board.
"""

class Tile(object):
    '''
    This class is to create an individual Tile object to represent a single
    space on the input board.
    '''
    def __init__(self, x, y, val=0):
        self.value = val
        self.visited = False
        self.x = x
        self.y = y
    
    def visit(self):
        '''
        Denote a Tile object as visited for tracing the bot's steps back
        to the beginning
        '''
        self.visited = True

class Board(object):
    '''
    This class creates a Board object which contains a board attribute
    which is a 2D list of Tile objects
    '''
    def __init__(self, fname='test_file.txt'):
        bd = []
        x = 0
        y = 0
        for line in open(fname):
            parts = line.split()
            temp = []
            for p in parts:
                temp.append(Tile(x,y,p))
                x+=1
            bd.append(temp)
            y+=1
        
        self.board = bd
        self.arrow = True
        self.botx = 0
        self.boty = len(self.board)-1
    
    def show(self):
        'Show the board attribute of Board class'
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                print(self.board[i][j].value,end = ' ')
            print()
    
    def move(self,direct):
        '''
        Update the bot's posistion on the board by moving is one space
        in the input cardinal direction
        '''
        if direct == 'n':
            self.boty = max(self.boty-1,0)
        if direct == 'e':
            self.botx = min(self.botx+1,len(self.board[0])-1)
        if direct == 's':
            self.boty = min(self.boty+1,len(self.board)-1)
        if direct == 'w':
            self.botx = max(self.botx-1,0)
    
    def kill_wump(self,d,kn):
        if self.arrow:
            if d == 'n' and self.boty-1>-1:
                if self.board[self.boty-1][self.botx].value == 'W':
                   self.board[self.boty-1][self.botx].value = '0' 
                   kn[self.boty-1][self.botx] = '0'
                   self.arrow = False
            elif d == 'e' and self.botx+1<len(self.board[0]):
                if self.board[self.boty][self.botx+1].value == 'W':
                   self.board[self.boty][self.botx+1].value = '0' 
                   kn[self.boty][self.botx+1] = '0'
                   self.arrow = False
            elif d == 's' and self.boty+1 < len(self.board):
                if self.board[self.boty+1][self.botx].value == 'W':
                   self.board[self.boty+1][self.botx].value = '0' 
                   kn[self.boty+1][self.botx] = '0'
                   self.arrow = False
            elif d == 'w' and self.botx-1>-1:
                if self.board[self.boty][self.botx-1].value == 'W':
                   self.board[self.boty][self.botx-1].value = '0' 
                   kn[self.boty][self.botx-1] = '0'
                   self.arrow = False
            else:
                self.arrow = False
        
    
    def query(self):
            '''
            Return integer signal based on the tiles surrounding the bot's
            current position.
            1 --> Breeze
            2 --> Stench
            4 --> Gliter
            8 --> On the Gold space
            0 --> All neighbors are safe/not gold
            Output is the sum of all discovered signals
            '''
            self.board[self.boty][self.botx].visit()
            info = [False, False, False, False]
            #check breeze
            if self.board[max(self.boty-1,0)][self.botx].value == 'H'or self.board[min(self.boty+1,len(self.board)-1)][self.botx].value == 'H'\
                or self.board[self.boty][max(self.botx-1,0)].value == 'H'or self.board[self.boty][min(self.botx+1,len(self.board[0])-1)].value == 'H':
                    info[0] = True
            #check stench
            if self.board[max(self.boty-1,0)][self.botx].value == 'W'or self.board[min(self.boty+1,3)][self.botx].value == 'W'\
                or self.board[self.boty][max(self.botx-1,0)].value == 'W'or self.board[self.boty][min(self.botx+1,3)].value == 'W':
                    info[1] = True
            #check glitter
            if self.board[max(self.boty-1,0)][self.botx].value == 'G'or self.board[min(self.boty+1,3)][self.botx].value == 'G'\
                or self.board[self.boty][max(self.botx-1,0)].value == 'G'or self.board[self.boty][min(self.botx+1,3)].value == 'G':
                    info[2] = True
            
            #check if gold
            if self.board[self.boty][self.botx].value == 'G':
                info[3] = True
            
            out = 0
            if info[0]: out+=1
            if info[1]: out+=2
            if info[2] and not info[3]: out+=4
            if info[3]: out+=8
            
            return out
    
