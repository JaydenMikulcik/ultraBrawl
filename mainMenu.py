import pygame

from Characters.characterSelect import characterSelectScreen
from OtherObjects.usernameBoxes import UsernameBox




def mainMenu(screen, username):
    menu_options = ["Play Locally", "Play Online", "Check Leaderboard"]
    font = pygame.font.SysFont(None, 50)
    screen_size = (1200, 720)
    
    # Create the input field for the username
    input_field = UsernameBox(screen, font, 800, 100, 400, 40, username)
    usernameTextPos = (800, 50)
    usernameText = font.render("Enter Your Username!!!", True, (0, 255, 255))
    # Create the select screen loop
    selected_option = 0

    menu_loop = True
    while menu_loop:
        # Fill the screen with black
        screen.fill((0, 0, 0))
        screen.blit(usernameText, usernameTextPos)
        
        # Draw the username box
        input_field.draw()

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
            input_field.handle_event(event)
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
                        game_option = "solo"
                        menu_loop = False
                        chosen_character = characterSelectScreen(screen, singlePlayer=True)
                        if not chosen_character:
                            game_option = False
                        return game_option, None, None, chosen_character, input_field.get_text()
                    elif selected_option == 1:
                        # Open the options screen
                        serverType, client = characterSelectScreen(screen)
                        # TODO make this chosen characther work aswell
                        return "multiplayer", serverType, client, None, input_field.get_text()
                    elif selected_option == 2:
                        # Quit the game
                        menu_loop = False
                        return "leaderboard", None, None, None, input_field.get_text()