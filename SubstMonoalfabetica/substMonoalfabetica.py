# Biblioteca para fazer verificação ortográfica
import enchant
import string
import random
import os.path
# Biblioteca para criação de funções parciais
from functools import partial

# Dicionário (a estrutura de dados) com a frequência das letras na lingua inglesa
englishLetterFreq = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 
'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 
'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}

# Inicialização do dicionário (não confundir com a estrutura de dados) na lingua inglesa
d = enchant.Dict("en_US")

# Dicionário (a estrutura de dados) do alfabeto com as letras minúsculas como chave
# e sua frequência absoluta no arquivo lido.
alphabet = dict.fromkeys(string.ascii_lowercase, 0)

# Dicionário (a estrutura de dados) do alfabeto com as letras minúsculas como chave
# e sua frequência relativa no arquivo lido.
alphabetFrequency = dict.fromkeys(string.ascii_lowercase, 0)

def getFileLines(path):
    """ 
    Função que retorna uma lista de strings de um arquivo a partir 
    do caminho do mesmo. Retorna um FileNotFoundError caso o arquivo
    não exista.
    """
    try:
        f = open(path, "r")
        lines = list(map(lambda x: x.rstrip().strip("\""), f.readlines()))
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
        raise RuntimeError("Something went wrong when writing to the file")

def generateTable():
    """
    Função que gera um alfabeto embaralhado, que será usado como chave, e 
    salva no caminho kTable.txt e retorna a mesma chave como uma lista.
    """
    randomTable = random.sample(string.ascii_lowercase, len(string.ascii_lowercase))
    writeLines("kTable.txt", randomTable)
    return randomTable

def shiftLetter(letter, mod, keyAux):
    """
    Substitui uma letra em relação ao alfabeto correspondente.
    """
    if(letter in keyAux and mod):
        letter = keyAux[string.ascii_lowercase.index(letter) % 26]
    elif(letter in keyAux):
        letter = string.ascii_lowercase[keyAux.index(letter) % 26]
    
    return letter

def mas(lines, mode, key):
    """
    Cifra ou decifra, utilizando a Substituição monoalafabética, uma lista de 
    strings utilizando o parâmetro k como chave. Se mode for verdadeiro, 
    a função irá cifrar. Caso contrário, irá decifrar.
    """
    for i,line in enumerate(lines):
        partial_func = partial(shiftLetter, mod = mode, keyAux = key)
        lineAux = str("".join(map(partial_func, line)))
        lines[i] = lineAux
    
    return lines

def letterCount(alphabet, lines):
    """
    Função auxiliar que conta a frequência absoluta de cada letra.
    """
    for line in lines: 
        for letter in line:
            if(letter in string.ascii_lowercase):
                alphabet[letter] += 1

def letterFrequency(alphabet, alphabetFrequency, lines):
    """
    Função auxiliar que calcula a frequência relativa de cada letra.
    """
    letterCount(alphabet, lines)
    totalLetters = sum(alphabet.values())
    for key in alphabetFrequency.keys():
        alphabetFrequency[key] = (alphabet[key] / totalLetters) * 100
    
    return dict(reversed(sorted(alphabetFrequency.items(), key = lambda item: item[1])))

def breakCypher(alphabet, alphabetFrequency, lines):
    """
    Quebra a cifra se utilizando das frequências das letras e comparando com as frequências das letras
    do mesmo idioma. 
    """
    alphabetFreqAux = letterFrequency(alphabet, alphabetFrequency, lines)
    solution = dict({list(alphabetFreqAux.keys())[x] : list(englishLetterFreq.keys())[x].lower() for x in range(26)})
    solution = dict(sorted(solution.items(), key = lambda item: item[1]))
    print("Writing possible key on solution.txt")
    writeLines("solution.txt", solution.keys())
    print("Writing decrypted text on decrypted.txt")
    writeLines("decryptedText.txt", mas(lines, False, list(solution.keys())))

def encriptFile(mode):
    """
    Função auxiliar para encriptação ou decriptação de um texto a partir das
    entradas do usuário.
    """
    key = getFileLines("kTable.txt")

    if(mode):
        print("Encrypting text.txt on encriptedText.txt")
        print("Assuming file path of text.txt")
        lines = mas(getFileLines("text.txt"), mode, key)
    else:
        print("Decrypting text.txt on encriptedText.txt")
        print("Assuming file path of encriptedText.txt")
        lines = mas(getFileLines("encriptedText.txt"), mode, key)
    
    writeLines("encriptedText.txt", lines)


def main():
    """
    CLI do programa
    """
    if(not os.path.exists('kTable.txt')):
        print("There is no key table, generating key on kTable.txt")
        generateTable()

    usrOp = -1
    while(usrOp != 0):
        print("------------------ Mono-alphabetic Substitution ------------------")
        print("0) Close program")
        print("1) Encript a file")
        print("2) Decript a file")
        print("3) Break a cipher")
        usrOp = int(input("Choose a option: "))

        if(usrOp == 1):
            encriptFile(True)
        elif(usrOp == 2):
            encriptFile(False)
        elif(usrOp == 3):
            if(os.path.exists("encriptedText.txt")):
                breakCypher(alphabet, alphabetFrequency, getFileLines("encriptedText.txt"))
                print("The key was written on solution.txt")
            else:
                print("There is no encrypted text.")
        elif(usrOp != 0):
            print("This is not a valid option")


main()