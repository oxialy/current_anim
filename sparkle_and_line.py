import pygame.mouse
import random
import json


pygame.init()


SAVED_DATA = 'linedrawB.json'

LOAD_LIST = True

WIDTH, HEIGHT = 1000,700

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

colors = ['#701070', '#808050', '#993030', '#BBBB80']

bg_color = '#060618'

DIRECTION = {
    -1: pygame.Vector2(0,-1),
    1: pygame.Vector2(0,1),
    -2: pygame.Vector2(-1,0),
    2: pygame.Vector2(1,0)
}

LINE_DIRECTION = {
    0: ()
}



def save_data(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f)

def load_json(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)

    return data


class Square:
    def __init__(self, x, y, size=270):
        self.x = x
        self.y = y
        self.size = size

        self.center = 20, 20

        self.rect_list = []
        self.timers = [0,10,20,30,40]

    def create_rect(self):
        rect_1 = (self.x, self.y, 40,40)
        rect_2 = (self.x+4, self.y+4, 32,32)
        rect_3 = (self.x+8, self.y+8, 24,24)
        rect_4 = (self.x+12, self.y+12, 16,16)
        rect_5 = (self.x+16, self.y+16, 8,8)

        self.rect_list = [rect_1, rect_2, rect_3, rect_4, rect_5]

        for i in range(5):
            rectA = (self.x+i*5, self.y+i*5, 50-i*10, 50-i*10)
            self.rect_list.append(rectA)


        '''rect_1 = (self.x, self.y, 80,80)
        rect_2 = (self.x+8, self.y+8, 64,64)
        rect_3 = (self.x+16, self.y+16, 48,48)
        rect_4 = (self.x+24, self.y+24, 32,32)
        rect_5 = (self.x+32, self.y+32, 16,16)

        self.rect_list = [rect_1, rect_2, rect_3, rect_4, rect_5]'''

    def draw(self, win):

        for rect, timer in zip(self.rect_list, self.timers):
            if timer < 50:
                pygame.draw.rect(win, colors[1], rect, 1)

    def increase_timer(self):
        for i in range(len(self.timers)):
            self.timers[i] += 3
            if self.timers[i] > 200:
                self.timers[i] = 0


    def move(self):
        gridsize = self.size//5
        Rx = random.randrange(WIDTH//gridsize)*gridsize
        Ry = random.randrange(HEIGHT//gridsize)*gridsize

        self.x = Rx
        self.y = Ry



def draw_screen(win):
    win.fill(bg_color)

    draw_lines(win)
    square.draw(win)
    square.increase_timer()

    if indicator:
        draw_mouse_indicator(win, pos)

    if highlight:
        line = lines[index2]

        for pos1, pos2 in zip(line, line[1:]):
            pygame.draw.line(win, colors[0], pos1, pos2)

        if len(line) > 1 and index2 < len(lines) - 1:
            pos1 = line[highlight_index]
            pos2 = line[highlight_index+1]

            pygame.draw.line(win, colors[2], pos1, pos2)


    write_text(win, index2, 50,50, 20)

def get_gridpos(pos):
    x,y = pos
    x2 = x // PXLSIZE + COLS // 2
    y2 = y // PXLSIZE + ROWS // 2

    return x2, y2

def centered_rect(rect, size=150):
    x,y,w,h = rect

    x2 = x + (w-size)/2
    y2 = y + (h-size)/2

    return pygame.Rect(x2, y2, size, size)

def draw_mouse_indicator(win, pos):
    x,y = pos

    pygame.draw.line(win, '#013040', (0,y),(WIDTH, y))
    pygame.draw.line(win, '#013040', (x,0),(x, HEIGHT))


def draw_lines(win):
    for line in lines:
        if len(line) > 1:
            for P1, P2 in zip(line, line[1:]):
                pygame.draw.line(win, colors[1], P1, P2)

def add_line(x,y):

    LINE_DIRECTION = {
        0: ((0,y),(x,y), (x,0),(x,y)),
        1: ((x,0),(x,y), (WIDTH,y),(x,y)),
        2: ((WIDTH, y),(x,y), (x,HEIGHT),(x,y)),
        3: ((x,HEIGHT),(x,y), (0,y),(x,y))
    }

    lines[index] = LINE_DIRECTION[switch]

def get_orthogonal(A,B):
    x1,y1 = A
    x2,y2 = B

    dist_x = abs(x2-x1)
    dist_y = abs(y2-y1)

    if dist_x < dist_y:
        return x1, y2
    else:
        return x2, y1

def align_grid(pos):
    x,y = pos

    posB = x//10*10, y//10*10

    return posB

def check_direction(A,B):
    x1,y1 = A
    x2,y2 = B

    dist_x = abs(x2-x1)
    dist_y = abs(y2-y1)

    if dist_x < dist_y:
        return 'x'
    else:
        return 'y'

def draw_info(surf):

    pygame.draw.rect(toolbar, color3, (0,0, 150,150), 2)   # toolbox BG

def write_text(win, data, x,y, size =25, color='#806630'):
    Font = pygame.font.SysFont('arial', size)
    text_surf = Font.render(str(data), 1, color)
    win.blit(text_surf, (x,y))

lines = [[]]
line = [(0,0)]

data = load_json(SAVED_DATA)

if LOAD_LIST:
    lines = data['lines']
    line = lines[0]

square = Square(300,300)
square.create_rect()


switch = 0
index1 = len(lines[0]) - 1
index2 = 0

running = True
highlight = True
highlight_index = 0
indicator = True
clock = pygame.time.Clock()
FPS = 30

while running:

    elapsed = pygame.time.get_ticks()//1000
    draw_screen(WIN)

    pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                pos_x, pos_y = pos
                pos0 = pos

                if pos_x < 17:
                    pos = 0, pos_y
                if pos_x > WIDTH-17:
                    pos = WIDTH, pos_y
                if pos_y < 17:
                    pos = pos_x, 0
                    print('align', pos)
                if pos_y > HEIGHT-17:
                    pos = pos_x, HEIGHT

                if len(line) > 1:
                    pos = get_orthogonal(line[len(line)-1], pos)
                    pos_x, pos_y = pos

                #pos = pos_x // 200 * 200, pos_y//200*200
                pos = align_grid(pos)

                print(pos0, index1, index2)

                line[index1] = pos

                lines[index2] = line

                index1 += 1
                line.append(pos)
                print(lines)

            if pygame.mouse.get_pressed()[2]:
                indicator = not indicator

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_w:
                print(len(lines[index2]), lines)
                if highlight_index == 0:
                    highlight_index = len(lines[index2])-3
                else:
                    highlight_index = 0

            if event.key == pygame.K_RETURN:
                index2 += 1
                if len(lines) <= index2:
                    lines.append([])

                index1 = 0
                line = [(0,0)]

            if event.key == pygame.K_e:
                line = [(0,0)]
                lines[index2] = [[]]
                index1 = 0
            if event.key == pygame.K_BACKSPACE and len(line) > 2:
                line[len(line)-2:len(line)] = [line[len(line)-3]]

                lines[index2] = line
                index1 -= 1

            if event.key == pygame.K_SPACE:
                highlight = not highlight


            if event.key == pygame.K_1:
                squares[0].move()
            if event.key == pygame.K_2:
                squares[1].move()
            if event.key == pygame.K_3:
                squares[2].move()

            if event.key == pygame.K_LEFT:
                index2 -= 1
                index2 = max(index2, 0)

                line = lines[index2]
                index1 = len(line) - 1

            if event.key == pygame.K_RIGHT:
                index2 += 1
                index2 = min(index2, len(lines)-1)

                line = lines[index2]
                index1 = len(line) - 1

            if event.key == pygame.K_UP:
                pos1 = lines[index2][highlight_index]
                pos2 = lines[index2][highlight_index+1]

                x1,y1 = pos1
                x2,y2 = pos2
                if check_direction(pos1,pos2) == 'x':
                    x1 += 5
                    x1 = min(x1, x2-5)
                    lines[index2][highlight_index] = x1,y1
                if check_direction(pos1,pos2) == 'y':
                    y1 += 5
                    y1 = min(x1, x2-5)
                    lines[index2][highlight_index] = x1,y1

            if event.key == pygame.K_DOWN:
                pos1 = lines[index2][highlight_index]
                pos2 = lines[index2][highlight_index + 1]

                x1, y1 = pos1
                x2, y2 = pos2
                if check_direction(pos1, pos2) == 'x':
                    x1 -= 5
                    x1 = min(x1, x2 + 5)
                    lines[index2][highlight_index] = x1, y1
                if check_direction(pos1, pos2) == 'y':
                    y1 -= 5
                    y1 = min(x1, x2 + 5)
                    lines[index2][highlight_index] = x1, y1


    clock.tick(FPS)
    pygame.display.update()

data = load_json(SAVED_DATA)

data['lines'] = lines

save_data(SAVED_DATA, data)