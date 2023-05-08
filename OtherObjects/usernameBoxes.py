import pygame

class UsernameBox:
    def __init__(self, screen, font, x, y, width, height, username):
        self.screen = screen
        self.font = font
        self.rect = pygame.Rect(x, y, width, height)
        self.text = username
        self.active = False

    def draw(self):
        # Draw the button
        pygame.draw.rect(self.screen, (0, 0, 255), self.rect, 2)

        # Draw the text
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            # Activate the input button
            self.active = True
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def get_text(self):
        return self.text