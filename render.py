from maze import *
import pygame, numpy, copy
size = 360

def grid(window, maze, numMoves=None):
    dim = len(maze)
    spaceDim = size // dim
    x = 0
    y = 0
    if numMoves is not None:
        grayscale = numpy.linspace(20,240,numMoves,dtype='int')
    for row in maze:
        for space in row:
            newSpace = pygame.Rect(x, y, spaceDim, spaceDim)
            if space == 0:
                pygame.draw.rect(window, (0,0,0), newSpace, width=0)
                pygame.draw.rect(window, (0,0,0), newSpace, width=1)
            elif space == 1:
                pygame.draw.rect(window, (255,255,255), newSpace, width=0)
                pygame.draw.rect(window, (0,0,0), newSpace, width=1)
            elif space == 2:
                pygame.draw.rect(window, (255,0,0), newSpace, width=0)
                pygame.draw.rect(window, (0,0,0), newSpace, width=1)
            elif space == 3:
                pygame.draw.rect(window, (grayscale[numMoves-1], grayscale[numMoves-1], grayscale[numMoves-1]), newSpace, width=0)
                pygame.draw.rect(window, (0,0,0), newSpace, width=1)
                numMoves -= 1
            elif space == -1:
                pygame.draw.rect(window, (0,255,255), newSpace, width=0)
                pygame.draw.rect(window, (0,0,0), newSpace, width=1)
            x += spaceDim
        y += spaceDim
        x = 0
    goalSpace = pygame.Rect(dim - 1 ,dim - 1, spaceDim, spaceDim)
    pygame.draw.rect(window, (255,255,0), newSpace, width=0)
    pygame.draw.rect(window, (0,0,0), newSpace, width=1)

def path(window, maze, prev):
    returnMaze = copy.deepcopy(maze)
    dim = len(maze)
    spaceDim = size // dim
    # prev is None when a search algorithm has failed to find a path
    if prev is None:
        #print("No solution")
        return maze, None
    # Loop and count the number of moves in the path found by the search algorithm
    numMoves = 0
    currentSpace = (dim - 1, dim - 1)
    while currentSpace != (0,0):
        currentSpace = prev[currentSpace]
        returnMaze[currentSpace[0]][currentSpace[1]] = 3
        numMoves += 1
    return returnMaze, numMoves

def draw(window, maze):
    window.fill((255,255,255))
    grid(window, maze)
    pygame.display.update()

def movementTwo(window, maze, agentLocation):
    dim = len(maze)
    spaceDim = size // dim
    prev = DFS(maze, agentLocation)
    if prev is None:
        return agentLocation
    currentSpace = (dim - 1, dim - 1)
    while prev[currentSpace] != agentLocation:
        currentSpace = prev[currentSpace]

    newCurrent = pygame.Rect(currentSpace[1]*spaceDim, currentSpace[0]*spaceDim, spaceDim, spaceDim)
    pygame.draw.rect(window, (0,255,255), newCurrent, width=0)
    pygame.draw.rect(window, (0,0,0), newCurrent, width=1)
    pygame.display.update()
    time.sleep(0.2)

    prevSpace = pygame.Rect(prev[currentSpace][1]*spaceDim, prev[currentSpace][0]*spaceDim, spaceDim, spaceDim)
    pygame.draw.rect(window, (50, 50, 50), prevSpace, width=0)
    pygame.draw.rect(window, (0,0,0), prevSpace, width=1)
    pygame.display.update()
    return currentSpace


def render():
    maze = buildMaze(10, 0.15, 0.1)
    agentLocation = (0,0)
    maze[0][0] = -1

    rows = len(maze)

    window = pygame.display.set_mode((size,size))
    show = True
    draw(window, maze)

    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show = False
        agentLocation = movementTwo(window, maze, agentLocation)

if __name__ == '__main__':
    render()
