#======================================================
# Student: Damien Rodriguez
# Washington State University, Tri-Cities: Fall 2015
# CptS111: Introduction to Algorithmic Problem Solving
# Assignment: Wumpus Final Project
# System: Python v3.4.x IDLE (windows 10)
#======================================================

from graphics import *
import math
from os import getcwd
from random import seed, randint

#=============================================================================================
# Purpose: To determine if the user is clicking on one of the two rectangles
# Input: iRect = rectangle passed in
#        iPt = point passed in
# Output: iFlag = Boolean value that will determine if the user clicked a certain button 
def myRectPtCheck(iRect, iPt):
    xFlag, yFlag = False, False
    if iPt.getX() >= iRect.getP1().getX() and iPt.getX() <= iRect.getP2().getX(): xFlag = True
    if iPt.getY() >= iRect.getP1().getY() and iPt.getY() <= iRect.getP2().getY(): yFlag = True
    iFlag = xFlag and yFlag
    return iFlag
#=============================================================================================


#=====================================================================
#Purpose: To display a start Menu for the user to determine difficulty
#Input: There is no input
#Output: difficulty - the determinant in the creation of the game

def startMenu():
    menu = GraphWin("Hunt the Wumpus",620,200)
    done = False

    difficultyList = ["Easy","Medium","Hard"]
    difficultyButton = Rectangle(Point(10,120),Point(210,190))
    difficultyButton.draw(menu)
    difficultyText = Text(Point(110,155),difficultyList[0])
    difficultyText.draw(menu)
    difficulty = difficultyList[0]

    startButton = Rectangle(Point(410,120),Point(610,190))
    startButton.draw(menu)
    startText = Text(Point(510,155),"Start")
    startText.draw(menu)

    clicks = 0
    
    while not done:
        userClick = menu.getMouse()
        if myRectPtCheck(difficultyButton,userClick) == True:
            clicks += 1
            if clicks == 1:
                difficultyText.undraw()
                difficultyText = Text(Point(110,155),difficultyList[1])
                difficultyText.draw(menu)
                difficulty = difficultyList[1]
                
            elif clicks == 2:
                difficultyText.undraw()
                difficultyText = Text(Point(110,155),difficultyList[2])
                difficultyText.draw(menu)
                difficulty = difficultyList[2]
                
            elif clicks == 3:
                difficultyText.undraw()
                difficultyText = Text(Point(110,155),difficultyList[0])
                difficultyText.draw(menu)
                clicks = 0
                difficulty = difficultyList[0]
                
        elif myRectPtCheck(startButton,userClick) == True:
            done = True
            menu.close()
    return difficulty
#====================================================================================

#====================================================================================
def initialsMenu():

#   Other tests need to be made to see if this is the problem

    tmpDone = False
    
    initialsWindow = GraphWin("The End",300,60)
    initialsEntry = Entry(Point(100,30),3)
    initialsQuit = Rectangle(Point(200,20),Point(270,50))
    initialsQuitText = Text(Point(235,35),"Quit?")
    

    initialsQuit.draw(initialsWindow)
    initialsEntry.draw(initialsWindow)
    initialsQuitText.draw(initialsWindow)
    
    

    while not tmpDone:
        tMC = initialsWindow.getMouse()
        tmpDone = myRectPtCheck(initialsQuit,tMC)

    initials = initialsEntry.getText()
    initialsWindow.close()

    return(initials)
    



#====================================================================================
#The following functions are being used with permission by Russell Swannack
# ===================================================================================
# Purpose: Create a list of unique XY points
# Input: maxPtVal = Maximum point value
#          totPt = Total number of points desired in the list
# Output: ptList = List of unique XY points

def create_PtList(maxPtVal, totPt):
    ptList = []
    ptCnt = 0
    while ptCnt < totPt:                                    # keep going until we have all uniqe value sets
        tmpPt = [randint(0, maxPtVal), randint(0, maxPtVal)]
        if not (tmpPt in ptList):                           # check if it is in the list already
            ptList.append(tmpPt)
            ptCnt += 1                                      # track how many we have
    return (ptList)
#==================================================================


# ===================================================================
def randomPlacement(difficulty):
    seed()  # Intialize random number

    # 1st subscript: Game Difficulty (Easy, Medium, Hard)
    # 2nd subscript: Number of Arrows to start
    #                Min/Max number of pits
    #                Min/Max number of treasures
    #                Number of Wumpus
    #                Number of Squares (horizontal & vertical)
    gameRef = [[5, 10, 15, 10, 15, 1, 8],
               [2, 15, 20, 10, 15, 1, 9],
               [2, 15, 20, 15, 20, 2, 10]]

    # Create required random number of treasure (gold) locations
    goldTempTotal = randint(gameRef[difficulty][3], gameRef[difficulty][4])
    goldLoc = create_PtList(gameRef[difficulty][6]-1, goldTempTotal)

    pitTempTotal = randint(gameRef[difficulty][1], gameRef[difficulty][2])
    pitLoc = create_PtList(gameRef[difficulty][6]-1,pitTempTotal)

    wumpusTempTotal = randint(gameRef[difficulty][5], gameRef[difficulty][5])
    wumpusLoc = create_PtList(gameRef[difficulty][6]-1,wumpusTempTotal)

    tmpFlag = True
    while tmpFlag:
        characterLoc = create_PtList(gameRef[difficulty][6]-1,1)
        if not (characterLoc[0] in goldLoc or characterLoc[0] in pitLoc or characterLoc[0] in wumpusLoc):
            tmpFlag = False

    return goldLoc,pitLoc,wumpusLoc,characterLoc, gameRef[difficulty][0]
#====================================================================================



#=====================================================================================
def main():

#Initialization of the Game
    myFilePath = getcwd() + "\\"
    
    userDifficulty = startMenu()                                    
    
    xMove = 0
    yMove = 0
    score = 100
    click = 0
    

    done = False # Game over flag

    grdSz = 400 # Grid Size

    gameBoard = GraphWin("Hunt the Wumpus", grdSz, grdSz)
    gameBoard.setBackground("dark grey")


    
#============================================================================
# Creation of the Gameboard

    if userDifficulty == "Easy":
        numSqr = 8
        difficultyIndex = 0
    elif userDifficulty == "Medium":
        numSqr = 9
        difficultyIndex = 1
    elif userDifficulty == "Hard":
        numSqr = 10
        difficultyIndex = 2

    sqrSz = grdSz/numSqr
    for x in range(1,numSqr):
        line = Line(Point(sqrSz * x, 0),Point(sqrSz * x, grdSz))
        line.draw(gameBoard)
        line = Line(Point(0, sqrSz * x),Point(grdSz, sqrSz * x))
        line.draw(gameBoard)
#============================================================================


#============================================================================
# Creation of the control menu for the user to use
# To-Do: Creation of the firing of the arrows menu
    controlWin = GraphWin("Controls",200,600)

#   While these buttons are horribly designed, it will be fixed after I have turned in the working project

    movementUp = Rectangle(Point(75,10),Point(125,60))      
    movementDown = Rectangle(Point(75,70),Point(125,120))   
    movementRight = Rectangle(Point(75,130),Point(125,180)) 
    movementLeft = Rectangle(Point(75,190),Point(125,240))  
    controlButton = Rectangle(Point(75,250),Point(125,300)) 
    quitButton = Rectangle(Point(75,310),Point(125,360))

    movementUp.draw(controlWin)         
    movementDown.draw(controlWin)
    movementRight.draw(controlWin)
    movementLeft.draw(controlWin)
    quitButton.draw(controlWin)


    textUp = Text(Point(100,35),"Up")
    textDown = Text(Point(100,95),"Down")
    textRight = Text(Point(100,155),"Right")
    textLeft = Text(Point(100,215),"Left")
    textScore = Text(Point(100,415),"Score: " + str(score))
    textControl = Text(Point(100,275),"M")
    textArrow = Text(Point(100,450),"")
    textQuit = Text(Point(100,335),"Quit")
    textArrowStatus = Text(Point(100,500),"")
    
    textUp.draw(controlWin)
    textDown.draw(controlWin)
    textRight.draw(controlWin)
    textLeft.draw(controlWin)
    textScore.draw(controlWin)
    textControl.draw(controlWin)
    textArrow.draw(controlWin)
    textQuit.draw(controlWin)
    textArrowStatus.draw(controlWin)
#============================================================================

#============================================================================

    goldLocation, pitLocation, wumpusLocation, characterLocation, numOfarrows = randomPlacement(difficultyIndex)
    textArrow.setText("Arrows: " + str(numOfarrows))
    wumpusAlive = [True,True]
    wumpusDead = [False,False]
    
    adjLst = [[0,-1],[0,1],[-1,0],[1,0]]

    visitLoc = []
    for x in range(10):
        tmpLst = []
        for y in range(10):
            tmpLst.append(False)
        visitLoc.append(tmpLst)

    chrC = Circle(Point((characterLocation[0][0]+.5)*sqrSz,(characterLocation[0][1]+.5)*sqrSz),sqrSz*.15)
    chrC.setFill("blue")
    chrC.draw(gameBoard)
    try:
        while not done:
            uMC = controlWin.getMouse()
            if myRectPtCheck(controlButton,uMC):
                if textControl.getText() == "M":
                    textControl.setText("F")
                elif textControl.getText() == ("F"):
                    textControl.setText("M")
            else:
                modX, modY = 0, 0
                if myRectPtCheck(movementUp, uMC): modY = -1
                if myRectPtCheck(movementDown, uMC): modY = 1
                if myRectPtCheck(movementLeft, uMC): modX = -1
                if myRectPtCheck(movementRight, uMC): modX = 1
                if textControl.getText() == "M":
                    if modX or modY:
                        score -= 1
                        futureX = int(characterLocation[0][0] + modX)
                        futureY = int(characterLocation[0][1] + modY)
                        if futureX < 0 or futureY < 0 or futureX > numSqr-1 or futureY> numSqr-1:
                            score-=1
                        else:
                            characterLocation[0] = [futureX, futureY]

                            if visitLoc[futureX][futureY]:
                                if characterLocation[0] in pitLocation:
                                    score -= 10

                                if characterLocation[0] in wumpusLocation:
                                    pos = wumpusLocation.index([futureX, futureY])
                                    if wumpusAlive[pos]:
                                        score -= 1000
                                    elif wumpusDead[pos] == False:
                                        score += 500
                                        wumpusDead[pos] = True
                                    
                            else:
                                visitLoc[futureX][futureY] =  True
                                if characterLocation[0] in pitLocation:
                                    tmpC = Circle(Point((futureX+.5)*sqrSz,(futureY+.5)*sqrSz),sqrSz*.45)
                                    tmpC.setFill("black")
                                    tmpC.draw(gameBoard)
                                    score -= 10

                                if characterLocation[0] in wumpusLocation:
                                    tmpC = Circle(Point((futureX+.5)*sqrSz,(futureY+.5)*sqrSz),sqrSz*.35)
                                    tmpC.setFill("red")
                                    tmpC.draw(gameBoard)
                                    pos = wumpusLocation.index([futureX, futureY])

                                    if wumpusAlive[pos]:
                                        score -= 1000
                                    elif wumpusDead[pos] == False:
                                        score += 500
      
                                if characterLocation[0] in goldLocation:
                                    tmpC = Circle(Point((futureX+.5)*sqrSz,(futureY+.5)*sqrSz),sqrSz*.25)
                                    tmpC.setFill("yellow")
                                    tmpC.draw(gameBoard)
                                    score += 100

                                pFlag, gFlag, wFlag = False, False, False
                                pTxt, gTxt, wTxt = "-","-","-"

                                for tmpAdj in adjLst:
                                    tmpLoc = [futureX + tmpAdj[0], futureY + tmpAdj[1]]
                                    if tmpLoc in pitLocation: pFlag = True
                                    if tmpLoc in goldLocation: gFlag = True
                                    if tmpLoc in wumpusLocation: wFlag = True
                                
                                if pFlag: pTxt = "P"
                                if gFlag: gTxt = "G"
                                if wFlag: wTxt = "W"
                                sTxt = pTxt+gTxt+wTxt
                                tmpText = Text(Point((futureX+.5)*sqrSz,(futureY+.1)*sqrSz), sTxt)
                                tmpText.setSize(16 - numSqr)
                                tmpText.setTextColor("white")
                                tmpText.draw(gameBoard)
                                    
                            chrC.undraw()
                            chrC = Circle(Point((futureX+.5)*sqrSz,(futureY+.5)*sqrSz),sqrSz*.15)
                            chrC.setFill("blue")
                            chrC.draw(gameBoard)
                        textScore.setText(score)
                else:
                    if (modX or modY) and numOfarrows:
                        numOfarrows -= 1
                        score -= 5
                        arrowResult = 0
                        hX, hY = characterLocation[0][0],characterLocation[0][1]
                        startX,stopX,incX = hX, hX + 1, 1
                        startY,stopY,incY = hY,hY + 1, 1
                        
                        if modX < 0: stopX,incX = -1,-1
                        if modX > 0: stopX = numSqr
                        if modY < 0: stopY,incY = -1,-1
                        if modY > 0: stopY = numSqr
                        
                        for tX in range(startX, stopX, incX):
                            for tY in range(startY,stopY,incY):
                                if [tX,tY] in wumpusLocation and not arrowResult:
                                    pos = wumpusLocation.index([tX,tY])
                                    if wumpusAlive[pos]:
                                        wumpusAlive[pos] = False
                                        arrowResult = 1
                                    else:
                                        arrowResult = 2
                        if arrowResult == 0:
                            textArrowStatus.setText("Thunk")
                        elif arrowResult == 1:
                            textArrowStatus.setText("Scream")
                        else:
                            textArrowStatus.setText("Plop")
                        textScore.setText(score)
                        textArrow.setText("Arrows: " + str(numOfarrows))
                if myRectPtCheck(quitButton,uMC) == True:
                    gameBoard.close()
                    controlWin.close()
                    print(score)
    except:
        initials = initialsMenu()

        
        readFile = open(myFilePath + "highScores.txt",'r')
        scoreList = readFile.readlines()
        readFile.close()
        print(scoreList)
        scoreInfo = []
        same = False
        
        for i in scoreList:
            tmpInfo = i[:-1].split(",")
            tmpInfo[0] = eval(tmpInfo[0])
            if tmpInfo[1] == initials:
                same = True
                if tmpInfo[0] < score:
                    tmpInfo[0] = score
                    
            scoreInfo.append(tmpInfo)
            
        if not same:
            tmpInfo =  [score,initials,userDifficulty]
            scoreInfo.append(tmpInfo)

        scoreInfo.sort()
        scoreInfo.reverse()

        if len(scoreInfo) > 10:
            scoreInfo.pop()
        
        inFile = open(myFilePath + "highScores.txt",'w')

        for i in scoreInfo:
                print(i[0],i[1],i[2], sep = ',', file = inFile)

        
                
        inFile.close()
        n = 1

        sTxt = "Rank Score Init Diff\n" + "-" *20 + "\n"

        for i in scoreInfo:
            sTxt += "{0:2} {1:5} {2:3} {3:6}\n".format(n,i[0],i[1],i[2])
            n += 1

        
        scoreMenu = GraphWin("High Scores",220,240)
        scores = Text(Point(110,130),sTxt)
        scores.setFace('courier')        
        scores.draw(scoreMenu)

                    
    return

main()