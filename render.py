from maze import *
import pygame, numpy, copy
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
    pathColor = (30,30,30)
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
                pygame.draw.rect(window, pathColor, newSpace, width=0)
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
    pygame.display.update()
##
#   A game loop implementing Strategy 2 for solving the maze.
#
#   @param window The pygame window which will be drawn on
#   @param maze The populated matrix representing the maze
##
def movementTwo(window, maze):
    dim = len(maze)
    spaceDim = size // dim
    # Starting agent location
    agentLocation = (0,0)
    # spacesTraveled - A dynamic visited list to be passed to DFS
    spacesTraveled = [agentLocation]
    # Perform 1 DFS to see if there is a path in the first place
    if DFS(maze, agentLocation, spacesTraveled) is None:
        return True
    # The "Game loop"
    while True:
        prev = DFS(maze, agentLocation, spacesTraveled)
        currentSpace = (dim - 1, dim - 1)
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
        time.sleep(0.1)
        # Update spacesTraveled and the agent's new location
        spacesTraveled.append(currentSpace)
        agentLocation = currentSpace
        # Return if at the Goal
        if agentLocation == (dim - 1, dim - 1):
            return True

def main():
    maze = buildMaze(30, 0.25, 0.1)
    maze[0][0] = -1

    dim = len(maze)

    window = pygame.display.set_mode((size,size))
    show = True
    grid(window, maze)
    pygame.display.update()
    #origin = pygame.Rect(0, 0, size // dim, size // dim)
    #pygame.draw.rect(window, (0,255,255), origin, width=0)
    #pygame.draw.rect(window, (0,0,0), origin, width=1)
    attemptedPath = False
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show = False
            if not attemptedPath:
                attemptedPath = movementTwo(window, maze)


if __name__ == '__main__':
    main()
