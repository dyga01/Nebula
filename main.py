# Nebula Game
import pygame
import random

# pygame setup
pygame.init()
WIDTH, HEIGHT = 500, 500 
STAR_COUNT = 50
PLANET_COUNT = 3
SCALE = 1
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nebula")
clock = pygame.time.Clock()
running = True
collision_flag = False
dt = 0
paused_time = 0  
delay_duration = 3 # delay at start of game

# Define game states
MENU = 0
RUNNING = 1
PAUSED = 2
game_state = MENU

# Defines music
pygame.mixer.init()
pygame.mixer.music.load("bgmusic.mp3")
pygame.mixer.music.set_volume(0.7) 
pygame.mixer.music.play() 

# Creates Ship 
oship = pygame.image.load("images/ship.png").convert_alpha()
ship = pygame.transform.scale(oship, (100, 100))
ship_center_x = WIDTH // 2 - ship.get_width() // 2
ship_center_y = HEIGHT // 2 - ship.get_height() // 2
ship_x = WIDTH // 2 - ship.get_width() // 2
ship_y = HEIGHT // 2 - ship.get_height() // 2
ship_rect = ship.get_rect(topleft=(200, 200))
ship_mask = pygame.mask.from_surface(ship)

# Creates Boost
oboost = pygame.image.load("images/boost.png")
boost = pygame.transform.scale(oboost, (40, 40))
boost_center_x = ship_center_x + (ship.get_width() // 2) - (boost.get_width() // 2)
boost_center_y = ship_center_y + ship.get_height()
boost_x = WIDTH // 2 - boost.get_width() // 2
boost_y = HEIGHT // 2 - boost.get_height() // 2

# Define Planets Class
class Planet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        radius = random.randint(30, 45)  
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)  
        pygame.draw.circle(self.image, "blue", (radius, radius), radius)  
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH)
        self.rect.y = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y += SCALE
        if self.rect.y > HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randrange(0, WIDTH)

# Create a group for planets
planets = pygame.sprite.Group()
for _ in range(PLANET_COUNT):
    planet = Planet()
    planets.add(planet)

# Define Star class
class Star(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        radius = random.randint(1, 3)  # Random radius between 1 and 3
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)  
        pygame.draw.circle(self.image, "white", (radius, radius), radius)  
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH)
        self.rect.y = random.randrange(0, HEIGHT)

    def update(self):
        self.rect.y += SCALE
        if self.rect.y > HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randrange(0, WIDTH)

# Create a group for stars
stars = pygame.sprite.Group()
for _ in range(STAR_COUNT):
    star = Star()
    stars.add(star)

# Creates score
pygame.font.init() 
my_font = pygame.font.SysFont('Tahoma', 20)

# Runs Pong
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            running = False

    # Background Color
    screen.fill("black")

    # Creates Moving Stars
    stars.update()
    stars.draw(screen)  

    if game_state == MENU:
        # Create a rectangle around the menu display with a purple fill
        menu_rect = pygame.Rect(WIDTH // 4, HEIGHT // 4, WIDTH // 2, HEIGHT // 2)
        pygame.draw.rect(screen, (197, 156, 255), menu_rect)  # Purple color
        
        # Display menu text
        menu_text = my_font.render("Nebula", True, (255, 255, 255))
        start_text = my_font.render("press enter to play", True, (255, 255, 255))
        exit_text = my_font.render("press esc to exit", True, (255, 255, 255))
        
        screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
        screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 50))

        # Display game over message
        if collision_flag:
            game_over_text = my_font.render("Game Over", True, (255, 0, 0))  # Red color for Game Over
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
        else:
            menu_text = my_font.render("Nebula", True, (255, 255, 255))
            start_text = my_font.render("press enter to play", True, (255, 255, 255))
            exit_text = my_font.render("press esc to exit", True, (255, 255, 255))
            
            screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
            screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 50))
        
        # Check for keypress to start game or exit
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            game_state = RUNNING
            elapsed_time = 0
        elif keys[pygame.K_ESCAPE]:
            pygame.mixer.music.stop()
            running = False
    
    elif game_state == RUNNING: 
        # Time and score
        elapsed_time = pygame.time.get_ticks() // 1000
        score = my_font.render(str(elapsed_time - paused_time), False, (255, 255, 255))

        # Updates Time
        screen.blit(score, (10,10))

        # Creates Moving Planets
        if elapsed_time >= delay_duration:
            planets.update()
            planets.draw(screen)  

        # Speeds Up Stars to Create Boost Illusion
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_w]:
            SCALE += .01
        if pressed_keys[pygame.K_a] and ship_x > 0:
            ship_x -= 3
            ship_center_x = ship_x  
            boost_x -= 3
            boost_center_x = boost_x
            screen.blit(boost, (boost_center_x, boost_center_y))
        if pressed_keys[pygame.K_d] and ship_x + ship.get_width() < WIDTH:
            ship_x += 3 
            ship_center_x = ship_x
            boost_x += 3
            boost_center_x = boost_x
            screen.blit(boost, (boost_center_x, boost_center_y))
        if pressed_keys[pygame.K_SPACE]:
            game_state = PAUSED

        # Updates Ship and Boost
        screen.blit(ship, (ship_center_x, ship_center_y))
        ship_rect.topleft = (ship_center_x, ship_center_y)  

       # Check for collision between ship and planets
        for planet in planets:
            offset_x = planet.rect.x - ship_rect.x
            offset_y = planet.rect.y - ship_rect.y
            if ship_mask.overlap(planet.mask, (offset_x, offset_y)):
                collision_flag = True
                game_state = MENU
                elapsed_time = 0
                break

    elif game_state == PAUSED:
        # Track paused time
        paused_time = pygame.time.get_ticks() // 1000
        # Display pause message or screen
        menu_rect = pygame.Rect(WIDTH // 4, HEIGHT // 4, WIDTH // 2, HEIGHT // 2)
        pygame.draw.rect(screen, (197, 156, 255), menu_rect)  # Purple color
        menu_text = my_font.render("Nebula", True, (255, 255, 255))
        start_text = my_font.render("press space to resume", True, (255, 255, 255))
        screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))

        # Check for space key press to resume game
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_SPACE]:
            game_state = RUNNING  # Resume game

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    dt = clock.tick(60) / 1000
