from maze import *
import pygame, numpy
size = 600

##
#   Draws the unsolved maze.
#
#   @param window The pygame window which will be drawn on
#   @param maze The populated matrix representing the maze
##
def grid(window, maze):
    window.fill((255,255,255))
    dim = len(maze)
    spaceDim = size // dim
    x = 0
    y = 0
    for row in maze:
        for space in row:
            newSpace = pygame.Rect(x, y, spaceDim, spaceDim)
            # Color in obstacles
            if space == 0:
                pygame.draw.rect(window, (0,0,0), newSpace, width=0)
                pygame.draw.rect(window, (0,0,0), newSpace, width=1)
            # Color in empty spaces
            elif space == 1:
                pygame.draw.rect(window, (255,255,255), newSpace, width=0)
                pygame.draw.rect(window, (0,0,0), newSpace, width=1)
            # Color in the starting fire
            elif space == 2:
                pygame.draw.rect(window, (255,0,0), newSpace, width=0)
                pygame.draw.rect(window, (0,0,0), newSpace, width=1)
            x += spaceDim
        y += spaceDim
        x = 0
    goalSpace = pygame.Rect(dim - 1 ,dim - 1, spaceDim, spaceDim)
    pygame.draw.rect(window, (255,255,0), newSpace, width=0)
    pygame.draw.rect(window, (0,0,0), newSpace, width=1)
    pygame.display.update()
##
#   A game loop implementing Strategy 2 for solving the maze.
#
#   @param window The pygame window which will be drawn on
#   @param maze The populated matrix representing the maze
##
def movementTwo(window, maze, firep, algorithm):
    dim = len(maze)
    spaceDim = size // dim
    # Starting agent location
    agentLocation = (0,0)
    # spacesTraveled - A dynamic visited list to be passed to DFS
    spacesTraveled = [agentLocation]
    # The "Game loop"
    while True:
        prev = None
        if algorithm == "dfs":
            prev = DFS(maze, agentLocation, spacesTraveled)
        elif algorithm == "bfs":
            prev = BFS(maze, agentLocation, spacesTraveled)[0]
        elif algorithm == "a*":
            prev = aStar(maze, agentLocation, spacesTraveled)[0]
        elif algorithm == "a*+":
            prev = aStarPlus(maze, agentLocation, spacesTraveled)[0]
        else:
            return
        currentSpace = (dim - 1, dim - 1)
        # If no more paths to goal are present, stop
        if prev is None:
            return True
        # While loop to find the next move for the agent
        while prev[currentSpace] != agentLocation:
            currentSpace = prev[currentSpace]
        # Color the previous space gray
        prevSpace = pygame.Rect(prev[currentSpace][1]*spaceDim, prev[currentSpace][0]*spaceDim, spaceDim, spaceDim)
        pygame.draw.rect(window, (150, 150, 150), prevSpace, width=0)
        pygame.draw.rect(window, (0,0,0), prevSpace, width=1)
        pygame.display.update()
        # Color the agent's new location blue
        newCurrent = pygame.Rect(currentSpace[1]*spaceDim, currentSpace[0]*spaceDim, spaceDim,  spaceDim)
        pygame.draw.rect(window, (0,0,255), newCurrent, width=0)
        pygame.draw.rect(window, (0,0,0), newCurrent, width=1)
        pygame.display.update()
        # Update spacesTraveled and the agent's new location
        spacesTraveled.append(currentSpace)
        agentLocation = currentSpace
        ####################################################################
        #   Fire spread
        ####################################################################
        maze, newFires = fireSpread(maze, firep)
        # Color new fire spaces red
        for space in newFires:
            newFire = pygame.Rect(space[1]*spaceDim, space[0]*spaceDim, spaceDim, spaceDim)
            pygame.draw.rect(window, (255,0,0), newFire, width=0)
            pygame.draw.rect(window, (0,0,0), newFire, width=1)
            pygame.display.update()
        time.sleep(0.15)
        # Agent dies if it catches on fire
        if agentLocation in newFires:
            return True
        # Return if at the Goal
        if agentLocation == (dim - 1, dim - 1):
            return True
##
#   Driver function
#
#   @argv[1] The dimension of the dim by dim maze
#   @argv[2] The probability that a matrix cell will be occupied (0 < p < 1)
#   @argv[3] The flammability rate (0 <= q <= 1)
#   @argv[4] The search algorithm to be performed (DFS, BFS, A*)
##
def main():
    # Command line arguments check
    if float(argv[2]) <= 0 or float(argv[2]) >= 1:
        print("Invalid occupancy probability.\nExiting...")
        return
    elif float(argv[3]) < 0 or float(argv[3]) > 1:
        print("Invalid flammability rate.\nExiting...")
        return
    elif argv[4].lower() not in ['dfs', 'bfs', 'a*', 'a*+']:
        print("Invalid search algorithm. Must be DFS, BFS, or A* (case-insensitive).\nExiting...")
        return
    dim = int(argv[1])
    occProbability = float(argv[2])
    firep = float(argv[3])
    algorithm = argv[4]
    # Generate a random maze
    maze = buildMaze(dim, occProbability, firep)
    window = pygame.display.set_mode((size,size))
    show = True
    # Build the maze grid
    grid(window, maze)
    spaceDim = size // dim
    # Color the agent's starting space blue
    origin = pygame.Rect(0, 0, spaceDim, spaceDim)
    pygame.draw.rect(window, (0,0,255), origin, width=0)
    pygame.draw.rect(window, (0,0,0), origin, width=1)
    pygame.display.update()

    attemptedPath = False
    # Overall window loop
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show = False
            if not attemptedPath:
                attemptedPath = movementTwo(window, maze, firep, algorithm.lower())
if __name__ == '__main__':
    main()
