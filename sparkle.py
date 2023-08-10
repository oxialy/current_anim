import pygame.mouse
import random
import json


pygame.init()


SAVED_DATA = 'currents_data.json'

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

colors = ['#9B9B50', '#808050', '#aa4040', '#BBBB80']

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

        self.positions = []

    def set_pos(self):
        pos1 = 0,0
        pos2 = self.size*4/8, self.size*4/8
        self.positions.append(pos1)
        self.positions.append(pos2)

    def draw(self, win):

        for pos in self.positions:
            s1 = self.size
            s2 = 180

            rect1 = pygame.Rect(pos[0] + self.x, pos[1] + self.y, self.size, self.size)
            rect2 = centered_rect(rect1, 150)
            rect3 = pygame.Rect(pos[0]+self.x-7, pos[1]+self.y-7, s1,s1)
            pygame.draw.rect(win, colors[1], rect1, 1)
            #pygame.draw.rect(win, colors[1], rect2, 1)
            pygame.draw.rect(win, colors[1], rect3, 1)






    def move(self):
        gridsize = self.size//5
        Rx = random.randrange(WIDTH//gridsize)*gridsize
        Ry = random.randrange(HEIGHT//gridsize)*gridsize

        self.x = Rx
        self.y = Ry


squares = []

for i in range(3):
    Rx = random.randrange(1000)
    Ry = random.randrange(700)

    square = Square(Rx, Ry)
    square.set_pos()

    squares.append(square)


def draw_screen(win):
    win.fill(bg_color)

    # screen middle crossbar:
    #pygame.draw.rect(win, 'purple', (WIDTH/2-4, HEIGHT/2, 8,1))
    #pygame.draw.rect(win, 'purple', (WIDTH / 2, HEIGHT / 2 - 4, 1, 8))

    """for square in squares:
        square.draw(win)"""

    draw_lines(win)

    if highlight:
        line = lines[index2]
        for pos1, pos2 in zip(line, line[1:]):
            pygame.draw.line(win, colors[2], pos1, pos2)



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


def draw_info(surf):

    pygame.draw.rect(toolbar, color3, (0,0, 150,150), 2)   # toolbox BG

def write_text(win, data, x,y, size =25):
    Font = pygame.font.SysFont('arial', size)
    text_surf = Font.render(str(data), 1, '#503030')
    win.blit(text_surf, (x,y))

lines = [[]]
line = [(0,0)]

switch = 0
index1 = 0
index2 = 0

running = True
highlight = True
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

            if pos_x < 17:
                pos = 0, pos_y
            if pos_x > WIDTH-17:
                pos = WIDTH, pos_y
            if pos_y < 17:
                pos = pos_x, 0
            if pos_y > HEIGHT-17:
                pos = pos_x, HEIGHT

            if len(line) > 1:
                pos = get_orthogonal(line[len(line)-1], pos)

            line[index1] = pos

            lines[index2] = line

            index1 += 1
            line.append(pos)
            print(index1,index2)
            print(lines)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_w:
                switch += 1
                if switch > 3:
                    switch = 0
                add_line2(pos_x,pos_y)

            if event.key == pygame.K_RETURN:
                index2 += 1
                lines.append([])

                index1 = 0
                line = [(0,0)]

            if event.key == pygame.K_e:
                line = [(0,0)]
                lines[index2] = [[]]
                index1 = 0
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
            if event.key == pygame.K_RIGHT:
                index2 += 1
                index2 = min(index2, len(lines)-1)


    clock.tick(FPS)
    pygame.display.update()