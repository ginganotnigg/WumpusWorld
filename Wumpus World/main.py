import pygame
from btn_text import *
from game import *




# INIT
pygame.init()

# CONSTANTS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
menu_img_path = "assets/monster.png"
state = {'inGame': False, 'execute': True}
text_boxes = []
buttons = []
levels = ["NO.1", "NO.2", "NO.3", "NO.4", "NO.5"]
selected_level = 0
len_level = len(levels)
run = True


def draw_menu():
    draw_text("WUMPUS WORLD", title_font, WHITE, 230, 40, screen)
    
    draw_text("MAP :", font, WHITE, 280, 190, screen)
    
    text_level_down = font.render("<", True, (255, 255, 255))
    text_level_down_rect = text_level_down.get_rect()
    text_level_down_rect.center = (370, 205)
    text_boxes.append({"text": "Map", "rect": text_level_down_rect,"action":"down"})
    screen.blit(text_level_down,text_level_down_rect)
    
    text_listlevel = font.render(f"{levels[selected_level]}", True, WHITE)
    screen.blit(text_listlevel, (397, 190))
    
    text_level_up = font.render(">", True, (255, 255, 255))
    text_level_up_rect = text_level_up.get_rect()
    text_level_up_rect.center = (470, 205)
    text_boxes.append({"text": "Map", "rect": text_level_up_rect,"action":"up"})
    screen.blit(text_level_up,text_level_up_rect)
    
    global button_start
    global button_quit

    button_start = Button("START", 320, 260, True, font, screen)
    button_quit = Button("QUIT", 320, 300, True, font, screen)

    buttons.append(button_start)
    buttons.append(button_quit)

    screen.blit(pygame.image.load("assets/monster.png"), (412, 420))
    screen.blit(pygame.transform.scale(pygame.image.load("assets/agent_up.png"), (100, 100)), (280, 520))
    pygame.display.flip()


def run_menu_screen():
    global inGame, screen, title_font, font, selected_level, state
    screen = pygame.display.set_mode((700, 750))
    pygame.display.set_caption("Wumpus World")

    title_font = pygame.font.Font("font/wormcuisine.ttf", 54)
    font = pygame.font.Font("font/wormcuisine.ttf", 36)
    
    run = True
    while run:
        for event in pygame.event.get():         
            if event.type == pygame.QUIT:
                run = False
                state["execute"] = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for box in text_boxes:
                    if box["rect"].collidepoint(event.pos):
                        if box["action"]=='up' and box["text"]=="Map":
                            if selected_level == len_level - 1:
                                break
                            else: 
                                selected_level += 1 
                                break 
                        elif box["action"]=='down' and box["text"]=="Map":
                            if selected_level == 0:
                                break 
                            else: 
                                selected_level -= 1 
                                break 
                for button in buttons:
                    if button.is_clicked(event):
                        if button.text == "QUIT":
                            run = False
                            state["execute"] = False
                            break 
                        
                        if button.text == "START":
                            state["inGame"] = not state["inGame"]
                            return
        
        background = pygame.transform.scale(pygame.image.load(f'assets/cave.png'), (750, 750))
        screen.blit(background, (0, 0))
        draw_menu()
        pygame.display.flip()
    pygame.quit()


while state["execute"]:
    if state["inGame"]:
        run_game_screen(state, selected_level + 1)
    else:
        run_menu_screen()
