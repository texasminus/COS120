import random

def getValidMovesList(player,board,forwardInc):
    validMovesList=[]
    for row in range(8):
        for col in range(8):
            if board[row][col] in [player[0],player[0].upper()]:
                if board[row][col] in ['b','r']:
                    rowIncs=[forwardInc]
                else:
                    rowIncs=[forwardInc,-forwardInc]
                for rowInc in rowIncs: 
                    for colInc in [1,-1]:
                        if row+rowInc in range(8) and col+colInc in range(8) and board[row+rowInc][col+colInc]=='':
                           validMovesList.append(chr(row+65)+str(col)+":"+chr(row+rowInc+65)+str(col+colInc))
    return validMovesList

def getValidJumpsList(player,board,forwardInc):
    if player=="red":
        enemyCheckers=['b','B']
    else:
        enemyCheckers=['r','R']
    validJumpsList=[]
    for row in range(8):
        for col in range(8):
            if board[row][col] in [player[0],player[0].upper()]:
                if board[row][col] in ['b','r']:
                    rowIncs=[forwardInc]
                else:
                    rowIncs=[forwardInc,-forwardInc]
                for rowInc in rowIncs: 
                    for colInc in [1,-1]:   #to the right and to the left one square
                        if row+rowInc*2 in range(8) and col+colInc*2 in range(8) \
                           and board[row+rowInc*2][col+colInc*2]==''  \
                           and board[row+rowInc][col+colInc] in enemyCheckers: 
                           validJumpsList.append(chr(row+65)+str(col)+":"+chr(row+rowInc*2+65)+str(col+colInc*2))
    return validJumpsList

def expandJumps(jumpsList,board,player,forwardInc):
    if player=="red":
        enemyCheckers=['b','B']
    else:
        enemyCheckers=['r','R']
    expandedJumpsList=[]
    for jmp in jumpsList:
        expandedJumpsList.append(jmp)
        fromRow=ord(jmp[-2])-65
        fromCol=int(jmp[-1])
        originalRow=ord(jmp[0])-65
        originalCol=int(jmp[1])
        if board[originalRow][originalCol] in ['b','r']:
            rowIncs=[forwardInc]
        else:
            rowIncs=[forwardInc,-forwardInc]
        for rowInc in rowIncs: 
            toRow=fromRow+rowInc*2
            for colInc in [-1,1]:
                toCol=fromCol+colInc*2
                if toRow in range(8) and toCol in range(8) \
                    and board[fromRow+rowInc][fromCol+colInc] in enemyCheckers \
                    and (board[toRow][toCol]=='' or jmp[0:2]==chr(toRow+65)+str(toCol)) \
                    and ((jmp[-2:]+":"+chr(toRow+65)+str(toCol)) not in jmp) \
                    and ((chr(toRow+65)+str(toCol))+':'+jmp[-2:] not in jmp) and (chr(toRow+65)+str(toCol)!=jmp[-5:-3]):
                        expandedJumpsList.append(jmp+":"+chr(toRow+65)+str(toCol))
                        if jmp in expandedJumpsList:
                            expandedJumpsList.remove(jmp)                            
    return expandedJumpsList

def getValidMove(player,board,forwardInc):
    validMovesList=getValidMovesList(player,board,forwardInc)
    print("MOVES",validMovesList)
    validSingleJumpsList=getValidJumpsList(player,board,forwardInc)
    print("JUMPS",validSingleJumpsList)

    oldJumpsList=validSingleJumpsList
    expandedJumpsList=expandJumps(oldJumpsList,board,player,forwardInc)
    while expandedJumpsList != oldJumpsList:
        oldJumpsList=expandedJumpsList
        expandedJumpsList=expandJumps(oldJumpsList,board,player,forwardInc)
        
    print("EXPANDED",expandedJumpsList)
    if expandedJumpsList==[]:
##        move=input("Enter move (e.g. "+ validMovesList[0] +") for "+player+" => ").upper()
##        while move.upper() != "QUIT" and move.upper() not in validMovesList:
##            print("Bad move . . .  try again!")
##            move=input("Enter move (e.g. "+ validMovesList[0] +") for "+player+" => ")
        move=validMovesList[random.randrange(len(validMovesList))]
    else:
##        move=input("Enter jump (e.g. "+ expandedJumpsList[0] +") for "+player+" => ").upper()
##        while move.upper() != "QUIT" and move.upper() not in expandedJumpsList:
##            print("Bad jump specification . . .  try again!")
##            move=input("Enter move (e.g. "+ expandedJumpsList[0] +") for "+player+" => ")
        move=expandedJumpsList[random.randrange(len(expandedJumpsList))]
    return move.upper()
