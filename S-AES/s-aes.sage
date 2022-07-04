k.<a> = GF(2^4, repr='int');

N = matrix(k, [[a^getLog(1),a^getLog(4)], [a^getLog(4),a^getLog(1)]])
sBox = matrix([[9,4,10,11],[13,1,8,5],[6,2,0,3],[12,14,15,7]])

def getLog(n):
    for i,x in enumerate(k):
        if(n == (x.integer_representation())):
            return i

def getIndex(n):
    l = getLog(n)
    if(l == 0):
        return 0
    else:
        return a^(l)

def inclusaoChave(estado, chave):
    estadoAtual = [[], []]
    for i in range(2):
        for j in range(2):
            estadoAtual[i].append(estado[i][j]^^chave[i][j])
    return estadoAtual

def deslocamentoLinha(estado):
    estado[1][0], estado[1][1] = estado[1][1], estado[1][0]

def substituicaoNibble(estado):
    estadoAtual = [[], []]
    for i in range(2):
        for j in range(2):
            estadoAtual[i].append(sBox[binIndex(estado[i][j], 1)][binIndex(estado[i][j], 0)])
    return estadoAtual

def fixSize(value):
    while(len(value) < 4):
        value = '0' + value
    return value

def binIndex(value, position):
    x = fixSize(value.binary())
    if(position == 1):
        x = x[0:2]
    else:
        x = x[2:4]
    return(int(str(x), base=2))

def embaralharColunas(estado):
    if(estado[0][0] == 0):
        a1 = 0
    else:
        a1 = a^getLog(estado[0][0])
    
    if(estado[0][1] == 0):
        a2 = 0
    else:
        a2 = a^getLog(estado[0][1])
    
    if(estado[1][0] == 0):
        a3 = 0
    else:
        a3 = a^getLog(estado[1][0])
    
    if(estado[1][1] == 0):
        a4 = 0
    else:
        a4 =a^getLog(estado[1][1])
    
    M = matrix([[a1, a2], [a3, a4]])
    
    return N*M