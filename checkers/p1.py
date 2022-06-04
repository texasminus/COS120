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


def findMovesToKingRow(validMovesList,kingRow): #
    movesToKingRowList=[]
    kingRow_=chr(kingRow+65)
    for move in validMovesList:
        if move[3]==kingRow_:
            movesToKingRowList.append(move)
    return movesToKingRowList
        
def findMovesToSideSquare(validMovesList): #
    movesToSideSquareList=[]
    for move in validMovesList:
        if move[4]=='7' or move[4]=='0':
            movesToSideSquareList.append(move)
    return movesToSideSquareList

def findLongestJumps(expandedJumpsList):
    maxLen=0
    maxIdxList=[]
    longestJumpsList=[]
    for idx in range(len(expandedJumpsList)):
        if len(expandedJumpsList[idx]) > maxLen:
            maxIdxList=[idx]
            maxLen=len(expandedJumpsList[idx])
        elif len(expandedJumpsList[idx])== maxLen:
            maxIdxList.append(idx)
    for idx in maxIdxList:
        longestJumpsList.append(expandedJumpsList[idx])
    return longestJumpsList

def findJumpsClosestToKingRowList(expandedJumpsList,kingRow):
    jumpsClosestToKingRowList=[]
    furthestIdxList=[]
    diff=10
    for idx in range(len(expandedJumpsList)):
        if abs((ord(expandedJumpsList[idx][-2])-65)-kingRow)<diff:
            furthestIdxList=[idx]
            diff=abs((ord(expandedJumpsList[idx][-2])-65)-kingRow)
        elif abs((ord(expandedJumpsList[idx][-2])-65)-kingRow)==diff:
            furthestIdxList.append(idx)
    for idx in furthestIdxList:
        jumpsClosestToKingRowList.append(expandedJumpsList[idx])
    return jumpsClosestToKingRowList

def blockLongestJumpList(opposingExpandedJumpsList,validMovesList,expandedJumpsList):
    opposingLongests=findLongestJumps(opposingExpandedJumpsList)
    blockLongestJumpsList=[]
    gothrus=[]
    for move in opposingLongests:
        gothrus=move[3:].split(':')
    for move2 in validMovesList:
        if move2[-2:] in gothrus:
            blockLongestJumpsList.append(move2)
    for jump in expandedJumpsList:
        if jump[-2:] in gothrus:
            blockLongestJumpsList.append(jump)
    return blockLongestJumpsList

def blockMoveToKingRowList(opposingMovesList,validMovesList,expandedJumpsList,enemyKingRow):
    opposingMovesToKingRowList=findMovesToKingRow(opposingMovesList,enemyKingRow)
    blockMovesToKingRowList=[]
    for move in opposingMovesToKingRowList:
        for move2 in validMovesList:
            if move2[-2:]==move[-2:]:
                blockMovesToKingRowList.append(move2)
        for jump in expandedJumpsList:
            if jump[-2:]==move[-2:]:
                blockMovesToKingRowList.append(jump)
    return blockMovesToKingRowList
            
def getValidMove(player,board,forwardInc):
    if player=="red":
        enemyPlayer='black'
    else:
        enemyPlayer='red'
        
    if forwardInc==1:
        kingRow=7
        enemyKingRow=0
    else:
        kingRow=0
        enemyKingRow=7
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
    
    #Opposing Player's Lists
    opposingValidSingleJumpsList=getValidJumpsList(enemyPlayer,board,-forwardInc)
    opposingExpandedJumpsList=expandJumps(opposingValidSingleJumpsList,board,enemyPlayer,-forwardInc)
    opposingMovesList=getValidMovesList(enemyPlayer,board,-forwardInc)
    blockMovesToKingRowList=blockMoveToKingRowList(opposingMovesList,validMovesList,expandedJumpsList,enemyKingRow)
    #Heuristic 7 - Block Moves To KingRow
    blockLongestJumpsList=blockLongestJumpList(opposingExpandedJumpsList,validMovesList,expandedJumpsList)
    if blockMovesToKingRowList!=[]:
        print("BlockMovesToKingRow ",blockMovesToKingRowList)
##        move=input("Enter move (e.g. "+ blockMovesToKingRowList[0] +") for "+player+" => ").upper()
##        while move.upper() != "QUIT" and move.upper() not in blockMovesToKingRowList:
##            print("Bad move . . .  try again!")
##            move=input("Enter move (e.g. "+ blockMovesToKingRowList[0] +") for "+player+" => ")
        move=blockMovesToKingRowList[random.randrange(len(blockMovesToKingRowList))]
        return move.upper()
    #Heuristic 6 - Block the jumps 
    elif blockLongestJumpsList != []:
        print("BlockJumps ",blockLongestJumpsList)
        move=blockLongestJumpsList[random.randrange(len(blockLongestJumpsList))]
        return move.upper()
   
    elif expandedJumpsList==[]:
        #Generate lists about board state
        movesToKingRowList=findMovesToKingRow(validMovesList,kingRow)
        movesToSideSquareList=findMovesToSideSquare(validMovesList)        
        #Heuristic 1  -  If a move to the King row with a regular checker is available, take it so the checker will become a King
        if movesToKingRowList != []:
            move=movesToKingRowList[random.randrange(len(movesToKingRowList))]
        #Heuristic 2  -  If a move to a side square is available, take it
        elif movesToSideSquareList != []:
            move=movesToSideSquareList[random.randrange(len(movesToSideSquareList))]
        elif validSingleJumpsList!=[]:
            move=validSingleJumpsList[random.randrange(len(validSingleJumpsList))]
        else:
            #Automated move
            move=validMovesList[random.randrange(len(validMovesList))]
    else:
        jumpsToKingRowList=findMovesToKingRow(expandedJumpsList,kingRow)
        jumpsToSideSquareList=findMovesToSideSquare(expandedJumpsList)
        longestJumpsList=findLongestJumps(expandedJumpsList)
        jumpsClosestToKingRowList=findJumpsClosestToKingRowList(expandedJumpsList,kingRow)
        #Heuristic #3  -  If a jump to a King row with a regular checker is available, take it so the checker will become a king
        if jumpsToKingRowList != []:
            move=jumpsToKingRowList[random.randrange(len(jumpsToKingRowList))]
            return move.upper()
        #Heuristic #4  -  If multiple jumps are available, take the longest jump.  If all jumps are equal length, take the jump that lands closest to the opposing home row.
        if longestJumpsList != []:
            move=longestJumpsList[random.randrange(len(longestJumpsList))]
            return move.upper()
        elif jumpsClosestToKingRowList != []:
            move=jumpsClosestToKingRowList[random.randrange(len(jumpsClosestToKingRowList))]
            return move.upper()
        elif jumpsToSideSquare != []:
            move=jumpsToSideSquare[random.randrange(len(jumpsToSideSquare))]
            return move.upper()
        elif validSingleJumpsList!=[]:
            move=validSingleJumpsList[random.randrange(len(validSingleJumpsList))]
            return move.upper()
        else:       
            #Automated jump
            move=expandedJumpsList[random.randrange(len(expandedJumpsList))]
    return move.upper()
