import enchant
import string
from functools import partial

d = enchant.Dict("en_US")
k = 3

def getFileLines(path):
    f = open(path, "r")
    lines = list(map(lambda x: x.rstrip().strip("\""), f.readlines()))
    f.close()
    return lines

def writeLines(path, lines):
    f = open(path, "w")
    for line in lines: f.write(line + "\n")
    f.close()

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

lines = getFileLines("../test.txt")
writeLines("../test.txt", caesar(lines, 3, False))