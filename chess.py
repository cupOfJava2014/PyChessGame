import pygame
import chess
import const

pygame.init()

def processClick(x, y):
    for sx in range(8):
        for sy in range(8):
            if sx * 32 < x < sx * 32 + 32 and sy * 32 + 64 < y < sy * 32 + 32 + 64:
                return (sx,sy)

def getIndex(x,y):
    index = 0
    index += x * 8
    index += y
    return index

def extractData(data):
    ranks = str(data).split('\n')
    for rank in ranks:
        for item in rank.split(' '):
            spaces.append(item)
    return spaces

boardData = chess.Board()

white = {}
black = {}

space_in_focus = -1
highlight_spaces = []

spaces = []

board = pygame.image.load('board.png')
pieces = pygame.image.load('pieces.png') # Pawn, Rook, Knight, Bishop, Queen, King

board = pygame.transform.scale(board,const.boardDim)

#Individual pieces
white['pawn'] = pieces.subsurface((0,0,const.pieceW,const.pieceH))
black['pawn'] = pieces.subsurface((0,const.pieceH,const.pieceW,const.pieceH))
white['rook'] = pieces.subsurface((const.pieceW,0,const.pieceW,const.pieceH))
black['rook'] = pieces.subsurface((const.pieceW,const.pieceH,const.pieceW,const.pieceH))
white['knight'] = pieces.subsurface((const.pieceW*2,0,const.pieceW,const.pieceH))
black['knight'] = pieces.subsurface((const.pieceW*2,const.pieceH,const.pieceW,const.pieceH))
black['knight'] = pygame.transform.flip(black['knight'], True, False)
white['bishop'] = pieces.subsurface((const.pieceW*3,0,const.pieceW,const.pieceH))
white['bishop'] = pygame.transform.flip(white['bishop'], True, False)
black['bishop'] = pieces.subsurface((const.pieceW*3,const.pieceH,const.pieceW,const.pieceH))
white['queen'] = pieces.subsurface((const.pieceW*4,0,const.pieceW,const.pieceH))
black['queen'] = pieces.subsurface((const.pieceW*4,const.pieceH,const.pieceW,const.pieceH))
white['king'] = pieces.subsurface((const.pieceW*5,0,const.pieceW,const.pieceH))
black['king'] = pieces.subsurface((const.pieceW*5,const.pieceH,const.pieceW,const.pieceH))

display = pygame.display.set_mode((640,640))
pygame.display.set_caption('Chess')
gameExit = False

while not gameExit:
    
    display.fill(const.white)
    display.blit(board,(0,0 + const.boardOffsetY))
    display.blit(const.label, (10,350))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mx, my = pygame.mouse.get_pos()
            spaceClicked = processClick(mx,my)
            if not spaceClicked == None:
                sx, sy = spaceClicked
                index = getIndex(sx, sy)
                print index
                move = []
                moves_str = []
                moves_index = []
                hspaces_old = highlight_spaces
                highlight_spaces = []
                
                index = getIndex(sx,sy)
                pc = spaces[index]
                
                highlight = False
                for sqr in range(64):
                    if chess.Move(index, sqr) in boardData.legal_moves:
                        move.append(chess.Move(index, sqr))
                if index in hspaces_old:
                    new_move = chess.Move(space_in_focus, index)
                    print "Move to commit(new_move): ",str(new_move)
                    print "Pre-push board data: ",str(boardData.fen())
                    boardData.push(new_move)
                    print "Post-push board data: ",str(boardData.fen())
                for m in move:
                    moves_str.append(m.uci()[2:])
                    for mstr in moves_str:
                        #moves_index.append(chess.SQUARE_NAMES.index(mstr))
                        highlight_spaces.append(chess.SQUARE_NAMES.index(mstr))
                    space_in_focus = index

                    
                    
                
    for i in highlight_spaces:
        files = i % 8
        ranks = int(i / 8)
        pygame.draw.rect(display, const.green, (ranks * const.pieceW, files * const.pieceW + const.boardOffsetY, const.pieceW, const.pieceW))
    spaces = []
    spaces = extractData(boardData)
    for x in range(8):
        for y in range(8):
            index = getIndex(x,y)
            pc = spaces[index]
            spr = {
                'P':black['pawn'],
                'p':white['pawn'],
                'R':black['rook'],
                'r':white['rook'],
                'N':black['knight'],
                'n':white['knight'],
                'B':black['bishop'],
                'b':white['bishop'],
                'Q':black['queen'],
                'q':white['queen'],
                'K':black['king'],
                'k':white['king'],
                '.':None
            }.get(pc)
            if not spr == None:
                w,h = spr.get_size()
                hOffset = h - 32
                display.blit(spr, (x*const.pieceW,y*(const.pieceH-hOffset) + const.boardOffsetY/2))
    pygame.display.update()
