from utils import *

import pygame.mouse
import random
import json


pygame.init()


def draw_screen(win):
    win.fill(bg_color)

    # screen middle crossbar:
    pygame.draw.rect(win, 'purple', (WIDTH/2-4, HEIGHT/2, 8,1))
    pygame.draw.rect(win, 'purple', (WIDTH / 2, HEIGHT / 2 - 4, 1, 8))

    animate_current(win, current1)


    '''for current in currentsB:
        if current.timer > TIME_LIMIT:
            c = current
            c.animate(win)
            if c.line_pos >= len(c.line)-1:
                c.timer = 0
                c.pos = pygame.Vector2(c.start)
                c.line_pos = 0'''

def animate_current(win, current):
    for line in current:
        line.animate(win)



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



running = True
hovering = True


while running:

    elapsed = pygame.time.get_ticks()//1000
    draw_screen(WIN)

    '''i = 30
    for j, c in enumerate(currentsB):
        text_pos = WIDTH-85+i*int(j*30/450), (j*30)%450+60
        write_text(WIN, round(c.timer), text_pos[0], text_pos[1], 12)'''

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

    clock.tick(FPS)
    pygame.display.update()

converted_lines = []


if update_json:
    data = load_json(SAVED_DATA)

    data['currents_list'] = converted_lines

    save_data(SAVED_DATA, data)