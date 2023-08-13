import pygame.mouse
import random
import json


pygame.init()


SAVED_DATA = r'utils\currents_data.json'
LIST_DATA = r'C:\Users\jingl\Documents\GitHub\current_anim\utils\linedraw.json'

update_json = False

WIDTH, HEIGHT = 700,600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

PXLSIZE = 10
pos = 0, 0
pos_x, pos_y = pos

TEXT1 = 'Too tanky waiting room'


TIME_LIMIT = 140

COLOR_MAPPING = {
    1: '#101010',
    2: '#302010',
    3: '#906060',
    4: '#A07074'
}

colors = ['#AAA850', '#104620']
colorsA = ['#']

bg_color = '#131818'

DIRECTION = {
    -1: pygame.Vector2(0,-1),
    1: pygame.Vector2(0,1),
    -2: pygame.Vector2(-1,0),
    2: pygame.Vector2(1,0)
}

clock = pygame.time.Clock()
FPS = 30


class Line():

    LINE_SIZE = 34

    def __init__(self, start, speed = 12):
        self.start = start
        x,y = start
        self.x = 0
        self.y = 0
        self.pos = pygame.Vector2(start)

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

        fill_list = [fill_segment for _ in range(len(self.body))]

        self.line[len(self.line):] = fill_list


    def animate(self, win):
        segment = self.line[self.line_pos]

        border_up    = self.start[1] + segment['pos'][1] - segment['dist']
        border_down  = self.start[1] + segment['pos'][1] + segment['dist']
        border_left  = self.start[0] + segment['pos'][0] - segment['dist']
        border_right = self.start[0] + segment['pos'][0] + segment['dist']

        self.pos += segment['toward'] * self.speed

        self.body[0] = {'pos': self.pos.copy(), 'toward': segment['toward']}
        self.cycle_body()

        if self.pos[0] <= border_left \
                or self.pos[0] >= border_right \
                or self.pos[1] <= border_up \
                or self.pos[1] >= border_down\
                or segment['toward'] == (0,0):

            self.line_pos += 1

            if self.line_pos >= len(self.line):
                self.line_pos = 0
                self.pos = pygame.Vector2(self.start)

        for j, pxl in enumerate(self.body):
            pos = pxl['pos']
            toward = pxl['toward']*self.pxl_size
            pos2 = pos - toward
            pos3 = pos2 - toward

            for i in range(self.speed//self.pxl_size):
                posB = pos - i*toward
                pygame.draw.rect(win, colors[0], (posB[0], posB[1], self.pxl_size, self.pxl_size))


        # drawing line size limit box:
        """pygame.draw.line(win, colors[1], (border_left, border_up), (border_right, border_up))
        pygame.draw.line(win, colors[1], (border_left, border_down), (border_right, border_down))
        pygame.draw.line(win, colors[1], (border_left, border_down), (border_left, border_up))
        pygame.draw.line(win, colors[1], (border_right, border_down), (border_right, border_up))"""

    def cycle_body(self):
        for i, point in list(enumerate(self.body))[:0:-1]:
            self.body[i] = self.body[i-1].copy()



def save_data(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f)

def load_json(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)

    return data

def color_list(colA, colB, n=130):
    pass

def get_toward(A,B):
    x1,y1 = A
    x2,y2 = B

    dist_x = x2-x1
    dist_y = y2-y1

    if x2-x1 > 0:
        direction = pygame.Vector2(1,0)
        dist = dist_x
    if x2-x1 < 0:
        direction = pygame.Vector2(-1,0)
        dist = dist_x

    if y2-y1 > 0:
        direction = pygame.Vector2(0,1)
        dist = dist_y
    if y2-y1 < 0:
        direction = pygame.Vector2(0,-1)
        dist = dist_y

    return direction, dist

def create_current(lines, start):
    raw_list = lines

    line_list = []

    start = pygame.Vector2(start)
    offset = pygame.Vector2(lines[0][0])

    for line in raw_list:
        converted_line = convert_json_list(line)

        first_position = line[0]

        new_line = Line(start + first_position - offset)
        new_line.line = converted_line

        line_list.append(new_line)

    return line_list


def convert_json_list(list, offset=pygame.Vector2(0,0)):
    converted_list = []
    pos = pygame.Vector2(0,0)

    for pos1, pos2 in zip(list, list[1:]):

        if pos1 != pos2:
            toward, dist = get_toward(pos1,pos2)

            converted_list.append({'pos': pos.copy(), 'toward': toward, 'dist': abs(dist), 'start': pos1})

            pos += toward * abs(dist)

    return converted_list


data = load_json(LIST_DATA)

current1 = create_current(data['linesD'], (300,300))
print(current1[2].line)

