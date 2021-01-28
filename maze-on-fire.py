from tkinter import *
from sys import *
import pandas as pd
import math
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
#   Colors in the grid representing the maze with the appropriate colors.
#   Black : Space is invalid to move onto -> maze[i][j] = 0
#   White : Space is valid to move onto -> maze[i][j] = 1
#
#   @param root The tkinter container that holds the maze
#   @param maze The populated matrix representing the maze
##
def colorGrid(root, maze):
    # Offset from the top of the window in grid units
    verticalOffset = 1
    cellWidth = 4
    cellHeight = 2
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
#   Renders the established maze GUI.
#
#   @param maze The populated matrix representing the maze
#   @param p The probability that a matrix cell will be occupied (0 < p < 1)
##
def render(maze, p):
    root = Tk()
    root.title("This Maze is on Fire")
    # This! Maze is on fi-yaaaa-a-a-a-a
    ##
    #   Builds a completely new maze with the same probability of a cell being occupied
    #   as the original maze.
    ##
    def reset():
        newMaze = buildMaze(len(maze), p)
        colorGrid(root,newMaze)
    # Reset button widget to generate a new maze
    reset_button = Button(root, text="New Maze", command=reset)
    reset_button.grid(row=0, column=0, columnspan=2)
    colorGrid(root, maze)
    root.mainloop()

def main():
    occProbability = float(argv[2])
    if occProbability >= 1 or occProbability <= 0:
        print("Invalid p. [0 < p < 1].")
        return
    dim = int(argv[1])
    maze = buildMaze(dim, occProbability)
    render(maze, occProbability)

if __name__ == '__main__':
    main()
