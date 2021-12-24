'''
FAZA I

reprezentacija stanja:
([dimenzijeTable],{pocetnePozicije},{pozicijePesaka},{pozicijeZidova},(preostaliZidovi))
([x,y],{"X1":(x,y),"X2":(x,y),"O1":(x,y),"O2":(x,y)},{"X1":(x,y),"X2":(x,y),"O1":(x,y),"O2":(x,y)},{(x,y):"Z|P"},([<preostaliZeleni>,<preostaliPlavi>],[<preostaliZeleni>,<preostaliPlavi>]))
'''
import os
import math
import copy

numberConversion=(1,2,3,4,5,6,7,8,9,'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S')
sampleState=([11, 14], {"X1": (2, 2), "X2": (4, 2), "O1": (2, 8), "O2": (6, 8)}, {"X1": (2, 3), "X2": (4, 6), "O1": (2, 8), "O2": (6, 10)}, {(0,0):"Z",(3,3):"Z",(6,6):"P"}, ([10, 10], [10, 10]))

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
        x,y=input("Unesite dimenzije table (x,y): ").split(",")
        x=int(x)
        y=int(y)
        if x<11 or x>22 or y<14 or y>28:
            print("Tabla moze biti dimenzija od 11x14 do 22x28!")
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
        if val=="y":
            isAIFirst=False
        elif val=="n":
            isAIFirst=True
        else:
            raise Exception()
        startGame(x,y,brZidova,xx1,xy1,xx2,xy2,ox1,oy1,ox2,oy2,isAIFirst)
    except:
        print("Nevalidan unos!")
        gameParamInput()

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
    pawn=str()
    if isX:
        pawn = input("Unesite ime figure(X1,X2): ")
        if not (pawn == "X1" or pawn == "X2"):
            print("Pogresna figura!")
            return False
    else:
        pawn = input("Unesite ime figure(O1,O2): ")
        if not (pawn == "O1" or pawn == "O2"):
            print("Pogresna figura!")
            return False
    x, y = input("Unesite polje (x,y): ").split(",")
    x = int(x)-1
    y = int(y)-1
    if not validatePawnMove(state,pawn,x,y):
        print("Nevalidan potez pijuna")
        return False
    state=placePawn(pawn,(x,y),state)
    color, xw, yw = input("Unesite zid (color,x,y): ").split(",")
    xw = int(xw)-1
    yw = int(yw)-1
    if not (color=="P" or color=="Z"):
        print("Nevalidna boja zida")
        return False
    if not validateWallPlacement(state,color,xw,yw,isX):
        print("Nevalidan polozaj zida")
        return False
    return placeWall((xw,yw),color,state,isX)

def startGame(x,y,brZidova,xx1,xy1,xx2,xy2,ox1,oy1,ox2,oy2,isAIFirst):
    state = tuple()
    state = ([x, y], {"X1": (xx1, xy1), "X2": (xx2, xy2), "O1": (ox1, oy1), "O2": (ox2, oy2)}, {"X1": (xx1, xy1), "X2": (xx2, xy2), "O1": (ox1, oy1), "O2": (ox2, oy2)}, {}, ([brZidova, brZidova], [brZidova, brZidova]))
    if not isAIFirst:
        while not isEnd(state):
            newState=inputMove(state,True)
            while not newState:
                newState=inputMove(state,True)
            state=newState
            printBoard(state)

            if isEnd(state):
                print(isEnd(state)," je pobednik!")
                #newGame eventualno
                return

            #AI/drugi igrac igra potez
            newState=inputMove(state,False)
            while not newState:
                newState=inputMove(state,False)
            state=newState
            printBoard(state)
        print(isEnd(state)," je pobednik!")
        #newGame eventualno
        return
    else:
        while not isEnd(state):
            #AI/drugi igrac igra potez
            newState=inputMove(state,True)
            while not newState:
                newState=inputMove(state,True)
            state=newState
            printBoard(state)

            if isEnd(state):
                print(isEnd(state)," je pobednik!")
                #newGame eventualno
                return
            
            newState=inputMove(state,False)
            while not newState:
                newState=inputMove(state,False)
            state=newState
            printBoard(state)
        print(isEnd(state)," je pobednik!")
        #newGame eventualno
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
            if not pawnAt(state, x,y):
                return True
              
    elif(state[2][pawn][0]-2==x and state[2][pawn][1]==y):
        #gore 2
        if not (wallAt(state,"P",state[2][pawn][0]-1,state[2][pawn][1]) or wallAt(state,"P",state[2][pawn][0]-2,state[2][pawn][1]) or wallAt(state,"P",state[2][pawn][0]-1,state[2][pawn][1]-1) or wallAt(state,"P",state[2][pawn][0]-2,state[2][pawn][1]-1)):
            if not pawnAt(state, x,y):
                return True
    
    elif(state[2][pawn][0]==x and state[2][pawn][1]+2==y):
        #desno 2
        if not (wallAt(state,"Z",state[2][pawn][0],state[2][pawn][1]) or wallAt(state,"Z",state[2][pawn][0],state[2][pawn][1]+1) or wallAt(state,"Z",state[2][pawn][0]-1,state[2][pawn][1]) or wallAt(state,"Z",state[2][pawn][0]-1,state[2][pawn][1]+1)):
            if not pawnAt(state, x,y):
                return True

    elif(state[2][pawn][0]==x and state[2][pawn][1]-2==y):
        #levo 2
        if not (wallAt(state,"Z",state[2][pawn][0],state[2][pawn][1]-1) or wallAt(state,"Z",state[2][pawn][0],state[2][pawn][1]-2) or wallAt(state,"Z",state[2][pawn][0]-1,state[2][pawn][1]-1) or wallAt(state,"Z",state[2][pawn][0]-1,state[2][pawn][1]-2)):
            if not pawnAt(state, x,y):
                return True

    elif(state[2][pawn][0]+1==x and state[2][pawn][1]+1==y):
        #dole desno
        if not wallAt(state,"Z",state[2][pawn][0],state[2][pawn][1]) or wallAt(state,"P",state[2][pawn][0],state[2][pawn][1]) or (wallAt(state,"Z",state[2][pawn][0]-1,state[2][pawn][1]) and wallAt(state,"P",state[2][pawn][0],state[2][pawn][1]-1)) or (wallAt(state,"Z",state[2][pawn][0]+1,state[2][pawn][1]) and wallAt(state,"P",state[2][pawn][0],state[2][pawn][1]+1)):
            if not pawnAt(state, x,y):
                return True

    elif(state[2][pawn][0]+1==x and state[2][pawn][1]-1==y):
        #dole levo
        if not wallAt(state,"Z",state[2][pawn][0],state[2][pawn][1]-1) or wallAt(state,"P",state[2][pawn][0],state[2][pawn][1]-1) or (wallAt(state,"Z",state[2][pawn][0]-1,state[2][pawn][1]-1) and wallAt(state,"P",state[2][pawn][0],state[2][pawn][1]-2)) or (wallAt(state,"Z",state[2][pawn][0]+1,state[2][pawn][1]-1) and wallAt(state,"P",state[2][pawn][0],state[2][pawn][1]-2)):
            if not pawnAt(state, x,y):
                return True

    elif(state[2][pawn][0]-1==x and state[2][pawn][1]+1==y):
        #gore desno
        if not wallAt(state,"Z",state[2][pawn][0]-1,state[2][pawn][1]) or wallAt(state,"P",state[2][pawn][0]-1,state[2][pawn][1]) or (wallAt(state,"Z",state[2][pawn][0],state[2][pawn][1]) and wallAt(state,"P",state[2][pawn][0]-1,state[2][pawn][1]-2)) or (wallAt(state,"Z",state[2][pawn][0]-2,state[2][pawn][1]) and wallAt(state,"P",state[2][pawn][0]-1,state[2][pawn][1]+1)):
            if not pawnAt(state, x,y):
                return True

    elif(state[2][pawn][0]-1==x and state[2][pawn][1]-1==y):
        #gore levo
        if not wallAt(state,"Z",state[2][pawn][0]-1,state[2][pawn][1]-1) or wallAt(state,"P",state[2][pawn][0]-1,state[2][pawn][1]-1) or (wallAt(state,"Z",state[2][pawn][0]-1,state[2][pawn][1]) and wallAt(state,"P",state[2][pawn][0]-1,state[2][pawn][1])) or (wallAt(state,"Z",state[2][pawn][0]-1,state[2][pawn][1]-2) and wallAt(state,"P",state[2][pawn][0]-1,state[2][pawn][1]-2)):
            if not pawnAt(state, x,y):
                return True

    elif(state[2][pawn][0]+1==x and state[2][pawn][1]==y):
        if not (wallAt(state,"P",state[2][pawn][0],state[2][pawn][1]) or wallAt(state,"P",state[2][pawn][0]+1,state[2][pawn][1]) or wallAt(state,"P",state[2][pawn][0],state[2][pawn][1]-1) or wallAt(state,"P",state[2][pawn][0]+1,state[2][pawn][1]-1)):
            if pawnAt(state, x+1,y):
                return True
    elif(state[2][pawn][0]-1==x and state[2][pawn][1]==y):
        if not (wallAt(state,"P",state[2][pawn][0]-1,state[2][pawn][1]) or wallAt(state,"P",state[2][pawn][0]-2,state[2][pawn][1]) or wallAt(state,"P",state[2][pawn][0]-1,state[2][pawn][1]-1) or wallAt(state,"P",state[2][pawn][0]-2,state[2][pawn][1]-1)):
            if pawnAt(state, x-1,y):
                return True
    elif(state[2][pawn][0]==x and state[2][pawn][1]+1==y):
        #desno 1
        if not (wallAt(state,"Z",state[2][pawn][0],state[2][pawn][1]) or wallAt(state,"Z",state[2][pawn][0],state[2][pawn][1]+1) or wallAt(state,"Z",state[2][pawn][0]-1,state[2][pawn][1]) or wallAt(state,"Z",state[2][pawn][0]-1,state[2][pawn][1]+1)):
            if pawnAt(state, x,y+1):
                return True
    elif(state[2][pawn][0]==x and state[2][pawn][1]-1==y):
        #levo 1
        if not (wallAt(state,"Z",state[2][pawn][0],state[2][pawn][1]-1) or wallAt(state,"Z",state[2][pawn][0],state[2][pawn][1]-2) or wallAt(state,"Z",state[2][pawn][0]-1,state[2][pawn][1]-1) or wallAt(state,"Z",state[2][pawn][0]-1,state[2][pawn][1]-2)):
            if pawnAt(state, x,y-1):
                return True
    return False

'''
FAZA II
'''
def possibleMoves(state,pawn):
    states=list()
    field=state[2][pawn]
    field[0]-=2
    if validatePawnMove(state,pawn,field[0],field[1]):
        possibleState=placePawn(pawn,field,state)
        states.append(possibleState)
    field[0]+=1
    field[1]+=1
    if validatePawnMove(state,pawn,field[0],field[1]):
        possibleState=placePawn(pawn,field,state)
        states.append(possibleState)
    field[1]-=2
    if validatePawnMove(state,pawn,field[0],field[1]):
        possibleState=placePawn(pawn,field,state)
        states.append(possibleState)
    field[0]+=1
    field[1]-=1
    if validatePawnMove(state,pawn,field[0],field[1]):
        possibleState=placePawn(pawn,field,state)
        states.append(possibleState)
    field[1]+=4
    if validatePawnMove(state,pawn,field[0],field[1]):
        possibleState=placePawn(pawn,field,state)
        states.append(possibleState)
    field[0]+=1
    field[1]-=1
    if validatePawnMove(state,pawn,field[0],field[1]):
        possibleState=placePawn(pawn,field,state)
        states.append(possibleState)
    field[1]-=2
    if validatePawnMove(state,pawn,field[0],field[1]):
        possibleState=placePawn(pawn,field,state)
        states.append(possibleState)
    field[0]+=1
    field[1]+=1
    if validatePawnMove(state,pawn,field[0],field[1]):
        possibleState=placePawn(pawn,field,state)
        states.append(possibleState)
    return

def pathHeuristics(origin: tuple, dest: tuple):
    return int(math.sqrt((origin[0]-dest[0])**2 + (origin[1]-dest[1])**2)*10)

def pathFind(state, startField: tuple, endField: tuple):
    pawn=str()
    if state[2]["X1"]==startField:
        pawn="X1"
    if state[2]["X2"]==startField:
        pawn="X2"
    if state[2]["O1"]==startField:
        pawn="O1"
    if state[2]["O2"]==startField:
        pawn="O2"

    start=copy.deepcopy(state)
    end=copy.deepcopy(state)
    end[2][pawn]=endField

    found_end = False
    open_set = set(start)
    closed_set = set()
    g = {}
    prev_nodes = {}
    g[start] = 0
    prev_nodes[start] = None
    while len(open_set) > 0 and (not found_end):
        node = None
        for next_node in open_set:
            if node is None or g[next_node] + pathHeuristics(next_node[2][pawn],endField) < g[node] + pathHeuristics(node[2][pawn],endField):
                node = next_node
        if node[2][pawn] == endField:
            found_end = True
            break
        for m in possibleMoves(state,pawn):
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

def validateWallPlacement(state,color,x,y,isX):
    potentialState=placeWall((x,y),color,state,isX)
    if pathFind(potentialState,potentialState[2]["X1"],potentialState[1]["O1"]) and pathFind(potentialState,potentialState[2]["X1"],potentialState[1]["O2"]) and pathFind(potentialState,potentialState[2]["X2"],potentialState[1]["O1"]) and pathFind(potentialState,potentialState[2]["X2"],potentialState[1]["O2"]) and pathFind(potentialState,potentialState[2]["O1"],potentialState[1]["X1"]) and pathFind(potentialState,potentialState[2]["O1"],potentialState[1]["X2"]) and pathFind(potentialState,potentialState[2]["O2"],potentialState[1]["X1"]) and pathFind(potentialState,potentialState[2]["O2"],potentialState[1]["X2"]):
        if isX:
            if not (state[4][0][0]>0 and color=="Z") or (state[4][0][1]>0 and color=="P"):
                return False
        else:
            if not (state[4][1][0]>0 and color=="Z") or (state[4][1][1]>0 and color=="P"):
                return False
        if not wallAt(state,"P",x,y) and not wallAt(state,"Z",x,y):
            if color=="P":
                if not wallAt(state,"P",x,y-1):
                    return True
            if color=="Z":
                if not wallAt(state,"Z",x-1,y):
                    return True
    return False

def placePawn(pawn: str,field : tuple, state):
    newState=copy.deepcopy(state)
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
    
game()