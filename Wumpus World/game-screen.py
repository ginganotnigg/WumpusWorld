import pygame
import sys


class Button:
    def __init__(self,  text, x, y,enable):
        self.text = text
        self.x = x
        self.y = y
        self.enable = enable
        self.draw()
        
    def draw(self):
        bt_text = font.render(self.text,True, BLACK)
        self.bt_rect = pygame.rect.Rect((self.x,self.y), (130, 30))   
        pygame.draw.rect(screen, 'gray', self.bt_rect, 0, 5)
        pygame.draw.rect(screen, 'black', self.bt_rect, 2, 5)
        screen.blit(bt_text,(self.x+10,self.y+3))
    
    def is_clicked(self, event):
        return self.bt_rect.collidepoint(event.pos)

def draw_text(text, font, text_color, x, y):
    imgx = font.render(text, True, text_color)
    screen.blit(imgx, (x, y))
    return imgx


pygame.init()

font = pygame.font.Font(None, 36)
# Kích thước cửa sổ
window_width, window_height = 800, 600
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Wumpus game")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
pri_color =(52, 78, 91)

# Kích thước và vị trí của menu
menu_width, menu_height = 200, window_height
menu_x, menu_y = 0, 0

# Kích thước và vị trí của màn hình chơi game
game_width, game_height = window_width - menu_width, window_height
game_x, game_y = menu_width, 0

# Độ dày của đường viền giữa menu và màn hình chơi game
border_thickness = 2
def draw_menu():
    
    pygame.draw.rect(screen, pri_color, (menu_x, menu_y, menu_width, menu_height))

    # Vẽ màn hình chơi game
    pygame.draw.rect(screen, WHITE, (game_x, game_y, game_width, game_height))

    # Vẽ đường viền giữa menu và màn hình chơi game
    pygame.draw.rect(screen, BLACK, (game_x - border_thickness, game_y - border_thickness,
                                    border_thickness, window_height + 2 * border_thickness), border_thickness)

    # vẽ các button của menu
    global button_pause, button_continue, button_quit
    button_pause = Button("Pause", 30, 100, True)
    button_continue = Button("Continue", 30, 150, True)
    button_quit = Button("Quit", 30, 200, True)

    menu_game = draw_text("Menu", font, WHITE, 55, 40)

    pygame.display.flip()

    
    


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    draw_menu()
    pygame.display.flip()

pygame.quit()
sys.exit()