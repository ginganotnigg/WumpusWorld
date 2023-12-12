import pygame
import subprocess
import os

pygame.init()

# Tạo cửa sổ trò chơi
screen = pygame.display.set_mode((500, 400))
pygame.display.set_caption("Wumpus World")

# Font
# Tạo font cho văn bản
font = pygame.font.Font(None, 36)
WHITE = (255,255,255)
BLACK = (0,0,0)

menu_img_path = "wumpus.png"
test_script_path = os.path.abspath("D:/HOC_KY7_4/CNTTNT/Wumpus/WumpusWorld/test.py")


# Tạo danh sách các ô văn bản
text_boxes = []
buttons = []

# Thay đổi levels, maps, al tại đây 
levels = ["Map 1", "Map 2", "Map 3"]
selected_level = 0
len_level = len(levels)


class Button:
    def __init__(self, text, x, y, active, font):
        self.text = text
        self.x = x
        self.y = y
        self.active = active
        self.font = font
        self.rect = pygame.Rect(x, y, 100, 30)
        self.draw()

    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0) if self.active else (0, 255, 0), self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.rect.collidepoint(event.pos) and event.button == 1
        return False


# Define draw_text function
def draw_text(text, font, text_color, x, y):
    imgx = font.render(text, True, text_color)
    screen.blit(imgx, (x, y))
    return imgx

def draw_menu():
    Name_game = draw_text("Wumpus game", font, WHITE, 160, 40)
    menu_game = draw_text("Menu", font, WHITE, 280, 110)
    
    text_map = draw_text("Map:", font, WHITE, 210, 180)
    
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

    button_start = Button("START", 260, 260, True, font)
    button_quit = Button("QUIT", 260, 300, True, font)

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
    print("Starting the game with the following options:")
    print("Map:", levels[selected_level])

# def launch_game(name):
#     subprocess.run(["python", name])
    


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
                        print("Button RUN is clicked.")

                        # code chuyển qua màn hình chơi game
                        
                        break;

    
            
                
            
            
    screen.fill((52, 78, 91))
    draw_menu()
    

    pygame.display.flip()

pygame.quit()