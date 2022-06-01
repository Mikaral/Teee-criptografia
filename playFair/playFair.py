import string

def getFileLines(path):
    """ 
    Função que retorna uma lista de strings de um arquivo a partir 
    do caminho do mesmo. Retorna um FileNotFoundError caso o arquivo
    não exista.
    """
    try:
        f = open(path, "r")
        lines = list(map(lambda x: x.strip(string.punctuation).replace("'", ""), f.readlines()))
        f.close()
        return lines
    except:
        raise FileNotFoundError("There is no such file with this name")

def writeLines(path, lines):
    """
    Escreve uma linha de strings (o parâmetro lines) em um determinado arquivo.
    """
    try:
        f = open(path, "w")
        for line in lines: f.write(line + "\n")
        f.close()
    except:
        raise Exception("Something went wrong when writing to the file")

def createMatrixKey(key):
    """
    Função que cria a matriz chave da cifra Playfair.
    """
    key = key.lower()
    matrix = [[0 for i in range (5)] for j in range(5)]
    letters_added = []
    row = 0
    col = 0

    for letter in key:
        if letter not in letters_added:
            matrix[row][col] = letter
            letters_added.append(letter)
        else:
            continue
        if (col==4):
            col = 0
            row += 1
        else:
            col += 1

    for letter in range(96,123):
        if letter==106:
                continue
        if chr(letter) not in letters_added:
            letters_added.append(chr(letter))

    index = 0
    
    for i in range(5):
        for j in range(5):
            matrix[i][j] = letters_added[index]
            index+=1
    
    return matrix

def indexOf(letter,matrix):
    """
    Função auxiliar que retorna o índice de uma letra na matriz chave.
    """
    for i in range (5):
        try:
            index = matrix[i].index(letter)
            return (i,index)
        except:
            continue

def separateSameLetters(lines):
    """
    Função auxiliar que trata algumas condições da cifra Playfair.
    As condições são adicionar a letra 'x' entre duas letras repetidas
    e adicionar um x no final de uma palavra caso ela tinha um número ímpar
    de letras.
    """
    for i, line in enumerate(lines):
        index = 0
        
        while(index < len(line)):
            character1 = line[index]
            
            if(index == len(line) - 1):
                line = line + 'x'
                index += 2
                continue
            
            character2 = line[index + 1]
            
            if (character1 == character2):
                line = line[:index+1] + 'x' + line[index+1:]
            
            index += 2
        
        lines[i] = line
            
    return lines

def pf(key, lines, encrypt=True):
    """
    Cifra ou decifra uma lista (o parâmetro lines) de strings utilizando o método Playfair.
    Utiliza o parâmetro key como a matriz chave. Se encrypt for verdadeiro, cifra. Caso contrário decifra.
    """
    if encrypt:
        lines = separateSameLetters(lines)

    matrix = createMatrixKey(key)

    for i, line in enumerate(lines):
        strAux = ""
        for word in line.lower().split():
            strAux = strAux + playfair(matrix, word, encrypt) + " "
        
        lines[i] = strAux
    
    return lines
        

def playfair(matrix, message, encrypt=True):
    """
    Função auxiliar a função pf, que cifra uma string utilizando o método Playfair.
    Utiliza o parâmetro matrix como a matriz chave. Se encrypt for verdadeiro, cifra, caso contrário decifra.
    """
    inc = 1
    if encrypt==False:
        inc = -1
    
    cipher_text=''
    
    for (l1, l2) in zip(message[0::2], message[1::2]):
        row1,col1 = indexOf(l1,matrix)
        row2,col2 = indexOf(l2,matrix)
        if row1==row2:
            cipher_text += matrix[row1][(col1+inc)%5] + matrix[row2][(col2+inc)%5]
        elif col1==col2:
            cipher_text += matrix[(row1+inc)%5][col1] + matrix[(row2+inc)%5][col2]
        else:
            cipher_text += matrix[row1][col2] + matrix[row2][col1]
    
    return cipher_text

def main():
    """
    CLI do programa
    """
    usrOp = -1
    path = input("Write the path of the desired file: ")
    lines = getFileLines(path)
    key = input("What is the key? ")

    while(usrOp != 0):
        print("------------------ Play Fair ------------------")
        print("0) Close program")
        print("1) Encript a file")
        print("2) Decript a file")
        usrOp = int(input("Choose a option: "))

        if(usrOp == 1):
            writeLines("chiper.txt", pf(key, lines))
            print("Saving encrypted file on chiper.txt")
        elif(usrOp == 2):
            writeLines("solution.txt", pf(key, lines, False))
            print("Saving decrypted file on solution.txt")
        elif(usrOp != 0):
            print("This is not a valid option")

main()
