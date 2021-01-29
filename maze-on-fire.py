from tkinter import *
from sys import *
import pandas as pd
import math
import time
from random import random
cellWidth = 4
cellHeight = 2
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
#   @param root The tkinter container that holds the maze
#   @param maze The populated matrix representing the maze
##
def colorPath(root, maze, prev):
    # prev is None when a search algorithm has failed to find a path
    if prev is None:
        print("No solution")
        return
    # Loop and count the number of moves in the path found by the search algorithm
    numMoves = 0
    currentSpace = (len(maze) - 1, len(maze) - 1)
    while currentSpace != (0,0):
        currentSpace = prev[currentSpace]
        numMoves += 1
    # Loop and label the moves taken in order
    currentSpace = (len(maze) - 1, len(maze) - 1)
    # Label the Goal Space appropriately
    Label(root,width=cellWidth, height=cellHeight,text=str(numMoves) + " (G)",bg="grey",relief="sunken").grid(row=currentSpace[0],column=currentSpace[1])
    currentSpace = prev[currentSpace]
    numMoves -= 1
    # Loop through previous spaces until the Start space is reached
    while currentSpace != (0,0):
        Label(root,width=cellWidth, height=cellHeight,text=str(numMoves),bg="grey",relief="sunken").grid(row=currentSpace[0],column=currentSpace[1])
        currentSpace = prev[currentSpace]
        numMoves -= 1
    # Label the Start space appropriately
    Label(root,width=cellWidth, height=cellHeight,text=str(numMoves) + "(S)",bg="grey",relief="sunken").grid(row=currentSpace[0],column=currentSpace[1])
    print("Success")
    return
##
#   Colors in the grid representing the maze with the appropriate colors.
#   Black : Space is invalid to move onto -> maze[i][j] = 0
#   White : Space is valid to move onto -> maze[i][j] = 1
#
#   @param root The tkinter container that holds the maze
#   @param maze The populated matrix representing the maze
##
def colorGrid(root, maze):
    # Offset from the top of the window in grid units
    verticalOffset = 0
    for i in range(len(maze)):
        # White = empty, Black = filled
        # Adjust for loop to skip top left corner (0,0)
        if i == 0:
            Label(root,width=cellWidth, height=cellHeight,bg="white",relief="sunken",text="S").grid(row=0+verticalOffset,column=0)
            for j in range(1, len(maze[0])):
                if maze[i][j]:
                    Label(root,width=cellWidth, height=cellHeight,bg="white",relief="sunken").grid(row=i+verticalOffset,column=j)
                else:
                    Label(root,width=cellWidth, height=cellHeight,bg="black",relief="sunken").grid(row=i+verticalOffset,column=j)
        # Adjust for loop to skip bottom right corner (dim, dim)
        elif i == len(maze) - 1:
            Label(root,width=cellWidth, height=cellHeight,bg="white",relief="sunken",text="G").grid(row=i+verticalOffset,column=j)
            for j in range(len(maze[0]) - 1):
                if maze[i][j]:
                    Label(root,width=cellWidth, height=cellHeight,bg="white",relief="sunken").grid(row=i+verticalOffset,column=j)
                else:
                    Label(root,width=cellWidth, height=cellHeight,bg="black",relief="sunken").grid(row=i+verticalOffset,column=j)
        # For loop for "normal" rows without the Start or Goal space
        else:
            for j in range(len(maze[0])):
                if maze[i][j]:
                    Label(root,width=cellWidth, height=cellHeight,bg="white",relief="sunken").grid(row=i+verticalOffset,column=j)
                else:
                    Label(root,width=cellWidth, height=cellHeight,bg="black",relief="sunken").grid(row=i+verticalOffset,column=j)
        # Having three different for loops cases avoids checking if (i,j) is (0,0) or (dim,dim) on
        # every iteration of a single inner for loop and only checks once per row (instead of
        # once per element)
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
#   In addition, colors spaces of the maze grid that have been in the fringe at some point in time.
#
#   @param root The tkinter container that holds the maze
#   @param maze The populated matrix representing the maze
##
def DFS(root, maze):
    fringe = [(0,0)]
    visited = []
    prev = {(0,0) : None}
    Label(root,width=cellWidth, height=cellHeight,text="S",bg="light grey",relief="sunken").grid(row=0,column=0)
    start_time = time.time()
    while fringe:
        (currentRow, currentCol) = fringe.pop()
        ######################################
        # Check the children of currentState #
        ######################################
        if (currentRow, currentCol) == (len(maze) - 1, len(maze) - 1):
            Label(root,width=cellWidth, height=cellHeight, text="G", bg="light grey",relief="sunken").grid(row=currentRow,column=currentCol)
            end_time = time.time()
            print(str(end_time - start_time) + "s to find path with DFS")
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
        # Don't want to overwrite the "S" on the Start space
        if (currentRow, currentCol) != (0,0):
            Label(root,width=cellWidth, height=cellHeight,bg="light grey",relief="sunken").grid(row=currentRow,column=currentCol)
    return None
##
#   Performs a Breadth First Search at the maze, starting with (0,0) to seek the Goal space.
#
#
##
def BFS(root, maze):
    fringe = [(0,0)]
    visited = []
    prev = {(0,0) : None}
    Label(root,width=cellWidth, height=cellHeight,text="S",bg="light grey",relief="sunken").grid(row=0,column=0)
    start_time = time.time()
    while fringe:
        (currentRow, currentCol) = fringe.pop(0)
        #takes off the first position coordinate off of fringe, acts as dequeue.
        #####################################
        # Checks the condition of the child #
        #####################################
        if (currentRow, currentCol) == (len(maze) - 1, len(maze) - 1):
            Label(root,width=cellWidth, height=cellHeight, text="G", bg="light grey",relief="sunken").grid(row=currentRow,column=currentCol)
            end_time = time.time()
            print(str(end_time - start_time) + "s to find a path with BFS")
            return prev
        #rightChild
        if isValid(maze, (currentRow, currentCol + 1)) and (currentRow, currentCol + 1) not in visited:
            fringe.append((currentRow, currentCol + 1))
            prev.update({(currentRow, currentCol + 1) : (currentRow, currentCol)})
        #downChild
        if isValid(maze, (currentRow + 1, currentCol)) and (currentRow + 1, currentCol) not in visited:
            fringe.append((currentRow + 1, currentCol))
            prev.update({(currentRow + 1, currentCol) : (currentRow, currentCol)})
        #leftChild
        if isValid(maze, (currentRow, currentCol - 1)) and (currentRow, currentCol - 1) not in visited:
            fringe.append((currentRow, currentCol - 1))
            prev.update({(currentRow, currentCol - 1) : (currentRow, currentCol)})
        #upChild
        if isValid(maze, (currentRow - 1, currentCol)) and (currentRow - 1, currentCol) not in visited:
            fringe.append((currentRow - 1, currentCol))
            prev.update({(currentRow - 1, currentCol) : (currentRow, currentCol)})
        ###################################################################################################
        # Order is (right, down, left, up), the reverse of the DFS. Chosen so upon dequeuing (in this case
        # fringe.pop(0)), it will prioritize going towards the goal per layer of the search before looking
        # left or up.
        ###################################################################################################
        visited.append((currentRow, currentCol))
        #To not overwrite the "S" on the Start space
        if (currentRow, currentCol) != (0,0):
            Label(root, width=cellWidth, height=cellHeight, bg="light grey", relief="sunken").grid(row=currentRow,column=currentCol)
    return None
##
#   Renders the established maze GUI.
#
#   @param dim The
#   @param p The probability that a matrix cell will be occupied (0 < p < 1)
##
def render(dim, p):
    colSpan = 2
    maze = buildMaze(dim, p)
    root = Tk()
    root.title("This Maze is on Fire")
    # This! Maze is on fi-yaaaa-a-a-a-a
    ##
    #   Builds a completely new maze with the same probability of a cell being occupied
    #   as the original maze.
    ##
    def performDFS():
        colorGrid(root,maze)
        prev = DFS(root, maze)
        colorPath(root, maze, prev)
    # DFS button widget to perform DFS
    dfs_button = Button(root, width=cellWidth*colSpan, text="DFS", command=performDFS)
    dfs_button.grid(row=len(maze), column=2, columnspan=colSpan)
    def performBFS():
        colorGrid(root,maze)
        prev = BFS(root, maze)
        colorPath(root,maze,prev)
    # BFS button widget to perform BFS
    bfs_button = Button(root, width=cellWidth*colSpan, text="BFS", command=performBFS)
    bfs_button.grid(row=len(maze), column=4, columnspan=colSpan)
    def stop():
        root.destroy()
    stop_button = Button(root, width=cellWidth*colSpan, text="Close", command=stop)
    stop_button.grid(row=len(maze), column=0, columnspan=colSpan)

    colorGrid(root, maze)
    root.mainloop()
##
#   Driver function
##
def main():
    occProbability = float(argv[2])
    if occProbability >= 1 or occProbability <= 0:
        print("Invalid p. [0 < p < 1].")
        return
    dim = int(argv[1])
    if dim < 1:
        print("Dimension is too small to generate a maze.")
    render(dim, occProbability)

if __name__ == '__main__':
    main()
