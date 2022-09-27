from csv import field_size_limit
import pygame as pg
from random import randint

cellSize = 50
bombsCount = 50

row, colum = 10, 15

borderRadius = int(cellSize/15)
gameOver = False
bombs = []
clearedBomb = 0
clearedField = 0

#-1 is a Bomb
field = [[0 for x in range(row)] for x in range(colum)]
maskField = [[0 for x in range(row)] for x in range(colum)]

def generateField(pg,scr):
    global field, maskField, row, colum, gameOver, bombs, clearedBomb, clearedField
    field = [[0 for x in range(row)] for x in range(colum)]
    maskField = [[0 for x in range(row)] for x in range(colum)]
    screen.fill((0,0,0))
    gameOver = False
    clearedBomb = 0
    clearedField = 0

    #Bomb generation
    tempBomb = [i for i in range(row*colum)]
    bombs.clear()
    for _ in range(bombsCount):
        bombs.append(tempBomb.pop(randint(0,len(tempBomb)-1)))
    for i in bombs:
        field[i % colum][i//colum] = -10
    
    #draw Playfield
    for i in range(colum):
        for j in range(row):
            drawCell((128,128,128), (i*cellSize, j*cellSize))
            if field[i][j] < 0:
                addNum(i,j)
                

def point2Cell(pos):
    return (int(pos[0]/cellSize), int(pos[1]/cellSize))

def cell2Point(pos):
    return (pos[0]*cellSize, pos[1]*cellSize)

#generate numberfield based on every input point
def addNum(x,y):
    global field, row, colum
    if x > 0:
        field[x-1][y] += 1
        if y > 0:
            field[x-1][y-1] += 1
        if y < row-1:
            field[x-1][y+1] += 1
    if x < colum-1:
        field[x+1][y] += 1
        if y > 0:
            field[x+1][y-1] += 1
        if y < row-1:
            field[x+1][y+1] += 1
    if y > 0:
        field[x][y-1] += 1
    if y < row-1:
        field[x][y+1] += 1

#recursivly open all neaboring cell which are 0
def clearZero(pg, scr, cell):
    global field, maskField, row, colum, cellSize, borderRadius, clearedField
    x,y = cell
    if maskField[x][y] == 0:
        maskField[x][y] = 1
        clearedField += 1
        drawCell((80,80,80), (x*cellSize, y*cellSize))
        if field[x][y] == 0:
            if x > 0:
                clearZero(pg, scr, (x-1,y))
                if y > 0:
                    clearZero(pg, scr, (x-1,y-1))
                if y < row-1:
                    clearZero(pg, scr, (x-1,y+1))
            if x < colum-1:
                clearZero(pg, scr, (x+1,y))
                if y > 0:
                    clearZero(pg, scr, (x+1,y-1))
                if y < row-1:
                    clearZero(pg, scr, (x+1,y+1))
            if y > 0:
                clearZero(pg, scr, (x,y-1))
            if y < row-1:
                clearZero(pg, scr, (x,y+1))
        else:
            drawNum(field[x][y], cell2Point(cell))
    else:
        return

def drawNum(cellNum, points):
    global font
    numSurface = font.render(str(cellNum), False, (255,255,255))
    screen.blit(numSurface,(points[0]+10, points[1]+10))

#based on cleared bombs and cleared Cell
def hasWon():
    global colum, clearedField, clearedBomb
    correctFlags = 0
    if clearedField + len(bombs) == colum * row:
        print("test")
        return True
    for pos in bombs:
        if maskField[pos%colum][pos//colum] == -1:
            correctFlags += 1
    if correctFlags == len(bombs) and correctFlags == clearedBomb:
        print(correctFlags)
        return True
    else:
        return False

def endScreen(text, color):
    global gameOver
    pg.draw.rect(screen, (200,200,200), (cellSize-1, cellSize*row/2-1, cellSize*11-2, cellSize*3-2), 0, borderRadius)
    textSurface = fontBig.render(text, False, color)
    screen.blit(textSurface,(cellSize+cellSize/5, cellSize*row/2))
    textSurface = font.render("Click to continue", False, (255,255,255))
    screen.blit(textSurface,(cellSize*3, cellSize*row/2+cellSize*2))
    gameOver = True

#draw a rounded cell
def drawCell(color, startPoints):
    pg.draw.rect(screen, color,(startPoints[0]-1, startPoints[1]-1, cellSize-2, cellSize-2),0,borderRadius)


#decide what happend based on the clicked cell
def unmaskCell(cell):
    global clearedField
    x, y = cell 
    mask = maskField[x][y]
    cellNum = field[x][y]
    points = cell2Point(cell)
    if mask != -1:
        if cellNum == 0:
            clearZero(pg, screen, cell)
        elif cellNum < 0:
            bombClicked()
        else:
            drawCell((80,80,80), points)
            drawNum(cellNum, points)
            maskField[x][y] = 1
            clearedField += 1
    if hasWon():
        endScreen("You Won!", (0,255,0))

#flag a cell as a bomb or unflag it
def flagBomb(cell):
    global clearedBomb
    x,y = cell
    mask = maskField[x][y]
    points = cell2Point(cell)
    if mask == 0:
        maskField[x][y] = -1
        drawCell((0,255,0), points)
        clearedBomb += 1
        if clearedBomb == len(bombs):
            if hasWon():
                endScreen("You Won!", (0,255,0))
    elif mask == -1:
        maskField[x][y] = 0
        drawCell((128,128,128), points)
        clearedBomb -= 1

#mark all bombs which are not flagged and draw endscreen
def bombClicked():
    for i in range(colum):
        for j in range(row):
            if field[i][j] < 0:
                points = cell2Point((i,j))
                drawCell((255,0,0), points)
    endScreen("game Over", (255,0,0))

pg.init()
pg.font.init()

#generate Font
font = pg.font.Font(pg.font.get_default_font(), int(0.75*cellSize))
fontBig = pg.font.Font(pg.font.get_default_font(), cellSize*2)
width, hight = cellSize * colum, cellSize * row
screen = pg.display.set_mode((width, hight))


generateField(pg,screen)
    

run = True
while(run):

    #event Handler Keyboard and Mouse
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                quit()
            if event.key == pg.K_N:
                #next steps
                pass
            if event.key == pg.K_A:
                #auto
                pass
        if event.type == pg.MOUSEBUTTONDOWN:
            if gameOver:
                generateField(pg,screen)
            else:
                cell = point2Cell(event.pos)
                #left mouse click
                if event.button == 1:
                    unmaskCell(cell)
                #right mouse click
                if event.button == 3:
                    flagBomb(cell)
    pg.display.flip()