#Manual checkers game
import turtle
import p1
import p2
import random
import copy

def drawFilledSquare(t,color):
    t.color(color)
    t.begin_fill()
    for x in range(4):
        t.forward(1)
        t.left(90)
    t.end_fill()

def drawCheckerRow(tu,color1,color2):
    for ct in range(4):
        drawFilledSquare(tu,color1)
        tu.forward(1)
        drawFilledSquare(tu,color2)
        tu.forward(1)

def positionTurtlefForNextRow(t1):
    t1.up()
    t1.backward(8)
    t1.left(90)
    t1.forward(1)
    t1.right(90)
    t1.down()

def drawChecker(t,wn,row,col,playerToken,ringColor,board):
    if playerToken in ["R","r"]:
        color='red'
    else:
        color='black'
    wn.tracer(False)
    t.color("black",color)
    t.begin_fill()
    t.up()
    t.goto(col+.5,row)
    t.down()
    t.circle(.48)
    t.end_fill()
    t.color(ringColor)
    for size in range(1,5):
        t.up()
        t.goto(col+.5,row+(.5-(size*.1)-.02))
        t.down()
        t.circle(size*.1)
    if row==0 and playerToken=='b':
        playerToken="B"
    if row==7 and playerToken=='r':
        playerToken="R"
    board[row][col]=playerToken
    if playerToken in ['R','B']:
        t.up()
        t.goto(col+.5,row+.4)
        t.down()
        t.color("yellow","yellow")
        t.begin_fill()
        t.circle(.1)
        t.end_fill()
        t.color("black",color)
    wn.tracer(True)

def drawLabel(t,wn,row,col):
    wn.tracer(False)
    t.up()
    t.color("white","white")
    t.goto(col+.81,row+1.03)
    t.write(chr(row+65)+str(col), font=("courier new",10,"bold"))
    wn.tracer(True)

def setupBoard():
    wn=turtle.Screen()
    wn.setworldcoordinates(-1,9,9.5,-1)
    t=turtle.Turtle()
    wn.tracer(False)
    for i in range(4):
        drawCheckerRow(t,"red","gray")
        positionTurtlefForNextRow(t)
        drawCheckerRow(t,"gray","red")
        positionTurtlefForNextRow(t)
    for row in range(8):
        for col in range(8):
            if (row+col)%2==1:
                drawLabel(t,wn,row,col)
    wn.tracer(True)
    t.hideturtle()
    row=[""]*8
    board=[]
    for i in range(8):
        board.append(row[:])
    return t,wn,board

def newGame(t,wn,board):
    for row in range(0,3):
        for col in range(8):
            if (row+col)%2==1:
                board[row][col]="r"
                drawChecker(t,wn,row,col,"r","gray",board)
    for row in range(5,8):
        for col in range(8):
            if (row+col)%2==1:
                board[row][col]="b"
                drawChecker(t,wn,row,col,"b","gray",board)

def showLogicalBoard(board):
    print("Board State")
    index=0
    print ("  01234567")
    for row in board:
        print(chr(index+65)+" ",end="")
        index+=1
        for col in row:
            if col=="":
                print("-",end="")
            else:
                print(col,end="")
        print()
    print()

def switchPlayer(currentPlayer):
    if currentPlayer=="black":
        currentPlayer="red"
        forwardInc=1
    else:
        currentPlayer="black"
        forwardInc=-1
    return currentPlayer,forwardInc

def removeChecker(t,wn,fromRow,fromCol,board):
    wn.tracer(False)
    board[fromRow][fromCol]=""
    t.up()
    t.goto(fromCol,fromRow)
    drawFilledSquare(t,"gray")
    t.color("white")
    drawLabel(t,wn,fromRow,fromCol)
    wn.tracer(True)

def parseValidMove(move):
    fromRow=ord(move[0])-65
    fromCol=int(move[1])
    toRow=ord(move[3])-65
    toCol=int(move[4])
    move=move[3:]
    return move,fromRow,fromCol,toRow,toCol

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

##def getValidMove(player,board,forwardInc):
##    validMovesList=getValidMovesList(player,board,forwardInc)
##    print("MOVES",validMovesList)
##    validSingleJumpsList=getValidJumpsList(player,board,forwardInc)
##    print("JUMPS",validSingleJumpsList)
##
##    oldJumpsList=validSingleJumpsList
##    expandedJumpsList=expandJumps(oldJumpsList,board,player,forwardInc)
##    while expandedJumpsList != oldJumpsList:
##        oldJumpsList=expandedJumpsList
##        expandedJumpsList=expandJumps(oldJumpsList,board,player,forwardInc)
##        
##    print("EXPANDED",expandedJumpsList)
##    if expandedJumpsList==[]:
##        move=input("Enter move (e.g. "+ validMovesList[0] +") for "+player+" => ").upper()
##        while move.upper() != "QUIT" and move.upper() not in validMovesList:
##            print("Bad move . . .  try again!")
##            move=input("Enter move (e.g. "+ validMovesList[0] +") for "+player+" => ")
##        #move=validMovesList[random.randrange(len(validMovesList))]
##    else:
##        move=input("Enter jump (e.g. "+ expandedJumpsList[0] +") for "+player+" => ").upper()
##        while move.upper() != "QUIT" and move.upper() not in expandedJumpsList:
##            print("Bad jump specification . . .  try again!")
##            move=input("Enter move (e.g. "+ expandedJumpsList[0] +") for "+player+" => ")
##        #move=expandedJumpsList[random.randrange(len(expandedJumpsList))]
##    return move.upper()

def oldGame(t,wn,fileName,board):
    inFile=open(fileName,'r')
    currentPlayer=inFile.readline()[:-1] #read the current player and strip newline
    if currentPlayer=="black":
        forwardInc=-1
    else:
        forwardInc=1
    #process 8 rows to build board
    row=0
    col=0
    for line in inFile:
        line=line[:-1]                  #strip newline
        for square in line:
            if square=='-':
                board[row][col]=''
            else:   #is a square with a player letter
                ringColor="gray"
                board[row][col]=square
                drawChecker(t,wn,row,col,square,ringColor,board)
            col+=1
        col=0
        row+=1
    return currentPlayer,forwardInc

def saveGame(outFileName,board,currentPlayer):
    #code needed here to write the game out to a file (same format as oldGame.txt)
    outFile=open(outFileName,'w')
    outFile.write(currentPlayer+'\n')
    for row in board:
        for col in board:
            if col=='':
                outFile.write('-')
            else:
                outFile.write(col)
        outFile.write('\n')
    outFile.close()
    
def win(board,countMoves,maxMoves):
    if countMoves>=maxMoves:
        redPoints=0
        blackPoints=0
        for row in board:
            for col in row:
                if col in ['B','b']:
                    if col=='b':
                        blackPoints+=1
                    else:
                        blackPoints+=2
                elif col in ['R','r']:
                    if col=='r':
                        redPoints+=1
                    else:
                        redPoints+=2
        if redPoints>blackPoints:
            print("red wins by points")
            return True
        elif blackPoints>redPoints:
            print("black wins by points")
            return True
        else:
            print("ties")            
            return True
    else:  #check for actual winner
        mList=getValidMovesList('red',board,1)
        jList=getValidJumpsList('red',board,1)
        if mList==[] and jList==[]:
            print("black wins")
            return True
        mList=getValidMovesList('black',board,-1)
        jList=getValidJumpsList('black',board,-1)
        if mList==[] and jList==[]:
            print("red wins")
            return True
        return False

def main():
    #Set up game old or new
    t,wn,board=setupBoard()
    fileName=input("Press enter for new game or enter file name to load old game => ")
    if fileName=='':    
        newGame(t,wn,board)
        currentPlayer="black"
        forwardInc=-1        
    else:
        currentPlayer,forwardInc=oldGame(t,wn,fileName,board)
    showLogicalBoard(board)
    #Start the game loop
    maxMoves=3000
    countMoves=0
    gameOver=False
    if currentPlayer=="black":
        move=p1.getValidMove(currentPlayer,board,forwardInc)
    else:
        move=p2.getValidMove(currentPlayer,board,forwardInc) 
    while not gameOver:
        if move!="QUIT":
            #Make the move
            while len(move)>=5:
                move,fromRow,fromCol,toRow,toCol=parseValidMove(move)               #break move e.g. A1:B2  into its numeric components
                drawChecker(t,wn,toRow,toCol,board[fromRow][fromCol],"gray",board)  #includes updating the board and graphics toRow, toCol
                removeChecker(t,wn,fromRow,fromCol,board)                           #includes updating the board and graphics fromRow, fromCol
                if abs(fromRow-toRow)==2:                                           #must be a jump, so
                    removeChecker(t,wn,(toRow+fromRow)//2,(toCol+fromCol)//2,board) #remove the jumped checker, includes all updating
                countMoves+=1
            showLogicalBoard(board)
            #Switch the current player
            currentPlayer,forwardInc=switchPlayer(currentPlayer)
            #Get the next move
            if not win(board,countMoves,maxMoves):
                if currentPlayer=="black":
                    move=p1.getValidMove(currentPlayer,board,forwardInc)
                else:
                    move=p2.getValidMove(currentPlayer,board,forwardInc) 
            else:
                gameOver=True
        else:
            outFileName=input("Press enter to quit or enter a filename to save the game => ")
            if outFileName!='':
                saveGame(outFileName,board,currentPlayer)
            return

main()
