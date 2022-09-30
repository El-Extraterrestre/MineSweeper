from random import randint

#class for the Minesweeper solver
class MSSolver():
    #constructor takes the custom events, 
    def __init__(self, field, pg, inputevent, commandevent):
        self.field = field
        self.pg = pg
        self.INPUTEVENT = inputevent
        self.COMMANDEVENT = commandevent
        self.colum = len(field)
        self.row = len(field[0])
        self.clickedSet = set()

    #requests a update from Minesweeper
    def update(self):
        cEvent = self.pg.event.Event(self.COMMANDEVENT, {"cmd":"update"})
        self.pg.event.post(cEvent)

    #sends a Click command
    def sendBtn(self, cell, btn):
        mEvent = self.pg.event.Event(self.INPUTEVENT, {"cell":cell, "btn":btn})
        self.pg.event.post(mEvent)
        self.update()

    #searches the biggest number on the field
    def maxNum(self):
        maxN = 0
        for x in range(self.colum):
            for y in range(self.row):
                if self.field[x][y] > maxN:
                    maxN = self.field[x][y]
        return maxN

    #get a dict of the cells neighboring
    #todo the dict doesnt need to be this big
    def getSourrounding(self, cell):
        around = {-2:[], -1:[], 0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[]}
        x,y = cell
        if x > 0:
            around[self.field[x-1][y]].append((x-1,y))
            if y > 0:
                around[self.field[x-1][y-1]].append((x-1,y-1))
            if y < self.row-1:
                around[self.field[x-1][y+1]].append((x-1,y+1))
        if x < self.colum-1:
            around[self.field[x+1][y]].append((x+1,y))
            if y > 0:
                around[self.field[x+1][y-1]].append((x+1,y-1))
            if y < self.row-1:
                around[self.field[x+1][y+1]].append((x+1,y+1))
        if y > 0:
            around[self.field[x][y-1]].append((x,y-1))
        if y < self.row-1:
            around[self.field[x][y+1]].append((x,y+1))
        return around


    #looks for the next step, wether logical or random
    def nextStep(self):
        maxCellNum = self.maxNum()
        cellNum = 1

        #starts with 1-8 if nothing works than random
        clicked = False
        while(cellNum <= maxCellNum):
            cells, btn = self.findSingleOne(cellNum)
            if cells:
                for cell in cells:
                    self.sendBtn(cell, btn)
                    cellNum = 1
                clicked = True
                break
            else:
                cellNum += 1
            

        if not clicked:
            allCells = set([x for x in range(self.colum * self.row)])
            allCells.difference_update(self.clickedSet)
            leftCells = list(allCells)
            cellPoint = leftCells[randint(0, len(leftCells)-1)]
            cell = (cellPoint%self.colum, cellPoint//self.colum)
            print(cellPoint)
            print(cell)
            self.sendBtn(cell, 1)

    #get the next logic step, for a cell Number
    def findSingleOne(self, cellNum):
        for x in range(self.colum):
            for y in range(self.row):
                if self.field[x][y] == cellNum:
                    neighbourCells = self.getSourrounding((x,y))
                    if len(neighbourCells[-2]) + len(neighbourCells[-1]) == cellNum:
                        if len(neighbourCells[-2]) > 0:
                            return neighbourCells[-2], 3
                    if len(neighbourCells[-1]) == cellNum and len(neighbourCells[-2]) > 0:
                        return neighbourCells[-2], 1
        return None, -1