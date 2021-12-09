'''
FAZA I

reprezentacija stanja:
([dimenzijeTable],{pocetnePozicije},{pozicijePesaka},{pozicijeZidova},(preostaliZidovi))
([x,y],{"X1":(x,y),"X2":(x,y),"O1":(x,y),"O2":(x,y)},{"X1":[x,y],"X2":[x,y],"O1":[x,y],"O2":[x,y]},{(x,y):"Z|P"},([<preostaliZeleni>,<preostaliPlavi>],[<preostaliZeleni>,<preostaliPlavi>]))
'''

def setup(x,y,brZidova,xx1,xy1,xx2,xy2,ox1,oy1,ox2,oy2,isAIFirst):
    state = tuple()
    state = ([x, y], {"X1": (xx1, xy1), "X2": (xx2, xy2), "O1": (ox1, oy1), "O2": (ox2, oy2)}, {"X1": (xx1, xy1), "X2": (xx2, xy2), "O1": (ox1, oy1), "O2": (ox2, oy2)}, {}, ([brZidova, brZidova], [brZidova, brZidova]))
    startGame(state, isAIFirst)

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
    '''
    unos sa konzole
    validacija unosa
    zove setup za unete parametre
    :return:
    '''

def printBoard(state):
    '''
    stampa tablu na konzolu
    :param state:
    :return:
    '''

def playMove(pawn,field,wall):
    '''
    validacija
    promena stanja
    :param pawn:
    :param field:
    :param wall:
    :return: bool isValid
    '''
def startGame(state, isAIFirst):
    '''
    krece igra
    :param state:
    :param isAIFirst:
    :return:
    '''