from tkinter import *
from sys import *
import pandas as pd
import math
import time
from random import random
##
#   Builds an n by n matrix of 0's and 1's representing a maze.
#   0 : Space is invalid to move onto -> occupied
#   1 : Space is valid to move onto -> empty
#
#   @param dim The given dimension to construct the dim by dim matrix
#   @param p The probability that a matrix cell will be occupied (0 < p < 1)
#   @return The populated matrix representing the maze
##
def buildMaze(dim, p):
    maze = [ [1 for col in range(dim)] for row in range(dim) ]
    for i in range(dim):
        for j in range(dim):
            rand = random()
            if rand <= p:
                maze[i][j] = 0
    # Ensure Start and Goal spaces are empty
    maze[0][0] = 1
    maze[dim - 1][dim - 1] = 1
    return maze
##
#   Colors the path found by the serach algorithm chosen with a grey color.
#   Starts coloring at Goal space and backtracks through previous spaces to reach Start space.
#
#   @param maze The populated matrix representing the maze
#   @param prev The populated dictionary representing the previously accessed space for all spaces
##
def tracePath(maze, prev):
    # prev is None when a search algorithm has failed to find a path
    if prev is None:
        #print("No solution")
        return
    # Loop and count the number of moves in the path found by the search algorithm
    numMoves = 0
    currentSpace = (len(maze) - 1, len(maze) - 1)
    while currentSpace != (0,0):
        currentSpace = prev[currentSpace]
        numMoves += 1
    # Loop and label the moves taken in order
    #print("Success")
    return numMoves
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
    if maze[coordinate[0]][coordinate[1]] == 0:
        return False
    return True
##
#   Performs a Depth-First Search on the maze starting at (0,0) to seek the Goal space.
#
#   @param maze The populated matrix representing the maze
##
def DFS(maze):
    fringe = [(0,0)]
    visited = []
    prev = {(0,0) : None}
    start_time = time.time()
    while fringe:
        (currentRow, currentCol) = fringe.pop()
        ######################################
        # Check the children of currentState #
        ######################################
        if (currentRow, currentCol) == (len(maze) - 1, len(maze) - 1):
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
##
def BFS(maze):
    fringe = [(0,0)]
    visited = []
    prev = {(0,0) : None}
    start_time = time.time()
    while fringe:
        (currentRow, currentCol) = fringe.pop(0)
        #takes off the first position coordinate off of fringe, acts as dequeue.
        #####################################
        # Checks the condition of the child #
        #####################################
        if (currentRow, currentCol) == (len(maze) - 1, len(maze) - 1):
            end_time = time.time()
            elapsed_time = end_time - start_time
            #print(str(elapsed_time) + "s to find path with DFS")
            return prev
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
    return None
##
#   Starts DFS
#
#   @param maze The populated matrix representing the maze
##
def performDFS(maze):
    prev = DFS(maze)
    steps = tracePath(maze, prev)
    if prev is None:
        return False
    return True
    #print(str(steps) + " steps taken to reach the end.")
##
#   Starts BFS
#
#   @param maze The populated matrix representing the maze
##
def performBFS(maze):
    prev = BFS(maze)
    steps = tracePath(maze,prev)
    print(str(steps) + " steps taken to reach the end.")
##
#   Driver function
##
def main():
    dim = int(argv[1])
    occProbability = float(argv[2])
    numRunsPerP = int(argv[3])
    if occProbability >= 1 or occProbability <= 0:
        print("Invalid p. [0 < p < 1].")
        return
    if dim < 1:
        print("Dimension is too small to generate a maze.")
        return
    p_vs_successRate = []
    p = occProbability
    while p < 1:
        print("Currently testing p = " + str(p) + "...")
        isSuccess = [False for x in range(numRunsPerP)]
        for i in range(numRunsPerP):
            maze = buildMaze(dim, p)
            isSuccess[i] = performDFS(maze)
            #print("\n")
            #performBFS(maze)
            #print("\n")
        numSuccesses = 0
        for result in isSuccess:
            if result:
                numSuccesses += 1
        successRate = float(numSuccesses / numRunsPerP)
        p_vs_successRate.append((p, successRate))
        p = round(p + 0.1, 1)
    for element in p_vs_successRate:
        print(element)

if __name__ == '__main__':
    main()
