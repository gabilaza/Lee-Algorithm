
import random
import pygame
pygame.font.init()

WIN_WIDTH = 600
WIN_HEIGHT = 600
SQUARE = 50
font = pygame.font.SysFont('ubuntumono', SQUARE//2)


def Ok(i, j):
    if i < 0 or j < 0 or i > WIN_HEIGHT//SQUARE-1 or j > WIN_WIDTH//SQUARE-1:
        return False
    return True


def draw_window(win, grid, color, obstacles, way, queue):
    win.fill((255, 255, 255))

    for pos in obstacles:
        text = font.render('#', True, (10, 10, 10))
        pygame.draw.rect(win, (235, 235, 235), (pos[1]*SQUARE, pos[0]*SQUARE, SQUARE, SQUARE))
        win.blit(text, (pos[1]*SQUARE + SQUARE//2 - text.get_width()//2, pos[0]*SQUARE + SQUARE//2 - text.get_height()//2))

    if queue != [] or grid[WIN_HEIGHT//SQUARE-1][WIN_WIDTH//SQUARE-1] == ' ':
        for i in range(WIN_HEIGHT//SQUARE):
            for j in range(WIN_WIDTH//SQUARE):
                if grid[i][j] != ' ':
                    text = font.render(str(grid[i][j]), True, (200, 200, 200))
                    pygame.draw.rect(win, color[grid[i][j]], (j*SQUARE, i*SQUARE, SQUARE, SQUARE))
                    win.blit(text, (j*SQUARE + SQUARE//2 - text.get_width()//2, i*SQUARE + SQUARE//2 - text.get_height()//2))
    else:
        for pos in way:
            i, j = pos
            if grid[i][j] != ' ':
                text = font.render(str(grid[i][j]), True, (200, 200, 200))
                pygame.draw.rect(win, color[grid[i][j]], (j * SQUARE, i * SQUARE, SQUARE, SQUARE))
                win.blit(text, (j*SQUARE + SQUARE//2 - text.get_width()//2, i*SQUARE + SQUARE//2 - text.get_height()//2))

    for i in range(1, WIN_WIDTH//SQUARE):
        pygame.draw.line(win, (0, 0, 0), (i*SQUARE, 0), (i*SQUARE, WIN_HEIGHT))
    for i in range(1, WIN_HEIGHT//SQUARE):
        pygame.draw.line(win, (0, 0, 0), (0, i*SQUARE), (WIN_WIDTH, i*SQUARE))
    pygame.draw.rect(win, (0, 0, 0), (0, 0, WIN_WIDTH, WIN_HEIGHT), 3)

    pygame.display.update()


def main():
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Lee')
    color = [(random.randint(10, 180), random.randint(10, 180), random.randint(10, 180)) for _ in range((WIN_WIDTH//SQUARE)*(WIN_HEIGHT//SQUARE))]
    color.insert(0, (20, 40, 60))
    color.insert(0, (0, 0, 0))
    grid = [[' ' for _ in range(WIN_WIDTH//SQUARE)] for _ in range(WIN_HEIGHT//SQUARE)]
    obstacles = [(random.randint(0, WIN_HEIGHT//SQUARE-1), random.randint(0, WIN_WIDTH//SQUARE-1)) for _ in range(random.randint((WIN_WIDTH//SQUARE)*2, (WIN_WIDTH//SQUARE)*4))]
    if (WIN_HEIGHT//SQUARE-1, WIN_WIDTH//SQUARE-1) in obstacles:
        obstacles.remove((WIN_HEIGHT//SQUARE-1, WIN_WIDTH//SQUARE-1))
    if (0, 0) in obstacles:
        obstacles.remove((0, 0))
    queue = [(0, 0)]
    way = [(WIN_HEIGHT//SQUARE-1, WIN_WIDTH//SQUARE-1)]
    cnt = -1
    grid[0][0] = 1

    run = True
    while run:
        clock.tick(45)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

                if event.key == pygame.K_r and (0, 0) in way:
                    color = [(random.randint(10, 180), random.randint(10, 180), random.randint(10, 180)) for _ in
                             range((WIN_WIDTH // SQUARE) * (WIN_HEIGHT // SQUARE))]
                    color.insert(0, (20, 40, 60))
                    color.insert(0, (0, 0, 0))
                    grid = [[' ' for _ in range(WIN_WIDTH // SQUARE)] for _ in range(WIN_HEIGHT // SQUARE)]
                    obstacles = [(random.randint(0, WIN_HEIGHT // SQUARE - 1), random.randint(0, WIN_WIDTH // SQUARE - 1)) for _ in range(random.randint((WIN_WIDTH // SQUARE) * 2, (WIN_WIDTH // SQUARE) * 4))]
                    if (WIN_HEIGHT // SQUARE - 1, WIN_WIDTH // SQUARE - 1) in obstacles:
                        obstacles.remove((WIN_HEIGHT // SQUARE - 1, WIN_WIDTH // SQUARE - 1))
                    if (0, 0) in obstacles:
                        obstacles.remove((0,0))
                    queue = [(0, 0)]
                    way = [(WIN_HEIGHT // SQUARE - 1, WIN_WIDTH // SQUARE - 1)]
                    cnt = -1
                    grid[0][0] = 1

        if queue != []:
            cnt += 1
            x, y = queue[0]

            if cnt == 0 and Ok(x-1, y) and grid[x-1][y] == ' ' and (x-1, y) not in obstacles:
                grid[x-1][y] = grid[x][y]+1
                queue.append((x-1, y))
            if cnt == 1 and Ok(x, y+1) and grid[x][y+1] == ' ' and (x, y+1) not in obstacles:
                grid[x][y+1] = grid[x][y] + 1
                queue.append((x, y+1))
            if cnt == 2 and Ok(x+1, y) and grid[x+1][y] == ' ' and (x+1, y) not in obstacles:
                grid[x+1][y] = grid[x][y] + 1
                queue.append((x+1, y))
            if cnt == 3 and Ok(x, y-1) and grid[x][y-1] == ' ' and (x, y-1) not in obstacles:
                grid[x][y-1] = grid[x][y] + 1
                queue.append((x, y-1))

            if cnt == 3:
                cnt = -1
                queue.remove(queue[0])
        elif queue == [] and grid[WIN_HEIGHT//SQUARE-1][WIN_WIDTH//SQUARE-1] != ' ' and (0, 0) not in way:
            x, y = way[-1]
            if Ok(x-1, y) and grid[x-1][y] != ' ' and grid[x][y] == grid[x-1][y]+1 and (x-1, y) not in obstacles:
                way.append((x-1, y))
            elif Ok(x, y+1) and grid[x][y+1] != ' ' and grid[x][y] == grid[x][y+1]+1 and (x, y+1) not in obstacles:
                way.append((x, y+1))
            elif Ok(x+1, y) and grid[x+1][y] != ' ' and grid[x][y] == grid[x+1][y]+1 and (x+1, y) not in obstacles:
                way.append((x+1, y))
            elif Ok(x, y-1) and grid[x][y-1] != ' ' and grid[x][y] == grid[x][y-1]+1 and (x, y-1) not in obstacles:
                way.append((x, y-1))


        draw_window(win, grid, color, obstacles, way, queue)


if __name__ == '__main__':
    main()
