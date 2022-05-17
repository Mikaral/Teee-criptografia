import enchant
import string

d = enchant.Dict("en_US")

def getFileLines(path):
    f = open(path, "r")
    lines = list(map(lambda x: x.rstrip().strip("\""), f.readlines()))
    f.close()
    return lines

def writeLines(path, lines):
    f = open(path, "w")
    for line in lines: f.write(line + "\n")
    f.close()

def caesar(lines, k, mode):
    k = k if mode else k*-1

    for i,line in enumerate(lines):
        lineAux = ""

        for letter in line:
            if(letter in string.ascii_letters):
                lineAux += string.ascii_letters[(string.ascii_letters.index(letter) + k) % 52]
            else:
                lineAux += letter

        lines[i] = lineAux
    
    return lines


def breakCypher(path):
    k = 1
    counter = 0
    correctKey = False
    
    while(not correctKey and k < 50):
        decipherAttempt = caesar(getFileLines(path), k, False)
        correctWords = list(map(lambda x: d.check(x), decipherAttempt[0].strip(string.punctuation).split())).count(True)
        correctKey = (correctWords >= len(decipherAttempt[0].split()) * 0.75 )
        k += 1
    
    return k - 1