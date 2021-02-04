from render import *
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
##
#   Performs a Depth-First Search on the maze starting at (0,0) to seek the fire space.
#
#   @param maze The populated matrix representing the maze
#   @param start The start position of the search, default is (0,0)
##
def findPathtoFire(maze, start=(0,0)):
    # Finds the fire space in the maze
    def findFire(maze):
        for r, row in enumerate(maze):
            for c, col in enumerate(row):
                if maze[r][c] == 2:
                    return (r,c)
        return None
    # Tests if a space is not obstructed (as opposed to valid to move on to)
    def isNotObstructed(maze, coordinate):
        if coordinate[0] < 0 or coordinate[0] >= len(maze) or coordinate[1] < 0 or coordinate[1] >= len(maze):
            return False
        if maze[coordinate[0]][coordinate[1]] != 0:
            return True
        return False
    # If there is no existing fire space, there is no path from start to fire space
    if findFire(maze) is None:
        return False
    fringe = [start]
    visited = []
    prev = {start : None}
    start_time = time.time()
    while fringe:
        (currentRow, currentCol) = fringe.pop()
        ######################################
        # Check the children of currentState #
        ######################################
        if maze[currentRow][currentCol] == 2:
            end_time = time.time()
            elapsed_time = end_time - start_time
            #print(str(elapsed_time) + "s to find path with DFS")
            return prev
        #upChild
        if isNotObstructed(maze, (currentRow - 1, currentCol)) and (currentRow - 1, currentCol) not in visited:
            fringe.append((currentRow - 1, currentCol))
            prev.update({(currentRow - 1, currentCol) : (currentRow, currentCol)})
        #leftChild
        if isNotObstructed(maze, (currentRow, currentCol - 1)) and (currentRow, currentCol - 1) not in visited:
            fringe.append((currentRow, currentCol - 1))
            prev.update({(currentRow, currentCol - 1) : (currentRow, currentCol)})
        #downChild
        if isNotObstructed(maze, (currentRow + 1, currentCol)) and (currentRow + 1, currentCol) not in visited:
            fringe.append((currentRow + 1, currentCol))
            prev.update({(currentRow + 1, currentCol) : (currentRow, currentCol)})
        #rightChild
        if isNotObstructed(maze, (currentRow, currentCol + 1)) and (currentRow, currentCol + 1) not in visited:
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
#   Generates plotfor obstacle density p vs. probability that S can be reached from G (Problem 2)
#
#   @param dim The given dimension to construct the dim by dim matrix
#   @param numRunsPerP The number of times a maze is generated and tested for each obstacle density
##
def pVSsuccessRateDFS(dim, numRunsPerP):
    successRates = []
    obstacle_density = []
    p = 0.0
    while p < 1:
        obstacle_density.append(p)
        print("Currently testing p = " + str(p) + "...")
        isSuccess = [False for x in range(numRunsPerP)]
        for i in range(numRunsPerP):
            # Print percent progress
            percentDone = str((i+1)*100/numRunsPerP) + "% done..."
            print(percentDone, end="\r")
            # Build maze and test if DFS finds a path
            maze = buildMaze(dim, p)
            isSuccess[i] = performDFS(maze)
        numSuccesses = 0
        for result in isSuccess:
            if result:
                numSuccesses += 1
        successRate = float(numSuccesses / numRunsPerP)
        successRates.append(successRate)
        p = round(p + 0.1, 1)
    print("Searching and data analysis complete!")
    ## Plot building + settings
    fig, ax = plt.subplots(figsize=(12,8))
    plt.rcParams["figure.figsize"] = (40,40)
    ax.plot(obstacle_density, successRates, marker='o')
    ax.spines['left'].set_position(('data',0))
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_xlabel('Obstacle Density (p)')
    ax.set_ylabel("Probability that S can be reached from G")
    plt.xticks(np.arange(0.0, 1, 0.1))
    plt.grid(b=True, which='major')
    plt.minorticks_on()
    plt.title('Obstacle density p vs. Probability that S can be reached from G \n (in ' + str(numRunsPerP) + ' unique maze runs for each obstacle density)\n w/dim = ' + str(dim))
    # Label point coordinates above each point
    for xy in zip(obstacle_density, successRates):
        ax.annotate('(%s, %s)' % xy, xy=xy, xytext=(xy[0], xy[1]+0.01), xycoords='data')
    plt.show()
    return
##
#   Generates plot for obstacle density p vs. number of nodes explored by BFS - number of nodes explored
#   by A* (Problem 3)
#
#   @param dim The given dimension to construct the dim by dim matrix
#   @param numRunsPerP The number of times a maze is generated and tested for each obstacle density
##
def BFS_AstarVSp(dim, numRunsPerP):
    avgNodesBFS_Astar = []
    obstacle_density = []
    p = 0.0
    while p < 1:
        obstacle_density.append(p)
        currentSum = 0
        print("Currently testing p = " + str(p) + "...")
        for i in range(numRunsPerP):
            # Print percent progress
            percentDone = str((i+1)*100/numRunsPerP) + "% done..."
            print(percentDone, end="\r")
            maze = buildMaze(dim, p)
            nodesBFS = BFS(maze)[1]
            nodesAstar = aStar(maze)[1]
            currentSum += nodesBFS - nodesAstar
        avgNodesBFS_Astar.append(currentSum / numRunsPerP)
        p = round(p + 0.1, 1)
    print("Searching and data analysis complete!")
    ## Plot building + settings
    fig, ax = plt.subplots(figsize=(12,8))
    plt.rcParams["figure.figsize"] = (40,40)
    ax.plot(obstacle_density, avgNodesBFS_Astar, marker='o')
    ax.spines['left'].set_position(('data',0))
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    plt.xticks(np.arange(0.0, 1, 0.1))
    plt.grid(b=True, which='major')
    plt.minorticks_on()
    ax.set_xlabel('Obstacle Density (p)')
    ax.set_ylabel("number of nodes explored by BFS - number of nodes explored by A*")
    plt.title('Obstacle density p vs. number of nodes explored by BFS - number of nodes explored by A*\n (in ' + str(numRunsPerP) + ' unique maze runs for each obstacle density)\n w/dim = ' + str(dim))
    for xy in zip(obstacle_density, avgNodesBFS_Astar):
        ax.annotate('(%s, %s)' % xy, xy=xy, xytext=(xy[0], xy[1]+0.01), xycoords='data')
    plt.show()
##
#   Generates plot for flammability rate q vs. % success rate @q (Problem 6) for Strategy 1
#
#   @param dim The given dimension to construct the dim by dim matrix
#   @param numRunsPerP The number of times a maze is generated and tested for each obstacle density
##
def strategyOneWinsVSflammability(dim, numRunsPerQ):
    averageSuccesses = []
    flammability = []
    p = 0.3
    q = 0.0
    while q < 1:
        flammability.append(q)
        currentWins = 0
        print("Currently testing q = " + str(q) + "...")
        # Make maze window
        window = pygame.display.set_mode((size,size))
        for i in range(numRunsPerQ):
            # Generate a random maze
            maze = buildMaze(dim, p, q)
            # Throw maze out if there is no path from start to goal or start to fire
            while DFS(maze) is None or findPathtoFire(maze) is None:
                maze = buildMaze(dim, p, q)
            # Color maze on pygame window
            grid(window, maze)
            # Shortest path => a*
            if movementOne(window, maze, q, 'a*') is True:
                currentWins += 1
            # Print percent progress
            percentDone = str((i+1)*100/numRunsPerQ) + "% done..."
            print(percentDone, end="\r")
        print("\t" + str(currentWins) + " sucesses on q = " + str(q) + "!")
        avgForThisQ = currentWins / numRunsPerQ
        print("\tsuccessRate = " + str(avgForThisQ*100) + "% for q = " + str(q) + ".")
        averageSuccesses.append(avgForThisQ*100)
        q = round(q + 0.1, 1)
    print(averageSuccesses)
    print(flammability)
    print("Searching and data analysis complete!")
    pygame.display.quit()
    ## Plot building + settings
    fig, ax = plt.subplots(figsize=(12,8))
    plt.rcParams["figure.figsize"] = (40,40)
    ax.plot(flammability, averageSuccesses, marker='o')
    ax.spines['left'].set_position(('data',0))
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    plt.xticks(np.arange(0.0, 1, 0.1))
    plt.grid(b=True, which='major')
    plt.minorticks_on()
    ax.set_xlabel('Flammability Rate (q)')
    ax.set_ylabel("% Success Rate")
    plt.title('[STRATEGY 1] Flammability Rate q vs. % Success Rate\n (in ' + str(numRunsPerQ) + ' unique maze runs for each flammability rate)\n w/dim = ' + str(dim) + " and p = 0.3")
    for xy in zip(flammability, averageSuccesses):
        ax.annotate('(%s, %s)' % xy, xy=xy, xytext=(xy[0], xy[1]+0.01), xycoords='data')
    plt.show()
##
#   Generates plot for flammability rate q vs. % success rate @q (Problem 6) for Strategy 2
#
#   @param dim The given dimension to construct the dim by dim matrix
#   @param numRunsPerP The number of times a maze is generated and tested for each obstacle density
##
def strategyTwoWinsVSflammability(dim, numRunsPerQ):
    averageSuccesses = []
    flammability = []
    p = 0.3
    q = 0.0
    while q < 1:
        flammability.append(q)
        currentWins = 0
        print("Currently testing q = " + str(q) + "...")
        # Make maze window
        window = pygame.display.set_mode((size,size))
        for i in range(numRunsPerQ):
            # Generate a random maze
            maze = buildMaze(dim, p, q)
            # Throw maze out if there is no path from start to goal or start to fire
            while DFS(maze) is None or findPathtoFire(maze) is None:
                maze = buildMaze(dim, p, q)
            # Color maze on pygame window
            grid(window, maze)
            # Shortest path => a*
            if movementTwo(window, maze, q, 'a*') is True:
                currentWins += 1
            # Print percent progress
            percentDone = str((i+1)*100/numRunsPerQ) + "% done..."
            print(percentDone, end="\r")
        print("\t" + str(currentWins) + " sucesses on q = " + str(q) + "!")
        avgForThisQ = currentWins / numRunsPerQ
        print("\tsuccessRate = " + str(avgForThisQ*100) + "% for q = " + str(q) + ".")
        averageSuccesses.append(avgForThisQ*100)
        q = round(q + 0.1, 1)
    print(averageSuccesses)
    print(flammability)
    print("Searching and data analysis complete!")
    pygame.display.quit()
    ## Plot building + settings
    fig, ax = plt.subplots(figsize=(12,8))
    plt.rcParams["figure.figsize"] = (40,40)
    ax.plot(flammability, averageSuccesses, marker='o')
    ax.spines['left'].set_position(('data',0))
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    plt.xticks(np.arange(0.0, 1, 0.1))
    plt.grid(b=True, which='major')
    plt.minorticks_on()
    ax.set_xlabel('Flammability Rate (q)')
    ax.set_ylabel("% Success Rate")
    plt.title('[STRATEGY 2] Flammability Rate q vs. % Success Rate\n (in ' + str(numRunsPerQ) + ' unique maze runs for each flammability rate)\n w/dim = ' + str(dim) + " and p = 0.3")
    for xy in zip(flammability, averageSuccesses):
        ax.annotate('(%s, %s)' % xy, xy=xy, xytext=(xy[0], xy[1]+0.01), xycoords='data')
    plt.show()
##
#   Driver function
#
#   @argv[1] The dimension of the dim by dim maze
#   @argv[2] The number of times a maze is generated and tested for each independent variable value
##
def main():
    dim = int(argv[1])
    numRunsPerX = int(argv[2])
    if dim < 1:
        print("Dimension is too small to generate a maze.")
    print("Please select which data to analyze.")
    print("\t1. Obstacle Density p vs. Probability that S can be reached from G [Problem 2]")
    print("\t2. Obstacle Density p vs. (# nodes explored w/BFS - # nodes explored w/A*) [Problem 3]")
    print("\t3. Strategy 1: Flammability q vs. % Success Rate @p = 0.3 [Problem 6]")
    print("\t4. Strategy 2: Flammability q vs. % Success Rate @p = 0.3 [Problem 6]")
    print("\t5. Strategy 3: Flammability q vs. % Success Rate @p = 0.3 [Problem 6]\n")
    selection = int(input("Your Selection > "))
    if selection == 1:
        pVSsuccessRateDFS(dim, numRunsPerX)
    elif selection == 2:
        BFS_AstarVSp(dim, numRunsPerX)
    elif selection == 3:
        strategyOneWinsVSflammability(dim, numRunsPerX)
    elif selection == 4:
        strategyTwoWinsVSflammability(dim, numRunsPerX)

if __name__ == '__main__':
    print("\nTo render and debug a singular maze, run 'render.py'.\nContinuing...\n")
    main()
