import pygame
import heapq
import math

# Constants
ROWS, COLS = 20, 20  # Grid size
WIDTH, HEIGHT = 800, 800  # Window size
CELL_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Pathfinding Visualizer")

# Grid representation
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]  # 0 = empty, 1 = wall, 2 = start, 3 = end

# Start and end points
start = (0, 0)
end = (ROWS - 1, COLS - 1)
grid[start[0]][start[1]] = 2
grid[end[0]][end[1]] = 3

# Heuristic function (Euclidean distance)
def heuristic(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

# A* Algorithm
def a_star(grid, start, end):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == end:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), ]:  # 8-directional movement
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < ROWS and 0 <= neighbor[1] < COLS and grid[neighbor[0]][neighbor[1]] != 1:
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    # print()
    return None  # No path found

# Draw the grid
def draw_grid():
    for i in range(ROWS):
        for j in range(COLS):
            color = WHITE
            if grid[i][j] == 1:
                color = BLACK  # Wall
            elif grid[i][j] == 2:
                color = GREEN  # Start
            elif grid[i][j] == 3:
                color = RED  # End
            elif grid[i][j] == 4:
                color = BLUE  # Path
            elif grid[i][j] == 5:
                color = YELLOW  # Visited nodes
            pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.update()

# Main loop
running = True
path_found = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle mouse clicks
        if pygame.mouse.get_pressed()[0]:  # Left mouse button
            x, y = pygame.mouse.get_pos()
            row, col = y // CELL_SIZE, x // CELL_SIZE
            if (row, col) != start and (row, col) != end:
                grid[row][col] = 1  # Place wall
        elif pygame.mouse.get_pressed()[2]:  # Right mouse button
            x, y = pygame.mouse.get_pos()
            row, col = y // CELL_SIZE, x // CELL_SIZE
            if (row, col) != start and (row, col) != end:
                grid[row][col] = 0  # Remove wall

        # Handle key presses
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_SPACE and not path_found:  # Run A* algorithm
                path = a_star(grid, start, end)
                if path:
                    for node in path:
                        if node != start and node != end:
                            grid[node[0]][node[1]] = 4  # Mark path
                    path_found = True
                else:
                    print("no path found")

    draw_grid()

pygame.quit()