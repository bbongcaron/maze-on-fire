from tkinter import *
from sys import *
import pandas as pd
from random import random

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

def render(maze):
    root = Tk()
    root.title("This Maze is on Fire")
    # This! Maze is on fi-yaaaa-a-a-a-a
    for i in range(len(maze)):
        # White = empty, Black = filled
        # Adjust for loop to skip top left corner (0,0)
        if i == 0:
            Label(root,width=6, height=3,bg="white",relief="sunken",text="S").grid(row=0,column=0)
            for j in range(1, len(maze[0])):
                if maze[i][j]:
                    Label(root,width=6, height=3,bg="white",relief="sunken").grid(row=i,column=j)
                else:
                    Label(root,width=6, height=3,bg="black",relief="sunken").grid(row=i,column=j)
        # Adjust for loop to skip bottom right corner (dim, dim)
        elif i == len(maze) - 1:
            Label(root,width=6, height=3,bg="white",relief="sunken",text="G").grid(row=i,column=j)
            for j in range(len(maze[0]) - 1):
                if maze[i][j]:
                    Label(root,width=6, height=3,bg="white",relief="sunken").grid(row=i,column=j)
                else:
                    Label(root,width=6, height=3,bg="black",relief="sunken").grid(row=i,column=j)
        # For loop for "normal" rows without the Start or Goal space
        else:
            for j in range(len(maze[0])):
                if maze[i][j]:
                    Label(root,width=6, height=3,bg="white",relief="sunken").grid(row=i,column=j)
                else:
                    Label(root,width=6, height=3,bg="black",relief="sunken").grid(row=i,column=j)
        # Having two different for loops cases avoids checking if (i,j) is (0,0) or (dim,dim) on
        # every iteration of a single inner for loop and only checks once per row (instead of
        # once per element)
    root.mainloop()

def main():
    occProbability = float(argv[2])
    if occProbability >= 1 or occProbability <= 0:
        print("Invalid p. [0 < p < 1].")
        return
    dim = int(argv[1])
    maze = buildMaze(dim, occProbability)
    render(maze)

if __name__ == '__main__':
    main()
