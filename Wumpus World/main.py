import pygame
from btn_text import *
from game import *




# INIT
pygame.init()

# CONSTANTS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
menu_img_path = "assets/monster.png"
state = {'inGame': False, 'execute': True, 'value': []}
text_boxes = []
buttons = []
indexs = ["NO.1", "NO.2", "NO.3", "NO.4", "NO.5"]
selected_idx = 0
genNums = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
selected_pit = 0
selected_wumpus = 0
selected_gold = 0
run = True
switch_btn = None
generate = False

def draw_select(text, _list, idx, x, y):
    draw_text(text, font, WHITE, x, y, screen)
    text_idx_down = font.render("<", True, WHITE)
    text_idx_down_rect = text_idx_down.get_rect()
    text_idx_down_rect.center = (x + 120, y + 15)
    text_boxes.append({"text": text, "rect": text_idx_down_rect, "action": "down"})
    screen.blit(text_idx_down, text_idx_down_rect)
    
    text_idx = font.render(f"{_list[idx]}", True, WHITE)
    text_idx_rect = text_idx.get_rect()
    text_idx_rect.center = (x + 160, y + 15)
    screen.blit(text_idx, text_idx_rect)
    
    text_idx_up = font.render(">", True, WHITE)
    text_idx_up_rect = text_idx_up.get_rect()
    text_idx_up_rect.center = (x + 200, y + 15)
    text_boxes.append({"text": text, "rect": text_idx_up_rect, "action": "up"})
    screen.blit(text_idx_up, text_idx_up_rect)

def draw_menu():
    global generate, switch_btn

    draw_text("WUMPUS WORLD", title_font, WHITE, 210, 40, screen)
    
    # Switch between choose and generate
    switch_btn = Button("GENERATE" if not generate else "CHOOSE", 280, 150, True, font, screen, 'teal', 140)
    buttons.append(switch_btn)
    
    if generate:
        draw_select("Pit", genNums, selected_pit, 250, 200)
        draw_select("Wumpus", genNums, selected_wumpus, 250, 250)
        draw_select("Gold", genNums, selected_gold, 250, 300)
    else:
        draw_select("Map", indexs, selected_idx, 250, 230)

    buttons.append(Button("START", 240, 650, True, font, screen))
    buttons.append(Button("QUIT", 360, 650, True, font, screen))

    screen.blit(pygame.image.load("assets/monster.png"), (412, 420))
    screen.blit(pygame.transform.scale(pygame.image.load("assets/agent_up.png"), (100, 100)), (280, 520))
    pygame.display.flip()

def select_event(box, idx, length):
    if box["action"]=='up':
        if idx == length - 1:
            pass
        else: 
            idx += 1
    elif box["action"]=='down':
        if idx == 0:
            pass
        else: 
            idx -= 1
    return idx

def run_menu_screen():
    global inGame, screen, title_font, font, selected_idx, selected_pit, selected_wumpus, selected_gold, state, generate, buttons, text_boxes
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
                        if box["text"] == "Map":
                            selected_idx = select_event(box, selected_idx, 5)
                            break
                        if box["text"] == "Pit":
                            selected_pit = select_event(box, selected_pit, 10)
                            break
                        if box["text"] == "Wumpus":
                            selected_wumpus = select_event(box, selected_wumpus, 10)
                            break
                        if box["text"] == "Gold":
                            selected_gold = select_event(box, selected_gold, 10)
                            break
                for button in buttons:
                    if button.is_clicked(event):
                        if button.text == "QUIT":
                            run = False
                            state["execute"] = False
                            break 
                        if button.text == "START":
                            state["inGame"] = not state["inGame"]
                            if generate:
                                state["value"] = [selected_pit + 1, selected_wumpus + 1, selected_gold + 1]
                            else: state["value"] = [selected_idx + 1]
                            return
                        if button == switch_btn:
                            generate = not generate
                            break

        
        background = pygame.transform.scale(pygame.image.load(f'assets/cave.png'), (750, 750))
        screen.blit(background, (0, 0))
        draw_menu()
        pygame.display.flip()
    pygame.quit()


while state["execute"]:
    if state["inGame"]:
        run_game_screen(state)
    else:
        run_menu_screen()
