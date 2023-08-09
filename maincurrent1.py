import pygame.mouse
import random



pygame.init()

WIDTH, HEIGHT = 700,600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

PXLSIZE = 10
pos = 0, 0
pos_x, pos_y = pos


COLOR_MAPPING = {
    1: '#101010',
    2: '#302010',
    3: '#906060',
    4: '#A07074'
}

colors = ['#BBBB80', '#103010']
current_colorB = [3,2,4,4,4,3,2,1,1,1,1,2,3,3,2,3,3,3,3,3,4,4,4,4,4,4,4,4,3,3,3,3,3,3,2,2,2,1,1,1,1,2,3,4,4,4,2,1]

current_colorB = [3,3,1,1,3,3,1,1, 3,3,1,1,3,3,1,1, 3,3,1,1,3,3,1,1, 3,3,1,1,3,3,1,1, 3,3,1,1,3,3,1,1, 3,3,1,1,3,3,1,1]

current_colorB = [4,4,4,4,1,1,1,1, 4,4,4,4,1,1,1,1, 4,4,4,4,1,1,1,1, 4,4,4,4,1,1,1,1, 4,4,4,4,1,1,1,1, 4,4,4,4,1,1,1,1]
#current_colorB = [3,2,4,2,1,1,1,1, 1,1,1,1,1,1,1,1, 1,1,1,2,2,3,3,4, 4,3,3,2,2,1,1,1, 1,1,1,1,1,1,1,1, 1,1,1,1,2,4,2,3]

current_color = [COLOR_MAPPING[i] for i in current_colorB]

bg_color = '#131818'

DIRECTION = {
    -1: pygame.Vector2(0,-1),
    1: pygame.Vector2(0,1),
    -2: pygame.Vector2(-1,0),
    2: pygame.Vector2(1,0)
}

timer1 = 0
timer2 = 200
timer3 = 20

timers = [timer1, timer2, timer3]
current_timer = {
    0: timer1,
    1: timer1,
    2: timer2,
    3: timer2,
    4: timer3,
    5: timer3
}


class Current():

    LINE_SIZE = 33

    def __init__(self, x, y, speed = 12):
        self.start = x, y
        self.x = 0
        self.y = 0
        self.pos = pygame.Vector2(x,y)

        self.speed = speed

        self.line_pos = 0
        self.line_index = 0
        self.line = []
        self.body = [{'toward': DIRECTION[1], 'pos': pygame.Vector2(0,1)} for _ in range(4)]
        self.pxl_size = 2

        self.timer = 0

    def create_segments(self, n):
        pos = pygame.Vector2(0, 0)
        r2 = -1

        for i in range(n):
            choice_list = [-2, -1, 1, 2]
            choice2 = choice_list.remove(-r2)
            r = random.choice(choice_list)

            segment = {'toward': DIRECTION[r], 'pos': pos.copy()}

            self.line.append(segment)

            pos += DIRECTION[r]
            r2 = r
        fill_segment = {'toward': pygame.Vector2(0,0), 'pos': pos}

        for _ in range(len(self.body)):
            self.line.append(fill_segment)


    def animate(self, win):
        segment = self.line[self.line_pos]

        border_up    = self.start[1] + (segment['pos'][1]-1) * self.LINE_SIZE
        border_down  = self.start[1] + (segment['pos'][1]+1) * self.LINE_SIZE
        border_left  = self.start[0] + (segment['pos'][0]-1) * self.LINE_SIZE
        border_right = self.start[0] + (segment['pos'][0]+1) * self.LINE_SIZE

        self.pos += segment['toward'] * self.speed

        self.body[0] = {'pos': self.pos.copy(), 'toward': segment['toward']}
        self.cycle_body()

        if self.pos[0] <= border_left \
                or self.pos[0] >= border_right \
                or self.pos[1] <= border_up \
                or self.pos[1] >= border_down\
                or segment['toward'] == (0,0):
            self.line_pos += 1

        for j, pxl in enumerate(self.body):
            pos = pxl['pos']
            toward = pxl['toward']*self.pxl_size
            pos2 = pos - toward
            pos3 = pos2 - toward

            for i in range(self.speed//self.pxl_size):
                posB = pos - i*toward
                pygame.draw.rect(win, colors[0], (posB[0], posB[1], self.pxl_size, self.pxl_size))

            '''pygame.draw.rect(win, colors[0], (pos[0], pos[1], 2,2))
            pygame.draw.rect(win, colors[0], (pos2[0], pos2[1], 2,2))
            pygame.draw.rect(win, colors[0], (pos3[0], pos3[1], 2,2))'''

        # drawing line size limit box:
        '''pygame.draw.line(win, colors[1], (border_left, border_up), (border_right, border_up))
        pygame.draw.line(win, colors[1], (border_left, border_down), (border_right, border_down))
        pygame.draw.line(win, colors[1], (border_left, border_down), (border_left, border_up))
        pygame.draw.line(win, colors[1], (border_right, border_down), (border_right, border_up))'''

    def animateaa(self, win):
        segment = self.line[self.line_pos]

        self.pos += segment['toward'] * self.speed

        self.body[0] = self.pos.copy()
        self.cycle_body()

        if self.pos[0] <= -self.LINE_SIZE \
                or self.pos[0] >= self.LINE_SIZE \
                or self.pos[1] <= -self.LINE_SIZE \
                or self.pos[1] >= self.LINE_SIZE:
            self.line_pos += 1
            self.pos *= 0

        for pos in self.body:
            pygame.draw.rect(win, colors[0],
                             (self.start[0] + pos[0] + segment['pos'][0] * self.LINE_SIZE,
                              self.start[1] + pos[1] + segment['pos'][1] * self.LINE_SIZE, 3, 3))

    def cycle_body(self):
        for i, point in list(enumerate(self.body))[:0:-1]:
            self.body[i] = self.body[i-1].copy()

currents = []
cur1 = Current(300,300)
cur1.create_segments(50)

for i in range(6):
    rx = random.randrange(250)
    current = Current(rx + 180, i*70+100)

    current.create_segments(16)
    currents.append(current)
    current.timer = i*30



def draw_screen(win):
    win.fill(bg_color)


    # screen middle crossbar:
    pygame.draw.rect(win, 'purple', (WIDTH/2-4, HEIGHT/2, 8,1))
    pygame.draw.rect(win, 'purple', (WIDTH / 2, HEIGHT / 2 - 4, 1, 8))

    for current in currents:
        if current.timer > 200:
            c = current
            c.animate(win)
            if c.line_pos >= len(c.line)-1:
                c.timer = 0
                c.pos = pygame.Vector2(c.start)
                c.line_pos = 0


def get_gridpos(pos):
    x,y = pos
    x2 = x // PXLSIZE + COLS // 2
    y2 = y // PXLSIZE + ROWS // 2

    return x2, y2


def draw_info(surf):

    pygame.draw.rect(toolbar, color3, (0,0, 150,150), 2)   # toolbox BG


running = True
hovering = True
clock = pygame.time.Clock()
FPS = 30

while running:

    elapsed = pygame.time.get_ticks()//1000
    draw_screen(WIN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            pos_x, pos_y = pos
            x,y = get_gridpos(pos)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False



    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        pos_y -= 8
    if keys[pygame.K_DOWN]:
        pos_y += 8
    if keys[pygame.K_LEFT]:
        pos_x -= 8
    if keys[pygame.K_RIGHT]:
        pos_x += 8

    for c in currents:
        c.timer += 3

    clock.tick(FPS)
    pygame.display.update()


