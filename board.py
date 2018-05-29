# -*- coding: utf-8 -*-

# Plateau de jeu
from card import *
import random
from pprint import pprint

class board(object):
    BLACK = 1
    WHITE = 0
    NOTDONE = -1
    def __init__(self, height, width, firstPlayer, maxDepth):
        """
            Constructs a board, right now maxDepth is statically assigned
        """
        self.width = width
        self.height = height
        # Crée deux liste par joueur qui contiennent les pièces et les cartes
        self.blacklist = []
        self.blackcards = ((),)
        self.whitelist = []
        self.whitecards = ((),)
        # Place les pieces
        for i in range(width):
            self.blacklist.append((i, 0))#((i, (i+1)%2))
            self.whitelist.append((i, height - 1))#((i, height - (i%2) - 1))
        # Instancie et distribue les cartes
        self.cards = {
            "wolf": Wolf(),
            "turtle": Turtle(),
            "snake": Snake(),
            "horse": Horse(),
            "monkey": Monkey()
        }
        self.cardsPool = ["wolf","turtle","snake","horse","monkey"]
        self.distributeCards()
        # boardState contient l'etat actuel du plateau.
        self.boardState = [[' '] * self.width for x in range(self.height)]
        self.gameWon = self.NOTDONE
        self.turn = firstPlayer
        self.maxDepth = maxDepth
        
        
    def getCard(self, name):
        return self.cards[name]
    
    def distributeCards(self):
        for i in range(0, 2):
            card1 = random.choice(self.cardsPool)
            self.cardsPool.remove(card1)
            card2 = random.choice(self.cardsPool)
            self.cardsPool.remove(card2)
            print(i)
            if i == 0:
                self.blackcards = (card1, card2)
            else:
                self.whitecards = (card1, card2)
                
    def getNewCardWhite(self, usedCard):
        #print("--------usedCard")
        #pprint(usedCard)
        index = self.whitecards.index(usedCard)
        newCard = random.choice(self.cardsPool)
        self.cardsPool.append(usedCard)
        self.cardsPool.remove(newCard)
        if index == 1:
            self.whitecards = (self.whitecards[0], newCard)
        else:
            self.whitecards = (newCard, self.whitecards[1])
    
    def getNewCardBlack(self, usedCard):
        #print("--------usedCard")
        #pprint(usedCard)
        index = self.blackcards.index(usedCard)
        newCard = random.choice(self.cardsPool)
        self.cardsPool.append(usedCard)
        self.cardsPool.remove(newCard)
        if index == 1:
            self.blackcards = (self.blackcards[0], newCard)
        else:
            self.blackcards = (newCard, self.blackcards[1])
                
    def printCards(self):
        print("Cartes joueur blanc:", self.whitecards)
        print("Cartes joueur noir:", self.blackcards)
        print("Carte restante:", self.cardsPool)
    
    def iterWhiteMoves(self):
        """
            Generateur pour les mouvements blancs.
        """
        for piece in self.whitelist:
            for move in self.iterWhitePiece(piece):
                yield move
                
    def iterBlackMoves(self):
        """
            Generateur pour les mouvements noirs.
        """
        for piece in self.blacklist:
            #print("PIECE:", piece)
            for move in self.iterBlackPiece(piece):
                #print("move", move)
                yield move
                
    def iterWhitePiece(self, piece):
        """
            Generates possible moves for a white piece
        """            
        return self.iterBoth(piece, ((-1,-1),(1,-1)), self.whitecards)
    
    def iterBlackPiece(self, piece):
        """
            Generates possible moves for a black piece
        """
        return self.iterBoth(piece, ((-1,1),(1,1)), self.blackcards)

    def iterBoth(self, piece, moves, cards):
        """
            Handles the actual generation of moves for either black or white pieces
        """
        
        for card in cards:
        
            if self.turn == self.BLACK:
                moves = self.getCard(card).availableMovesBlack(piece)
            if self.turn == self.WHITE:
                moves = self.getCard(card).availableMovesWhite(piece)
            
            for move in moves:
                # Regular Move
                targetx = piece[0] + move[0]
                targety = piece[1] + move[1]
                # Si le mouvement est en dehors du plateau
                if targetx < 0 or targetx >= self.width or targety < 0 or targety >= self.height:
                    continue
                target = (targetx, targety)
                # Verifie si la destination du mouvement est une piece
                black = target in self.blacklist
                white = target in self.whitelist
                #if not black and not white:
                if not (self.turn == self.BLACK and black) and not (self.turn == self.WHITE and white):
                    if (target == (2, 4) and self.turn == self.BLACK) or (target == (2, 0) and self.turn == self.WHITE):
                        yield (piece, target, self.turn, card)
                    else:
                        yield (piece, target, self.NOTDONE, card)
                else:
                    continue            
    
    def updateBoard(self):
        """
            Met à jour la liste contenant le plateau par rapport aux listes de pièces
        """
        a = 0
        for i in range(self.width):
            for j in range(self.height):
                self.boardState[i][j] = " "
        for piece in self.blacklist:
            self.boardState[piece[1]][piece[0]] = 'B'#str(a)#u'◆'
            a = a + 1
        for piece in self.whitelist:
            self.boardState[piece[1]][piece[0]] = 'W'#u'◇'

    # Mouvements des pièces
    def moveSilentBlack(self, moveFrom, moveTo, winLoss, card): 
        """
            Bouge une pièce noire
        """
        #try:
        self.getNewCardBlack(card)
        #except:
        #    print("Erreur tirage carte")
        if moveTo[0] < 0 or moveTo[0] >= self.width or moveTo[1] < 0 or moveTo[1] >= self.height:
            raise Exception("Impossible, la pièce", moveFrom, "est en dehors du plateau.")
        black = moveTo in self.blacklist
        white = moveTo in self.whitelist
        if not black:
            self.blacklist[self.blacklist.index(moveFrom)] = moveTo
            if white:
                self.whitelist.remove(moveTo)
            self.updateBoard()
            self.turn = self.WHITE
            self.gameWon = winLoss
            #if moveTo == (2, 4):
            #    self.gameWon = self.BLACK
        else:
            raise Exception
        
    def moveSilentWhite(self, moveFrom, moveTo, winLoss, card):
        """
            Bouge une pièce blanche
        """
        # Tirage nouvelle carte
        self.getNewCardWhite(card)
        #try:
        #    self.getNewCardWhite(card)
        #except:
        #    print("Erreur tirage carte")
        if moveTo[0] < 0 or moveTo[0] >= self.width or moveTo[1] < 0 or moveTo[1] >= self.height:
            raise Exception("Impossible, la pièce", moveFrom, "est en dehors du plateau.")
        black = moveTo in self.blacklist
        white = moveTo in self.whitelist
        if not white:
            self.whitelist[self.whitelist.index(moveFrom)] = moveTo
            if black:
                self.blacklist.remove(moveTo)
            self.updateBoard()
            self.turn = self.BLACK
            self.gameWon = winLoss
            #if moveTo == (2, 0):
            #    self.gameWon = self.WHITE
        else:
            raise Exception
    
    def moveBlack(self, moveFrom, moveTo, winLoss, card):
        """
            Bouge une pièce noire d'une position à une autre.
            winLoss passé en tant que 0 (WHITE) ou 1 (BLACK)
        """
        self.moveSilentBlack(moveFrom, moveTo, winLoss, card)
        self.printBoard()
        
    def moveWhite(self, moveFrom, moveTo, winLoss, card):
        """
            Bouge une pièce blanche d'une position à une autre.
            winLoss passé en tant que 0 (WHITE) ou 1 (BLACK)
        """
        self.moveSilentWhite(moveFrom, moveTo, winLoss, card)
        self.printBoard()

    def printBoard(self):
        """
            Affiche le tableau et les cartes.
        """
        print(self)
        print(self.printCards())
        
    def __str__(self):
        self.updateBoard()
        lines = []
        # En-tetes du tableau
        lines.append('    ' + '   '.join(map(str, range(self.width))))
        # Dessine les lignes
        lines.append(u'  ╭' + (u'───┬' * (self.width-1)) + u'───╮')
        for num, row in enumerate(self.boardState[:-1]):
            lines.append(chr(num+65) + u' │ ' + u' │ '.join(row) + u' │')
            lines.append(u'  ├' + (u'───┼' * (self.width-1)) + u'───┤')
        lines.append(chr(self.height+64) + u' │ ' + u' │ '.join(self.boardState[-1]) + u' │')
        lines.append(u'  ╰' + (u'───┴' * (self.width-1)) + u'───╯')
        return '\n'.join(lines)