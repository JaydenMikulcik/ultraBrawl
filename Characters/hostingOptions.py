import pygame
import random


from client import Client

def options(screen):


    # The Client that will be used to connect to the server
    onlineClient = Client()

    # Get the id of the game if its chosen to host game
    random_ints = [random.randint(1, 100) for _ in range(2)]
    random_ints_string = "".join(str(i) for i in random_ints)

    # set up the screen
    screen_width = 1280
    screen_height = 720

    # set up the fonts
    font = pygame.font.Font(None, 36)

    def get_host_code(screen):
        running = True
        text = font.render("Enter Game Code: " + random_ints_string, True, (255, 0, 0))
        text_rect = text.get_rect(center=(700, 500))  # Center the text in the window
        screen.blit(text, text_rect)
        while running:
            for event in pygame.event.get():
                # I think need to render game again idk
                if event.type == pygame.QUIT:
                    running = False
            gameStatus = onlineClient.join_game(random_ints_string.encode())

            if gameStatus:
                return
            pygame.display.update()


    def enter_host_code(screen):
        # Set up the text input field
        input_box = pygame.Rect(700, 500, 200, 32)  # x, y, width, height
        input_text = ''

        # Set up the submit button
        submit_button = pygame.Rect(900, 500, 100, 32)

        # Main game loop
        running = True
        trying_to_join = False
        while running:
            for event in pygame.event.get():

                # Try to join the game looking for join code
                if trying_to_join:
                    gameStatus = onlineClient.join_game(input_text.encode())
                    print(gameStatus)
                    if gameStatus:
                        return
                    
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                        # TODO: When backspace remove the removed text
                        # screen.fill((0, 0, 0), text_surface)
                        text_surface = font.render(input_text, True, (0, 0, 0))
                        print(input_text)
                    if event.key == pygame.K_RETURN:  # Submit the form when the user presses Enter
                        print("Form submitted with input:", input_text)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if submit_button.collidepoint(event.pos):  # Submit the form when the user clicks the button
                        print("Form submitted with input:", input_text)
                        while True:
                            gameStatus = onlineClient.join_game(input_text.encode())
                            trying_to_join = True
                            if gameStatus:
                                return
                elif event.type == pygame.TEXTINPUT:
                    input_text += event.text


            # Draw the input box and text
            pygame.draw.rect(screen, (0, 0, 0), input_box, 2)
            text_surface = font.render(input_text, True, (0, 0, 0))
            screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

            # Draw the submit button
            pygame.draw.rect(screen, (0, 0, 255), submit_button)
            submit_text_surface = font.render("Submit", True, (255, 0, 0))
            screen.blit(submit_text_surface, (submit_button.x + 5, submit_button.y + 5))

            # Update the screen
            pygame.display.update()

        # Return the final input text
        return input_text


    # set up the buttons
    button_width = 200
    button_height = 50
    button_padding = 100
    button_x1 = (screen_width - button_width * 2 - button_padding) / 2
    button_x2 = button_x1 + button_width + button_padding
    button_y = 600
    button1_rect = pygame.Rect(button_x1, button_y, button_width, button_height)
    button2_rect = pygame.Rect(button_x2, button_y, button_width, button_height)

    # set up the colors
    button_color = (0, 0, 255)
    text_color = (255, 255, 255)

    # main game loop
    while True:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button1_rect.collidepoint(event.pos):
                    print("Creating a server... ")
                    get_host_code(screen)
                    return "create", onlineClient
                elif button2_rect.collidepoint(event.pos):
                    print("Joining a server... ")
                    enter_host_code(screen)
                    return "join", onlineClient

        pygame.draw.rect(screen, button_color, button1_rect)
        pygame.draw.rect(screen, button_color, button2_rect)
        button1_text = font.render("Host Game", True, text_color)
        button2_text = font.render("Join Game", True, text_color)
        screen.blit(button1_text, (button_x1 + button_width/2 - button1_text.get_width()/2, 600))
        screen.blit(button2_text, (button_x2 + button_width/2 - button2_text.get_width()/2, 600))
        pygame.display.update()