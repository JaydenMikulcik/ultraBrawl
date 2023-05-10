import pygame



def showGameOver(screen, winner):
    
    # Define the colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Define the fonts
    font = pygame.font.Font(None, 48)
    button_font = pygame.font.Font(None, 36)

    # Render the "Game Over" text
    game_over_text = font.render("Game Over\nPlayer {} Won".format(winner), True, WHITE)

    # Create the buttons
    button1_rect = pygame.Rect(300, 400, 300, 50)
    button1_text = button_font.render("Play Again", True, BLACK)

    button2_rect = pygame.Rect(700, 400, 300, 50)
    button2_text = button_font.render("Return Home", True, BLACK)

    # Draw everything to the screen
    screen.blit(game_over_text, (400, 100))

    pygame.draw.rect(screen, WHITE, button1_rect)
    screen.blit(button1_text, (button1_rect.x + 25, button1_rect.y + 10))

    pygame.draw.rect(screen, WHITE, button2_rect)
    screen.blit(button2_text, (button2_rect.x + 25, button2_rect.y + 10))

    pygame.display.flip()

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle button clicks
            if event.type == pygame.MOUSEBUTTONUP:
                if button1_rect.collidepoint(event.pos):
                    return True
                elif button2_rect.collidepoint(event.pos):
                    return False