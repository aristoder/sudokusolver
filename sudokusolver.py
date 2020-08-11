import time
animationsleeptime=0.7

class puzzle:
    def __init__(self, *cells):
        if len(cells) != 81:
            raise ValueError
        self.puzzle={}
        for row_index in range(9):
            row={}
            for column_index in range(9):
                data=cells[(row_index*9) + column_index]
                # might remove the first "if"
                if data==" ":
                    data=0
                if data>=0 and data<=9:
                    celltobeadded=cell(hline=row_index+1, vline=column_index+1, block=((int(row_index/3)*3) + int(column_index/3)) + 1, confirmed=data)
                row[column_index + 1]=celltobeadded
            self.puzzle[row_index + 1]=row

    def checkhline(self, hline, arg):
        for column_index in range(1,10):
            if self.puzzle[hline][column_index].confirmed==arg:
                break
        else:
            # arg not found
            return False
        # arg found
        return True
            
    def checkvline(self, vline, arg):
        for row_index in range(1,10):
            if self.puzzle[row_index][vline].confirmed==arg:
                break
        else:
            # arg not found
            return False
        # arg found
        return True

    def checkblock(self, block, arg):
        for row_index in range(1,10):
            for column_index in range(1,10):
                cell_obj=self.puzzle[row_index][column_index]
                if cell_obj.block==block:
                    if cell_obj.confirmed==arg:
                        return True
        return False

    def issolved(self):
        for hline in range(1,10):
            for vline in range(1,10):
                if self.puzzle[hline][vline].confirmed == 0:
                    return False
        else:
            return True

    def print(self, toclear=True):
        if toclear:
            import os
            os.system("clear")
        for row_index in range(1,10):
            if row_index == 1 or row_index == 4 or row_index == 7:
                self.printlineforsudoku()
            for column_index in range(1,10):
                if column_index == 1:
                    print("| ", end="")
                elif column_index == 4 or column_index == 7:
                    print("| ", end="")
                value=self.puzzle[row_index][column_index].confirmed
                if value==0:
                    value = " "
                print(value, end=" ")
            print("|")
        self.printlineforsudoku()
    
    def printlineforsudoku(self, length=12, character=chr(0x2015)):
        for i in range(length):
            print(character, end=character)
        print(character)

    def solvebyhline(self, animate=False):
        pass

    def solvebyvline(self, animate=False):
        pass

    def solveparticularhline(self, hline, animate=False):
        pass

    def solveparticularvline(self, vline, animate=False):
        pass

    def solvebyblock(self, animate=False):
        pass

    def solveparticularblock(self, animate=False):
        pass

    def solvebypossibility(self, animate=False):
        flag=True
        nothingchange=True
        while flag:
            anythingchangedinthisloop=False
            for hline in range(1,10):
                for vline in range(1,10):
                    self.fillpossible(hline=hline, vline=vline)
            for hline in range(1,10):
                for vline in range(1,10):
                    if self.puzzle[hline][vline].confirmed == 0:
                        if self.puzzle[hline][vline].converge():
                            anythingchangedinthisloop=True
                            nothingchange=False
            if anythingchangedinthisloop:
                if animate:
                    time.sleep(animationsleeptime)
                    self.print()
            else:
                flag = False
        if nothingchange:
            return False
        else:
            return True

    def solve(self, animate=False):
        while self.issolved() == False:
            progress=self.solvebypossibility(animate=animate)
            if progress:
                if animate:
                    time.sleep(animationsleeptime)
                    self.print()
            progress=self.solvebyhline(animate=animate)
            if progress:
                if animate:
                    time.sleep(animationsleeptime)
                    self.print()
            progress=self.solvebyvline(animate=animate)
            if progress:
                if animate:
                    time.sleep(animationsleeptime)
                    self.print()
            progress=self.solvebyblock(animate=animate)
            if progress:
                if animate:
                    time.sleep(animationsleeptime)
                    self.print()

    def fillpossible(self, hline, vline):
        if self.puzzle[hline][vline].confirmed != 0:
            return
        else:
            self.puzzle[hline][vline].clear()
        for checked_number in range(1,10):
            if self.checkhline(hline=hline, arg=checked_number):
                continue
            if self.checkvline(vline=vline, arg=checked_number):
                continue
            if self.checkblock(block=self.puzzle[hline][vline].block, arg=checked_number):
                continue
            self.puzzle[hline][vline].add(checked_number)


class cell:
    def __init__(self, hline, vline, block, confirmed=0, possible=[]):
        self.confirmed=confirmed
        self.possible=possible
        self.hline=hline
        self.vline=vline
        self.block=block

    def add(self,arg):
        self.possible.append(arg)

    def clear(self):
        self.possible=[]
    
    def remove(self, arg):
        if arg in self.possible:
            self.possible.remove(arg)

    def converge(self):
        if len(self.possible) == 1:
            self.confirmed=self.possible[0]
            self.clear()
            return self.confirmed
        else:
            return False


ot = [2,7,6,3,1,4,9,5,8,8,5,4,9,6,2,7,1,3,9,1,3,8,7,5,2,6,4,4,6,8,1,2,7,3,9,5,5,9,7,4,3,8,6,2,1,1,3,2,5,9,6,4,8,7,3,2,5,7,8,9,1,4,6,6,4,1,2,5,3,8,7,9,7,8,9,6,4,1,5,3,2]
it = [2,7,6,3,1,4,0,5,8,8,5,4,9,6,2,7,1,3,9,1,3,8,7,5,2,6,0,4,6,8,1,2,7,3,9,5,5,9,7,4,3,8,6,0,1,1,3,2,5,9,6,4,0,7,3,2,5,7,8,9,1,4,6,6,4,1,2,5,3,8,7,9,7,8,9,6,4,1,5,3,2]
nt = [0,0,0,0,0,3,6,0,0,0,0,0,0,2,0,0,0,0,0,3,9,8,0,0,0,0,1,9,0,0,0,4,0,0,0,3,3,4,0,6,0,2,0,8,0,0,6,0,0,1,0,9,0,0,0,8,0,0,0,0,2,0,0,0,5,6,1,3,0,4,0,0,4,0,0,0,8,7,0,0,0]
t=puzzle(*nt)
t.print()
input("Press enter to solve")
t.solve(animate=True)