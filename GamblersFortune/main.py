import pygame
import random
from scipy import stats

START_Y = 30
MAX_Y = 260
MIN_Y = 0
SCALE = 10
SPEED = 100

WIDTH = 800
HEIGHT = 600
BOTTOM_LINE_Y = HEIGHT // 2 + 100
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

MAX_STEPS = 1000
NUM_SIMULATIONS = 1000

WIN_PROBABILITY = 0.5

game_display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gambler's Ruin")
clock = pygame.time.Clock()


class Line:

    def __init__(self, color, start, end):
        self.start = start
        self.end = end
        self.color = color


def draw_environment(lines, count, step, theory):
    game_display.fill(WHITE)
    for line in lines:
        pygame.draw.line(game_display, line.color, line.start, line.end)

    denom = 1
    if step != 0:
        denom = step

    # Get the average number of steps
    avg_steps = (len(lines)-2)/denom

    myfont = pygame.font.SysFont('Comic Sans MS', 10)
    textsurface = myfont.render('{} / {} = {:.3f}, Total = {}, Win Prob. = {}, Start = {:.2f}, Min = {:.2f}, Max = {:.2f}, Avg. Steps = {:.2f}'.\
                                format(count, step, count/denom, NUM_SIMULATIONS, WIN_PROBABILITY, START_Y/SCALE,\
                                       MIN_Y/SCALE, MAX_Y/SCALE, avg_steps), False, (0, 0, 0))
    myfont_theory = pygame.font.SysFont('Comic Sans MS', 10)
    textsurface_theory = myfont_theory.render('Theory (bankrupt probability) = {:.4f} (to 4.d.p.)  Theory (Expected Steps) = {:.2f} (to 2.d.p.)'.\
                                format(theory[0], theory[1]), False, (0, 0, 0))
    game_display.blit(textsurface, (0, 0))

    game_display.blit(textsurface_theory, (0, 20))
    pygame.display.update()


def get_theory():
    theory = []
    k = START_Y/SCALE
    N = MAX_Y/SCALE

    # Get the bankrupt probability
    if WIN_PROBABILITY == 0.5:
        theory.append(1 - k / N)
    elif WIN_PROBABILITY == 0:
        theory.append(1)
    else:
        ratio = (1 - WIN_PROBABILITY)/WIN_PROBABILITY
        theory.append((pow(ratio, k) - pow(ratio, N))/(1 - pow(ratio, N)))

    # Get the expected number of steps
    if WIN_PROBABILITY == 0.5:
        theory.append(N*k - k**2)
    elif WIN_PROBABILITY == 0:
        theory.append(k)
    else:
        ratio = N/((2*WIN_PROBABILITY - 1)*(1-pow((1-WIN_PROBABILITY)/WIN_PROBABILITY, N)))
        theory.append(ratio*(1-pow((1-WIN_PROBABILITY)/WIN_PROBABILITY, k)) - k/(2*WIN_PROBABILITY-1))

    return theory


def stop(y, min_y, max_y):
    if y >= max_y:
        return True
    elif y <= min_y:
        return True
    else:
        return False


def propagate():
    scale_movements = SCALE

    lines = list()
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

    return lines, count


def get_next_value(p):
    '''
    A function which returns a 1 or a -1. p is the probability of obtaining a 1
    :param p: float between 0 and 1. The probability of success
    :return: integer. Either -1 or 1
    '''
    return stats.bernoulli.rvs(p)*2 - 1


def propagate(start, minimum, maximum):
    # This scales the movements to speed up the process
    scale_movements = SCALE

    # To contain the trajectory information
    lines = list()

    # This is the start. (0,0) is the top left of the screen. -start is actually +start in terms of value
    y = minimum - start

    # We need the previous y value in order to start the drawing of the next line from this point
    prev_y = y

    # This stores the steps where the value hit the min
    count = list()

    # Each simulation is to pick a random color for the trajectory
    r = random.randrange(0, 255)
    g = random.randrange(0, 255)
    b = random.randrange(0, 255)

    # Loop and randomly increase by 1 or decrease by 1
    for i in range(1, MAX_STEPS):
        # The value of y increases by 1 or decreases by 1 according to a bernoulli random variable. The step is then
        # scaled
        y = get_next_value(WIN_PROBABILITY) * scale_movements

        # Save a line to the lines list that starts from the previous position and ends at the current position
        lines.append(Line((r, g, b), (i - 1, prev_y), (i, prev_y - y)))

        # Save the previous position as this position
        prev_y = prev_y - y

        # If the current y value hits the min value, it is a bankrupt, if it hits the max value it is not a bankrupt
        if stop(prev_y, maximum, minimum):
            if prev_y <= maximum:
                count.append(0)
            else:
                count.append(1)
            break
        else:
            count.append(0)

    return lines, count


def main():
    # lines holds the trajectory information
    lines = list()

    # Holds simulation information
    sim_no = list()

    # count holds information about whether a bankrupt has occurred or not at each step
    count = list()

    # The number or simulations/trajectories
    total = NUM_SIMULATIONS

    # Run the simulations
    for i in range(0, total):
        # Run a simulation and store the trajectory and count information
        lines_temp, count_temp = propagate(START_Y, BOTTOM_LINE_Y, BOTTOM_LINE_Y - MAX_Y)

        # Extend the main count information with the count data from the simulation
        count.extend(count_temp)

        # Save simulation number
        sim_no.extend([i]*len(lines_temp))

        # Extend the main trajectory information with the trajectory information from this simulation
        lines.extend(lines_temp)

    # Debug info
    print(sum(count)/total)

    # default_lines contains information to draw the objects on the screen that should alway be there
    # i.e. the red line representing $0 and the green line representing $M
    default_lines = list()
    default_lines.append(Line(RED, (0, BOTTOM_LINE_Y), (WIDTH, BOTTOM_LINE_Y)))
    default_lines.append(Line(GREEN, (0, BOTTOM_LINE_Y - MAX_Y), (WIDTH, BOTTOM_LINE_Y - MAX_Y)))

    # Form a final list of lines which contain the default lines and the simulation lines
    final_lines = default_lines
    final_lines.extend(lines)

    theory = get_theory()

    step = 0
    while True:
        # Quit if the X is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # We want to progress the simulation step by step. The first 2 elements of the final_lines list are the
        # objects that are always there
        if step < len(lines):
            draw_environment(final_lines[:step+2], sum(count[:step]), sim_no[step], theory)
        else:
            draw_environment(final_lines, sum(count), i + 1, theory)
        clock.tick(60)
        step += SPEED


if __name__ == '__main__':
    pygame.font.init()
    main()
