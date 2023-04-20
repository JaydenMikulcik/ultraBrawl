import pygame
import random
import pickle
from PIL import Image



class Weapon(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        """
        Constructor to create a new  weapon object that
        can be used to attack the other player playing the game
        Param x: the original x position of the attack
        Param y: the original y position of the attack
        Param direction: the direction we want the attack to go
        """
        super().__init__()

        # Setup for the attack
        self.image = pygame.Surface((22, 22))
        self.image.fill((255, 150, 33))  # Red color
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.direction = direction

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['image']  # Remove the unserializable attribute
        return state
    
    def __setstate__(self, state):
        self.__dict__.update(state)
        # Recreate the image attribute from the serialized data
        image_data = pickle.loads(state['image'])
        pil_image = Image.frombytes('RGBA', image_data['size'], image_data['data'])
        surface = pygame.image.frombuffer(pil_image.tobytes(), pil_image.size, 'RGBA')
        self.image = surface
        self.rect = self.image.get_rect()


    def update(self):
        """
        Param to update the spot that the attack is at on the screen
        """
        # todo: add the directions to this function
        if "right" in self.direction:
            self.rect.x += 5
        elif "left" in self.direction:
            self.rect.x -= 5 
        elif "up" in self.direction:
            self.rect.y -= 5 
        elif "down" in self.direction:
            self.rect.y += 5 




class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, platforms_group):
        """
        Constructor for the Player Class
        Param x: the starting x position
        Param y: the starting y position
        Param platforms_group: the platforms that check if the player is standing
        """
        super().__init__()

        # Setup for the game logic
        self.lives = 3
        self.health = 0

        # Setup for the player
        self.image = pygame.Surface((32, 64))
        self.image.fill((255, 0, 0))  # Red color
        self.rect = self.image.get_rect()
        # self.img_bytes = pygame.image.tostring(image, 'RGB')
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.jump_speed = 80
        self.gravity = 3
        self.on_ground = False
        self.platforms = platforms_group
        
        # Setup for attacks
        self.outgoingAttacks = pygame.sprite.Group()
        self.velocity = 2
        self.last_attack_press = 0

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['image']  # Remove the unserializable attribute
        return state
    
    def __setstate__(self, state):
        self.__dict__.update(state)
        # Recreate the image attribute from the serialized data
        image_data = pickle.loads(state['image'])
        pil_image = Image.frombytes('RGBA', image_data['size'], image_data['data'])
        surface = pygame.image.frombuffer(pil_image.tobytes(), pil_image.size, 'RGBA')
        self.image = surface
        self.rect = self.image.get_rect()


    def got_hit(self):
        """
        Method to check if the player got hit and 
        flinging in random direction if hit
        """

        print("One player got hit health is at: " + str(self.health))
        flatHitX = random.randint(-80, 80)
        flatHitY = random.randint(-80, 0)

        varHitX = flatHitX * self.health
        varHitY = flatHitY * self.health

        self.rect.x += varHitX + flatHitX
        self.rect.y += varHitY + flatHitY
        self.health += 1
        


    def add_attack(self, keys):
        """
        This method checks how many outgoing attacks there are if there
        is less than 3 than it adds another attack
        """
        direction = "right"
        if len(self.outgoingAttacks.sprites()) > 3:
            print("to many only 3 attack allowed")
            self.outgoingAttacks.remove(self.outgoingAttacks.sprites()[0])
            return
        
        if keys[pygame.K_RIGHT]:
            direction = "right"
        elif keys[pygame.K_LEFT]:
            direction = "left"
        elif keys[pygame.K_UP]:
            direction = "up"
        elif keys[pygame.K_DOWN]:
            direction = "down"
        elif keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
            direction = "upright"
        elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
            direction = "upleft"
        elif keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
            direction = "rightdown"
        elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
            direction = "leftdown"
        newAttack = Weapon(self.rect.x, self.rect.y, direction)
        self.outgoingAttacks.add(newAttack)



    def execute_attack(self, screen):
        """
        Function to attack the player
        Param: Screen the screen that the attacks are drawn to.
        """
        self.outgoingAttacks.update()
        self.outgoingAttacks.draw(screen)


    def check_game_status(self):
        """
        Method to check if the game should go on
        also checks the lives of each player
        """
        if self.lives and self.rect.y > 780:
            self.rect.x = 740
            self.rect.y = 0
            self.lives -= 1
            self.health = 0
            return
        
        if not self.lives:
            print("Game Over! All 3 lives gone")
            self.lives = 3

        

    def update(self, keys, screen):
        """
        Method to update the player class on the screen
        Param keys: the incoming keys from main logic
        Param screen: the scree from the main logic
        """

        # Checking for the game status to see if over
        self.check_game_status()


        # Logic to control the characters
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if keys[pygame.K_e]:
            if pygame.time.get_ticks() - self.last_attack_press > 200:
                self.add_attack(keys)
                self.last_attack_press = pygame.time.get_ticks()
        self.execute_attack(screen)
    

        # Apply gravity
        if not self.on_ground:
            self.rect.y += self.gravity

        # Check for collisions with platforms
        collided_platforms = pygame.sprite.spritecollide(self, self.platforms, False)
        if collided_platforms:
            self.on_ground = True
            self.rect.bottom = min(platform.rect.top for platform in collided_platforms)
        else:
            self.on_ground = False

        # Handle jumping
        if keys[pygame.K_SPACE] and self.on_ground:
            # Move the player up slightly to avoid collision detection with the platform
            self.rect.y -= 1 
            self.rect.y -= self.jump_speed
            self.on_ground = False