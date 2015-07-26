import pygame

pygame.font.init()

#colors
white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)
red = (255,0,0)

pieceH = 64
pieceW = 32 # dimensions of a piece

#How many pixels to push the board down on the screen so the pieces dont get screwed up
boardOffsetY = 64

# board text
font = pygame.font.Font('font.otf', 12)
label = font.render("# Move", 0, blue)
checkmate = font.render("CHECKMATE", 0, red)
check = font.render("CHECK", 0, red)
illegal = font.render("ILLEGAL MOVE", 0, red)
promote = font.render("Promote pawn:", 0, blue)

boardDim = (256,256)
