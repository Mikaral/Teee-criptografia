import enchant
import string

d = enchant.Dict("en_US")

def getFileLines(path):
    f = open("Teee-criptografia/" + path +".txt", "r")
    lines = list(map(lambda x: x.rstrip(), f.readlines()))
    f.close()
    return lines

def writeLines(path, lines):
    f = open("Teee-criptografia/" + path +".txt", "w")
    for line in lines: f.write(line + "\n")
    f.close()

def caesar(lines, k, mode):
    k = k if mode else k*-1

    for i,line in enumerate(lines):
        lineAux = ""

        for letter in line:
            if(letter != " " and letter not in string.punctuation):
                lineAux += string.ascii_letters[string.ascii_letters.index(letter) + k]
            else:
                lineAux += letter
        
        lines[i] = lineAux
    
    return lines


def breakCypher(path):
    k = 1
    correctKey = False
    
    while(not correctKey and k < 50):
        decipherAttempt = caesar(getFileLines("text"), k, False)
        correctKey = all(list(map(lambda x: d.check(x), decipherAttempt[0].split())))
        k += 1
    
    return k - 1


#lines = caesar(getFileLines("text"), 3, True)
#writeLines("text", lines)
print(breakCypher("text"))