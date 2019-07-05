import random
import time
import os
# from scipy.spatial import distance

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

clear = "\n" * 100
freeVertex = ' '
visitedVertex = 'i'
sleepTime = 0.3
timeOn = False

def numberOfLinesAndLength():
    with open(fileName) as file:
        flag = True
        for i, j in enumerate(file):
            if (flag):
                length = len(j)
                flag = False
        return i + 1, length - 1


def changeAndPrintMatrix(number, characterToChange):
    if 'flag' not in changeAndPrintMatrix.__dict__:
        flag = True
        matr = matrix

    y, x = numberToVertex(number, len(matr[0]))
    matr[y][x] = characterToChange
    # clearne konzoli
    cls()
    for line in matr:
        for column in line:
            print(column, end='')
        print()

# manhattan distance
def distance(vertexOne, vertexTwo, length):
    x1, y1 = numberToVertex(vertexOne, length)
    x2, y2 = numberToVertex(vertexTwo, length)
    return (abs(x1 - x2) + abs(y1 - y2))

    # return distance.euclidean((x1, y1),(x2, y2))

def nodeInfo(nodesExpanded, nodesPath):
    print("-----------------------------")
    print("Nodes expanded: ", nodesExpanded)
    print("Path length: ", nodesPath)
    print("-----------------------------")

def printRes(seen, path):
    nodesExpanded = 1
    nodesPath = 0

    changeAndPrintMatrix(seen[0], "S")
    nodeInfo(nodesExpanded, nodesPath)
    seen.pop(0)

    for vertex in seen:

        if timeOn:
            time.sleep(sleepTime)

        nodesExpanded += 1
        changeAndPrintMatrix(vertex, "#")
        nodeInfo(nodesExpanded, nodesPath)

    last = path[len(path) - 1]
    path.pop(0)

    for vertex in path:
        nodesPath += 1

        if vertex == last:
            changeAndPrintMatrix(last, "E")
            nodeInfo(nodesExpanded, nodesPath)
            return

        changeAndPrintMatrix(vertex, "o")
        nodeInfo(nodesExpanded, nodesPath)


def AStar(adjacencyList, startVertex, endVertex, length):
    seen = ([startVertex])
    queue = [(startVertex, [startVertex])]
    visited = []

    while queue:
        min = 90000000
        minVertex = 0
        for vertex in queue:
            if (len(vertex[1]) + distance(vertex[0], endVertex, length)) < min:
                min = (len(vertex[1]) + distance(vertex[0], endVertex, length))
                minVertex = queue.index(vertex)

        current, path = queue[minVertex]
        queue.remove(queue[minVertex])
        visited.append(current)

        # ukoncujici podminka
        if current == endVertex:
            printRes(visited, path)
            return

        for vertex in adjacencyList[current]:
            if vertex in seen:
                if vertex in queue:
                    if len(queue[queue.index(vertex)]) > (len(path) + 1):
                        path.append(current)
                        queue[queue.index(vertex)] = path
            else:
                seen.append(vertex)
                queue.append((vertex, path + [vertex]))


def GreedySearch(adjacencyList, startVertex, endVertex, length):
    seen = ([startVertex])
    queue = [(startVertex, [startVertex])]
    visited = []
    while queue:
        min = 9000000
        minVertex = 0
        for vertex in queue:
            # distance(vertex[0], endVertex, length)
            if distance(vertex[0], endVertex, length) < min:
                min = distance(vertex[0], endVertex, length)
                minVertex = queue.index(vertex)

        current, path = queue[minVertex]
        queue.remove(queue[minVertex])
        visited.append(current)

        if current == endVertex:
            # path.pop(0)
            # visited.pop(0)
            # visited.pop()
            printRes(visited, path)
            return

        for vertex in adjacencyList[current]:
            if vertex not in seen:
                seen.append(vertex)
                queue.append((vertex, path + [vertex]))


def Dijkstra(adjacencyList, startVertex, endVertex):
    seen = ([startVertex])
    queue = [(startVertex, [startVertex])]
    while queue:
        min = 90000000
        minVertex = 0
        for vertex in queue:
            if len(vertex[1]) < min:
                min = len(vertex[1])
                minVertex = queue.index(vertex)
        current, path = queue[minVertex]
        queue.remove(queue[minVertex])

        if current == endVertex:
            printRes(seen, path)
            return

        for vertex in adjacencyList[current]:
            if vertex in seen:
                if vertex in queue:
                    if len(queue[queue.index(vertex)]) > (len(path) + 1):
                        path.append(current)
                        queue[queue.index(vertex)] = path
            else:
                seen.append(vertex)
                queue.append((vertex, path + [vertex]))


def BFS(adjacencyList, startVertex, endVertex):
    seen = ([startVertex])
    queue = [(startVertex, [startVertex])]
    while queue:
        current, path = queue.pop(0)

        for vertex in adjacencyList[current]:
            if vertex == endVertex:
                # return seen , path + [vertex]
                path.append(vertex)
                printRes(seen, path)
                return
            if vertex not in seen:
                seen.append(vertex)
                queue.append((vertex, path + [vertex]))


def DFS(adjacencyList, startVertex, endVertex):
    seen = []
    stack = [(startVertex, [startVertex])]
    while stack:
        current, path = stack.pop()
        if current not in seen:
            if current == endVertex:
                path.append(vertex)
                printRes(seen, path)
                return
                # return path, visited
            seen.append(current)
            for vertex in adjacencyList[current]:
                stack.append((vertex, path + [vertex]))


def RandomSearch(adjacencyList, startVertex, endVertex):
    seen = ([startVertex])
    set = [(startVertex, [startVertex])]
    while set:
        current, path = set.pop(random.randint(0, len(set) - 1))
        for vertex in adjacencyList[current]:
            if vertex == endVertex:
                path.append(vertex)
                printRes(seen, path)
                return
            if vertex not in seen:
                seen.append(vertex)
                set.append((vertex, path + [vertex]))

def checkIfEndVertexEqualStartVertex(startVertex, endVertex):
    if startVertex == endVertex:
        printRes([startVertex],[endVertex])
        return True;
    return False;

def vertexToNumber(vertex, length):
    return vertex[0] * length + vertex[1]


def numberToVertex(number, length):
    y = number // length
    x = number % length
    return y, x

def findNeighbours(matrix, vertex):
    length = len(matrix[0])

    neighbours = [[vertex[0] - 1, vertex[1]], [vertex[0] + 1, vertex[1]],
                  [vertex[0], vertex[1] - 1], [vertex[0], vertex[1] + 1]]
    result = []
    for neighbour in neighbours:
        if (matrix[neighbour[0]][neighbour[1]] == freeVertex):
            result.append(vertexToNumber([neighbour[0], neighbour[1]], length))

    return result

while True:
    cls()

    print("Write number 0 - 6 for:")
    print("0. Exit program")
    print("1. Random search")
    print("2. BFS")
    print("3. DFS")
    print("4. Dijkstra")
    print("5. Greedy search")
    print("6. A*")

    inp = input()

    if inp == "0":
        quit(0)

    fileName = input("Write number of file (without '.txt'). Every number is different maze"
                     "(examples: 0, 2, 4, 5, 26 - all maps can be found in \"dataset\" directory)")
    fileName.strip()
    fileName = "dataset/" + fileName + ".txt"

    with open(fileName, "r") as file:
        numberOfLines, length = numberOfLinesAndLength()

        print("lenght of line, and number of lines ", length, numberOfLines - 2)
        matrix = [[0 for i in range(length)] for j in range(numberOfLines - 2)]

        cnt = 0
        for line in file:

            if (line[0] == 'X'):
                line = line.rstrip()
                charCnt = 0
                for char in line:
                    matrix[cnt][charCnt] = char
                    charCnt += 1
                cnt += 1

            else:
                line = line.split(' ')
                startVertex = int(line[2].strip()), int(line[1].strip(',').strip())
                line = file.readline()
                line = line.split(' ')
                endVertex = int(line[2].strip()), int(line[1].strip(',').strip())

                startVertex = vertexToNumber(startVertex, length)
                endVertex = vertexToNumber(endVertex, length)
                break

    adjacencyList = {}

    for i in range(1, numberOfLines - 3):
        for j in range(1, length - 1):
            if (matrix[i][j] == freeVertex):
                neighbours = list(findNeighbours(matrix, [i, j]))
                adjacencyList.update({vertexToNumber([i, j], length): neighbours})

    changeAndPrintMatrix(startVertex, "S")
    changeAndPrintMatrix(endVertex, "E")

    if checkIfEndVertexEqualStartVertex(startVertex, endVertex):
        inp = 0

    if inp == "1":
        RandomSearch(adjacencyList, startVertex, endVertex)
    if inp == "2":
        BFS(adjacencyList, startVertex, endVertex)
    if inp == "3":
        DFS(adjacencyList, startVertex, endVertex)
    if inp == "4":
        Dijkstra(adjacencyList, startVertex, endVertex)
    if inp == "5":
        GreedySearch(adjacencyList, startVertex, endVertex, len(matrix[0]))
    if inp == "6":
        AStar(adjacencyList, startVertex, endVertex, len(matrix[0]))

    input("Hit enter for another run")
