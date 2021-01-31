from maze import *
import pygame, numpy
size = 600
def visualAstar(window, maze, start=(0,0), spacesTraveled=[]):
    spaceDim = size // len(maze)
    fringeNodes = [start]
    distances = [0]
    distance = {}
    visited = []
    for alreadyVisited in spacesTraveled:
        visited.append(alreadyVisited)
    prev = {start : None}
    nodesExplored = 0
    start_time = time.time()
    while fringeNodes:
        # Find the node which has the lowest distance to the goal
        lowestDistance = 0
        closestNode = (0,0)
        for key in distance:
            lowestDistance = min(distance[key], lowestDistance)
            if lowestDistance == distance[key]:
                closestNode = key
        currentRow = closestNode[0]

        (currentRow, currentCol) = fringeNodes.remove(closestNode)
        ####################### Visualize node just popped from fringe
        expandedNode = pygame.Rect(currentCol*spaceDim, currentRow*spaceDim, spaceDim, spaceDim)
        distances.pop(index)
        pygame.draw.rect(window, (150,150,150), expandedNode, width=0)
        pygame.draw.rect(window, (0,0,0), expandedNode, width=1)
        pygame.display.update()

        #######################
        nodesExplored += 1
        #################################################################################################
        # Check the current condition of the child. If it's the goal, done. If not, find more children. #
        #################################################################################################
        if (currentRow, currentCol) == (len(maze) - 1, len(maze) - 1):
            end_time = time.time()
            elapsed_time = end_time - start_time
            return prev, nodesExplored
        #rightChild
        if isValid(maze, (currentRow, currentCol + 1)) and ((currentRow, currentCol + 1) not in visited and (currentRow, currentCol + 1) not in fringeNodes):
            x_squared = pow((len(maze) - 1) - (currentCol + 1), 2)
            y_squared = pow((len(maze) - 1) - (currentRow), 2)
            nodeDistance = math.sqrt(x_squared + y_squared)
            fringeNodes.append((currentRow, currentCol + 1))
            distances.append(nodeDistance)
            prev.update({(currentRow, currentCol + 1) : (currentRow, currentCol)})
        #downChild
        if isValid(maze, (currentRow + 1, currentCol)) and ((currentRow + 1, currentCol) not in visited and (currentRow + 1, currentCol) not in fringeNodes):
            x_squared = pow((len(maze) - 1) - (currentCol), 2)
            y_squared = pow((len(maze) - 1) - (currentRow + 1), 2)
            nodeDistance = math.sqrt(x_squared + y_squared)
            fringeNodes.append((currentRow + 1, currentCol))
            distances.append(nodeDistance)
            prev.update({(currentRow + 1, currentCol) : (currentRow, currentCol)})
        #leftChild
        if isValid(maze, (currentRow, currentCol - 1)) and ((currentRow, currentCol - 1) not in visited and (currentRow, currentCol - 1) not in fringeNodes):
            x_squared = pow((len(maze) - 1) - (currentCol - 1), 2)
            y_squared = pow((len(maze) - 1) - (currentRow), 2)
            nodeDistance = math.sqrt(x_squared + y_squared)
            fringeNodes.append((currentRow, currentCol - 1))
            distances.append(nodeDistance)
            prev.update({(currentRow, currentCol - 1) : (currentRow, currentCol)})
        #upChild
        if isValid(maze, (currentRow - 1, currentCol)) and ((currentRow - 1, currentCol) not in visited and (currentRow - 1, currentCol) not in fringeNodes):
            x_squared = pow((len(maze) - 1) - (currentCol), 2)
            y_squared = pow((len(maze) - 1) - (currentRow - 1), 2)
            nodeDistance = math.sqrt(x_squared + y_squared)
            fringeNodes.append((currentRow - 1, currentCol))
            distances.append(nodeDistance)
            prev.update({(currentRow - 1, currentCol) : (currentRow, currentCol)})
        visited.append((currentRow, currentCol))
    return None, nodesExplored
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
def movementTwo(window, maze, firep):
    dim = len(maze)
    spaceDim = size // dim
    # Starting agent location
    agentLocation = (0,0)
    # spacesTraveled - A dynamic visited list to be passed to DFS
    spacesTraveled = [agentLocation]
    # The "Game loop"
    while True:
        prev = DFS(maze, agentLocation, spacesTraveled)
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

def tracePath(window, maze, prev):
    dim = len(maze)
    spaceDim = size // dim
    # prev is None when a search algorithm has failed to find a path
    if prev is None:
        #print("No solution")
        return
    # Loop and count the number of moves in the path found by the search algorithm
    currentSpace = (len(maze) - 1, len(maze) - 1)
    while currentSpace != (0,0):
        currentSpace = prev[currentSpace]
        pathSpace = pygame.Rect(currentSpace[1]*spaceDim, currentSpace[0]*spaceDim, spaceDim, spaceDim)
        pygame.draw.rect(window, (0,255,0), pathSpace, width=0)
        pygame.draw.rect(window, (0,0,0), pathSpace, width=1)
        time.sleep(0.05)
        pygame.display.update()
    # Loop and label the moves taken in order
    #print("Success")
    return
##

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
    #elif argv[4].lower() not in ['dfs', 'bfs', 'a*']:
     #   print("Invalid search algorithm. Must be DFS, BFS, or A* (case-insensitive).\nExiting...")
     #   return
    dim = int(argv[1])
    occProbability = float(argv[2])
    firep = float(argv[3])
    #algorithm = argv[4]
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
                #attemptedPath = movementTwo(window, maze, firep)
                prev = visualAstar(window, maze)[0]
                #tracePath(window, maze, prev)
                attemptedPath = True
if __name__ == '__main__':
    main()
