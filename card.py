# -*- coding: utf-8 -*-

# Liste des cartes et leurs mouvements
class card:
    def __init__(self, name):
        self.name = name

    def availableMovesWhite(self, coor):
        """
            Liste les mouvements disponibles à partir de coordonnees pour une piece blanche.
        """
        return [coor]
    def availableMovesBlack(self, coor):
        """
            Liste les mouvements disponibles à partir de coordonnees pour une piece noire.
        """
        return [coor]

    def __str__(self):
        return self.name
    def __repr__(self):
        return self.__str__()

class Wolf(card):
    def __init__(self, name = "Wolf"):
        self.name = name
    def availableMovesWhite(self, coor):
        x = coor[0]
        y = coor[1]
        return [(x-1,y-1), (x,y-1), (x+1,y-1)]
    def availableMovesBlack(self, coor):
        x = coor[0]
        y = coor[1]
        return [(x-1,y+1), (x,y+1), (x+1,y+1)]

class Turtle(card):
    def __init__(self, name = "Turtle"):
        self.name = name
    def availableMovesWhite(self, coor):
        x = coor[0]
        y = coor[1]
        return [(x+2,y), (x-1,y+1), (x+1,y+1), (x-2,y)]
    def availableMovesBlack(self, coor):
        x = coor[0]
        y = coor[1]
        return [(x+2,y), (x-1,y-1), (x+1,y-1), (x-2,y)]

class Snake(card):
    def __init__(self, name = "Snake"):
        self.name = name
    def availableMovesWhite(self, coor):
        x = coor[0]
        y = coor[1]
        return [(x-1,y), (x+1,y+1), (x+1,y-1)]
    def availableMovesBlack(self, coor):
        x = coor[0]
        y = coor[1]
        return [(x+1,y), (x-1,y-1), (x-1,y+1)]

class Horse(card):
    def __init__(self, name = "Horse"):
        self.name = name
    def availableMovesWhite(self, coor):
        x = coor[0]
        y = coor[1]
        return [(x,y+1), (x,y-1), (x-1,y)]
    def availableMovesBlack(self, coor):
        x = coor[0]
        y = coor[1]
        return [(x,y-1), (x,y+1), (x+1,y)]
    
class Monkey(card):
    def __init__(self, name = "Monkey"):
        self.name = name
    def availableMovesWhite(self, coor):
        x = coor[0]
        y = coor[1]
        return [(x-1, y-1), (x-1, y+1), (x+1, y+1), (x+1, y-1)]
    def availableMovesBlack(self, coor):
        x = coor[0]
        y = coor[1]
        return [(x+1, y+1), (x+1, y-1), (x-1, y-1), (x-1, y+1)]