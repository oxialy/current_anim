import pygame.mouse
import random
import json


pygame.init()


SAVED_DATA = 'currents_data.json'

WIDTH, HEIGHT = 700,600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

PXLSIZE = 10
pos = 0, 0
pos_x, pos_y = pos

TIME_LIMIT = 50

COLOR_MAPPING = {
    1: '#101010',
    2: '#302010',
    3: '#906060',
    4: '#A07074'
}

colors = ['#AAAAAA', '#103010']
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

class Current():

    LINE_SIZE = 33

    def __init__(self, x, y, speed = 10):
        self.start = x, y
        self.x = 0
        self.y = 0
        self.pos = pygame.Vector2(x,y)

        self.speed = speed

        self.line_pos = 0
        self.line_index = 0
        self.line = []
        self.body = [{'toward': DIRECTION[1], 'pos': pygame.Vector2(0,1)} for _ in range(3)]
        self.pxl_size = 1

        self.timer = 0

    def create_segments(self, n):
        pos = pygame.Vector2(0, 0)
        ordered = [-2, -1, 1, 2]

        random.shuffle(ordered)
        r2 = ordered[0]
        ordered.remove(-r2)
        ordered.append(-r2)

        for i in range(n):
            choice_list = ordered.copy()
            choice_list.remove(-r2)

            r = random.randrange(100)

            if r < 45:
                r = choice_list[0]
            elif r < 90:
                r = choice_list[1]
            else:
                r = choice_list[2]


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

    def cycle_body(self):
        for i, point in list(enumerate(self.body))[:0:-1]:
            self.body[i] = self.body[i-1].copy()

currentsA = []
cur1 = Current(300,300)
cur1.create_segments(50)

for i in range(50):
    rx = random.randrange(50,650, 5)
    ry = random.randrange(50,670, 5)
    n = random.choice([7,9,12])
    t = random.choice([0, TIME_LIMIT])
    current = Current(rx, ry)

    current.create_segments(n)
    currentsA.append(current)
    current.timer = t

currentsB = currentsA[:10]

currentsC = [c.line for c in currentsA]


def save_data(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f)

def load_json(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)

    return data

def draw_screen(win):
    win.fill(bg_color)


    # screen middle crossbar:
    pygame.draw.rect(win, 'purple', (WIDTH/2-4, HEIGHT/2, 8,1))
    pygame.draw.rect(win, 'purple', (WIDTH / 2, HEIGHT / 2 - 4, 1, 8))

    for current in currentsB:
        if current.timer > TIME_LIMIT:
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

def write_text(win, data, x,y, size =25):
    Font = pygame.font.SysFont('arial', size)
    text_surf = Font.render(str(data), 1, '#A09040')
    win.blit(text_surf, (x,y))


c = currentsB[0]
T1 = 0

running = True
hovering = True
clock = pygame.time.Clock()
FPS = 30

while running:

    elapsed = pygame.time.get_ticks()//1000
    draw_screen(WIN)

    i = 30
    for j, c in enumerate(currentsB):
        text_pos = WIDTH-85+i*int(j*30/450), (j*30)%450+60
        write_text(WIN, round(c.timer), text_pos[0], text_pos[1], 12)

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

    for c in currentsB:
        c.timer += ( 70-2*len(c.line) ) / len(c.line)**2

    clock.tick(FPS)
    pygame.display.update()

converted_lines = []

for line in currentsC:
    lineB = []

    for segment in line:
        new_segment = {
            'toward': list(segment['toward']),
            'pos'   : list(segment['pos'])
        }

        lineB.append(new_segment)
    converted_lines.append(lineB)


print(converted_lines)
data = load_json(SAVED_DATA)

data['currents_list'] = converted_lines

save_data(SAVED_DATA, data)