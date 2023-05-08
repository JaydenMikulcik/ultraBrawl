# Leaderboard that is rendered when leaderboard is 
# Checked checking who has the most wins via username
import pygame
import requests


def leaderboard(screen):


    # Show the size of the screen
    screen_width = 800

    # Set up the font
    font = pygame.font.Font(None, 36)

    # Set up the scores and names
    scores = [100, 75, 50, 25, 10]
    names = ["Alice", "Bob", "Charlie", "Dave", "Eve"]

    # Create a list of text objects for the leaderboard
    leaderboard = []
    for i in range(len(scores)):
        text = f"{i+1}. {names[i]}: {scores[i]}"
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (screen_width // 2, 100 + 50*i)
        leaderboard.append((text_surface, text_rect))

    # Draw the leaderboard onto the screen
    for text_surface, text_rect in leaderboard:
        screen.blit(text_surface, text_rect)

    # Update the display
    pygame.display.update()

    # Wait for the user to close the window
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()