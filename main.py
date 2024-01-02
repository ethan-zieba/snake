import pygame as pg
import pygame.font
import random as rd


pygame.init()
dimensions = (500, 500)
screen = pg.display.set_mode(dimensions)
FPS = 30
snake_radius = 20
running = True
orange = (255, 128, 0)
pink = (200, 10, 200)
clock = pg.time.Clock()
game_state = "start"


class Snake():
    def __init__(self, radius = 20, speed = 0.7, posx = 45, posy = 45):
        self.posx = posx
        self.posy = posy
        self.direction = "RIGHT"
        self.speed = speed
        self.radius = radius

    def changedirection(self, newdirection):
        self.direction = newdirection

    def gethead_pos(self):
        return (self.posx, self.posy)

    def move(self):
        match self.direction:
            case "RIGHT": self.posx += 10 * self.speed
            case "LEFT": self.posx -= 10 * self.speed
            case "UP": self.posy -= 10 * self.speed
            case "DOWN": self.posy += 10 * self.speed


class Apple():
    def __init__(self, posx, posy, golden = False, taken = False):
        self.isgold = golden
        self.posx = posx
        self.posy = posy
        self.taken = taken

    def getpos(self):
        return (self.posx, self.posy)

    def reset(self, avoid_list):
        self.taken = False
        self.posx, self.posy = rd.randint(20, 480), rd.randint(20, 480)
        self.isgold = True if rd.randint(0, 10) > 9 else False
        while (self.posx, self.posy) in avoid_list:
            self.posx, self.posy = rd.randint(20, 480), rd.randint(20, 480)

    def collide(self):
        self.reset()


def gameover():
    pass

def start_menu():
    global running, game_state
    screen.fill((0, 0, 0))
    font = pg.font.SysFont('arial', 40)
    title = font.render('le snake original', True, (255, 255, 255))
    subfont = pg.font.SysFont('arial', 35)
    subtitle = subfont.render('(il peut traverser les murs)', True, (255, 255, 255))
    start_button = font.render('Start', True, (0, 0, 0), (250, 250, 250))
    screen.blit(title, (dimensions[0] / 2 - title.get_width() / 2, dimensions[1] / 2 - title.get_height() / 2))
    screen.blit(subtitle, (dimensions[0] / 2 - subtitle.get_width() / 2, dimensions[1] / 2 + title.get_height() / 2))
    start_button_pos = (dimensions[0] / 2 - start_button.get_width() / 2,
    dimensions[1] / 2 + start_button.get_height() / 2 + subtitle.get_height() + 50)
    screen.blit(start_button, (start_button_pos[0], start_button_pos[1]))
    pg.display.update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if ((start_button_pos[0] < pg.mouse.get_pos()[0] < start_button_pos[0] + start_button.get_width())
                    and (start_button_pos[1] < pg.mouse.get_pos()[1] < start_button_pos[1] + start_button.get_height())):
                print("Start")
                game_state = "playing"


grass_bg = pg.image.load("textures/greengrass2.png")


def construct_background(frame):
    for i in range(0, 500, 128):
        for u in range(0, 500, 128):
            frame.blit(grass_bg, (i, u))


def out_of_boundaries(position):
    if position[0] >= 500:
        return 10, position[1]
    elif position[0] <= 0:
        return 490, position[1]
    if position[1] >= 500:
        return position[0], 10
    elif position[1] <= 0:
        return position[0], 490
    return position
snakehead = Snake()
snake_length = 8
previous_positions = []
apple = Apple(250, 250)
score = 0
font = pg.font.SysFont('arial', 40)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    if game_state == "start":
        start_menu()
    elif game_state == "over":
        gameover()
    else:
        if (abs(snakehead.gethead_pos()[0] - apple.getpos()[0]) < 50
                and abs(snakehead.gethead_pos()[1] - apple.getpos()[1]) < 50):
            snake_length += 3 if apple.isgold == False else 6
            score += 1 if apple.isgold == False else 2
            apple.reset(previous_positions)
        snaketail = []
        previous_positions = previous_positions[:snake_length*2:]
        previous_positions.insert(0, snakehead.gethead_pos())
        for i in range(len(previous_positions)):
            snaketail.append(Snake())
            snaketail[i].posx, snaketail[i].posy = previous_positions[i][0], previous_positions[i][1]
            if i != 0 and snakehead.gethead_pos() == snaketail[i].gethead_pos():
                running = False
        print(previous_positions)
        keys = pg.key.get_pressed()
        if keys[pg.K_DOWN] and snakehead.direction != "UP":
            snakehead.changedirection("DOWN")
        elif keys[pg.K_UP] and snakehead.direction != "DOWN":
            snakehead.changedirection("UP")
        elif keys[pg.K_LEFT] and snakehead.direction != "RIGHT":
            snakehead.changedirection("LEFT")
        elif keys[pg.K_RIGHT] and snakehead.direction != "LEFt":
            snakehead.changedirection("RIGHT")
        construct_background(screen)
        snakehead.move()
        snakehead.posx, snakehead.posy = out_of_boundaries(snakehead.gethead_pos())

        snakehead_sprite = pg.draw.circle(surface=screen, color=orange, center=snakehead.gethead_pos(), radius=snake_radius)
        for i in range(len(snaketail)):
            pg.draw.circle(surface=screen, color=pink, center=snaketail[i].gethead_pos(), radius=max(8, snaketail[i].radius-(i*0.06)))
        apple_sprite = pg.image.load("textures/apple.png") if not apple.isgold else pg.image.load("textures/goldenapple.png")
        screen.blit(apple_sprite, (apple.getpos()[0]-32, apple.getpos()[1]-32))
        score_text = font.render(str(score), True, (255, 255, 255))
        screen.blit(score_text,
                    (dimensions[0] / 2 - score_text.get_width() / 2, 100 - score_text.get_height() / 2))

        pg.display.flip()
        clock.tick(FPS)
