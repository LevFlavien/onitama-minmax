import sys
from board import *
from minmax import *
from pprint import pprint

# Paramètres
width = 5 # Default 5
height = 5 # Default 5
firstPlayer = 0 # Default 0
maxDepth = 2 # Default 10

# Récupération du l'entrée du joueur
def getUserMove(b):
    message = "Entrez un mouvement: "
    print(message)
    while True:
        move = []
        move = input().lower().split()
        if "stop" in move:
            sys.exit("*** GAME STOPPED ***")
        if not(len(move) == 3):
            print("Commande invalide.", message)
            continue
        moveFromTup = (int(move[0][1]), ord(move[0][0]) - 97)
        moveToTup = (int(move[1][1]), ord(move[1][0]) - 97)
        card = move[2]
        print("mouvements joueur :", moveFromTup, moveToTup)
        if not card in b.whitecards:
            print("Vous ne possédez pas cette carte")
            continue
        usedCard = b.getCard(card)
        if not (moveToTup in usedCard.availableMovesWhite(moveFromTup)):
            print("Le mouvement", moveToTup,
                  "n'est pas possible. Mouvements disponibles pour cette carte: ",
                  usedCard.availableMovesWhite(moveFromTup))
            continue
        # Vérification de l'appartenance de la pièce
        if not (moveFromTup in b.whitelist):
            print("La pièce", moveFromTup, "ne vous appartient pas. Sélectionnez l'un des suivantes : ", b.whitelist)
            continue
        break
    move = (moveFromTup, moveToTup, b.NOTDONE, card)
    return move

### MAIN PROGRAM ###

b = board(width, height, firstPlayer, maxDepth)
b.printBoard()

# Boucle principale
while True:#b.gameWon == -1:
    # Tour du joueur
    userMove = getUserMove(b)
    b.moveWhite(*userMove)
    print("***Tour terminé, attente de l'ordinateur...")
        
    # Tour de l'ordinateur
    temp = minMax(b)
    b = temp[0]
    print("**********COMPUTER MOVE**********")
    b.printBoard()
    if b.gameWon == b.WHITE:
        print("White Wins\nGame Over")
        #break
    elif b.gameWon == b.BLACK:
        print("Black Wins\nGame Over")
        #break
