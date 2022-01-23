'''
FAZA I

reprezentacija stanja:
([dimenzijeTable],{pocetnePozicije},{pozicijePesaka},{pozicijeZidova},(preostaliZidovi),{putanje})
([x,y],{"X1":(x,y),"X2":(x,y),"O1":(x,y),"O2":(x,y)},{"X1":(x,y),"X2":(x,y),"O1":(x,y),"O2":(x,y)},{(x,y):"Z|P"},([<preostaliZeleni>,<preostaliPlavi>],[<preostaliZeleni>,<preostaliPlavi>]),{putanje})
'''
import os
import math
import copy
import bisect
import threading

numberConversion=('1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S')
sampleState=([11, 14], {"X1": (3, 3), "X2": (7, 3), "O1": (3, 10), "O2": (7, 10)}, {"X1": (0, 0), "X2": (10, 0), "O1": (0, 13), "O2": (10, 13)}, {(3,2):"Z",(5,1):"Z",(5,2):"Z",(3,3):"Z",(2,3):"P",(6,3):"P",(7,3):"P",(6,4):"Z",(3,9):"Z",(6,9):"Z",(2,10):"P",(7,10):"P"}, ([0, 0], [0, 0]),{"X1": {"O1":[],"O2":[]}, "X2": {"O1":[],"O2":[]}, "O1": {"X1":[],"X2":[]}, "O2": {"X1":[],"X2":[]}})

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def isEnd(state):

    if state[2]["X1"] == state[1]["O1"] or state[2]["X1"] == state[1]["O2"]:
        return "X"
    if state[2]["X2"] == state[1]["O1"] or state[2]["X2"] == state[1]["O2"]:
        return "X"
    if state[2]["O1"] == state[1]["X1"] or state[2]["O1"] == state[1]["X2"]:
        return "O"
    if state[2]["O2"] == state[1]["X1"] or state[2]["O2"] == state[1]["X2"]:
        return "O"
    return False

def gameParamInput():
    try:
        val=input("Da li zelite podrazumevane parametre partije (11x14 tabla) (y/n)?")
        if val=="y" or val=="":
            
            x=11
            y=14
            brZidova=9
            xx1=4
            xy1=4
            xx2=8
            xy2=4
            ox1=4
            oy1=11
            ox2=8
            oy2=11
            '''
            x=5
            y=6
            brZidova=9
            xx1=1
            xy1=1
            xx2=5
            xy2=1
            ox1=1
            oy1=6
            ox2=5
            oy2=6
            '''
            
        else:   
            x,y=input("Unesite dimenzije table (x,y): ").split(",")
            x=int(x)
            y=int(y)
            if  x>22  or y>28:
                print("Tabla moze biti dimenzija do 22x28!")
                raise Exception()
            if x%2==0 or y%2!=0:
                print("Broj vrsti mora biti neparan, a kolona paran!")
                raise Exception()
            brZidova=int(input("Unesite broj zidova: "))
            if brZidova>18 or brZidova<0:
                print("Broj zidova moze biti 0-18")
                raise Exception()
            xx1,xy1=input("Unesite prvo pocetno polje X igraca (x,y): ").split(",")
            xx1=int(xx1)
            xy1=int(xy1)
            if xx1>x or xx1<1 or xy1>y or xy1<1:
                print("Polje se mora nalaziti unutar table!")
                raise Exception()
            xx2,xy2=input("Unesite drugo pocetno polje X igraca (x,y): ").split(",")
            xx2=int(xx2)
            xy2=int(xy2)
            if xx2>x or xx2<1 or xy2>y or xy2<1:
                print("Polje se mora nalaziti unutar table!")
                raise Exception()
            if xx2==xx1 and xy1==xy2:
                print("Startna polja se ne mogu preklapati!")
                raise Exception()
            ox1,oy1=input("Unesite prvo pocetno polje O igraca (x,y): ").split(",")
            ox1=int(ox1)
            oy1=int(oy1)
            if ox1>x or ox1<1 or oy1>y or oy1<1:
                print("Polje se mora nalaziti unutar table!")
                raise Exception()
            if (xx2==ox1 and oy1==xy2) or (xx1==ox1 and oy1==xy1):
                print("Startna polja se ne mogu preklapati!")
                raise Exception()
            ox2,oy2=input("Unesite drugo pocetno polje O igraca (x,y): ").split(",")
            ox2=int(ox2)
            oy2=int(oy2)
            if ox2>x or ox2<1 or oy2>y or oy2<1:
                print("Polje se mora nalaziti unutar table!")
                raise Exception()
            if (xx2==ox2 and oy2==xy2) or (xx1==ox2 and oy2==xy1) or (ox1==ox2 and oy2==oy1):
                print("Startna polja se ne mogu preklapati!")
                raise Exception()
        val=input("Da li zelite da igrate prvi (y/n)? ")
        if val=="y" or val=="":
            isAIFirst=False
        elif val=="n":
            isAIFirst=True
        else:
            raise Exception()
        startGame(x,y,brZidova,xx1-1,xy1-1,xx2-1,xy2-1,ox1-1,oy1-1,ox2-1,oy2-1,isAIFirst)
        val=input("Da li zelite da igrate ponovo (y/n)? ")
        if val=="y" or val=="":
            gameParamInput()
    except:
        print("Nevalidan unos!")
        gameParamInput()

def printMarkedBoard(state, marks):
    cls()
    printval="  "
    for i in range(0,state[0][1]):
        printval+=str(numberConversion[i])
        printval+=" "
    print(printval)
    printval="  "
    for i in range(1,state[0][1]+1):
        printval+="="
        printval+=" "
    print(printval)
    for i in range(0,state[0][0]):
        printField=str(numberConversion[i])
        printField+= "ǁ"
        printWall="  "
        for j in range(0,state[0][1]):
            if (i,j) in marks:
                printField+="J"
            elif state[2]["X1"]==(i,j) or state[2]["X2"]==(i,j):
                printField+="X"
            elif state[2]["O1"]==(i,j) or state[2]["O2"]==(i,j):
                printField+="O"
            elif state[1]["X1"]==(i,j) or state[1]["X2"]==(i,j):
                printField+="x"
            elif state[1]["O1"]==(i,j) or state[1]["O2"]==(i,j):
                printField+="o"
            else:
                printField+=" "
            
            if (i>0 and (i-1,j) in state[3].keys() and state[3][(i-1,j)]=="Z") or ((i,j) in state[3].keys() and state[3][(i,j)]=="Z") or j==state[0][1]-1:
                printField+="ǁ"
            else:
                printField+="|"
            
            if(j>0 and (i,j-1) in state[3].keys() and state[3][(i,j-1)]=="P") or ((i,j) in state[3].keys() and state[3][(i,j)]=="P") or i==state[0][0]-1:
                printWall+="="
            else:
                printWall+="-"
            
            printWall+=" "
        print(printField)
        print(printWall)

def printBoard(state):
    cls()
    printval="  "
    for i in range(0,state[0][1]):
        printval+=str(numberConversion[i])
        printval+=" "
    print(printval)
    printval="  "
    for i in range(1,state[0][1]+1):
        printval+="="
        printval+=" "
    print(printval)
    for i in range(0,state[0][0]):
        printField=str(numberConversion[i])
        printField+= "ǁ"
        printWall="  "
        for j in range(0,state[0][1]):
            if state[2]["X1"]==(i,j) or state[2]["X2"]==(i,j):
                printField+="X"
            elif state[2]["O1"]==(i,j) or state[2]["O2"]==(i,j):
                printField+="O"
            elif state[1]["X1"]==(i,j) or state[1]["X2"]==(i,j):
                printField+="x"
            elif state[1]["O1"]==(i,j) or state[1]["O2"]==(i,j):
                printField+="o"
            else:
                printField+=" "
            
            if (i>0 and (i-1,j) in state[3].keys() and state[3][(i-1,j)]=="Z") or ((i,j) in state[3].keys() and state[3][(i,j)]=="Z") or j==state[0][1]-1:
                printField+="ǁ"
            else:
                printField+="|"
            
            if(j>0 and (i,j-1) in state[3].keys() and state[3][(i,j-1)]=="P") or ((i,j) in state[3].keys() and state[3][(i,j)]=="P") or i==state[0][0]-1:
                printWall+="="
            else:
                printWall+="-"
            
            printWall+=" "
        print(printField)
        print(printWall)

def inputMove(state,isX):
    try:
        pawn=str()
        if isX:
            pawn = input("Unesite ime figure(X1,X2): ")
            if not (pawn == "X1" or pawn == "X2"):
                print("Pogresna figura!")
                raise Exception()
        else:
            pawn = input("Unesite ime figure(O1,O2): ")
            if not (pawn == "O1" or pawn == "O2"):
                print("Pogresna figura!")
                raise Exception()
        x, y = input("Unesite polje (x,y): ").split(",")
        x = numberConversion.index(x)
        y = numberConversion.index(y)
        if not validatePawnMove(state,pawn,x,y):
            print("Nevalidan potez pijuna")
            raise Exception()
        newState=placePawn(pawn,(x,y),state)
        if (isX and newState[4][0]!= (0,0)) or (not isX and newState[4][1]!= (0,0)):
            color=input("Unesite boju zida (Z/P): ")
            xw, yw = input("Unesite polozaj zida (x,y): ").split(",")
            xw = numberConversion.index(xw)
            yw = numberConversion.index(yw)
            if not (color=="P" or color=="Z"):
                print("Nevalidna boja zida")
                raise Exception()
            if isX:
                if (color=="P" and newState[4][0][1]<=0) or (color=="Z" and newState[4][0][0]<=0):
                    print("Nemate preostalih zidova")
                    raise Exception()
            else:
                if (color=="P" and newState[4][1][1]<=0) or (color=="Z" and newState[4][1][0]<=0):
                    print("Nemate preostalih zidova")
                    raise Exception()
            if not validateWallPlacement(newState,color,xw,yw,isX):
                print("Nevalidan polozaj zida")
                raise Exception()
            return placeWall((xw,yw),color,newState,isX)
        return newState
    except:
        print("Nevalidan unos!")
        return inputMove(state,isX)

def startGame(x,y,brZidova,xx1,xy1,xx2,xy2,ox1,oy1,ox2,oy2,isAIFirst):
    minimaxDepth=3
    state = tuple()
    state = ([x, y], {"X1": (xx1, xy1), "X2": (xx2, xy2), "O1": (ox1, oy1), "O2": (ox2, oy2)}, {"X1": (xx1, xy1), "X2": (xx2, xy2), "O1": (ox1, oy1), "O2": (ox2, oy2)}, {}, ([brZidova, brZidova], [brZidova, brZidova]),{"X1": {"O1":[],"O2":[]}, "X2": {"O1":[],"O2":[]}, "O1": {"X1":[],"X2":[]}, "O2": {"X1":[],"X2":[]}})
    #state=sampleState
    state=recalculatePaths(state)
    print(len(possibleStates(state,True)))
    printBoard(state)
    if not isAIFirst:
        while not isEnd(state):
            state=inputMove(state,True)
            printBoard(state)

            if isEnd(state):
                print(isEnd(state)," je pobednik!")
                return

            #AI/drugi igrac igra potez
            state=minimax(state,minimaxDepth,isAIFirst)[0]
            printBoard(state)

        print(isEnd(state)," je pobednik!")
        return
    else:
        while not isEnd(state):
            #AI/drugi igrac igra potez
            state=minimax(state,minimaxDepth,isAIFirst)[0]
            printBoard(state)

            if isEnd(state):
                print(isEnd(state)," je pobednik!")
                return
            
            state=inputMove(state,False)
            #state=minimax(state,minimaxDepth,not isAIFirst)[0]
            printBoard(state)
        print(isEnd(state)," je pobednik!")
        return

def wallAt(state,color,x,y):
    if (x,y) in state[3].keys() and state[3][(x,y)]==color:
        return True
    return False

def pawnAt(state,x,y):
    if state[2]["X1"]==(x,y) or state[2]["X2"]==(x,y) or state[2]["O1"]==(x,y) or state[2]["O2"]==(x,y):
        return True
    return False

def validatePawnMove(state,pawn,x,y):
    #opseg table
    if x<0 or x>state[0][0]-1 or y<0 or y>state[0][1]-1:
        return False

    if(state[2][pawn][0]+2==x and state[2][pawn][1]==y):
        #dole 2
        if not (wallAt(state,"P",state[2][pawn][0],state[2][pawn][1]) or wallAt(state,"P",state[2][pawn][0]+1,state[2][pawn][1]) or wallAt(state,"P",state[2][pawn][0],state[2][pawn][1]-1) or wallAt(state,"P",state[2][pawn][0]+1,state[2][pawn][1]-1)):
            if not pawnAt(state, x,y) or ((pawn=="X1" or pawn=="X2") and (state[1]["O1"]==(x,y) or state[1]["O2"]==(x,y))) or ((pawn=="O1" or pawn=="O2")and (state[1]["X1"]==(x,y) or state[1]["X2"]==(x,y))):
                return True
              
    elif(state[2][pawn][0]-2==x and state[2][pawn][1]==y):
        #gore 2
        if not (wallAt(state,"P",state[2][pawn][0]-1,state[2][pawn][1]) or wallAt(state,"P",state[2][pawn][0]-2,state[2][pawn][1]) or wallAt(state,"P",state[2][pawn][0]-1,state[2][pawn][1]-1) or wallAt(state,"P",state[2][pawn][0]-2,state[2][pawn][1]-1)):
            if not pawnAt(state, x,y) or ((pawn=="X1" or pawn=="X2") and (state[1]["O1"]==(x,y) or state[1]["O2"]==(x,y))) or ((pawn=="O1" or pawn=="O2")and (state[1]["X1"]==(x,y) or state[1]["X2"]==(x,y))):
                return True
    
    elif(state[2][pawn][0]==x and state[2][pawn][1]+2==y):
        #desno 2
        if not (wallAt(state,"Z",state[2][pawn][0],state[2][pawn][1]) or wallAt(state,"Z",state[2][pawn][0],state[2][pawn][1]+1) or wallAt(state,"Z",state[2][pawn][0]-1,state[2][pawn][1]) or wallAt(state,"Z",state[2][pawn][0]-1,state[2][pawn][1]+1)):
            if not pawnAt(state, x,y) or ((pawn=="X1" or pawn=="X2") and (state[1]["O1"]==(x,y) or state[1]["O2"]==(x,y))) or ((pawn=="O1" or pawn=="O2")and (state[1]["X1"]==(x,y) or state[1]["X2"]==(x,y))):
                return True

    elif(state[2][pawn][0]==x and state[2][pawn][1]-2==y):
        #levo 2
        if not (wallAt(state,"Z",state[2][pawn][0],state[2][pawn][1]-1) or wallAt(state,"Z",state[2][pawn][0],state[2][pawn][1]-2) or wallAt(state,"Z",state[2][pawn][0]-1,state[2][pawn][1]-1) or wallAt(state,"Z",state[2][pawn][0]-1,state[2][pawn][1]-2)):
            if not pawnAt(state, x,y) or ((pawn=="X1" or pawn=="X2") and (state[1]["O1"]==(x,y) or state[1]["O2"]==(x,y))) or ((pawn=="O1" or pawn=="O2")and (state[1]["X1"]==(x,y) or state[1]["X2"]==(x,y))):
                return True

    elif(state[2][pawn][0]+1==x and state[2][pawn][1]+1==y):
        #dole desno
        if not (wallAt(state,"Z",state[2][pawn][0],state[2][pawn][1]) or wallAt(state,"P",state[2][pawn][0],state[2][pawn][1]) or (wallAt(state,"Z",state[2][pawn][0]-1,state[2][pawn][1]) and wallAt(state,"P",state[2][pawn][0],state[2][pawn][1]-1)) or (wallAt(state,"Z",state[2][pawn][0]+1,state[2][pawn][1]) and wallAt(state,"P",state[2][pawn][0],state[2][pawn][1]+1))or (wallAt(state,"Z",state[2][pawn][0]-1,state[2][pawn][1]) and wallAt(state,"Z",state[2][pawn][0]+1,state[2][pawn][1])) or (wallAt(state,"P",state[2][pawn][0],state[2][pawn][1]-2) and wallAt(state,"P",state[2][pawn][0],state[2][pawn][1]))):
            if not pawnAt(state, x,y) or ((pawn=="X1" or pawn=="X2") and (state[1]["O1"]==(x,y) or state[1]["O2"]==(x,y))) or ((pawn=="O1" or pawn=="O2")and (state[1]["X1"]==(x,y) or state[1]["X2"]==(x,y))):
                return True

    elif(state[2][pawn][0]+1==x and state[2][pawn][1]-1==y):
        #dole levo
        if not (wallAt(state,"Z",state[2][pawn][0],state[2][pawn][1]-1) or wallAt(state,"P",state[2][pawn][0],state[2][pawn][1]-1) or (wallAt(state,"Z",state[2][pawn][0]-1,state[2][pawn][1]-1) and wallAt(state,"P",state[2][pawn][0],state[2][pawn][1]-2)) or (wallAt(state,"Z",state[2][pawn][0]+1,state[2][pawn][1]-1) and wallAt(state,"P",state[2][pawn][0],state[2][pawn][1]-2))or (wallAt(state,"Z",state[2][pawn][0]-1,state[2][pawn][1]-1) and wallAt(state,"Z",state[2][pawn][0]+1,state[2][pawn][1])-1) or (wallAt(state,"P",state[2][pawn][0],state[2][pawn][1]-2) and wallAt(state,"P",state[2][pawn][0],state[2][pawn][1]))):
            if not pawnAt(state, x,y) or ((pawn=="X1" or pawn=="X2") and (state[1]["O1"]==(x,y) or state[1]["O2"]==(x,y))) or ((pawn=="O1" or pawn=="O2")and (state[1]["X1"]==(x,y) or state[1]["X2"]==(x,y))):
                return True

    elif(state[2][pawn][0]-1==x and state[2][pawn][1]+1==y):
        #gore desno
        if not (wallAt(state,"Z",state[2][pawn][0]-1,state[2][pawn][1]) or wallAt(state,"P",state[2][pawn][0]-1,state[2][pawn][1]) or (wallAt(state,"Z",state[2][pawn][0],state[2][pawn][1]) and wallAt(state,"P",state[2][pawn][0]-1,state[2][pawn][1]-2)) or (wallAt(state,"Z",state[2][pawn][0]-2,state[2][pawn][1]) and wallAt(state,"P",state[2][pawn][0]-1,state[2][pawn][1]+1)) or (wallAt(state,"Z",state[2][pawn][0]-2,state[2][pawn][1]) and wallAt(state,"Z",state[2][pawn][0],state[2][pawn][1])) or (wallAt(state,"P",state[2][pawn][0]-1,state[2][pawn][1]-1) and wallAt(state,"P",state[2][pawn][0]-1,state[2][pawn][1]+1))):
            if not pawnAt(state, x,y) or ((pawn=="X1" or pawn=="X2") and (state[1]["O1"]==(x,y) or state[1]["O2"]==(x,y))) or ((pawn=="O1" or pawn=="O2")and (state[1]["X1"]==(x,y) or state[1]["X2"]==(x,y))):
                return True

    elif(state[2][pawn][0]-1==x and state[2][pawn][1]-1==y):
        #gore levo
        if not (wallAt(state,"Z",state[2][pawn][0]-1,state[2][pawn][1]-1) or wallAt(state,"P",state[2][pawn][0]-1,state[2][pawn][1]-1) or (wallAt(state,"Z",state[2][pawn][0],state[2][pawn][1]-1) and wallAt(state,"P",state[2][pawn][0]-1,state[2][pawn][1])) or (wallAt(state,"Z",state[2][pawn][0]-2,state[2][pawn][1]-1) and wallAt(state,"P",state[2][pawn][0]-1,state[2][pawn][1]-2)) or (wallAt(state,"Z",state[2][pawn][0]-2,state[2][pawn][1]-1) and wallAt(state,"Z",state[2][pawn][0],state[2][pawn][1]-1))or (wallAt(state,"P",state[2][pawn][0]-1,state[2][pawn][1]-2) and wallAt(state,"P",state[2][pawn][0]-1,state[2][pawn][1]))):
            if not pawnAt(state, x,y) or ((pawn=="X1" or pawn=="X2") and (state[1]["O1"]==(x,y) or state[1]["O2"]==(x,y))) or ((pawn=="O1" or pawn=="O2")and (state[1]["X1"]==(x,y) or state[1]["X2"]==(x,y))):
                return True

    elif(state[2][pawn][0]-1==x and state[2][pawn][1]==y):
        #gore1
        if not (wallAt(state,"P",state[2][pawn][0]-1,state[2][pawn][1]) or wallAt(state,"P",state[2][pawn][0]-1,state[2][pawn][1]-1)):
            if pawnAt(state, x-1,y)  or ((pawn=="X1" or pawn=="X2") and (state[1]["O1"]==(x,y) or state[1]["O2"]==(x,y))) or ((pawn=="O1" or pawn=="O2")and (state[1]["X1"]==(x,y) or state[1]["X2"]==(x,y))):
                return True
    elif(state[2][pawn][0]+1==x and state[2][pawn][1]==y):
        #dole1
        if not (wallAt(state,"P",state[2][pawn][0],state[2][pawn][1]) or wallAt(state,"P",state[2][pawn][0],state[2][pawn][1]-1)):
            if pawnAt(state, x+1,y) or ((pawn=="X1" or pawn=="X2") and (state[1]["O1"]==(x,y) or state[1]["O2"]==(x,y))) or ((pawn=="O1" or pawn=="O2")and (state[1]["X1"]==(x,y) or state[1]["X2"]==(x,y))) :
                return True
    elif(state[2][pawn][0]==x and state[2][pawn][1]+1==y):
        #desno 1
        if not (wallAt(state,"Z",state[2][pawn][0],state[2][pawn][1]) or wallAt(state,"Z",state[2][pawn][0]-1,state[2][pawn][1])):
            if pawnAt(state, x,y+1)  or ((pawn=="X1" or pawn=="X2") and (state[1]["O1"]==(x,y) or state[1]["O2"]==(x,y))) or ((pawn=="O1" or pawn=="O2")and (state[1]["X1"]==(x,y) or state[1]["X2"]==(x,y))):
                return True
    elif(state[2][pawn][0]==x and state[2][pawn][1]-1==y):
        #levo 1
        if not (wallAt(state,"Z",state[2][pawn][0],state[2][pawn][1]-1)  or wallAt(state,"Z",state[2][pawn][0]-1,state[2][pawn][1]-1)):
            if pawnAt(state, x,y-1)  or ((pawn=="X1" or pawn=="X2") and (state[1]["O1"]==(x,y) or state[1]["O2"]==(x,y))) or ((pawn=="O1" or pawn=="O2")and (state[1]["X1"]==(x,y) or state[1]["X2"]==(x,y))):
                return True
    return False

'''
FAZA II
'''
def connectedToWalls(state,wallPos,wallColor):
    walls=list()
    if wallColor=="Z":

        nPosition=(wallPos[0]-2,wallPos[1])
        if nPosition in state[3].keys() and state[3][nPosition]=="Z":
            walls.append((nPosition,"Z"))

        nPosition=(wallPos[0]+2,wallPos[1])
        if nPosition in state[3].keys() and state[3][nPosition]=="Z":
            walls.append((nPosition,"Z"))
            
        nPosition=(wallPos[0]-1,wallPos[1]-1)
        if nPosition in state[3].keys() and state[3][nPosition]=="P":
            walls.append((nPosition,"P"))
                    
        nPosition=(wallPos[0]-1,wallPos[1])
        if nPosition in state[3].keys() and state[3][nPosition]=="P":
            walls.append((nPosition,"P"))
                    
        nPosition=(wallPos[0]-1,wallPos[1]+1)
        if nPosition in state[3].keys() and state[3][nPosition]=="P":
            walls.append((nPosition,"P"))
                    
        nPosition=(wallPos[0]+1,wallPos[1]-1)
        if nPosition in state[3].keys() and state[3][nPosition]=="P":
            walls.append((nPosition,"P"))
                    
        nPosition=(wallPos[0]+1,wallPos[1])
        if nPosition in state[3].keys() and state[3][nPosition]=="P":
            walls.append((nPosition,"P"))
                    
        nPosition=(wallPos[0]+1,wallPos[1]+1)
        if nPosition in state[3].keys() and state[3][nPosition]=="P":
            walls.append((nPosition,"P"))
        
        nPosition=(wallPos[0],wallPos[1]-1)
        if nPosition in state[3].keys() and state[3][nPosition]=="P":
            walls.append((nPosition,"P"))
        
        nPosition=(wallPos[0],wallPos[1]+1)
        if nPosition in state[3].keys() and state[3][nPosition]=="P":
            walls.append((nPosition,"P"))

    elif wallColor=="P":

        nPosition=(wallPos[0],wallPos[1]-2)
        if nPosition in state[3].keys() and state[3][nPosition]=="P":
            walls.append((nPosition,"P"))

        nPosition=(wallPos[0],wallPos[1]+2)
        if nPosition in state[3].keys() and state[3][nPosition]=="P":
            walls.append((nPosition,"P"))

        nPosition=(wallPos[0]-1,wallPos[1]-1)
        if nPosition in state[3].keys() and state[3][nPosition]=="Z":
            walls.append((nPosition,"Z"))

        nPosition=(wallPos[0],wallPos[1]-1)
        if nPosition in state[3].keys() and state[3][nPosition]=="Z":
            walls.append((nPosition,"Z"))
        
        nPosition=(wallPos[0]+1,wallPos[1]-1)
        if nPosition in state[3].keys() and state[3][nPosition]=="Z":
            walls.append((nPosition,"Z"))
        
        nPosition=(wallPos[0]-1,wallPos[1]+1)
        if nPosition in state[3].keys() and state[3][nPosition]=="Z":
            walls.append((nPosition,"Z"))
        
        nPosition=(wallPos[0],wallPos[1]+1)
        if nPosition in state[3].keys() and state[3][nPosition]=="Z":
            walls.append((nPosition,"Z"))
        
        nPosition=(wallPos[0]+1,wallPos[1]+1)
        if nPosition in state[3].keys() and state[3][nPosition]=="Z":
            walls.append((nPosition,"Z"))

        nPosition=(wallPos[0]+1,wallPos[1])
        if nPosition in state[3].keys() and state[3][nPosition]=="Z":
            walls.append((nPosition,"Z"))
        
        nPosition=(wallPos[0]-1,wallPos[1])
        if nPosition in state[3].keys() and state[3][nPosition]=="Z":
            walls.append((nPosition,"Z"))
    
    return walls

def isBorderConnected(state,wallPos,wallColor):
    if wallColor=="Z":
        if wallPos[0]==0 or wallPos[0]==state[0][0]-2:
            return True
    elif wallColor=="P":
        if wallPos[1]==0 or wallPos[1]==state[0][1]-2:
            return True
    return False

def checkEnclosure(state, wallPos, wallColor, path, pathConnected):
    if not path:
        path=list()
        path.append((wallPos,wallColor))
        tmpState=placeWall(wallPos,wallColor,state,False)
        if not tmpState:
            tmpState=placeWall(wallPos,wallColor,state,True)
    else:
        tmpState=state
    nWalls=connectedToWalls(tmpState,wallPos,wallColor)

    for wall in nWalls:
        if wall == path[0] and len(path)>3:
            #loop zidova pronadjen
            return True
        if pathConnected and not wall == path[0]:
            #put povezan sa krajem ili sa ogranicavajucim zidovima
            if isBorderConnected(tmpState,wall[0],wall[1]):
                return True

    for wall in nWalls:
        if wall not in path and (len(path)<2 or wall not in connectedToWalls(tmpState,path[-2][0],path[-2][1])):
            if isBorderConnected(tmpState,wall[0],wall[1]):
                newPath=copy.deepcopy(path)
                newPath.append(wall)
                inversePath=newPath[::-1]
                if checkEnclosure(tmpState,path[-1][0],path[-1][1],inversePath,True):
                    return True
            else:
                newPath=copy.deepcopy(path)
                newPath.append(wall)
                if checkEnclosure(tmpState,wall[0],wall[1],newPath,pathConnected):
                    return True
    return False


def possibleMoves(state,pawn,position):
    fields=list()
    tmpState=copy.deepcopy(state)
    tmpState[2][pawn]=position
    field=list(position)
    field[0]-=2
    if validatePawnMove(tmpState,pawn,field[0],field[1]):
        fields.append(tuple(field))
    field[0]+=1
    field[1]+=1
    if validatePawnMove(tmpState,pawn,field[0],field[1]):
        fields.append(tuple(field))
    field[1]-=2
    if validatePawnMove(tmpState,pawn,field[0],field[1]):
        fields.append(tuple(field))
    field[0]+=1
    field[1]-=1
    if validatePawnMove(tmpState,pawn,field[0],field[1]):
        fields.append(tuple(field))
    field[1]+=4
    if validatePawnMove(tmpState,pawn,field[0],field[1]):
        fields.append(tuple(field))
    field[0]+=1
    field[1]-=1
    if validatePawnMove(tmpState,pawn,field[0],field[1]):
        fields.append(tuple(field))
    field[1]-=2
    if validatePawnMove(tmpState,pawn,field[0],field[1]):
        fields.append(tuple(field))
    field[0]+=1
    field[1]+=1
    if validatePawnMove(tmpState,pawn,field[0],field[1]):
        fields.append(tuple(field))

    if validatePawnMove(tmpState,pawn,position[0]+1,position[1]):
        fields.append((position[0]+1,position[1]))
    if validatePawnMove(tmpState,pawn,position[0]-1,position[1]):
        fields.append((position[0]-1,position[1]))
    if validatePawnMove(tmpState,pawn,position[0],position[1]+1):
        fields.append((position[0],position[1]+1))
    if validatePawnMove(tmpState,pawn,position[0],position[1]-1):
        fields.append((position[0],position[1]-1))
    
    return fields

def pathHeuristics(origin: tuple, dest: tuple):
    return int(math.sqrt((origin[0]-dest[0])**2 + (origin[1]-dest[1])**2)*10)

def pathFind(state, start: tuple, end: tuple):
    pawn=str()
    if state[2]["X1"]==start:
        pawn="X1"
    if state[2]["X2"]==start:
        pawn="X2"
    if state[2]["O1"]==start:
        pawn="O1"
    if state[2]["O2"]==start:
        pawn="O2"
    
    found_end = False
    open_set = set()
    open_set.add(start)
    closed_set = set()
    g = {}
    prev_nodes = {}
    g[start] = 0
    prev_nodes[start] = None
    while len(open_set) > 0 and (not found_end):
        node = None
        for next_node in open_set:
            if node is None or g[next_node] + pathHeuristics(next_node,end) < g[node] + pathHeuristics(node,end):
                node = next_node
        if node == end:
            found_end = True
            break
        for m in possibleMoves(state,pawn,node):
            if m not in open_set and m not in closed_set:
                open_set.add(m)
                prev_nodes[m] = node
                g[m] = g[node] + 20
            else:
                if g[m] > g[node] + 20:
                    g[m] = g[node] + 20
                    prev_nodes[m] = node
                    if m in closed_set:
                        closed_set.remove(m)
                        open_set.add(m)
        open_set.remove(node)
        closed_set.add(node)
    path = []
    if found_end:
        prev = end
        while prev_nodes[prev] is not None:
            path.append(prev)
            prev = prev_nodes[prev]
        path.append(start)
        path.reverse()
    return path

def recalculatePaths(oldState):
    state=copy.deepcopy(oldState)
    if state[5]["X1"]["O1"] and state[5]["X1"]["O1"][0]!=-1:
        state[5]["X1"]["O1"]=[-1,pathFind(state,state[2]["X1"],state[1]["O1"])[1:]]
        state[5]["X1"]["O2"]=[-1,pathFind(state,state[2]["X1"],state[1]["O2"])[1:]]
        state[5]["X2"]["O1"]=[-1,pathFind(state,state[2]["X2"],state[1]["O1"])[1:]]
        state[5]["X2"]["O2"]=[-1,pathFind(state,state[2]["X2"],state[1]["O2"])[1:]]
        state[5]["O1"]["X1"]=[-1,pathFind(state,state[2]["O1"],state[1]["X1"])[1:]]
        state[5]["O1"]["X2"]=[-1,pathFind(state,state[2]["O1"],state[1]["X2"])[1:]]
        state[5]["O2"]["X1"]=[-1,pathFind(state,state[2]["O2"],state[1]["X1"])[1:]]
        state[5]["O2"]["X2"]=[-1,pathFind(state,state[2]["O2"],state[1]["X2"])[1:]]
    else:
        state[5]["X1"]["O1"]=[0,pathFind(state,state[2]["X1"],state[1]["O1"])[1:]]
        state[5]["X1"]["O2"]=[0,pathFind(state,state[2]["X1"],state[1]["O2"])[1:]]
        state[5]["X2"]["O1"]=[0,pathFind(state,state[2]["X2"],state[1]["O1"])[1:]]
        state[5]["X2"]["O2"]=[0,pathFind(state,state[2]["X2"],state[1]["O2"])[1:]]
        state[5]["O1"]["X1"]=[0,pathFind(state,state[2]["O1"],state[1]["X1"])[1:]]
        state[5]["O1"]["X2"]=[0,pathFind(state,state[2]["O1"],state[1]["X2"])[1:]]
        state[5]["O2"]["X1"]=[0,pathFind(state,state[2]["O2"],state[1]["X1"])[1:]]
        state[5]["O2"]["X2"]=[0,pathFind(state,state[2]["O2"],state[1]["X2"])[1:]]
    return state

def validateWallPlacement(state,color,x,y,isX):
    
    potentialState=placeWall((x,y),color,state,isX)

    if isX:
        if not ((state[4][0][0]>0 and color=="Z") or (state[4][0][1]>0 and color=="P")):
            return False
    else:
        if not ((state[4][1][0]>0 and color=="Z") or (state[4][1][1]>0 and color=="P")):
            return False
    
    if not wallAt(state,"P",x,y) and not wallAt(state,"Z",x,y):
        if color=="P":
            if not wallAt(state,"P",x,y-1) and not  wallAt(state,"P",x,y+1):
                if checkEnclosure(potentialState,(x,y),color,False,isBorderConnected(potentialState,(x,y),color)):
                    return validatePaths(potentialState)
                return True
        if color=="Z":
            if not wallAt(state,"Z",x-1,y) and not wallAt(state,"Z",x+1,y):
                if checkEnclosure(potentialState,(x,y),color,False,isBorderConnected(potentialState,(x,y),color)):
                    return validatePaths(potentialState)
                return True
    return False

def placePawn(pawn: str,field : tuple, state):
    newState=copy.deepcopy(state)
    if pawn=="X1" or pawn=="X2":
        newState[5][pawn]["O1"][1].insert(0,state[2][pawn])
        newState[5][pawn]["O2"][1].insert(0,state[2][pawn])
    else:
        newState[5][pawn]["X1"][1].insert(0,state[2][pawn])
        newState[5][pawn]["X2"][1].insert(0,state[2][pawn])
    newState[2][pawn] = field
    return newState

def placeWall(wall : tuple, wallColor:str, state, isX: bool):
    newState=copy.deepcopy(state)
    if isX:
        if wallColor=="Z":
            newState[4][0][0]-=1
        else:
            newState[4][0][1]-=1
    else:
        if wallColor=="Z":
            newState[4][1][0]-=1
        else:
            newState[4][1][1]-=1
    newState[3][wall] = wallColor
    return newState

def game():
    gameParamInput()
    


'''
FAZA III
'''
def possibleWalls(state, isX):
    walls=list()
    dist=1
    lineDist=1
    positions=set()
    #oko kucice
    #oko protivnika
    for x in range(-dist,dist):
        for y in range(-dist,dist):
            if isX:
                pos=state[2]["O1"]
                positions.add((pos[0]+x,pos[1]+y))
                pos=state[2]["O2"]
                positions.add((pos[0]+x,pos[1]+y))
                pos=state[1]["X1"]
                positions.add((pos[0]+x,pos[1]+y))
                pos=state[1]["X2"]
                positions.add((pos[0]+x,pos[1]+y))
            else:
                pos=state[1]["O1"]
                positions.add((pos[0]+x,pos[1]+y))
                pos=state[1]["O2"]
                positions.add((pos[0]+x,pos[1]+y))
                pos=state[2]["X1"]
                positions.add((pos[0]+x,pos[1]+y))
                pos=state[2]["X2"]
                positions.add((pos[0]+x,pos[1]+y))
    #linije
    
    lines=list()
    if isX:
        lines.append(getLine(state,state[2]["O1"],state[1]["X1"]))
        lines.append(getLine(state,state[2]["O1"],state[1]["X2"]))
        lines.append(getLine(state,state[2]["O2"],state[1]["X1"]))
        lines.append(getLine(state,state[2]["O2"],state[1]["X2"]))
    else:
        lines.append(getLine(state,state[1]["O1"],state[2]["X1"]))
        lines.append(getLine(state,state[1]["O1"],state[2]["X2"]))
        lines.append(getLine(state,state[1]["O2"],state[2]["X1"]))
        lines.append(getLine(state,state[1]["O2"],state[2]["X2"]))
    
    lines.sort(key=len)
    for l in lines[:1]:
        for pos in l:
            for x in range(-lineDist,lineDist):
                for y in range(-lineDist,lineDist):
                    positions.add((pos[0]+x,pos[1]+y))

    for pos in positions:
        if not checkEnclosure(state,pos,"Z",False,isBorderConnected(state,pos,"Z")):
            if validateWallPlacement(state,"Z",pos[0],pos[1],isX):
                walls.append(((pos[0],pos[1]),"Z"))
        if not checkEnclosure(state,pos,"P",False,isBorderConnected(state,pos,"P")):
            if validateWallPlacement(state,"P",pos[0],pos[1],isX):
                walls.append(((pos[0],pos[1]),"P"))
            
    return walls

    
    '''
    for x in range(0,state[0][0]):
        for y in range(0,state[0][1]):
            if validateWallPlacement(state,"P",x,y,isX):
                walls.append(((x,y),"P"))
    '''        
    return walls

def possibleStates(state, isX):
    count=10
    bestValues=list()
    pawnCount=3
    withThreading=False
    states=list()
    threads=list()
    walls=possibleWalls(state,isX)
    if(state[4][0][0]+state[4][0][1]+state[4][1][0]+state[4][1][1])==0:
        pawnCount=16
    if isX:
        moves=list()
        pawn1Moves=possibleMoves(state,"X1",state[2]["X1"])
        pawn2Moves=possibleMoves(state,"X2",state[2]["X2"])
        for move in pawn1Moves:
            tempState=copy.deepcopy(state)
            tempState=placePawn("X1",move,tempState)
            moves.append((move,evalState(tempState,isX)))
        for move in pawn2Moves:
            tempState=copy.deepcopy(state)
            tempState=placePawn("X2",move,tempState)
            moves.append((move,evalState(tempState,isX)))
        moves.sort(key=lambda x:x[1],reverse=True)

        for move in pawn1Moves:
            if move in [x[0] for x in moves[:pawnCount]]:
                if withThreading:
                    threads.append(threading.Thread(target=generateStates,args=(state,move,count,walls,"X1",isX,states,bestValues)))
                else:
                    generateStates(state,move,count,walls,"X1",isX,states,bestValues)
        for move in pawn2Moves:
            if move in [x[0] for x in moves[:pawnCount]]:
                if withThreading:
                    threads.append(threading.Thread(target=generateStates,args=(state,move,count,walls,"X2",isX,states,bestValues)))
                else:
                    generateStates(state,move,count,walls,"X2",isX,states,bestValues)
    else:
        moves=list()
        pawn1Moves=possibleMoves(state,"O1",state[2]["O1"])
        pawn2Moves=possibleMoves(state,"O2",state[2]["O2"])
        for move in pawn1Moves:
            tempState=copy.deepcopy(state)
            tempState=placePawn("O1",move,tempState)
            moves.append((move,evalState(tempState,isX)))
        for move in pawn2Moves:
            tempState=copy.deepcopy(state)
            tempState=placePawn("O2",move,tempState)
            moves.append((move,evalState(tempState,isX)))
        moves.sort(key=lambda x:x[1],reverse=False)
        for move in pawn1Moves:
            if move in [x[0] for x in moves[:pawnCount]]:
                if withThreading:
                    threads.append(threading.Thread(target=generateStates,args=(state,move,count,walls,"O1",isX,states,bestValues)))
                else:
                    generateStates(state,move,count,walls,"O1",isX,states,bestValues)
        for move in pawn2Moves:
            if move in [x[0] for x in moves[:pawnCount]]:
                if withThreading:
                    threads.append(threading.Thread(target=generateStates,args=(state,move,count,walls,"O2",isX,states,bestValues)))
                else:
                    generateStates(state,move,count,walls,"O2",isX,states,bestValues)

    if withThreading:
        for t in threads:
            t.start()
        for t in threads:
            t.join()
    
    retVal=list()
    for s in states:
        if isX:
            if s[1]>=bestValues[0]:
                retVal.append(s)
        else:
            if s[1]<=bestValues[-1]:
                retVal.append(s)
    return retVal

def minimax(state, depth, isX):
    if(state[4][0][0]+state[4][0][1]+state[4][1][0]+state[4][1][1])==0:
        state=recalculatePaths(state)
    alpha=(state,-math.inf)
    beta=(state,math.inf)
    #x je uvek max player
    if isX:
        retVal=max_value(alpha, depth, alpha, beta)
        return retVal
    else:
        retVal=min_value(beta, depth, alpha, beta)
        return retVal

def max_value(state, depth, alpha, beta):
    if depth == 0:
        #return (state, evalState(state,True))
        return state
    else:
        for s in possibleStates(state[0],True):
            best=min_value(s, depth - 1, alpha, beta)
            if(alpha[1]<best[1]):
                alpha=(s[0],best[1])
            if alpha[1] > beta[1]:
                return beta
    return alpha

def min_value(state, depth, alpha, beta):
    if depth == 0:
        #return (state, evalState(state,False))
        return state
    else:
        for s in possibleStates(state[0],False):
            best=max_value(s, depth - 1, alpha, beta)
            if(beta[1]>best[1]):
                beta=(s[0],best[1])
            if beta[1] < alpha[1]:
                return alpha
    return beta

'''
FAZA IV
'''
def generateStates(state,move,count,walls,pawn,isX,states,bestValues):
    tempState=copy.deepcopy(state)
    tempState=placePawn(pawn,move,tempState)
    if walls:
        for wall in walls:
            eval=evalState(placeWall(wall[0],wall[1],tempState,isX),isX)
            if len(states)>count-1:
                if isX:
                    if eval>bestValues[0]:
                        bisect.insort(bestValues,eval)
                        bestValues=bestValues[1:]
                        states.append((placeWall(wall[0],wall[1],tempState,isX),eval))
                else:
                    if eval<bestValues[-1]:
                        bisect.insort(bestValues,eval)
                        bestValues=bestValues[:-1]
                        states.append((placeWall(wall[0],wall[1],tempState,isX),eval))
            else:
                bisect.insort(bestValues,eval)
                states.append((placeWall(wall[0],wall[1],tempState,isX),eval))
    else:
        eval=evalState(state,isX)
        bisect.insort(bestValues,eval)
        states.append((tempState,eval))

def getLine(state,start,end):
    x1=start[0]
    y1=start[1]
    x2=end[0]
    y2=end[1]
    retval=list()
    x,y=x1,y1
    dx=abs(x2-x1)
    dy=abs(y2-y1)

    if dx==0:
        for y in range(y1,y2):
            retval.append((x1,y))
        return retval
    if dy==0:
        for x in range(x1,x2):
            retval.append((x,y1))
        return retval


    gradient=dy/float(dx)
    if gradient>1:
        dx,dy=dy,dx
        x,y=y,x
        x1,y1=y1,x1
        x2,y2=y2,x2
    
    p=2*dy-dx
    retval.append((x,y))
    for k in range(dx):
        if p>0:
            y=y+1 if y<y2 else y-1
            p=p+2*(dy-dx)
        else:
            p=p+2*dy
        
        x=x+1 if x<x2 else x-1

        retval.append((x,y))

    return retval

def validatePaths(state):
    for pawn in state[5]:
        for end in state[5][pawn]:
            tmp=copy.deepcopy(state)
            for jump in state[5][pawn][end][1]:
                if not validatePawnMove(tmp,pawn,jump[0],jump[1]):
                    newPath=pathFind(state,state[2][pawn],state[1][end])
                    if not newPath:
                        return False
                    state[5][pawn][end][1]=newPath
                    state[5][pawn][end][0]+=1
                else:
                    tmp=placePawn(pawn,(jump[0],jump[1]),tmp)
    return True

def evalState(state,isX):
    win=isEnd(state)
    if win=="X":
        return 1000000
    if win=="O":
        return -1000000

    retVal=0
    if validatePawnMove(state,"X1",state[1]["O1"][0],state[1]["O1"][1]) or validatePawnMove(state,"X1",state[1]["O2"][0],state[1]["O2"][1]) or validatePawnMove(state,"X2",state[1]["O1"][0],state[1]["O1"][1]) or validatePawnMove(state,"X2",state[1]["O2"][0],state[1]["O2"][1]):
        retVal +=500000
    if validatePawnMove(state,"O1",state[1]["X1"][0],state[1]["X1"][1]) or validatePawnMove(state,"O1",state[1]["X2"][0],state[1]["X2"][1])or validatePawnMove(state,"O2",state[1]["X1"][0],state[1]["X1"][1])or validatePawnMove(state,"O2",state[1]["X2"][0],state[1]["X2"][1]):
        retVal-=500000
    if retVal!=0:
        return retVal

    
    xPiun= 10000 - pathHeuristics(state[2]["X1"],state[1]["O1"])-pathHeuristics(state[2]["X1"],state[1]["O2"])-pathHeuristics(state[2]["X2"],state[1]["O1"])-pathHeuristics(state[2]["X2"],state[1]["O2"])
    oPiun= -10000 + pathHeuristics(state[2]["O1"],state[1]["X1"])+pathHeuristics(state[2]["O1"],state[1]["X2"])+pathHeuristics(state[2]["O2"],state[1]["X1"])+pathHeuristics(state[2]["O2"],state[1]["X2"])

    if state[5]["X1"]["O1"][0]==-1:
        xPaths=list()
        if state[2]["X1"] in state[5]["X1"]["O1"][1]:
            xPaths.append(len(state[5]["X1"]["O1"][1])-state[5]["X1"]["O1"][1].index(state[2]["X1"]))
        if state[2]["X1"] in state[5]["X1"]["O2"][1]:
            xPaths.append(len(state[5]["X1"]["O2"][1])-state[5]["X1"]["O2"][1].index(state[2]["X1"]))
        if state[2]["X2"] in state[5]["X2"]["O1"][1]:
            xPaths.append(len(state[5]["X2"]["O1"][1])-state[5]["X2"]["O1"][1].index(state[2]["X2"]))
        if state[2]["X2"] in state[5]["X2"]["O2"][1]:
            xPaths.append(len(state[5]["X2"]["O2"][1])-state[5]["X2"]["O2"][1].index(state[2]["X2"]))
        if xPaths:
            xPiun=100000-min(xPaths)*50
        oPaths=list()
        if state[2]["O1"] in state[5]["O1"]["X1"][1]:
            oPaths.append(len(state[5]["O1"]["X1"][1])-state[5]["O1"]["X1"][1].index(state[2]["O1"]))
        if state[2]["O1"] in state[5]["O1"]["X2"][1]:
            oPaths.append(len(state[5]["O1"]["X2"][1])-state[5]["O1"]["X2"][1].index(state[2]["O1"]))
        if state[2]["O2"] in state[5]["O2"]["X1"][1]:
            oPaths.append(len(state[5]["O2"]["X1"][1])-state[5]["O2"]["X1"][1].index(state[2]["O2"]))
        if state[2]["O2"] in state[5]["O2"]["X2"][1]:
            oPaths.append(len(state[5]["O2"]["X2"][1])-state[5]["O2"]["X2"][1].index(state[2]["O2"]))
        if oPaths:
            oPiun=-100000+min(oPaths)*50
        return xPiun+oPiun
        

    Lines=list()
    Lines.append(getLine(state,state[2]["X1"],state[1]["O1"]))
    Lines.append(getLine(state,state[2]["X2"],state[1]["O1"]))
    Lines.append(getLine(state,state[2]["X1"],state[1]["O2"]))
    Lines.append(getLine(state,state[2]["X2"],state[1]["O2"]))
    oZid= 0
    for line in Lines:
        for dot in line:
            if (wallAt(state,"Z",dot[0],dot[1]) and (line[0][0]-line[-1][0]) <= (line[0][1]-line[-1][1])) or (wallAt(state,"P",dot[0],dot[1]) and (line[0][0]-line[-1][0]) >= (line[0][1]-line[-1][1])):
                oZid-=min(pathHeuristics(dot,line[0]),pathHeuristics(dot,line[-1]))/(len(line)*10)

    Lines=list()
    Lines.append(getLine(state,state[1]["X1"],state[2]["O1"]))
    Lines.append(getLine(state,state[1]["X2"],state[2]["O1"]))
    Lines.append(getLine(state,state[1]["X1"],state[2]["O2"]))
    Lines.append(getLine(state,state[1]["X2"],state[2]["O2"]))
    xZid= 0
    for line in Lines:
        for dot in line:
            if (wallAt(state,"Z",dot[0],dot[1]) and (line[0][0]-line[-1][0]) <= (line[0][1]-line[-1][1])) or (wallAt(state,"P",dot[0],dot[1]) and (line[0][0]-line[-1][0]) >= (line[0][1]-line[-1][1])):
                xZid+=min(pathHeuristics(dot,line[0]),pathHeuristics(dot,line[-1]))/(len(line)*10)


    connected=0
    for wall in state[3]:
        connected+=len(connectedToWalls(state,wall,state[3][wall]))
    if isX:
        return xPiun+oPiun+xZid*3+oZid
    else:
        return xPiun+oPiun+oZid*3+xZid


game()
