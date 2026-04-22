import pygame

class Button:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text

    def draw(self, screen, font):
        pygame.draw.rect(screen, (200,200,200), self.rect)
        pygame.draw.rect(screen, (0,0,0), self.rect, 2)

        txt = font.render(self.text, True, (0,0,0))
        screen.blit(
            txt,
            (self.rect.centerx - txt.get_width()//2,
             self.rect.centery - txt.get_height()//2)
        )

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)