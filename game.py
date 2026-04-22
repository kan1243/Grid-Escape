import pygame
import sys

from loader import load_level
from level import Level
from player import Player
from mechanics import Mechanics
from config import DIR
from button import Button
import random

# ===== GAME STATE =====
MENU = "menu"
SELECT = "select"
PLAYING = "playing"
STAT = "stat"
NAME_INPUT = "name_input"
RESULT = "result"

game_state = MENU

current_level = 0
current_variant = 0
player_name = ""
result_message = ""

# ===== CONFIG =====
COLOR_POOL = [
    (255,100,100),
    (100,255,100),
    (100,100,255),
    (255,255,100),
    (255,100,255),
    (100,255,255),
    (255,150,50),
    (150,50,255),
    (50,200,200),
    (200,50,150)
]

TILE_SIZE = 60
time_limit = 15

WHITE = (240, 240, 240)
BLACK = (30, 30, 30)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (100, 100, 100)

# ====== COLOR SYSTEM ======
COLOR_MAP = {
    "Y": (255, 200, 0),
    "G": (0, 200, 0),
    "B": (0, 150, 255)
}

# ===== INIT =====
pygame.init()

spike_img = pygame.image.load("picture/spike.png")
spike_img = pygame.transform.scale(spike_img, (TILE_SIZE, TILE_SIZE))

glass_img = pygame.image.load("picture/glass.png")
glass_img = pygame.transform.scale(glass_img, (TILE_SIZE, TILE_SIZE))

void_img = pygame.image.load("picture/void.png")
void_img = pygame.transform.scale(void_img, (TILE_SIZE, TILE_SIZE))

goal_img = pygame.image.load("picture/goal.png")
goal_img = pygame.transform.scale(goal_img, (TILE_SIZE, TILE_SIZE))

lava_on_img = pygame.image.load("picture/lava_on.png")
lava_on_img = pygame.transform.scale(lava_on_img, (TILE_SIZE, TILE_SIZE))

lava_off_img = pygame.image.load("picture/lava_off.png")
lava_off_img = pygame.transform.scale(lava_off_img, (TILE_SIZE, TILE_SIZE))

ice_img = pygame.image.load("picture/ice.png")
ice_img = pygame.transform.scale(ice_img, (TILE_SIZE, TILE_SIZE))

font_big = pygame.font.SysFont(None, 60)
font_small = pygame.font.Font("C:/Windows/Fonts/arial.ttf", 40)

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Grid Escape: A Time-Constrained Puzzle Game")

clock = pygame.time.Clock()

# ===== MENU BUTTONS =====
btn_play = Button((0, 0, 200, 60), "PLAY")
btn_stat = Button((0, 0, 200, 60), "STAT")
btn_quit = Button((0, 0, 200, 60), "QUIT")

# ===== LEVEL BUTTONS =====
level_buttons = []
start_x = 100
start_y = 150
gap = 100

for i in range(15):
    row = i // 5
    col = i % 5
    x = start_x + col * gap
    y = start_y + row * gap
    level_buttons.append(Button((x, y, 70, 70), str(i + 1)))

# ===== GAME OBJECTS =====
level = None
player = None
mech = None

ROWS = 0
COLS = 0

start_time = 0


# ===== LOAD LEVEL =====
def load_current_level():
    global level, player, player_name, mech, ROWS, COLS, start_time, current_variant, time_limit

    level_data, current_variant, time_limit = load_level(f"level{current_level + 1}")
    level = Level(level_data)
    player = Player(level.start)
    mech = Mechanics(level)

    ROWS, COLS = level.grid_size

    start_time = pygame.time.get_ticks()

    print("LEVEL", current_level+1, "VARIANT", current_variant)


# ===== RESET =====
def reset():
    player.reset()
    level.reset_state()


# ===== DRAW GAME =====
def draw():
    screen.fill(WHITE)

    # ===== OFFSET CENTER =====
    offset_x = (screen.get_width() - COLS * TILE_SIZE) // 2
    offset_y = (screen.get_height() - ROWS * TILE_SIZE) // 2

    # ===== BASE GRID =====
    for r in range(ROWS):
        for c in range(COLS):
            x = c * TILE_SIZE + offset_x
            y = r * TILE_SIZE + offset_y

            if (r, c) in level.walls:
                pygame.draw.rect(screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE))

            # ===== GOAL =====
            elif (r, c) == level.goal:
                screen.blit(goal_img, (x, y))

            # ===== GLASS =====
            elif (r, c) in level.glass:
                screen.blit(glass_img, (x, y))

            # ===== VOID (Glass broken) =====
            elif (r, c) in level.broken_glass:
                screen.blit(void_img, (x, y))    

            # ===== LAVA =====
            elif (r, c) in level.lava:
                if mech.laser_on:
                    screen.blit(lava_on_img, (x, y))
                else:
                    screen.blit(lava_off_img, (x, y))

            # ===== ICE =====
            elif (r, c) in level.ice:
                screen.blit(ice_img, (x, y))        

            else:
                pygame.draw.rect(screen, WHITE, (x, y, TILE_SIZE, TILE_SIZE))

            pygame.draw.rect(screen, GRAY, (x, y, TILE_SIZE, TILE_SIZE), 1)

    # ===== BARRIERS (TRANSPARENT) =====
    for k in level.barriers:
        for (r, c) in level.barriers[k]:
            if level.barrier_active[k]:
                x = c * TILE_SIZE + offset_x
                y = r * TILE_SIZE + offset_y

                color = COLOR_MAP.get(k, (255, 200, 0))

                barrier_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                barrier_surface.fill((*color, 120))  # alpha 120

                screen.blit(barrier_surface, (x, y))

    # ===== SWITCHES =====
    for k in level.switches:
        for (r, c) in level.switches[k]:
            center = (
                c*TILE_SIZE + TILE_SIZE//2 + offset_x,
                r*TILE_SIZE + TILE_SIZE//2 + offset_y
            )

            pygame.draw.circle(
                screen,
                COLOR_MAP.get(k, (255, 200, 0)),
                center,
                TILE_SIZE//4
            )
            pygame.draw.circle(screen, BLACK, center, TILE_SIZE//4, 2)

    # ===== TELEPORTERS =====
    for i, (k, pair) in enumerate(level.teleporters.items()):
        color = COLOR_POOL[i % len(COLOR_POOL)]

        for (r, c) in pair:
            x = c * TILE_SIZE + offset_x
            y = r * TILE_SIZE + offset_y

            center = (x + TILE_SIZE//2, y + TILE_SIZE//2)

            # outer ring
            pygame.draw.circle(screen, color, center, TILE_SIZE//2 - 6)

            # inner white
            pygame.draw.circle(screen, (255,255,255), center, TILE_SIZE//4)

            # small core
            pygame.draw.circle(screen, color, center, 5)  

    # ===== SPIKES =====
    for (r, c) in level.spikes:
        screen.blit(
            spike_img,
            (c * TILE_SIZE + offset_x, r * TILE_SIZE + offset_y)
        )

    # ===== PLAYER =====
    pr, pc = player.pos
    pygame.draw.rect(screen,RED,(
                                player.pixel_x + 10 + offset_x,
                                player.pixel_y + 10 + offset_y,
                                TILE_SIZE-20,
                                TILE_SIZE-20
                            )
                        )

    # ===== TIMER UI =====
    elapsed = (pygame.time.get_ticks() - start_time) / 1000
    time_left = max(0, int(time_limit - elapsed))

    color = (200,0,0) if time_left <= 5 else (0,0,0)
    
    #change timer color to red when last five second
    timer_text = font_small.render(f"Time Left: {time_left}", True, color)
    screen.blit(timer_text, (20, 20))


# ===== DRAW MENU =====
def draw_menu():
    screen.fill((30, 30, 30))

    center_x = screen.get_width() // 2

    # ===== TITLE =====
    title = font_big.render("Grid Escape", True, (255,255,255))
    subtitle = font_small.render("A Time-Constrained Puzzle Game", True, (200,200,200))

    title_rect = title.get_rect(center=(center_x, 120))
    subtitle_rect = subtitle.get_rect(center=(center_x, 180))

    screen.blit(title, title_rect)
    screen.blit(subtitle, subtitle_rect)

    # ===== BUTTONS (center) =====
    btn_play.rect.center = (center_x, 280)
    btn_stat.rect.center = (center_x, 350)
    btn_quit.rect.center = (center_x, 420)

    btn_play.draw(screen, font_small)
    btn_stat.draw(screen, font_small)
    btn_quit.draw(screen, font_small)


# ===== DRAW SELECT =====
def draw_select():
    screen.fill((40, 40, 40))

    # ===== TITLE (center) =====
    title = font_big.render("Choose Level", True, (255, 255, 255))
    title_rect = title.get_rect(center=(screen.get_width() // 2, 60))
    screen.blit(title, title_rect)

    # ===== GRID LAYOUT =====
    cols = 5
    rows = 3
    button_size = 70
    gap = 30

    total_width = cols * button_size + (cols - 1) * gap
    total_height = rows * button_size + (rows - 1) * gap

    start_x = (screen.get_width() - total_width) // 2
    start_y = (screen.get_height() - total_height) // 2 + 40

    # ===== DRAW BUTTONS =====
    for i, b in enumerate(level_buttons):
        row = i // cols
        col = i % cols

        x = start_x + col * (button_size + gap)
        y = start_y + row * (button_size + gap)

        b.rect.topleft = (x, y)
        b.draw(screen, font_small)

# ===== DRAW STAT =====
def draw_stat():
    screen.fill((20, 20, 20))

    center_x = screen.get_width() // 2

    title = font_big.render("Statistics", True, (255,255,255))
    title_rect = title.get_rect(center=(center_x, 120))
    screen.blit(title, title_rect)

    text = font_small.render("Coming Soon...", True, (200,200,200))
    text_rect = text.get_rect(center=(center_x, 220))
    screen.blit(text, text_rect)

    hint = font_small.render("Press ESC to go back", True, (150,150,150))
    hint_rect = hint.get_rect(center=(center_x, 350))
    screen.blit(hint, hint_rect)

# ===== DRAW NAME INPUT =====
def draw_name_input():
    screen.fill((20, 20, 20))

    center_x = screen.get_width() // 2

    title = font_big.render("Enter Your Name", True, (255,255,255))
    title_rect = title.get_rect(center=(center_x, 120))
    screen.blit(title, title_rect)

   # input box
    box_rect = pygame.Rect(0, 0, 400, 60)
    box_rect.center = (center_x, 250)

    # border
    pygame.draw.rect(screen, (255,255,255), box_rect, 2)

    # text
    text_surface = font_small.render(player_name, True, (255,255,255))
    screen.blit(text_surface, (box_rect.x + 10, box_rect.y + 15))

# ===== DRAW RESULT =====
def draw_result():
    screen.fill((20,20,20))

    center_x = screen.get_width() // 2

    text = font_big.render(result_message, True, (255,255,255))
    rect = text.get_rect(center=(center_x, 200))
    screen.blit(text, rect)

    hint = font_small.render("Press ENTER to continue", True, (150,150,150))
    hint_rect = hint.get_rect(center=(center_x, 300))
    screen.blit(hint, hint_rect)    

# ===== INPUT =====
def handle_menu(event):
    global game_state

    if event.type == pygame.MOUSEBUTTONDOWN:
        if btn_play.is_clicked(event.pos):
            game_state = NAME_INPUT

        elif btn_stat.is_clicked(event.pos):
            game_state = STAT

        elif btn_quit.is_clicked(event.pos):
            pygame.quit()
            sys.exit()

def handle_select(event):
    global game_state, current_level

    if event.type == pygame.MOUSEBUTTONDOWN:
        for i, b in enumerate(level_buttons):
            if b.is_clicked(event.pos):
                current_level = i
                load_current_level()
                game_state = PLAYING

def handle_name_input(event):
    global player_name, game_state

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            if player_name.strip() != "":
                game_state = SELECT

        elif event.key == pygame.K_BACKSPACE:
            player_name = player_name[:-1]

        else:
            if len(player_name) < 12:
                if event.unicode.isalnum():
                    player_name += event.unicode

# ===== MAIN LOOP =====
while True:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_state == MENU:
            handle_menu(event)

        elif game_state == STAT:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = MENU    

        elif game_state == SELECT:
            handle_select(event)

        elif game_state == NAME_INPUT:
            handle_name_input(event)

        elif game_state == RESULT:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state = MENU

        elif game_state == PLAYING:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.move(DIR["UP"], level)
                elif event.key == pygame.K_DOWN:
                    player.move(DIR["DOWN"], level)
                elif event.key == pygame.K_LEFT:
                    player.move(DIR["LEFT"], level)
                elif event.key == pygame.K_RIGHT:
                    player.move(DIR["RIGHT"], level)
                elif event.key == pygame.K_r:
                    reset()
                elif event.key == pygame.K_n:   # N = next (ผ่านด่าน)
                    print("CHEAT: WIN")
                    player.pos = level.goal

    # ===== GAME LOGIC =====
    if game_state == PLAYING:
        player.update(dt)   
        mech.update(dt)
        result = mech.apply_all(player)  

        if result == "dead":
            reset()
            continue 
    
        if player.pos == level.goal:
            result_message = f"YOU WIN! (Level {current_level+1})"
            game_state = RESULT
    
        elapsed = (pygame.time.get_ticks() - start_time) / 1000
        if elapsed > time_limit:
            result_message = "TIME UP!"
            game_state = RESULT

    # ===== DRAW =====
    if game_state == MENU:
        draw_menu()
    elif game_state == SELECT:
        draw_select()
    elif game_state == PLAYING:
        draw()
    elif game_state == STAT:
        draw_stat()
    elif game_state == NAME_INPUT:
        draw_name_input()
    elif game_state == RESULT:
        draw_result()

    pygame.display.flip()