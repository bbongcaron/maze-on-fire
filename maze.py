from sys import *
import math, time, copy
from random import random, randrange
##
#   Builds an n by n matrix of 0's and 1's representing a maze.
#   0 : Space is invalid to move onto -> occupied
#   1 : Space is valid to move onto -> empty
#   2 : Space is on fire
#   @param dim The given dimension to construct the dim by dim matrix
#   @param p The probability that a matrix cell will be occupied (0 < p < 1)
#   @return The populated matrix representing the maze
#
#   Default firep = 0 so it does not interefere with vanilla DFS/BFS/A*
##
def buildMaze(dim, p, firep=0):
    maze = [ [1 for col in range(dim)] for row in range(dim) ]
    # Randomly arranges obstacles
    fireTile = False
    for i in range(dim):
        for j in range(dim):
            rand = random()
            if rand <= p:
                maze[i][j] = 0
    # Randomly selects a fire tile
    while True:
        randx = randrange(dim)
        randy = randrange(dim)
        if maze[randx][randy] == 1 and randx != 0 and randx != (dim - 1) and randy != 0 and randy != (dim - 1):
            maze[randx][randy] = 2
            break
    # Ensure Start and Goal spaces are empty
    maze[0][0] = 1
    maze[dim - 1][dim - 1] = 1
    return maze
##
#   Checks if a space in the maze is "valid".
#       => Is not an obstructed spaces
#       => Is not out of the bounds of the maze
#
#   @param maze The populated matrix representing the maze
#   @param coordinate The (row,column) tuple representing the space being checked
##
def isValid(maze, coordinate):
    if coordinate[0] < 0 or coordinate[0] >= len(maze) or coordinate[1] < 0 or coordinate[1] >= len(maze):
        return False
    if maze[coordinate[0]][coordinate[1]] == 1:
        return True
    return False
##
#   Performs a Depth-First Search on the maze starting at (0,0) to seek the Goal space.
#
#   @param maze The populated matrix representing the maze
#   @param start The start position of the search, default is (0,0)
##
def DFS(maze,start=(0,0),spacesTraveled=[], target=None):
    fringe = [start]
    visited = []
    for alreadyVisited in spacesTraveled:
        visited.append(alreadyVisited)
    prev = {start : None}
    if target is None:
        target = (len(maze) - 1, len(maze) - 1)
    start_time = time.time()
    while fringe:
        (currentRow, currentCol) = fringe.pop()
        ######################################
        # Check the children of currentState #
        ######################################
        if (currentRow, currentCol) == target:
            end_time = time.time()
            elapsed_time = end_time - start_time
            #print(str(elapsed_time) + "s to find path with DFS")
            return prev
        #upChild
        if isValid(maze, (currentRow - 1, currentCol)) and (currentRow - 1, currentCol) not in visited:
            fringe.append((currentRow - 1, currentCol))
            prev.update({(currentRow - 1, currentCol) : (currentRow, currentCol)})
        #leftChild
        if isValid(maze, (currentRow, currentCol - 1)) and (currentRow, currentCol - 1) not in visited:
            fringe.append((currentRow, currentCol - 1))
            prev.update({(currentRow, currentCol - 1) : (currentRow, currentCol)})
        #downChild
        if isValid(maze, (currentRow + 1, currentCol)) and (currentRow + 1, currentCol) not in visited:
            fringe.append((currentRow + 1, currentCol))
            prev.update({(currentRow + 1, currentCol) : (currentRow, currentCol)})
        #rightChild
        if isValid(maze, (currentRow, currentCol + 1)) and (currentRow, currentCol + 1) not in visited:
            fringe.append((currentRow, currentCol + 1))
            prev.update({(currentRow, currentCol + 1) : (currentRow, currentCol)})
        #################################################################################################
        # Order (up,left,down,right) chosen so that any moves to the right or down (which is closer # to
        # the Goal space, assuming no obstructions) are placed at the top of the stack and popped off
        # before any moves up or left.
        #################################################################################################
        visited.append((currentRow, currentCol))
    return None
##
#   Performs a Breadth First Search at the maze, starting with (0,0) to seek the Goal space.
#
#   @param maze The populated matrix representing the maze
#   @param start The start position of the search, default is (0,0)
##
def BFS(maze, start=(0,0), spacesTraveled=[]):
    fringe = [start]
    visited = []
    for alreadyVisited in spacesTraveled:
        visited.append(alreadyVisited)
    prev = {start : None}
    nodesExplored = 0
    start_time = time.time()
    while fringe:
        (currentRow, currentCol) = fringe.pop(0)
        nodesExplored += 1
        #takes off the first position coordinate off of fringe, acts as dequeue.
        #####################################
        # Checks the condition of the child #
        #####################################
        if (currentRow, currentCol) == (len(maze) - 1, len(maze) - 1):
            end_time = time.time()
            elapsed_time = end_time - start_time
            #print(str(elapsed_time) + "s to find path with DFS")
            return prev, nodesExplored
        #rightChild
        if isValid(maze, (currentRow, currentCol + 1)) and ((currentRow, currentCol + 1) not in visited and (currentRow, currentCol + 1) not in fringe):
            fringe.append((currentRow, currentCol + 1))
            prev.update({(currentRow, currentCol + 1) : (currentRow, currentCol)})
        #downChild
        if isValid(maze, (currentRow + 1, currentCol)) and ((currentRow + 1, currentCol) not in visited and (currentRow + 1, currentCol) not in fringe):
            fringe.append((currentRow + 1, currentCol))
            prev.update({(currentRow + 1, currentCol) : (currentRow, currentCol)})
        #leftChild
        if isValid(maze, (currentRow, currentCol - 1)) and ((currentRow, currentCol - 1) not in visited and (currentRow, currentCol - 1) not in fringe):
            fringe.append((currentRow, currentCol - 1))
            prev.update({(currentRow, currentCol - 1) : (currentRow, currentCol)})
        #upChild
        if isValid(maze, (currentRow - 1, currentCol)) and ((currentRow - 1, currentCol) not in visited and (currentRow - 1, currentCol) not in fringe):
            fringe.append((currentRow - 1, currentCol))
            prev.update({(currentRow - 1, currentCol) : (currentRow, currentCol)})
        ###################################################################################################
        # Order is (right, down, left, up), the reverse of the DFS. Chosen so upon dequeuing (in this case
        # fringe.pop(0)), it will prioritize going towards the goal per layer of the search before looking
        # left or up.
        ###################################################################################################
        visited.append((currentRow, currentCol))
    return None, nodesExplored
##
#   Performs an A* search algorithm to find the goal using the euclidean distance from node to the goal.
#
#   @param maze The populated matrix representing the maze
#   @param start The start position of the search, default is (0,0)
##
def aStar(maze, start=(0,0), spacesTraveled=[]):
    fringeNodes = [start]
    distances = [0]
    visited = []
    for alreadyVisited in spacesTraveled:
        visited.append(alreadyVisited)
    prev = {start: None}
    nodesExplored = 0
    start_time = time.time()
    while fringeNodes:
        # Find the node which has the lowest distance to the goal
        lowestDistance = min(distances)
        index = distances.index(lowestDistance)
        (currentRow, currentCol) = fringeNodes.pop(index)
        ####################### Visualize node just popped from fringe
        distances.pop(index)
        #######################
        nodesExplored += 1
        #################################################################################################
        # Check the current condition of the child. If it's the goal, done. If not, find more children. #
        #################################################################################################
        if (currentRow, currentCol) == (len(maze) - 1, len(maze) - 1):
            end_time = time.time()
            elapsed_time = end_time - start_time
            return prev, nodesExplored
        # rightChild
        if isValid(maze, (currentRow, currentCol + 1)) and ((currentRow, currentCol + 1) not in visited and (currentRow, currentCol + 1) not in fringeNodes):
            x_squared = pow((len(maze) - 1) - (currentCol + 1), 2)
            y_squared = pow((len(maze) - 1) - (currentRow), 2)
            nodeDistance = math.sqrt(x_squared + y_squared)
            fringeNodes.append((currentRow, currentCol + 1))
            distances.append(nodeDistance)
            prev.update({(currentRow, currentCol + 1): (currentRow, currentCol)})
        # downChild
        if isValid(maze, (currentRow + 1, currentCol)) and ((currentRow + 1, currentCol) not in visited and (currentRow + 1, currentCol) not in fringeNodes):
            x_squared = pow((len(maze) - 1) - (currentCol), 2)
            y_squared = pow((len(maze) - 1) - (currentRow + 1), 2)
            nodeDistance = math.sqrt(x_squared + y_squared)
            fringeNodes.append((currentRow + 1, currentCol))
            distances.append(nodeDistance)
            prev.update({(currentRow + 1, currentCol): (currentRow, currentCol)})
        # leftChild
        if isValid(maze, (currentRow, currentCol - 1)) and ((currentRow, currentCol - 1) not in visited and (currentRow, currentCol - 1) not in fringeNodes):
            x_squared = pow((len(maze) - 1) - (currentCol - 1), 2)
            y_squared = pow((len(maze) - 1) - (currentRow), 2)
            nodeDistance = math.sqrt(x_squared + y_squared)
            fringeNodes.append((currentRow, currentCol - 1))
            distances.append(nodeDistance)
            prev.update({(currentRow, currentCol - 1): (currentRow, currentCol)})
        # upChild
        if isValid(maze, (currentRow - 1, currentCol)) and ((currentRow - 1, currentCol) not in visited and (currentRow - 1, currentCol) not in fringeNodes):
            x_squared = pow((len(maze) - 1) - (currentCol), 2)
            y_squared = pow((len(maze) - 1) - (currentRow - 1), 2)
            nodeDistance = math.sqrt(x_squared + y_squared)
            fringeNodes.append((currentRow - 1, currentCol))
            distances.append(nodeDistance)
            prev.update({(currentRow - 1, currentCol): (currentRow, currentCol)})
        visited.append((currentRow, currentCol))
    return None, nodesExplored

def aStarPlus(maze, firep, start=(0,0), spacesTraveled=[]):
    fringeNodes = [start]
    distances = [0]
    visited = []
    #for alreadyVisited in spacesTraveled:
    #    visited.append(alreadyVisited)
    prev = {start: None}
    nodesExplored = 0
    start_time = time.time()
    def checkCost(maze, checkNode, direction, firep, spacesTraveled):
    # A helper function to help make any node being checked if it's dangerous or not by adding more cost based on
    # if it has a fire nearby or wall nearby.
        addedCost = 0
        if direction == "right":
            if (checkNode[0], checkNode[1]) in spacesTraveled:
                addedCost += 1
            addedCost += calcCost(maze, (checkNode[0], checkNode[1] + 1), firep)
            addedCost += calcCost(maze, (checkNode[0], checkNode[1] + 2), firep)
            addedCost += calcCost(maze, (checkNode[0] + 1, checkNode[1] + 1), firep)
            addedCost += calcCost(maze, (checkNode[0] - 1, checkNode[1] + 1), firep)
            addedCost += calcCost(maze, (checkNode[0] + 1, checkNode[1]), firep)
            addedCost += calcCost(maze, (checkNode[0] + 2, checkNode[1]), firep)
            addedCost += calcCost(maze, (checkNode[0] - 1, checkNode[1]), firep)
            addedCost += calcCost(maze, (checkNode[0] - 2, checkNode[1]), firep)
        if direction == "down":
            if (checkNode[0], checkNode[1]) in spacesTraveled:
                addedCost += 1
            addedCost += calcCost(maze, (checkNode[0] + 1, checkNode[1]), firep)
            addedCost += calcCost(maze, (checkNode[0] + 2, checkNode[1]), firep)
            addedCost += calcCost(maze, (checkNode[0] + 1, checkNode[1] + 1), firep)
            addedCost += calcCost(maze, (checkNode[0] + 1, checkNode[1] - 1), firep)
            addedCost += calcCost(maze, (checkNode[0], checkNode[1] + 1), firep)
            addedCost += calcCost(maze, (checkNode[0], checkNode[1] + 2), firep)
            addedCost += calcCost(maze, (checkNode[0], checkNode[1] - 1), firep)
            addedCost += calcCost(maze, (checkNode[0], checkNode[1] - 2), firep)
        if direction == "left":
            if (checkNode[0], checkNode[1]) in spacesTraveled:
                addedCost += 1
            addedCost += calcCost(maze, (checkNode[0], checkNode[1] - 1), firep)
            addedCost += calcCost(maze, (checkNode[0], checkNode[1] - 2), firep)
            addedCost += calcCost(maze, (checkNode[0] + 1, checkNode[1] - 1), firep)
            addedCost += calcCost(maze, (checkNode[0] - 1, checkNode[1] - 1), firep)
            addedCost += calcCost(maze, (checkNode[0] + 1, checkNode[1]), firep)
            addedCost += calcCost(maze, (checkNode[0] + 2, checkNode[1]), firep)
            addedCost += calcCost(maze, (checkNode[0] - 1, checkNode[1]), firep)
            addedCost += calcCost(maze, (checkNode[0] - 2, checkNode[1]), firep)
        if direction == "up":
            if (checkNode[0], checkNode[1]) in spacesTraveled:
                addedCost += 1
            addedCost += calcCost(maze, (checkNode[0] - 1, checkNode[1]), firep)
            addedCost += calcCost(maze, (checkNode[0] - 2, checkNode[1]), firep)
            addedCost += calcCost(maze, (checkNode[0] - 1, checkNode[1] - 1), firep)
            addedCost += calcCost(maze, (checkNode[0] - 1, checkNode[1] + 1), firep)
            addedCost += calcCost(maze, (checkNode[0], checkNode[1] + 1), firep)
            addedCost += calcCost(maze, (checkNode[0], checkNode[1] + 2), firep)
            addedCost += calcCost(maze, (checkNode[0], checkNode[1] - 1), firep)
            addedCost += calcCost(maze, (checkNode[0], checkNode[1] - 2), firep)
        return addedCost
    def calcCost(maze, coordinate, firep):
        spaceCost = 0
        fireCost = (firep * 100) + 3
        if isBurning(maze, (coordinate[0], coordinate[1])):
            spaceCost += fireCost
        if not isValid(maze, (coordinate[0], coordinate[1])):
            spaceCost += 1
        return spaceCost
    while fringeNodes:
        # Find the node which has the lowest distance to the goal
        lowestDistance = min(distances)
        index = distances.index(lowestDistance)
        (currentRow, currentCol) = fringeNodes.pop(index)
        ####################### Visualize node just popped from fringe
        distances.pop(index)
        #######################
        nodesExplored += 1
        #################################################################################################
        # Check the current condition of the child. If it's the goal, done. If not, find more children. #
        #################################################################################################
        if (currentRow, currentCol) == (len(maze) - 1, len(maze) - 1):
            end_time = time.time()
            elapsed_time = end_time - start_time
            return prev, nodesExplored
        # rightChild
        if isValid(maze, (currentRow, currentCol + 1)) and ((currentRow, currentCol + 1) not in visited and (currentRow, currentCol + 1) not in fringeNodes):
            x_squared = pow((len(maze) - 1) - (currentCol + 1), 2)
            y_squared = pow((len(maze) - 1) - (currentRow), 2)
            addedCost = checkCost(maze, (currentRow, currentCol + 1), "right", firep, spacesTraveled)
            nodeCost = math.sqrt(x_squared + y_squared) + addedCost
            fringeNodes.append((currentRow, currentCol + 1))
            distances.append(nodeCost)
            prev.update({(currentRow, currentCol + 1): (currentRow, currentCol)})
        # downChild
        if isValid(maze, (currentRow + 1, currentCol)) and ((currentRow + 1, currentCol) not in visited and (currentRow + 1, currentCol) not in fringeNodes):
            x_squared = pow((len(maze) - 1) - (currentCol), 2)
            y_squared = pow((len(maze) - 1) - (currentRow + 1), 2)
            addedCost = checkCost(maze, (currentRow + 1, currentCol), "down", firep, spacesTraveled)
            nodeCost = math.sqrt(x_squared + y_squared) + addedCost
            fringeNodes.append((currentRow + 1, currentCol))
            distances.append(nodeCost)
            prev.update({(currentRow + 1, currentCol): (currentRow, currentCol)})
        # leftChild
        if isValid(maze, (currentRow, currentCol - 1)) and ((currentRow, currentCol - 1) not in visited and (currentRow, currentCol - 1) not in fringeNodes):
            x_squared = pow((len(maze) - 1) - (currentCol - 1), 2)
            y_squared = pow((len(maze) - 1) - (currentRow), 2)
            addedCost = checkCost(maze, (currentRow, currentCol - 1), "left", firep, spacesTraveled)
            nodeCost = math.sqrt(x_squared + y_squared) + addedCost
            fringeNodes.append((currentRow, currentCol - 1))
            distances.append(nodeCost)
            prev.update({(currentRow, currentCol - 1): (currentRow, currentCol)})
        # upChild
        if isValid(maze, (currentRow - 1, currentCol)) and ((currentRow - 1, currentCol) not in visited and (currentRow - 1, currentCol) not in fringeNodes):
            x_squared = pow((len(maze) - 1) - (currentCol), 2)
            y_squared = pow((len(maze) - 1) - (currentRow - 1), 2)
            addedCost = checkCost(maze, (currentRow - 1, currentCol), "down", firep, spacesTraveled)
            nodeCost = math.sqrt(x_squared + y_squared) + addedCost
            fringeNodes.append((currentRow - 1, currentCol))
            distances.append(nodeCost)
            prev.update({(currentRow - 1, currentCol): (currentRow, currentCol)})
        visited.append((currentRow, currentCol))
    return None, nodesExplored

def isBurning(maze, coordinate):
        if coordinate[0] < 0 or coordinate[0] >= len(maze) or coordinate[1] < 0 or coordinate[1] >= len(maze):
            return False
        if maze[coordinate[0]][coordinate[1]] == 2:
            return True
        return False
##
#   Performs a probability check, seeing if a free tile will turn into fire depending on the number of fire neighbors
#   nearby.
##
def fireSpread(maze, fireProbability):
    newMaze = copy.deepcopy(maze)
    newFires = []
    for currentRow in range(len(maze)):
        for currentCol in range(len(maze)):
            if isValid(maze, (currentRow, currentCol)) and (currentRow, currentCol) not in newFires:
                k = 0
                if isBurning(maze, (currentRow - 1, currentCol)):
                    k += 1
                if isBurning(maze, (currentRow, currentCol - 1)):
                    k += 1
                if isBurning(maze, (currentRow + 1, currentCol)):
                    k += 1
                if isBurning(maze, (currentRow, currentCol + 1)):
                    k += 1
                fireProb = 1 - pow((1 - fireProbability),k)
                if random() <= fireProb:
                   newMaze[currentRow][currentCol] = 2
                   newFires.append((currentRow, currentCol))
    return newMaze, newFires

if __name__ == '__main__':
    print("To perform maze simulation, run 'simulate.py'.\nExiting...")
