import pygame,sys,time
from pygame.locals import *
from constants import *
from random import *


brd_size = 4
total_points = 0
default_score = 2




pygame.init()

bg = pygame.display.set_mode((400,500),0,32)
pygame.display.set_caption("game")

myfont = pygame.font.SysFont("monospace",40)
scorefont = pygame.font.SysFont("monospace",30)

tileMatrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
undoMat = []

def main(fromLoaded = False):
    
    if not fromLoaded:
        placeRandomTile()
        placeRandomTile()
    printMatrix()


    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if checkIfCanGo() == True:
                if event.type == KEYDOWN:
                    if isArrow(event.key):
                        rotations = getRotations(event.key)
                        addToUndo()
                        for i in range(0,rotations):
                            rotateMatrixClockwise()

                        if canMove():
                            moveTiles()
                            mergeTiles()
                            placeRandomTile()

                        for j in range(0,(4-rotations)%4):
                            rotateMatrixClockwise()
                            
                        printMatrix()
            else: # just checking wait
                printGameOver()

            if event.type == KEYDOWN:
                global brd_size

                if event.key == pygame.K_r:
                 
                    reset()
                if 50<event.key and 56 > event.key:
                    
                    brd_size = event.key - 48
                    reset()
                if event.key == pygame.K_s:
                   
                    saveGameState()
                elif event.key == pygame.K_l:
                    loadGameState()
                    
                elif event.key == pygame.K_u:
                    undo()
                   
        pygame.display.update()

#  This module helps to check if it is possible to move or not  

def canMove():
    for i in range(0,brd_size):
        for j in range(1,brd_size):
            if tileMatrix[i][j-1] == 0 and tileMatrix[i][j] > 0:
                return True 
            elif (tileMatrix[i][j-1] == tileMatrix[i][j]) and tileMatrix[i][j-1] != 0:
                return True
    return False

    # This module moves 
def moveTiles():
    for i in range(0,brd_size):
        for j in range(0,brd_size-1):
            
            while tileMatrix[i][j] == 0 and sum(tileMatrix[i][j:]) > 0:
                for k in range(j,brd_size-1):
                    tileMatrix[i][k] = tileMatrix[i][k+1]
                tileMatrix[i][brd_size-1] = 0


# This module is used for merging tiles

def mergeTiles():
    global total_points

    for i in range(0,brd_size):
        for k in range(0,brd_size-1):
            if tileMatrix[i][k] == tileMatrix[i][k+1] and tileMatrix[i][k] != 0:
                tileMatrix[i][k] = tileMatrix[i][k]*2
                tileMatrix[i][k+1] = 0 # this was not intailized so the k value was going out the range value so by this we ever we merge the files it assigns the present value to zero and merge the number with the ahead value 
                total_points += tileMatrix[i][k]
                moveTiles()


#  This module helps in getting a random tile 

def placeRandomTile():
    c = 0
    for i in range(0,brd_size):
        for j in range(0,brd_size):
            if tileMatrix[i][j] == 0:
                c += 1
    
    k = floor(random() * brd_size * brd_size)
    print("click")

    while tileMatrix[floor(k/brd_size)][k%brd_size] != 0:
        k = floor(random() * brd_size * brd_size)

    tileMatrix[floor(k/brd_size)][k%brd_size] = 2



#  This is used to get the floor value out of the given value to the module

def floor(n):
    return int(n - (n % 1 ))  

# This module is used to print the given matrix

def printMatrix():
        bg.fill(BLACK)
        global brd_size
        global total_points

        for i in range(0,brd_size):
            for j in range(0,brd_size):
                pygame.draw.rect(bg,getColor(tileMatrix[i][j]),(i*(400/brd_size),j*(400/brd_size)+100,400/brd_size,400/brd_size))
                label = myfont.render(str(tileMatrix[i][j]),1,(255,255,255))
                label2 = scorefont.render("YourScore:"+str(total_points),1,(255,255,255))
                bg.blit(label,(i*(400/brd_size)+30,j*(400/brd_size)+130))
                bg.blit(label2,(10,20))


# We can call this a checker module

def checkIfCanGo():
    for i in range(0,brd_size ** 2): 
        if tileMatrix[floor(i/brd_size)][i%brd_size] == 0:
            return True
    
    for i in range(0,brd_size):
        for j in range(0,brd_size-1):
            if tileMatrix[i][j] == tileMatrix[i][j+1]:
                return True
            elif tileMatrix[j][i] == tileMatrix[j+1][i]:
                return True
    return False

# This module returns a matrix rather than we can call it a list 

def convertToLinearMatrix():

    mat = []
    for i in range(0,brd_size ** 2):
        mat.append(tileMatrix[floor(i/brd_size)][i%brd_size])

    mat.append(total_points)
    return mat

#  This module is the main reason to make the covert linearn function 

def addToUndo():
    undoMat.append(convertToLinearMatrix())   

#  This module is used to mix up the matrix after a button/ move is done by the user

def rotateMatrixClockwise():
    for i in range(0,int(brd_size/2)):
        for k in range(i,brd_size- i- 1):
            temp1 = tileMatrix[i][k]
            temp2 = tileMatrix[brd_size - 1 - k][i]
            temp3 = tileMatrix[brd_size - 1 - i][brd_size - 1 - k]
            temp4 = tileMatrix[k][brd_size - 1 - i]

            tileMatrix[brd_size - 1 - k][i] = temp1
            tileMatrix[brd_size - 1 - i][brd_size - 1 - k] = temp2
            tileMatrix[k][brd_size - 1 - i] = temp3
            tileMatrix[i][k] = temp4

# When you dont have any place in the matrix or you are out of move then this module is called so it is in the else part of the main func

def printGameOver():
    global total_points

    bg.fill(BLACK)

    label = scorefont.render("GameOver!",1,(255,255,255))
    label2 = scorefont.render("Score : "+str(total_points),1,(255,255,255))
    label3 = myfont.render("press 'R' to play again!! ",1,(255,255,255))

    bg.blit(label,(50,100))
    bg.blit(label2,(50,200))
    bg.blit(label3,(50,300))

# This module is to reset matrix

def reset():
    global total_points
    global tileMatrix

    total_points = 0
    bg.fill(BLACK)
    tileMatrix = [[0 for i in range(0,brd_size)] for j in range(0,brd_size) ]
    main()

#  This module saves the state of moves

def saveGameState():
    f = open("savedata","w")

    line1 = " ".join([str(tileMatrix[floor(x/brd_size)][x%brd_size]) for x in range(0,brd_size ** 2)])
    f.write(line1+"\n")
    f.write(str(brd_size)+"\n")
    f.write(str(total_points))
    f.close

# This module is used to get the last move

def undo():
    if len(undoMat) > 0:
        mat = undoMat.pop()

        for i in range(0,brd_size ** 2):
            tileMatrix[floor(i/brd_size)][i%brd_size] = mat[i]
        global total_points 
        total_points  = mat[brd_size ** 2]

        printMatrix()

def loadGameState():
    global total_points
    global brd_size
    global tileMatrix

    f = open("savedata","r")

    mat = (f.readline()).split(' ',brd_size ** 2)
    brd_size = int(f.readline())
    total_points = int(f.readline())

    for i in range(0,brd_size ** 2):
        tileMatrix[floor(i/brd_size)][i%brd_size] = int(mat[i])

    f.close()

    main(True)


# This help you find the which arrow is clicked by the user
def isArrow(k):
    return (k == pygame.K_UP or k == pygame.K_DOWN or k == pygame.K_LEFT or k == pygame.K_RIGHT)

def getRotations(k):
    if k == pygame.K_UP:
        return 0
    elif k == pygame.K_DOWN:
        return 2 
    elif k == pygame.K_LEFT:
        return 1
    elif k == pygame.K_RIGHT:
        return 3


main()
