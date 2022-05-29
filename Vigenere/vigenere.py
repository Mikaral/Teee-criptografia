import string
import random

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
        for line in lines: f.write(str(line) + "\n")
        f.close()
    except:
        raise RuntimeError("Something went wrong when writing to the file")
    
def generateKeys(size = 6):
    keys = []
    for i in range(size):
        keys.append(random.randint(1,25))
    
    print(keys)
    writeLines("key.txt", keys)
    
    return keys

def shiftLetter(letter, k):
    if(letter in string.ascii_letters):
        letter = string.ascii_letters[(string.ascii_letters.index(letter) + k) % 52]
    
    return letter

def vigenere(lines, keys, mode):
    
    for i, line in enumerate(lines):
        lines[i] = caesar(line, int(keys[i % len(keys)]), mode)
    
    return lines

def caesar(line, k,  mode):
    key = k if mode else k*-1
    lineAux = ""

    for letter in line:
        lineAux = lineAux + shiftLetter(letter, key)
    
    return lineAux

def getUserVariables(mode):
    key = 0
    path = input("Write the path of the file: ")
    if mode:
        key = input("Write the key size: ")

    return (path, int(key))

def encriptFile(mode):
    userInputs = getUserVariables(mode)
    
    if(mode):
        print("Writing encrypted text on ../encryptedText.txt")
        keys = generateKeys(userInputs[1])
    else:
        keys = getFileLines("key.txt")
        print("Writing decrypted text on ../encryptedText.txt")
    

    lines = vigenere(getFileLines(userInputs[0]), keys, mode)
    writeLines("encryptedText.txt", lines)


def main():
    usrOp = -1
    while(usrOp != 0):
        print("------------------ Vigenere Chiper ------------------")
        print("0) Close program")
        print("1) Encript a file")
        print("2) Decript a file")
        usrOp = int(input("Choose a option: "))

        if(usrOp == 1):
            encriptFile(True)
        elif(usrOp == 2):
            encriptFile(False)
        elif(usrOp != 0):
            print("This is not a valid option")

main()
