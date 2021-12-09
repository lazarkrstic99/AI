'''
FAZA I

reprezentacija stanja:
([dimenzijeTable],{pocetnePozicije},{pozicijePesaka},{pozicijeZidova},(preostaliZidovi))
([x,y],{"X1":(x,y),"X2":(x,y),"O1":(x,y),"O2":(x,y)},{"X1":[x,y],"X2":[x,y],"O1":[x,y],"O2":[x,y]},{(x,y):"Z|P"},([<preostaliZeleni>,<preostaliPlavi>],[<preostaliZeleni>,<preostaliPlavi>]))
'''

numberConversion=(1,2,3,4,5,6,7,8,9,'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S')

def startGame(x,y,brZidova,xx1,xy1,xx2,xy2,ox1,oy1,ox2,oy2,isAIFirst):
    state = tuple()
    state = ([x, y], {"X1": (xx1, xy1), "X2": (xx2, xy2), "O1": (ox1, oy1), "O2": (ox2, oy2)}, {"X1": (xx1, xy1), "X2": (xx2, xy2), "O1": (ox1, oy1), "O2": (ox2, oy2)}, {}, ([brZidova, brZidova], [brZidova, brZidova]))


def isEnd(state):

    if state[2]["X1"] == state[1]["O1"] or state[2]["X1"] == state[1]["O2"]:
        print("X je pobednik!")
        return True
    if state[2]["X2"] == state[1]["O1"] or state[2]["X2"] == state[1]["O2"]:
        print("X je pobednik!")
        return True
    if state[2]["O1"] == state[1]["X1"] or state[2]["O1"] == state[1]["X2"]:
        print("O je pobednik!")
        return True
    if state[2]["O2"] == state[1]["X1"] or state[2]["O2"] == state[1]["X2"]:
        print("O je pobednik!")
        return True
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
        return True
    except:
        print("Nevalidan unos!")
        return False

def printBoard(state):
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
        printField=str(numberConversion[i+1])
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
            
            if (i>0 and (i-1,j) in state[4] and state[4][(i-1,j)]=="Z") or ((i,j) in state[4] and state[4][(i,j)]=="Z"):
                printField+="ǁ"
            else:
                printField+="|"
            
            if(j>0 and (i,j-1) in state[4] and state[4][(i,j-1)]=="P") or ((i,j) in state[4] and state[4][(i,j)]=="P"):
                printWall+="="
            else:
                printWall+="-"
            
            printWall+=" "
            



def playMove(pawn: str,field : tuple, wall : tuple, wallColor:str, state):
    '''
    validacija ide u zasebnu fju
    promena stanja
    '''
    state[2][pawn] = field
    state[3][wall] = wallColor
    return state
def inputandvalidatemove(pawn: str, field :tuple, wall:tuple, wallColor:str,state):
    isValid = False
    while not isValid:
        pawn = input("Unesite ime figure(X1,X2,O1,O2): ")
        if pawn == "X1" or pawn == "X2" or pawn == "O1" or pawn == "O2":
           isValid = True
        else:
           isValid = False
           print("Pogresna figura!")
        x, y = input("Unesite polje %s igraca (x,y): ", pawn).split(",")
        x = int(x)
        y = int(y)
        #granice table
        if x < state[0][0] or x > state[0][0] or y < state[0][1] or y > state[0][1]:
            isValid = False
        else:
            isValid = True
            print("Pokusavate postaviti figuru izvan table!")
        #da li je zid ispred ili igrac
        #if state[2][pawn][0]+2 == x and state[2][pawn][0]+2 < state[0][0] and state[3][(state[2][pawn][0]+2, y)] is None:




printBoard(([11, 14], {"X1": (2, 2), "X2": (4, 2), "O1": (2, 8), "O2": (6, 8)}, {"X1": (2, 3), "X2": (4, 6), "O1": (2, 8), "O2": (6, 10)}, {}, ([10, 10], [10, 10])))
while gameParamInput() is not True:
    next