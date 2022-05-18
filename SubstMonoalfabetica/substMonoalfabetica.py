import enchant
import string
import random
from functools import partial

englishLetterFreq = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 
'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 
'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}
d = enchant.Dict("en_US")
alphabet = dict.fromkeys(string.ascii_lowercase, 0)
alphabetFrequency = dict.fromkeys(string.ascii_lowercase, 0)

def getFileLines(path):
    f = open(path, "r")
    lines = list(map(lambda x: x.rstrip().strip("\"").lower(), f.readlines()))
    f.close()
    return lines

key = getFileLines("../kTable.txt")
lines = getFileLines("../testC.txt")

def writeLines(path, lines):
    f = open(path, "w")
    for line in lines: f.write(line + "\n")
    f.close()

def generateTable():
    randomTable = random.sample(string.ascii_lowercase, len(string.ascii_lowercase))
    writeLines("../kTable.txt", randomTable)
    return randomTable

def shiftLetter(letter, mod, keyAux):
    if(letter in keyAux and mod):
        letter = keyAux[string.ascii_lowercase.index(letter) % 26]
    elif(letter in keyAux):
        letter = string.ascii_lowercase[keyAux.index(letter) % 26]
    
    return letter

def mas(lines, mode, key):
    for i,line in enumerate(lines):
        partial_func = partial(shiftLetter, mod = mode, keyAux = key)
        lineAux = str("".join(map(partial_func, line)))
        lines[i] = lineAux
    
    return lines

def letterCount(alphabet, lines):
    for line in lines: 
        for letter in line:
            if(letter in string.ascii_lowercase):
                alphabet[letter] += 1

def letterFrequency(alphabet, alphabetFrequency, lines):
    letterCount(alphabet, lines)
    totalLetters = sum(alphabet.values())
    for key in alphabetFrequency.keys():
        alphabetFrequency[key] = (alphabet[key] / totalLetters) * 100
    
    return dict(reversed(sorted(alphabetFrequency.items(), key = lambda item: item[1])))

def crushCypher(alphabet, alphabetFrequency, lines):
    alphabetFreqAux = letterFrequency(alphabet, alphabetFrequency, lines)
    solution = dict({list(alphabetFreqAux.keys())[x] : list(englishLetterFreq.keys())[x].lower() for x in range(26)})
    solution = dict(sorted(solution.items(), key = lambda item: item[1]))
    writeLines("../solution.txt", mas(lines, False, list(solution.keys())))
