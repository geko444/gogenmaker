import string
import collections
import random

def makeDictionary():
    word_dict = collections.defaultdict(list)
    with open('words.txt') as f:
        for w in f.readlines():
            if len(w) > 3:
                word_dict[w[0]].append(w.strip())
    return word_dict

def makeGogenGrid():
    letters = list(string.ascii_lowercase[:-1])
    random.shuffle(letters)
    return [[letters[5*a+b] for b in range(5)] for a in range(5)]

def gridPrint(grid):
    grid_string = '\n'.join([''.join(row) for row in grid])
    print grid_string

def getLetter(grid, coordinate):
    return grid[coordinate[1]][coordinate[0]]

def getLetters(grid, coordinates):
    return [getLetter(grid, coordinate) for coordinate in coordinates]


def getPosition(grid, letter):
    size = len(grid)
    for j in range(size):
        if letter in grid[j]:
            return (grid[j].index(letter), j)

def getNeighbours(grid, coordinate, path=[]):
    size = len(grid)
    neighbours = []
    if coordinate not in path:
        path.append(coordinate)
    c, r = coordinate
    for j in range(r-1, r+2):
        if j in range(size):
            for i in range(c-1, c+2):
                if i in range(size):
                    if (i, j) not in path:
                        neighbours.append((i, j))
    return neighbours


def swapLetters(grid, a, b):
    ai, aj = getPosition(grid, a)
    bi, bj = getPosition(grid, b)
    grid[bj][bi] = a
    grid[aj][ai] = b
    return grid

def placeVowels(grid):
    vowels = ['a', 'e', 'i', 'o', 'u']
    midpoints = [(1,1), (3,1), (1,3), (3,3)]
    midpoint_letters = getLetters(grid, midpoints)
    midpoint_vowels = []
    for m in midpoint_letters:
        if m in vowels:
            vowels.remove(m)
            midpoint_letters.remove(m)
    random.shuffle(vowels)
    for i in range(len(midpoint_letters)):
        swapLetters(grid, vowels[i], midpoint_letters[i])
    return grid

def placeQU(grid):
    vowels = ['a', 'e', 'i', 'o', 'u']
    u_pos = getPosition(grid, 'u')
    u_neighbours = getLetters(grid, getNeighbours(grid, u_pos))
    u_neighbours = [n for n in u_neighbours if n not in vowels]
    if 'q' not in u_neighbours:
        swapLetters(grid, 'q', random.choice(u_neighbours))
    return grid

def placeUVowel(grid):
    vowels = ['a', 'e', 'i', 'o']
    u_pos = getPosition(grid, 'u')
    u_neighbours = getLetters(grid, getNeighbours(grid, u_pos))
    u_neighbours = [n for n in u_neighbours if n != 'q']
    u_neighbours_vowels = [n for n in u_neighbours if n in vowels]
    if len(u_neighbours_vowels) == 0:
        swapLetters(grid, random.choice(vowels), random.choice(u_neighbours))
    return grid



def getWordFromPath(grid, coordinates):
    return ''.join(getLetters(grid, coordinates))

def getWordsStartingWith(letters, dictionary):
    return [word for word in dictionary[letters[0]] if word.startswith(letters)]

def isWord(letters, dictionary):
    return letters in dictionary[letters[0]]

def isWordStart(letters, dictionary):
    if len(getWordsStartingWith(letters, dictionary)) == 0:
        return False
    else:
        return True

def findWords(grid, dictionary, start):
    path = [start]
    words = []
    max_length = len(grid) ** 2
    def takeStep(position):
        letters = getWordFromPath(grid, path)
        if isWord(letters, dictionary):
            words.append(letters)
        if len(letters) < max_length and isWordStart(letters, dictionary) is True:
            neighbours = getNeighbours(grid, position, path)
            if len(neighbours) > 0:
                for n in neighbours:
                    path.append(n)
                    takeStep(n)
                    path.pop()

    takeStep(start)
    return words

def solveBoggle(grid, dictionary):
    words = []
    size = len(grid)
    for r in range(size):
        for c in range(size):
            words.extend(findWords(grid, dictionary, (c, r)))
    return words

test_gogen = makeGogenGrid()
gridPrint(test_gogen)
print '\n'
# test_gogen = placeVowels(test_gogen)
test_gogen = placeQU(test_gogen)
# test_gogen = placeUVowel(test_gogen)
gridPrint(test_gogen)
print '\n'
dictionary = makeDictionary()

words = solveBoggle(test_gogen, dictionary)
print words
print len(words)

def countWordsContainingLetter(words):
    letters = list(string.ascii_lowercase)[:-1]
    letters_dict = {}
    for l in letters:
        letters_dict[l] = 0
    for word in words:
        for letter in list(word):
            letters_dict[letter] += 1
    return letters_dict

print countWordsContainingLetter(words)