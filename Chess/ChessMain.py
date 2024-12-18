"""
This is our main driver file.
"""

import pygame as p
from Chess import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

'''
Initialize a global dictionary of images. This will be called exactly once in the main function.
'''
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


'''
The main driver for our code. This will handle user input and updating the graphics.
'''
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False # flag variable for when a move is made

    loadImages()
    running = True
    sqSelected = () # no square is selected, keep track of the last click of the user (tuple: row, col)
    playerClicks = [] # keep track of the player clicks (two tuples: [(6,4), (4,4)])

    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False

            # mouse handler
            elif event.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # (x,y) location of the mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE

                if sqSelected == (row, col): # the user clicked the same square twice
                    sqSelected = () # deselect
                    playerClicks = [] # clear the player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) # append for both first and second clicks

                if len(playerClicks) == 2: # after second click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            moveMade = True
                            sqSelected = () # reset user clicks
                            playerClicks = []
                    if not moveMade:
                            playerClicks = [sqSelected]

            # key presses
            elif event.type == p.KEYDOWN:
                if event.key == p.K_z: # undo when 'Z' is pressed
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[((row+col)%2)]
            p.draw.rect(screen, color, p.Rect(row*SQ_SIZE, col*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == '__main__':
    main()
