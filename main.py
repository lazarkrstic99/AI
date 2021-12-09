'''
FAZA I

reprezentacija stanja:
([dimenzijeTable],{pocetnePozicije},{pozicijePesaka},{pozicijeZidova},(preostaliZidovi))
([x,y],{"X1":(x,y),"X2":(x,y),"O1":(x,y),"O2":(x,y)},{"X1":[x,y],"X2":[x,y],"O1":[x,y],"O2":[x,y]},{(x,y):"Z|P"},([<preostaliZeleni>,<preostaliPlavi>],[<preostaliZeleni>,<preostaliPlavi>]))
'''

def setup(x,y,brZidova,xx1,xy1,xx2,xy2,ox1,oy1,ox2,oy2,isAIFirst):
    '''
    todo implementiraj
    :param x:
    :param y:
    :param brZidova:
    :param xx1:
    :param xy1:
    :param xx2:
    :param xy2:
    :param ox1:
    :param oy1:
    :param ox2:
    :param oy2:
    :return:
    '''

def isEnd(state):
    '''
    :param state:
    :return: bool isEnded
    '''

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
