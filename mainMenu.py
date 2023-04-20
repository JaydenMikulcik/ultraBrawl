import pygame

from Characters.characterSelect import characterSelectScreen




def mainMenu(screen):
    menu_options = ["Play Locally", "Play Online", "Check Leaderboard"]
    font = pygame.font.SysFont(None, 50)
    screen_size = (1200, 720)
    # Create the select screen loop
    selected_option = 0

    menu_loop = True
    while menu_loop:
        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Loop through the menu options
        for i in range(len(menu_options)):
            # Set the text to the current menu option
            text = font.render(menu_options[i], True, (255, 255, 255))

            # Center the text horizontally
            text_rect = text.get_rect(center=(screen_size[0] / 2, (screen_size[1] / len(menu_options)) * i + screen_size[1] / (len(menu_options) * 2)))

            # Draw the text to the screen
            screen.blit(text, text_rect)

            # Check if the current menu option is selected
            if i == selected_option:
                # Draw a rectangle around the selected option
                pygame.draw.rect(screen, (255, 255, 255), (text_rect.x - 10, text_rect.y - 10, text_rect.width + 20, text_rect.height + 20), 5)

        # Update the Pygame screen
        pygame.display.update()

        # Handle Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit the game if the user closes the window
                menu_loop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    # Move the selection up
                    selected_option -= 1
                    if selected_option < 0:
                        selected_option = len(menu_options) - 1
                elif event.key == pygame.K_DOWN:
                    # Move the selection down
                    selected_option += 1
                    if selected_option >= len(menu_options):
                        selected_option = 0
                elif event.key == pygame.K_RETURN:
                    # Start the game or open the options screen
                    if selected_option == 0:
                        # Start the game
                        menu_loop = False
                        return "solo", None
                    elif selected_option == 1:
                        # Open the options screen
                        serverType = characterSelectScreen(screen)
                        return "multiplayer", serverType
                    elif selected_option == 2:
                        # Quit the game
                        menu_loop = False
                        return "leaderboard", None