k.<a> = GF(2^4, repr='int');
rc = [[8,0],[3,0]]
key = [[2,13],[5,5]]

def getLog(n):
    for i,x in enumerate(k):
        if(n == (x.integer_representation())):
            return i

N = matrix(k, [[a^(k.int_to_log(4)),a^(k.int_to_log(1))], [a^(k.int_to_log(1)),a^(k.int_to_log(4))]])
NInvertido = matrix(k, [[a^(k.int_to_log(9)),a^(k.int_to_log(2))], [a^(k.int_to_log(2)),a^(k.int_to_log(9))]]);
sBox = matrix([[9,4,10,11],[13,1,8,5],[6,2,0,3],[12,14,15,7]])
sBoxInvertida = matrix([[10,5,9,11],[1,7,8,15],[6,0,2,3],[12,4,13,14]])


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

def substituicaoNibbleDecriptar(estado):
    estadoAtual = [[], []]
    for i in range(2):
        for j in range(2):
            estadoAtual[i].append(sBoxInvertida[binIndex(estado[i][j], 1)][binIndex(estado[i][j], 0)])
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
    aux = [[],[]]
    for i in range(2):
        for j in range(2):
                aux[i].append(k.log_to_int(estado[i][j]))

    M = matrix(k, aux)
    return N*M

def embaralharColunasDecriptar(estado):
    aux = [[],[]]
    for i in range(2):
        for j in range(2):
            exp = k.int_to_log(estado[i][j])
            if(exp == 0):
                aux[i].append(0)
            else:
                aux[i].append(a^(exp))

    M = matrix(k, aux)
    return NInvertido*M

def gFunction(wA,wB, rodada):
    wBAux = wB.copy()
    wBAux[0], wBAux[1] = wBAux[1], wBAux[0]
    w1Aux = []
    for i in range(2):
        w1Aux.append(sBox[binIndex(wBAux[i], 1)][binIndex(wBAux[i], 0)])
        w1Aux[i] = (rc[rodada - 1][i] ^^ w1Aux[i])
    return w1Aux

def expandirChave(wA, wB, rodada):
    gFun = gFunction(wA, wB, rodada)
    wC = []
    wD = []
    for i in range(2):
        wC.append(wA[i] ^^ gFun[i])
        wD.append(wC[i] ^^ wB[i])
    return (wC, wD)

def saesEncrypt(text, key):
    w0 = [key[0][0], key[0][1]]
    w1 = [key[1][0], key[1][1]]
    estado = inclusaoChave(text, key)
    
    ## Rodada 1
    estado = substituicaoNibble(estado)
    estado = deslocamentoLinha(estado)
    estado = embaralharColunas(estado)
    w2, w3 = expandirChave(w0, w1, 1)
    estado = inclusaoChave(estado, [w2,w3])
    ## Rodada 2
    estado = substituicaoNibble(estado)
    estado = deslocamentoLinha(estado)
    w4, w5 = inclusaoChave(w2, w3, 2)
    estado = inclusaoChave(estado, [w4,w5])
    
    return estado

def saesDecrypt(text, key):
    w0 = [key[0][0], key[0][1]]
    w1 = [key[1][0], key[1][1]]
    w2, w3 = expandirChave(w0, w1, 1)
    w4, w5 = expandirChave(w2,w3, 2)
    estado = inclusaoChave(estado, [w4,w5])
    
    ## Rodada 1
    estado = deslocamentoLinha(estado)
    estado = substituicaoNibbleDecriptar(estado)
    estado = inclusaoChave(estado, [w2, w3])
    estado = embaralharColunasDecriptar(estado)
    
    ## Rodada 2
    estado = deslocamentoLinha(estado)
    estado = substituicaoNibbleDecriptar(estado)
    estado = inclusaoChave(estado, [w0, w1])
    
    return estado
