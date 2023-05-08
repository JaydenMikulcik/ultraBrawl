import pygame

from Characters.hostingOptions import options

def characterSelectScreen(screen, singlePlayer=False):
    
    # Initialize the chosen charachter and screen size
    playerSelected = False
    screen_width = 1280
    screen_height = 600
    chosen_character = None

    # Set up the font
    font = pygame.font.Font(None, 50)
    selecText = font.render("Select Your Character", True, (255, 0, 0))
    selectRect = selecText.get_rect()
    selectRect.center = (screen_width // 2, 100)


    # Set the box dimensions
    box_size = 100

    # Set the box padding
    box_padding = 20

    # Set the number of rows and columns
    num_rows = 3
    num_cols = 3

    # Calculate the total box area dimensions
    total_box_width = (num_cols * box_size) + ((num_cols - 1) * box_padding)
    total_box_height = (num_rows * box_size) + ((num_rows - 1) * box_padding)

    # Calculate the starting x and y positions of the box area
    start_x = (screen_width - total_box_width) / 2
    start_y = (screen_height - total_box_height) / 2

    # Create a list to hold the boxes
    boxes = []

    # The face of each character that will go in the boxes
    boxesFaces = [r"images\characters\blazefist\face.PNG", r"images\characters\bloodMoon\face.PNG", r"images\characters\deathBringer\face.PNG",
                  r"images\characters\quantumKnight\face.PNG", None, None,
                  None, None, None]

    # Create the boxes
    for row in range(num_rows):
        for col in range(num_cols):
            x = start_x + (col * (box_size + box_padding))
            y = start_y + (row * (box_size + box_padding))
            box = pygame.Rect(x, y, box_size, box_size)
            boxes.append(box)

    # Game loop
    running = True
    while running:
        keys = pygame.key.get_pressed()
        pygame.display.update()
        # Handle events
        for event in pygame.event.get():
            if keys[pygame.K_ESCAPE]:
                return False
            
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if a box was clicked
                for i, box in enumerate(boxes):
                    if box.collidepoint(event.pos):

                        if i == 0:
                            print("Default Character Chosen")
                            chosen_character = "blazeFist"

                        if i == 1:
                            print("Blaze Fist Chosen")
                            chosen_character = "bloodMoon"
                       

                        if i == 2:
                            print("Blood Moon Chosen")
                            chosen_character = "deathBringer"
    

                        if i == 3:
                            print("Death Bringer Chosen")
                            chosen_character = "quantumKnight"
                  

                        if i == 4:
                            print("Quantum Knight Chosen")
                            chosen_character = "default"
        

                        if i == 5:
                            print("TODO ADD Charachert")
                            chosen_character = "default"
                    

                        if i == 6:
                            print("TODO ADD Charachert")
                            chosen_character = "default"
                    
                    
                        playerSelected = True

        # Clear the screen
        screen.fill((255, 255, 255))
        screen.blit(selecText, selectRect)

        # Draw the boxes
        for i, box in enumerate(boxes):
            pygame.draw.rect(screen, (0,0,0), box)

            # If the charachter exists then draw face
            if boxesFaces[i]:
                image = pygame.image.load(boxesFaces[i]).convert_alpha()
                screen.blit(image, box)

        if playerSelected:
            if not singlePlayer:
                game_type, client = options(screen)
                return game_type, client
            else:
                return chosen_character

