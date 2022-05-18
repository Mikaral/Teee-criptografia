import enchant
import string
from functools import partial

d = enchant.Dict("en_US")
k = 3

def getFileLines(path):
    try:
        f = open(path, "r")
        lines = list(map(lambda x: x.rstrip().strip("\""), f.readlines()))
        f.close()
        return lines
    except:
        raise FileNotFoundError("There is no such file with this name")

def writeLines(path, lines):
    try:
        f = open(path, "w")
        for line in lines: f.write(line + "\n")
        f.close()
    except:
        raise Exception("Something went wrong when writing to the file")

def shiftLetter(letter, k):
    if(letter in string.ascii_letters):
        letter = string.ascii_letters[(string.ascii_letters.index(letter) + k) % 52]
    
    return letter

def caesar(lines, k,  mode):
    key = k if mode else k*-1
    partial_func = partial(shiftLetter, k = key)

    for i,line in enumerate(lines):
        lineAux = str("".join(map(partial_func, line)))
        lines[i] = lineAux
    
    return lines

def breakCypher(path):
    k = 1
    correctKey = False
    
    while(not correctKey and k < 50):
        decipherAttempt = caesar(getFileLines(path), k, False)
        correctWords = list(map(lambda x: d.check(x), decipherAttempt[0].strip(string.punctuation).split())).count(True)
        correctKey = (correctWords >= len(decipherAttempt[0].split()) * 0.75 )
        k += 1
    
    return k - 1


def getUserVariables():
    path = input("Write the path of the file: ")
    key = input("Write the key: ")

    return (path + ".txt", int(key))


def encriptFile(mode):
    userInputs = getUserVariables()
    lines = caesar(getFileLines(userInputs[0]), userInputs[1], mode)

    if(mode):
        print("Writing encrypted text on ../encryptedText.txt")
    else:
        print("Writing decrypted text on ../encryptedText.txt")
    writeLines("../encryptedText.txt", lines)



usrOp = -1
while(usrOp != 0):
    print("------------------ Caesar Cypher ------------------")
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
        key = breakCypher(input("Write the path of the file: ") + ".txt")
        print("The key is: {}".format(key))
    elif(usrOp != 0):
        print("This is not a valid option")
