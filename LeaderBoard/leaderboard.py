# Leaderboard that is rendered when leaderboard is 
# Checked checking who has the most wins via username
import pygame
import requests


def leaderboard(screen):


    # Show the size of the screen
    screen_width = 1280

    # Set up the font
    font = pygame.font.Font(None, 36)

    # Set up the scores and names
    scores = ["Total Wins", 75, 50, 25, 10]
    names = ["Username", "Bob", "Charlie", "Dave", "Eve"]

    # Create a list of text objects for the leaderboard
    leaderboard = []
    headers = True
    for i in range(len(scores)):
        if headers:
            text = f"-- {names[i]} - {scores[i]} --"
            headers = False
        else:
            text = f"{i}. {names[i]}: {scores[i]}"
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (screen_width // 2, 100 + 50*i)
        leaderboard.append((text_surface, text_rect))

    # Draw the leaderboard onto the screen
    screen.fill((0, 0, 0))
    for text_surface, text_rect in leaderboard:
        screen.blit(text_surface, text_rect)

    # Update the display
    pygame.display.update()
    

    # Wait for the user to close the window
    while True:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            
            # If escape is clicked show the menu
            if keys[pygame.K_ESCAPE]:
                return
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()