# Fonctions minmax et evaluation
from copy import deepcopy

def is_won(board):
    """
        Returns true if the game has been won
    """
    return board.gameWon != board.NOTDONE
        

def minMax(board):
    """
        Fonction minmax principale.
        A partir d'un plateau, retourne le meilleur plateau possible au prochain tour.
    """
    bestBoard = None
    currentDepth = board.maxDepth + 1
    while not bestBoard and currentDepth > 0:
        currentDepth -= 1
        # Get the best move and it's value from maxMinBoard (minmax handler)
        (bestBoard, bestVal) = maxMove(board, currentDepth)
        # If we got a NUll board raise an exception
    if not bestBoard:
        raise Exception("Seuls des plateaux nuls n'ont pu etre retournes")
    # Otherwise return the board and it's value
    else:
        return (bestBoard, bestVal)

def maxMove(maxBoard, currentDepth):
    """
        Appelle le calcul du meilleur mouvement pour le joueur noir (IA).
        Cherche un plateau avec une valeur INF.
    """
    return maxMinBoard(maxBoard, currentDepth-1, float('-inf'))
    

def minMove(minBoard, currentDepth):
    """
        Appelle le calcul du meilleur mouvement pour le joueur blanc.
        Cherche un plateau avec une valeur -INF.
    """
    return maxMinBoard(minBoard, currentDepth-1, float('inf'))

def maxMinBoard(board, currentDepth, bestMove):
    """
        Calcule le meilleur mouvement.
    """
    # Verifie si le noeud est final
    if is_won(board) or currentDepth <= 0:
        return (board, staticEval(board))

    # Valeurs setup pour minmax
    best_move = bestMove
    best_board = None    

    # MaxNode
    if bestMove == float('-inf'):
        # Recupere la liste des mouvements possibles
        moves = board.iterBlackMoves()
        for move in moves:
            maxBoard = deepcopy(board)
            maxBoard.moveSilentBlack(*move)
            value = minMove(maxBoard, currentDepth-1)[1] # Appel recursif
            if value > best_move:
                best_move = value
                best_board = maxBoard         

    # MinNode
    elif bestMove == float('inf'):
        moves = board.iterWhiteMoves()
        for move in moves:
            minBoard = deepcopy(board)
            minBoard.moveSilentWhite(*move)
            value = maxMove(minBoard, currentDepth-1)[1] # Appel recursif
            if value < best_move:
                best_move = value
                best_board = minBoard

    else:
        raise Exception("bestMove different de inf et -inf")
  
    return (best_board, best_move)

def staticEval(evalBoard):
    """
        Evalue un plateau.
        Retourne -INF si le joueur blanc (WHITE) gagne.
        Retourne INF is le joueur noir (BLACK) gagne.
        Sinon, il est evalue avec une fonction particuliere.
    """
    # Has someone won the game? If so return an INFINITE value
    # Si l'un des joueurs est evalue comme gagnant
    if evalBoard.gameWon == evalBoard.BLACK:
        print("VICTOIRE NOIRE trouve")
        return float('inf')  
    elif evalBoard.gameWon == evalBoard.WHITE:
        print("VICTOIRE BLANCHE trouve")
        return float('-inf')
    
    score = 0
    pieces = None   
    if evalBoard.turn == evalBoard.WHITE:
        pieces = evalBoard.whitelist
        scoremod = -1
    elif evalBoard.turn == evalBoard.BLACK:
        pieces = evalBoard.blacklist
        scoremod = 1

    # Super Gigadeath Defense Evaluator
    # This AI will attempt to keep it's peices as close together as possible until it has a chance
    # to jump the opposing player. It's super effective
    """
    distance = 0
    for piece1 in pieces:
        for piece2 in pieces:
            if piece1 == piece2:
                continue
            dx = abs(piece1[0] - piece2[0])
            dy = abs(piece1[1] - piece2[1])
            distance += dx**2 + dy**2
    distance /= len(pieces)
    score = 1.0/distance * scoremod
    """
    
    return score
