from render import *
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
##
#   Generates data and plot for obstacle density p vs. probability that S can be reached from G (Problem 2)
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
    plt.title('Obstacle density p vs. Probability that S can be reached from G \n (in ' + str(numRunsPerP) + ' unique maze runs for each obstacle density)\n w/ dim = ' + str(dim))
    # Label point coordinates above each point
    for xy in zip(obstacle_density, successRates):
        ax.annotate('(%s, %s)' % xy, xy=xy, xytext=(xy[0], xy[1]+0.01), xycoords='data')
    plt.show()
    return

def BFS_AvsP():

##
#   Driver function
#
#   @argv[1] The dimension of the dim by dim maze
#   @argv[2] The number of times a maze is generated and tested for each obstacle density
#   @argv[3] The probability that fire will spread to an adjacent space
##
def main():
    dim = int(argv[1])
    numRunsPerP = int(argv[2])
    fireProbability = float(argv[3])
    if dim < 1:
        print("Dimension is too small to generate a maze.")
    pVSsuccessRateDFS(dim, numRunsPerP)

    # For now range(1), will be changed
    for i in range(1):
        print("Run #" + str(i+1))
        #maze = buildMaze(dim, occProbability, fireProbability)

if __name__ == '__main__':
    print("\nTo render and debug a singular maze, run 'render.py'.\nContinuing...\n")
    main()
