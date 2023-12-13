import pygame

class Button:
    def __init__(self, text, x, y, active, font, screen):
        self.text = text
        self.x = x
        self.y = y
        self.active = active
        self.font = font
        self.rect = pygame.Rect(x, y, 100, 30)
        self.draw(screen)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0) if self.active else (0, 255, 0), self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.rect.collidepoint(event.pos) and event.button == 1
        return False


# Define draw_text function
def draw_text(text, font, text_color, x, y, screen):
    imgx = font.render(text, True, text_color)
    screen.blit(imgx, (x, y))
    return imgx
