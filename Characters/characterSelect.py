import pygame

from Characters.hostingOptions import options

def characterSelectScreen(screen):
    
    # Initialize the chosen character as NULL
    chosen_character = None

    # Set the screen dimensions
    playerSelected = False
    screen_width = 400
    screen_height = 400


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
        pygame.display.update()
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if a box was clicked
                for i, box in enumerate(boxes):
                    if box.collidepoint(event.pos):
                        if i == 0:
                            print("Default Character Chosen")
                            chosen_character = "default"
                        if i == 1:
                            print("Blaze Fist Chosen")
                            chosen_character = "blazeFist"
                        print("Box clicked:", box)
                        playerSelected = True

        # Clear the screen
        screen.fill((255, 255, 255))

        # Draw the boxes
        for box in boxes:
            pygame.draw.rect(screen, (0, 0, 0), box)

        if playerSelected:
            game_type, client = options(screen)
            return game_type, client

