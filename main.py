
import pygame
import asyncio
import pygbag
import requests

from mainMenu import mainMenu
from OtherObjects.platforms import Platform
from OtherObjects.gameOver import showGameOver
from instantiatePlayer import createPlayer


from Characters.playerDefault import Player
from Characters.blazeFist import blazeFist

from LeaderBoard.leaderboard import leaderboard


async def run():

    # pygame setup
    pygame.init()
    username = ""

    # Creating the background image and initializing the game
    font = pygame.font.SysFont(None, 30)
    screen = pygame.display.set_mode((1280, 720))
    background_image = pygame.image.load(r'images/backDrop.png').convert()
    clock = pygame.time.Clock()
    running = True
    dt = 0


    # Initialize the platforms TODO in the future make a map pool
    platform1 = Platform(screen.get_width() / 2 - 400, screen.get_height() / 2, 600, 20)
    platform2 = Platform(screen.get_width() / 2 - 800, screen.get_height() / 2 + 200, 600, 20)
    platform3 = Platform(screen.get_width() / 2 + 600, screen.get_height() / 2 - 50, 600, 20)


    # Add all the platform objects of the game here
    objects = pygame.sprite.Group()
    objects.add(platform1)
    objects.add(platform2)
    objects.add(platform3)


    # Add all the players of the game here
    player1 = Player(screen.get_width() / 2 - 400, screen.get_height() / 2, objects)
    player2 = blazeFist(screen.get_width() / 2 + 378, screen.get_height() / 2, objects)
    allPlayers = pygame.sprite.Group()
    allPlayers.add(player1)
    allPlayers.add(player2)


    player1LivesPos = (90, 100)
    player2LivesPos = (1000, 100)

    player1HealthPos = (90, 600)
    player2HealthPos = (1000, 600)

    menuHelpPos = (300, 100)
    menuHelp = font.render("Press (esc) to go back to menu", True, (0, 0, 0))

    showMenu = True

    # Init both online players as null
    onlinePlayer1 = None
    onlinePlayer2 = None

    # Check if the online player needs to be initialized
    initializePlayer = False

    while running:

        # Get the keys pressed
        keys = pygame.key.get_pressed()
    
        # If escape is clicked show the menu
        if keys[pygame.K_ESCAPE]:
            showMenu = True
    
        # Toggle Showing the Menu
        if showMenu:
            menuChoice, serverType, onlineClient, character, username = mainMenu(screen, username)
            showMenu = False
            print("Current Player: " + username)
            if not menuChoice:
                showMenu = True
            elif menuChoice == "solo":
                # Goes through here if playing against the bot online
                onlinePlayer1 = None
                onlinePlayer2 = None
                player1 = createPlayer(character, screen.get_width() / 2 - 378, screen.get_height() / 2, objects)
                player1.userName = username
                allPlayers.add(player1)
                continue
            elif menuChoice == "multiplayer":
                # Goes here if the person playing choses to play online
                initializePlayer = True
                if serverType == "create":
                    # The Connected player 2
                    onlinePlayer2 = onlineClient
                    player1 = createPlayer(character, screen.get_width() / 2 - 378, screen.get_height() / 2, objects)
                    player1.userName = username
                    continue
                else:
                    # The connected player 1
                    onlinePlayer1 = onlineClient
                    player2 = createPlayer(character, screen.get_width() / 2 + 378, screen.get_height() / 2, objects)
                    player2.userName = username
                    continue
            else:
                # Shows the leaderboard
                leaderboard(screen)
                showMenu = True
    
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Checks if player 2 is a online player or not
        if onlinePlayer2 != None:
            onlinePlayer2.send_data(keys, character, username, False, (20, 20))
            player2Data = onlinePlayer2.receive_data()
            
            if player2Data:
                # Checks if a new player instance needs to be created
                if initializePlayer:
                    print("Initialize Second Character")
                    player2 = createPlayer(player2Data["chosenCharacter"], screen.get_width() / 2 + 378, screen.get_height() / 2, objects)
                    player2.userName = player2Data["playerUsername"]
                    initializePlayer = False
                player2.update(player2Data["playerKeys"], screen)
            player1.update(keys, screen)
    
        elif onlinePlayer1 != None:
            onlinePlayer1.send_data(keys, character, username, False, (20, 20))
            player1Data = onlinePlayer1.receive_data()
            
            if player1Data:
                # Checks if a new player instance needs to be created
                if initializePlayer:
                    print("Initialize First Player")
                    player1 = createPlayer(player1Data["chosenCharacter"], screen.get_width() / 2 - 400, screen.get_height() / 2, objects)
                    player1.userName = player1Data["playerUsername"]
                    initializePlayer = False
                player1.update(player1Data["playerKeys"], screen)
            player2.update(keys, screen)
    
        else:

            # TODO: Add the bot that you play against locally
            player1.update(keys, screen)
            player2.play_bot(player1.rect.x, screen)
            
        # Logic for game over
        if player1.lives == 0 or player2.lives == 0:
            winner = None
            playAgain = showGameOver(screen, winner)
            if player1.lives == 0:
                winner = "Player 2"
                if player2.userName:
                    requests.post(r"https://7zo46xcxefurhkuktmn7sjrvlm0flydm.lambda-url.us-east-2.on.aws/", json={"username": player2.userName})
            else:
                winner = "Player 1"
                if player1.userName:
                    requests.post(r"https://7zo46xcxefurhkuktmn7sjrvlm0flydm.lambda-url.us-east-2.on.aws/", json={"username": player1.userName})
            if playAgain:
                player1.resetStats()
                player2.resetStats()
            else:
                showMenu = True
            


        # Updating the players and screen and stuff
        player1Lives = font.render("Player 1 Lives: " + str(player1.lives), True, (0, 0, 0))
        player2Lives = font.render("Player 2 Lives: " + str(player2.lives), True, (0, 0, 0))

        player1Health = font.render("Player 1 Power: " + str(player1.health), True, (0, 0, 0))
        player2Health = font.render("Player 2 Power: " + str(player2.health), True, (0, 0, 0))

        screen.blit(background_image, (0, 0))
        screen.blit(player1Lives, player1LivesPos)
        screen.blit(player2Lives, player2LivesPos)
        screen.blit(player1Health, player1HealthPos)
        screen.blit(player2Health, player2HealthPos)
        screen.blit(menuHelp, menuHelpPos)
        objects.draw(screen)
        allPlayers.draw(screen)
        player1.outgoingAttacks.draw(screen)
        player2.outgoingAttacks.draw(screen)

        # Checking if player 2 was hit 
        if pygame.sprite.spritecollide(player1, player2.outgoingAttacks, False):
            player1.got_hit()
    
        # Checking if player 1 was hit
        if pygame.sprite.spritecollide(player2, player1.outgoingAttacks, False):
            player2.got_hit()

        # flip() the display to put your work on screen
        pygame.display.flip()

        dt = clock.tick(60) / 1000
        await asyncio.sleep(0)

    pygame.quit()
    
    
if __name__ == "__main__":
    asyncio.run(run())