import pygame
from btn_text import *
from main import *





WHITE = (255,255,255)
BLACK = (0,0,0)

menu_img_path = "assets/wumpus.png"



# Tạo danh sách các ô văn bản
text_boxes = []
buttons = []

# Thay đổi levels, maps, al tại đây 
levels = ["Map 1", "Map 2", "Map 3"]
selected_level = 0
len_level = len(levels)




def draw_menu():
    Name_game = draw_text("Wumpus game", font, WHITE, 160, 40, screen)
    menu_game = draw_text("Menu", font, WHITE, 280, 110, screen)
    
    text_map = draw_text("Map:", font, WHITE, 210, 180, screen)
    
    text_level_down = font.render("<", True, (255, 255, 255))
    text_level_down_rect = text_level_down.get_rect()
    text_level_down_rect.center = (280, 190)
    text_boxes.append({"text": "Map", "rect": text_level_down_rect,"action":"down"})
    screen.blit(text_level_down,text_level_down_rect)
    
    text_listlevel = font.render(f"{levels[selected_level]}", True, WHITE)
    screen.blit(text_listlevel, (310, 180))
    
    text_level_up = font.render(">", True, (255, 255, 255))
    text_level_up_rect = text_level_up.get_rect()
    text_level_up_rect.center = (410, 190)
    text_boxes.append({"text": "Map", "rect": text_level_up_rect,"action":"up"})
    screen.blit(text_level_up,text_level_up_rect)
    
    #các btn
    global button_start
    
    # button_start = Button("RUN", 260, 260, True)
    # buttons.append({"text":"Run", "rect": button_start})
    global button_quit
    # button_quit = Button("QUIT", 260, 300, True)
    # buttons.append({"text":"Quit", "rect": button_quit})

    button_start = Button("START", 260, 260, True, font, screen)
    button_quit = Button("QUIT", 260, 300, True, font, screen)

    buttons.append(button_start)
    buttons.append(button_quit)


    #img menu
    image = pygame.image.load(menu_img_path)
    image_width, image_height = image.get_size()

    scale_factor = 2 
    scaled_image = pygame.transform.scale(image, (image_width * scale_factor, image_height * scale_factor))

    screen.blit(scaled_image, (50, (400 - 150) // 2))
    pygame.display.flip()


def start_game():
    print("Starting the game with the following options:",levels[selected_level])
    main_run()


def menu_run():
    pygame.init()

    global screen, font
    # Tạo cửa sổ trò chơi
    screen = pygame.display.set_mode((700, 750))
    pygame.display.set_caption("Wumpus World")

    # Font
    # Tạo font cho văn bản
    font = pygame.font.Font(None, 36)
    
    running = True
    while running:
        for event in pygame.event.get():         
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for box in text_boxes:
                    if box["rect"].collidepoint(event.pos):
                        if box["action"]=='up' and box["text"]=="Map":
                            print(f"Đã click vào up Map")
                            if selected_level == len_level - 1:
                                break;
                            else: 
                                selected_level +=1;
                            break;
                        elif box["action"]=='down' and box["text"]=="Map":
                            print(f"Đã click vào down Map")
                            if selected_level == 0:
                                break;
                            else: 
                                selected_level -= 1;
                                break;
                for button in buttons:
                    if button.is_clicked(event):

                        if button.text == "QUIT":
                            print("Button QUIT is clicked.")
                            # thoát game
                            running = False
                            break;
                        
                        if button.text == "START":
                            start_game()
                            break;
        
        screen.fill((52, 78, 91))
        draw_menu()
        pygame.display.flip()

    pygame.quit()
    
    

menu_run()


