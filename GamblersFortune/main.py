import pygame
import random

STARTING_BLUE_BLOBS = 10
STARTING_RED_BLOBS = 3
START_Y = 125
MAX_Y = 250
MIN_Y = 0
SCALE = 10

WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

MAX_STEPS = 1000

game_display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Testing")
clock = pygame.time.Clock()

class Blob:

    def __init__(self, color):
        self.x = random.randrange(0, WIDTH)
        self.y = random.randrange(0, HEIGHT)
        self.size = random.randrange(4, 8)
        self.color = color

    def move(self):
        self.move_x = random.randrange(-1, 2)
        self.move_y = random.randrange(-1, 2)
        self.x += self.move_x
        self.y += self.move_y

        if self.x < 0:
            self.x = 0
        elif self.x > WIDTH:
            self.x = WIDTH

        if self.y < 0:
            self.y = 0
        elif self.y > HEIGHT:
            self.y = HEIGHT



class Line:

    def __init__(self, color, start, end):
        self.start = start
        self.end = end
        self.color = color


def draw_environment(blobs):
    game_display.fill(WHITE)
    for blob in blobs:
        pygame.draw.circle(game_display, blob.color, [blob.x, blob.y], blob.size)
    pygame.display.update()
    [blob.move() for blob in blobs]


def draw_environment2(lines, count, step):
    game_display.fill(WHITE)
    for line in lines:
        pygame.draw.line(game_display, line.color, line.start, line.end)

    #f = pygame.font.Font(None, 20)
    #f.render("foo", True, [0, 0, 0], [255, 255, 255])
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    textsurface = myfont.render('{} / {}'.format(count, step), False, (0, 0, 0))
    game_display.blit(textsurface, (0, 0))
    pygame.display.update()


def stop(y, min_y, max_y):
    if y >= max_y:
        return True
    elif y <= min_y:
        return True
    else:
        return False


def propogate():
    scale_movements = SCALE

    lines = list()
    #lines.append(Line(RED, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2)))
    #lines.append(Line(GREEN, (0, HEIGHT // 2 - MAX_Y), (WIDTH, HEIGHT // 2 - MAX_Y)))
    y = HEIGHT // 2 - START_Y
    prev_y = y
    count = list()

    r = random.randrange(0, 255)
    g = random.randrange(0, 255)
    b = random.randrange(0, 255)

    for i in range(1, MAX_STEPS):
        y = random.choice([-1, 1]) * scale_movements
        lines.append(Line((r,g,b), (i - 1, prev_y), (i, prev_y + y)))
        prev_y = prev_y + y

        if stop(prev_y, HEIGHT // 2 - MAX_Y, HEIGHT // 2):
            if prev_y <= HEIGHT // 2 - MAX_Y:
                count.append(0)
            else:
                count.append(1)
            break
        else:
            count.append(0)

    return lines, prev_y >= (HEIGHT // 2), count


def main():
    blobs = [Blob(color=BLUE) for i in range(STARTING_BLUE_BLOBS)]
    blobs.extend([Blob(color=RED) for i in range(STARTING_RED_BLOBS)])

    bankrupt = False
    lines = list()
    count = list()
    total = 100

    for i in range(0, total):
        lines_temp, bankrupt, count_temp = propogate()
        count.extend(count_temp)
        lines.extend(lines_temp)

    print(sum(count)/total)

    step = 0

    default_lines = list()
    default_lines.append(Line(RED, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2)))
    default_lines.append(Line(GREEN, (0, HEIGHT // 2 - MAX_Y), (WIDTH, HEIGHT // 2 - MAX_Y)))
    final_lines = default_lines
    final_lines.extend(lines)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if step < len(lines):
            draw_environment2(final_lines[:step+2], sum(count[:step]), i + 1)
        else:
            draw_environment2(final_lines, sum(count), i + 1)
        clock.tick(60)
        step += 1

if __name__ == '__main__':
    pygame.font.init()
    main()
