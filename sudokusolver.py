import time
from os import system
# animationsleeptime=0.3

class puzzle:
    def __init__(self, *cells, recursivecount=0, recursivelimit=2, gui=False):
        if len(cells) != 81:
            raise ValueError
        self.puzzle={}
        self.recursivecount=recursivecount
        self.recursivelimit=recursivelimit
        if gui:
            pass
        else:
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

    def debugcheck(self):
        for hline in range(1,10):
            print("Row", hline, ":")
            for vline in range(1,10):
                temp=self.puzzle[hline][vline]
                print(vline, ":", temp.confirmed, "\t",*temp.possible)
            print("")

    def presentinhline(self, hline, arg):
        for column_index in range(1,10):
            if self.puzzle[hline][column_index].confirmed==arg:
                break
        else:
            # arg not found
            return False
        # arg found
        return True
            
    def presentinvline(self, vline, arg):
        for row_index in range(1,10):
            if self.puzzle[row_index][vline].confirmed==arg:
                break
        else:
            # arg not found
            return False
        # arg found
        return True

    def checkifright(self):
        return True

    def export(self):
        returndata=[]
        for hline in range(1,10):
            for vline in range(1,10):
                returndata.append(self.puzzle[hline][vline].confirmed)
        return returndata

    def clearall(self):
        for hline in range(1,10):
            for vline in range(1,10):
                self.puzzle[hline][vline].clear()

    def presentinblock(self, block, arg):
        for row_index in range(1,10):
            for column_index in range(1,10):
                cell_obj=self.puzzle[row_index][column_index]
                if cell_obj.block==block:
                    if cell_obj.confirmed==arg:
                        return True
        return False

    def notsolved(self):
        return not self.issolved()

    def solvebyguessing(self):
        if self.recursivecount == 0:
            for recursivelimit in range(2,10):
                self.recursivelimit=recursivelimit
                solved=self.solverecursivly()
                if solved:
                    return True
        else:
            return self.solverecursivly()
        return False

    def solverecursivly(self):
        if self.recursivecount>=self.recursivelimit:
            return False
        for hline in range(1,10):
            for vline in range(1,10):
                if self.puzzle[hline][vline].confirmed==0:
                    for checked_number in range(1,10):
                        if not self.presentinblock(block=self.puzzle[hline][vline].block, arg=checked_number) and not self.presentinhline(hline=hline, arg=checked_number) and not self.presentinvline(vline=vline, arg=checked_number):
                            logtext=str(self.recursivecount)+" guessing [" + str(hline) + "][" + str(vline) + "]\tChecked number:" + str(checked_number)
                            command="echo " + logtext + " >> logfile.txt"
                            system(command)
                            newpuzzle=puzzle(*self.export(), recursivecount=(self.recursivecount+1), recursivelimit=self.recursivelimit)
                            newpuzzle.puzzle[hline][vline].confirmed=checked_number
                            newpuzzle.print()
                            if self.recursivecount > 4:
                                print(self.recursivelimit)
                                input()
                            f=open("logfile.txt")
                            print(f.read())
                            solved=newpuzzle.solve(printatlast=False, animationsleeptime=0)
                            if solved:
                                for hline in range(1,10):
                                    for vline in range(1,10):
                                        self.puzzle[hline][vline].confirmed=newpuzzle.puzzle[hline][vline].confirmed
                                return True

    def issolved(self):
        for hline in range(1,10):
            for vline in range(1,10):
                if self.puzzle[hline][vline].confirmed == 0:
                    return False
        else:
            return True

    def print(self, toclear=True, printtofile=False, filename=None):
        if toclear:
            system("clear")
        if printtofile:
            if filename==None:
                raise FileNotFoundError
            f=open(filename,"w")
            for row_index in range(1,10):
                line=""
                if row_index==1 or row_index==4 or row_index==7:
                    f.write(self.printlineforsudoku(returnback=True)+"\n")
                for column_index in range(1,10):
                    if column_index==1 or column_index==4 or column_index==7:
                        line+="| "
                    if self.puzzle[row_index][column_index].confirmed==0:
                        line+="  "
                    else:
                        line+=str(self.puzzle[row_index][column_index].confirmed)+" "
                line+="|"
                f.write(line+"\n")
            f.write(self.printlineforsudoku(returnback=True)+"\n")
            f.close()
        else:
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
    
    def printlineforsudoku(self, length=25, character=chr(0x2015), returnback=False):
        texttoprint=""
        for i in range(length):
            texttoprint=texttoprint+character
        if returnback:
            return texttoprint
        else:
            print(texttoprint)

    def solvebyhline(self, animate=False, animationsleeptime=0.3):
        anychange=False
        for hline in range(1,10):
            for checked_number in range(1,10):
                if self.presentinhline(hline,checked_number):
                    continue
                else:
                    self.clearall()
                    positionofpossibilities=[]
                    for vline in range(1,10):
                        if self.puzzle[hline][vline].confirmed == 0:
                            if self.presentinvline(vline, checked_number):
                                continue
                            if self.presentinblock(self.puzzle[hline][vline].block, checked_number):
                                continue
                            self.puzzle[hline][vline].add(checked_number)
                            positionofpossibilities.append(vline)
                    if len(positionofpossibilities) == 1:
                        self.puzzle[hline][positionofpossibilities[0]].converge()
                        if animate:
                            time.sleep(animationsleeptime)
                            self.print()
                        anychange=True
        return anychange

    def solvebyvline(self, animate=False, animationsleeptime=0.3):
        anychange=False
        for vline in range(1,10):
            for checked_number in range(1,10):
                if self.presentinvline(vline,checked_number):
                    continue
                else:
                    self.clearall()
                    positionofpossibilities=[]
                    for hline in range(1,10):
                        if self.puzzle[hline][vline].confirmed == 0:
                            if self.presentinhline(hline, checked_number):
                                continue
                            if self.presentinblock(self.puzzle[hline][vline].block, checked_number):
                                continue
                            self.puzzle[hline][vline].add(checked_number)
                            positionofpossibilities.append(hline)
                    if len(positionofpossibilities) == 1:
                        self.puzzle[positionofpossibilities[0]][vline].converge()
                        if animate:
                            time.sleep(animationsleeptime)
                            self.print()
                        anychange=True
        return anychange

    def solveparticularhline(self, hline, animate=False):
        pass

    def solveparticularvline(self, vline, animate=False):
        pass

    def solvebyblock(self, animate=False, animationsleeptime=0.3):
        anychange=False
        for block in range(1,10):
            # checking for each number
            for checked_number in range(1,10):
                if self.presentinblock(block=block, arg=checked_number):
                    continue            # already present
                else:
                    self.clearall()     # prep
                    positionofpossibilities=[]
                    for hline in range(1,10):
                        for vline in range(1,10):
                            if self.puzzle[hline][vline].block==block:
                                if self.puzzle[hline][vline].confirmed==0:
                                    if self.presentinhline(hline=hline, arg=checked_number):
                                        continue
                                    if self.presentinvline(vline=vline, arg=checked_number):
                                        continue
                                    self.puzzle[hline][vline].add(checked_number)
                                    positionofpossibilities.append({"hline":hline, "vline":vline})
                    if len(positionofpossibilities)==1:
                        anychange=True
                        self.puzzle[positionofpossibilities[0]["hline"]][positionofpossibilities[0]["vline"]].converge()
                        if animate:
                            time.sleep(animationsleeptime)
                            self.print()
        return anychange

    def solveparticularblock(self, animate=False):
        pass

    def solvebypossibility(self, animate=False):
        self.clearall()
        flag=True
        nothingchange=True
        while flag:
            anythingchangedinthisloop=False
            # loop to fill all possibilities
            for hline in range(1,10):
                for vline in range(1,10):
                    self.fillpossible(hline=hline, vline=vline)
            # loop to check all the possibilities, and if singular->fill
            for hline in range(1,10):
                for vline in range(1,10):
                    if self.puzzle[hline][vline].confirmed == 0:
                        if bool(self.puzzle[hline][vline].converge()):
                            if animate:
                                time.sleep(animationsleeptime)
                                self.print()
                            anythingchangedinthisloop=True
                            nothingchange=False
                    else:
                        continue
            if anythingchangedinthisloop:
                pass
            else:
                flag = False
        if nothingchange:
            return False
        else:
            return True

    def solve(self, animate=False, logoutput=False, animationsleeptime=0.3, printatlast=True):
        if self.recursivecount==0:
            system("rm logfile.txt")
        notsolved=True
        flag=False
        while notsolved:
            anythingchanged=False
            # solve by horizontal line
            progress=self.solvebyhline(animate=animate, animationsleeptime=animationsleeptime)
            if progress:
                anythingchanged=True
                if animate:
                    self.print()
            # sovle by vertical line
            progress=self.solvebyvline(animate=animate, animationsleeptime=animationsleeptime)
            if progress:
                anythingchanged=True
                if animate:
                    self.print()
            # solve by block
            progress=self.solvebyblock(animate=animate, animationsleeptime=animationsleeptime)
            if progress:
                anythingchanged=True
                if animate:
                    self.print()
                    time.sleep(animationsleeptime)
            if anythingchanged:
                pass
            else:
                notsolved=self.notsolved()  # break if solved
                if flag:                    # stays off the first time
                    progress=self.solvebyguessing()
                    if progress:
                        anythingchanged=True
                        if animate:
                            self.print()
                            time.sleep(animationsleeptime)
                    else:
                        clearlogfile("logfile.txt", pre=(self.recursivecount)-1)
                        break
                    pass
                flag=True                   # flags that it wasn't solved the last time too
        if printatlast:
            self.print()
        if notsolved:
            if logoutput:
                print("Either there has been an error or the given sudoku had logical fallacies.")
                input("")
            return False
        else:
            self.print()
            print("Sudoku solved!")
            return True

    def fillpossible(self, hline, vline):
        if self.puzzle[hline][vline].confirmed != 0:
            self.puzzle[hline][vline].clear()
            return
        else:
            self.puzzle[hline][vline].clear()
        for checked_number in range(1,10):
            if self.presentinhline(hline=hline, arg=checked_number):
                continue
            if self.presentinvline(vline=vline, arg=checked_number):
                continue
            if self.presentinblock(block=self.puzzle[hline][vline].block, arg=checked_number):
                continue
            self.puzzle[hline][vline].add(checked_number)

def clearlogfile(filename, pre):
    tempfile=".tempfile.txt"
    system("tail -n 1 " + filename + " > .tempfile.txt")
    File=open(tempfile)
    # input("Stop.."+str(pre))
    if int(File.read().split()[0])==int(pre):
        system("cat " + filename+" | head -n -1 > " + tempfile)
        system("rm "+filename)
        system("mv "+tempfile+ " "+filename)
    # input("Stop..")
    

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
        if self.confirmed == 0:
            if len(self.possible) == 1:
                self.confirmed=self.possible[0]
                self.clear()
                return True
            else:
                return False
        else:
            return False

et = [0,0,0,0,0,3,6,0,0,0,0,0,0,2,0,0,0,0,0,3,9,8,0,0,0,0,1,9,0,0,0,4,0,0,0,3,3,4,0,6,0,2,0,8,0,0,6,0,0,1,0,9,0,0,0,8,0,0,0,0,2,0,0,0,5,6,1,3,0,4,0,0,4,0,0,0,8,7,0,0,0]
mt = [0,0,0,3,0,0,0,0,0,0,0,5,0,0,0,0,0,6,0,9,0,6,0,4,8,1,7,5,0,6,9,0,0,0,0,0,0,0,0,0,0,3,0,0,5,0,0,1,0,2,0,4,0,0,0,0,9,0,0,7,0,3,2,0,0,7,0,0,0,5,6,0,0,6,2,0,8,0,7,0,0]
ht = [0,0,5,0,0,0,9,0,0,0,0,4,6,9,0,1,0,0,7,9,0,0,0,0,0,0,0,0,1,0,2,0,0,0,0,3,0,7,0,0,0,6,0,8,0,0,0,0,0,1,4,6,0,2,2,3,0,0,0,8,0,0,0,0,0,0,0,5,0,0,0,7,0,0,0,4,0,3,0,1,0]
if __name__ == "__main__":
    t=puzzle(*ht)
    t.print()
    input("Press enter to solve")
    t.print()
    t.solve(animate=True, logoutput=True)