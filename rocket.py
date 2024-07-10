import pygame
import sys
import random
import math

pygame.init()

# screen set up 
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Airstrike Game using Rocket")

#color fixed
WHITE = "white"
BLACK = "black"
RED = "red"
ORANGE = "orange"
YELLOW = "yellow"
DARK_BLUE = "blue"
GRAY = "gray"

width = 50  # Chokhuro motsho
height = 100  # Uro motsho

# rocket settings
rocket_x = screen_width // 2 - width // 2  # Rocket er x position
rocket_y = screen_height - height - 20  # Rocket er y position
rocket_speed = 15  # Rocket er speed
rocket_moving_up = False  # Rocket uporer dike chole
rocket_moving_down = False  # Rocket nicher dike chole
rocket_moving_left = False  # Rocket bame chole
rocket_moving_right = False  # Rocket dane chole

# plane settings

plane_width = 60 
plane_height = 40  
plane_speed = 5  

# bigplane settings

big_plane_width = 120  
big_plane_height = 80  
big_plane_speed = 3  
big_plane_health = 10  

flame_particles = 20  
flame_color = [ORANGE, YELLOW]  # Agun er color

# stars fixed
num_stars = 20  # Tara er sonkha
stars = [(random.randint(0, screen_width), random.randint(0, screen_height)) for _ in range(num_stars)]  # Tara

# chad  
moon_x = screen_width - 100  # Chad er x position
moon_y = 100  # Chad er y position
moon_radius = 50  # Chad er radius

# bomb lagar por sound
collision_sound = pygame.mixer.Sound('boom.wav')

# boom banano , moving and speed dewa 
class Boom:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10
        self.active = True

    def move(self):
        self.y -= self.speed # move koro
        if self.y < 0:
            self.active = False # nahole inactive

    def draw(self):
        pygame.draw.circle(screen, RED, (self.x, self.y), 5)

booms = []

# plane banano , movement , draw using transformation 
class Plane:
    def __init__(self):
        self.x = random.randint(0, screen_width - plane_width) # X position
        self.y = random.randint(-200, -plane_height) # Y position
        self.speed = plane_speed 
        self.active = True 

    def move(self):
        self.y += self.speed # move koro
        if self.y > screen_height:
            self.active = False # nahole inactive

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, plane_width, plane_height))
        pygame.draw.polygon(screen, WHITE, [(self.x + 10, self.y), (self.x + plane_width - 10, self.y), 
                                            (self.x + plane_width - 10, self.y - 10), (self.x + 10, self.y - 10)])
        pygame.draw.polygon(screen, WHITE, [(self.x + 20, self.y + plane_height), (self.x + plane_width - 20, self.y + plane_height), 
                                            (self.x + plane_width - 20, self.y + plane_height + 10), (self.x + 20, self.y + plane_height + 10)])
        pygame.draw.polygon(screen, WHITE, [(self.x + plane_width - 20, self.y), (self.x + plane_width, self.y), 
                                            (self.x + plane_width - 15, self.y - 20)])
        pygame.draw.polygon(screen, ORANGE, [(self.x + 20, self.y + 10), (self.x + 40, self.y + 10), 
                                             (self.x + 35, self.y - 15), (self.x + 25, self.y - 15)])

planes = [Plane() for _ in range(5)]

# bigplane draw moving and destroy rocket 
class BigPlane:
    def __init__(self):
        self.x = random.randint(0, screen_width - big_plane_width)
        self.y = random.randint(-400, -big_plane_height)
        self.speed = big_plane_speed
        self.health = big_plane_health
        self.active = True
        self.bomb_drop_interval = 50  # Bomb drop korar interval
        self.frames_since_last_bomb = 0 # Last bomb drop er por ber hoye gesi

    def move(self):
        self.y += self.speed
        if self.y > screen_height:
            self.active = False

        self.frames_since_last_bomb += 1 # Ekta bomb drop korle
        if self.frames_since_last_bomb >= self.bomb_drop_interval:
            self.drop_bomb()
            self.frames_since_last_bomb = 0 # Shesh hole

    def drop_bomb(self):
        bomb_x = self.x + big_plane_width // 2
        bomb_y = self.y + big_plane_height
        big_plane_bombs.append(BigPlaneBomb(bomb_x, bomb_y)) # Bomb drop
    # draw bigplane 
    def draw(self):
        pygame.draw.rect(screen, YELLOW, (self.x, self.y, big_plane_width, big_plane_height))
        pygame.draw.polygon(screen, YELLOW, [(self.x + 20, self.y), (self.x + big_plane_width - 20, self.y), 
                                             (self.x + big_plane_width - 20, self.y - 20), (self.x + 20, self.y - 20)])
        pygame.draw.polygon(screen, YELLOW, [(self.x + 30, self.y + big_plane_height), (self.x + big_plane_width - 30, self.y + big_plane_height), 
                                             (self.x + big_plane_width - 30, self.y + big_plane_height + 20), (self.x + 30, self.y + big_plane_height + 20)])
        pygame.draw.polygon(screen, YELLOW, [(self.x + big_plane_width - 30, self.y), (self.x + big_plane_width, self.y), 
                                             (self.x + big_plane_width - 25, self.y - 40)])
        pygame.draw.polygon(screen, RED, [(self.x + 30, self.y + 20), (self.x + 90, self.y + 20), 
                                          (self.x + 80, self.y - 30), (self.x + 40, self.y - 30)])

big_plane = None
big_plane_active = False
big_plane_diff_score = {"Easy": 50, "Medium": 30, "Hard": 15} # difficulty choose for games

class BigPlaneBomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 7
        self.active = True

    def move(self):
        self.y += self.speed
        if self.y > screen_height:
            self.active = False

    def draw(self):
        pygame.draw.circle(screen, RED, (self.x, self.y), 10)

big_plane_bombs = []
rocket_hit_count = 0
max_hits_by_big_plane_bombs = 20

score = 0
missed_planes = 0
font = pygame.font.SysFont(None, 35)

# agun draw using circle
def draw_flame(x, y):
    for _ in range(flame_particles):
        offset_x = random.randint(-width // 2, width // 2)
        offset_y = random.randint(0, 30)
        flame_radius = random.randint(2, 8)
        flame_color_index = random.randint(0, len(flame_color) - 1)
        pygame.draw.circle(screen, flame_color[flame_color_index], (x + offset_x, y + offset_y), flame_radius)
#draw full moon but saw half moon 
def draw_moon(x, y, radius):
    pygame.draw.circle(screen, YELLOW, (x, y), radius)
    pygame.draw.circle(screen, BLACK, (x - radius // 4, y), radius)

# draw rocket
def draw_rocket(x, y):
    pygame.draw.rect(screen, GRAY, (x, y, width, height))
    pygame.draw.polygon(screen, RED, [(x + width // 2, y - 30),
                                      (x, y),
                                      (x + width, y)])
    pygame.draw.polygon(screen, ORANGE, [(x, y + height - 20),
                                         (x - 20, y + height),
                                         (x, y + height)])
    pygame.draw.polygon(screen, ORANGE, [(x + width, y + height - 20),
                                         (x + width + 20, y + height),
                                         (x + width, y + height)])
    pygame.draw.circle(screen, WHITE, (x + width // 2, y + height // 2), 10)

# display messsage show
def display_message(message, size, color, y_offset=0):
    font = pygame.font.SysFont(None, size)
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 + y_offset))
    screen.blit(text, text_rect)

#collision check
def check_collision(x1, y1, x2, y2, w, h):
    return x1 < x2 + w and x1 + width > x2 and y1 < y2 + h and y1 + height > y2

def draw_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def draw_missed_planes(missed_planes):
    missed_text = font.render(f"Missed Planes: {missed_planes}", True, WHITE)
    screen.blit(missed_text, (10, 50))

def draw_rocket_hit_count(hit_count):
    hit_text = font.render(f"Rocket Hits: {hit_count}", True, WHITE)
    screen.blit(hit_text, (10, 90))


player_id=" "
player_name=" "

#score save using file
def save_score(score, player_id, player_name):
    with open("scores.txt", "a") as file:
        file.write(f"{player_id},{player_name},{score}\n")

#reset game when game over 
def reset_game():
    global rocket_x, rocket_y, rocket_moving_up, rocket_moving_down, rocket_moving_left, rocket_moving_right
    global score, missed_planes, planes, booms, big_plane, big_plane_active, big_plane_bombs, rocket_hit_count
    rocket_x = screen_width // 2 - width // 2
    rocket_y = screen_height - height - 20
    rocket_moving_up = False
    rocket_moving_down = False
    rocket_moving_left = False
    rocket_moving_right = False
    score = 0
    missed_planes = 0
    rocket_hit_count = 0
    planes = [Plane() for _ in range(5)]
    booms = []
    big_plane = None
    big_plane_active = False
    big_plane_bombs = []

def main_menu():
    global player_id, player_name ,difficulty,plane_speed,max_missed_planes # Make sure difficulty is global

    menu = True
    while menu:
        screen.fill(BLACK)
        display_message("Main Menu", 60, WHITE, -200)
        display_message("1. New Game", 40, WHITE, -100)
        display_message("2. Difficulty Levels", 40, WHITE, 0)
        display_message("3. Score Display", 40, WHITE, 100)
        display_message("Press 1, 2, or 3 to select an option", 30, WHITE, 200)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    #new game logic 
                    difficulty = "Easy"  
                    plane_speed=5
                    max_missed_planes=10
                    player_input_screen()  # Pass difficulty to player_input_screen
                elif event.key == pygame.K_2:
                    difficulty_menu()
                elif event.key == pygame.K_3:
                    score_display()

        pygame.display.flip()
    
    difficulty_menu()

def player_input_screen():
    global player_id, player_name
    
    screen.fill(BLACK)
    # display_message("Enter Player ID and Name:", 40, WHITE, -200)
    # display_message("Player ID:", 30, WHITE, -100)
    # display_message("Player Name:", 30, WHITE, 0)
    # pygame.display.flip()

    input_active = "id"
    input_text = ""
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_active == "id":
                        player_id = input_text.strip() 
                        input_active = "name"
                        input_text = ""
                        screen.fill(BLACK)
                        display_message("Enter Player ID and Name:", 40, WHITE, -200)
                        display_message(f"Player ID: {player_id}", 30, WHITE, -100)
                        display_message("Player Name:", 30, WHITE, 0)
                    elif input_active == "name":
                        player_name = input_text.strip()  # Ensure no leading/trailing whitespace
                        screen.fill(BLACK)
                        display_message("Press Enter to start the game...", 30, WHITE, 100)
                        pygame.display.flip()
                        while True:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                elif event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_RETURN:
                                        game_loop()
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        screen.fill(BLACK)
        if input_active == "id":
            display_message(f"Player ID: {input_text}", 30, WHITE, -100)
        elif input_active == "name":
            # display_message(f"Player ID: {player_id}", 30, WHITE, -100)
            display_message(f"Player Name: {input_text}", 30, WHITE, 0)
        pygame.display.flip()
        pygame.time.Clock().tick(30)



def difficulty_menu():
    global difficulty, plane_speed, max_missed_planes
    menu = True
    while menu:
        screen.fill(BLACK)
        display_message("Difficulty Levels", 60, WHITE, -200)
        display_message("1. Easy", 40, WHITE, -100)
        display_message("2. Medium", 40, WHITE, 0)
        display_message("3. Hard", 40, WHITE, 100)
        display_message("Press 1, 2, or 3 to select a difficulty level", 30, WHITE, 200)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    difficulty = "Easy"
                    plane_speed = 5
                    max_missed_planes = 10
                    menu = False
                    player_input_screen()
                elif event.key == pygame.K_2:
                    difficulty = "Medium"
                    plane_speed = 7
                    max_missed_planes = 5
                    menu = False
                    player_input_screen()
                elif event.key == pygame.K_3:
                    difficulty = "Hard"
                    plane_speed = 10
                    max_missed_planes = 3
                    menu = False
                    player_input_screen()

        pygame.display.flip()

def score_display():
    screen.fill(BLACK)
    display_message("Scores", 60, WHITE, -200)

    try:
        with open("scores.txt", "r") as file:
            scores = file.readlines()

        if not scores:
            display_message("No scores available", 40, WHITE, 0)
        else:
            scores = [score.strip().split(',') for score in scores if ',' in score]
            scores = [score for score in scores if len(score) >= 3] 

            if not scores:
                display_message("No valid scores found", 40, WHITE, 0)
            else:
                scores.sort(key=lambda x: int(x[2]), reverse=True) 
                top_scores = scores[:5] 
                for i, score in enumerate(top_scores):
                    display_message(f"{score[1]} - Score: {score[2]}", 40, WHITE, -100 + i * 40)

    except FileNotFoundError:
        display_message("No scores available", 40, WHITE, 0)

    pygame.display.flip()
    pygame.time.wait(2000)
    main_menu()



def game_over():
    screen.fill(BLACK)
    display_message("Game Over", 60, RED)
    display_message(f"Final Score: {score}", 40, WHITE, 100)
    display_message(f"Player ID: {player_id}", 40, WHITE, 150)
    display_message(f"Player Name: {player_name}", 40, WHITE, 200)
    pygame.display.flip()
    pygame.time.wait(2000)
    save_score(score, player_id, player_name)
    reset_game()
    main_menu()

def game_loop():
    global rocket_x, rocket_y, rocket_moving_up, rocket_moving_down, rocket_moving_left, rocket_moving_right
    global score, missed_planes, planes,player_id ,booms, stars, big_plane, big_plane_active, big_plane_bombs, rocket_hit_count
 
   
    screen.fill(BLACK)
    # display_message(f"Player ID: {player_id}.strip()", 30, WHITE, -screen_height//2 + 50)
    # display_message(f"Player Name: {player_name}", 30, WHITE, -screen_height//2 + 100)
    display_message(f"The Game Start....",100, ORANGE,-screen_height//2 + 100)

    pygame.display.flip()
    pygame.time.wait(2000)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # ekhne key kursor press korle rocket move korbe ar space press korle rocket theke bomb ber hbe sei logic dewa hoyeche
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    rocket_moving_up = True
                elif event.key == pygame.K_DOWN:
                    rocket_moving_down = True
                elif event.key == pygame.K_LEFT:
                    rocket_moving_left = True
                elif event.key == pygame.K_RIGHT:
                    rocket_moving_right = True
                elif event.key == pygame.K_SPACE:
                    boom_x = rocket_x + width // 2
                    boom_y = rocket_y
                    booms.append(Boom(boom_x, boom_y))
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    rocket_moving_up = False
                elif event.key == pygame.K_DOWN:
                    rocket_moving_down = False
                elif event.key == pygame.K_LEFT:
                    rocket_moving_left = False
                elif event.key == pygame.K_RIGHT:
                    rocket_moving_right = False
        # rocket jeno window er bahir e na jay etar logic 
        if rocket_moving_up and rocket_y > 0:
            rocket_y -= rocket_speed
        if rocket_moving_down and rocket_y < screen_height - height:
            rocket_y += rocket_speed
        if rocket_moving_left and rocket_x > 0:
            rocket_x -= rocket_speed
        if rocket_moving_right and rocket_x < screen_width - width:
            rocket_x += rocket_speed

        screen.fill(BLACK)
        for star in stars:
            pygame.draw.circle(screen, WHITE, (star[0], star[1]), 2)
        draw_moon(moon_x, moon_y, moon_radius)
        draw_flame(rocket_x + width // 2, rocket_y + height)
        draw_rocket(rocket_x, rocket_y)
        
        # plane activate logic
        for plane in planes:
            if plane.active:
                plane.move()
                if plane.y > screen_height:
                    missed_planes += 1
                    plane.active = False
                plane.draw()
        # boom activate hbe and collision check korbe always jkhn boom plane touch korbe tkhn sound hbe
        for boom in booms:
            if boom.active:
                boom.move()
                boom.draw()
                for plane in planes:
                    if plane.active and check_collision(boom.x, boom.y, plane.x, plane.y, plane_width, plane_height):
                        collision_sound.play()
                        boom.active = False
                        plane.active = False
                        score += 1

        booms = [boom for boom in booms if boom.active]
        planes = [plane for plane in planes if plane.active]

        while len(planes) < 5:
            planes.append(Plane())
        
        #bigplane active hbe jkhn difficulty score er cheye jkhn besi hbe
        if not big_plane_active and score >= big_plane_diff_score[difficulty]:
            big_plane = BigPlane()
            big_plane_active = True

        if big_plane_active:
            big_plane.move()
            big_plane.draw()
            for boom in booms:
                if boom.active and check_collision(boom.x, boom.y, big_plane.x, big_plane.y, big_plane_width, big_plane_height):
                    boom.active = False
                    big_plane.health -= 1
                    if big_plane.health <= 0:
                        big_plane.active = False
                        big_plane_active = False
                        score += 20  # Bonus points big plane marar jonno
            if not big_plane.active:
                big_plane_active = False
        # bigplane theke bomb nambe rocket e hit korle rocket er health kome jabe
        for bomb in big_plane_bombs:
            if bomb.active:
                bomb.move()
                bomb.draw()
                if check_collision(bomb.x, bomb.y, rocket_x, rocket_y, width, height):
                    bomb.active = False
                    rocket_hit_count += 1
                    if rocket_hit_count >= max_hits_by_big_plane_bombs:
                        running = False
                        game_over()

        big_plane_bombs = [bomb for bomb in big_plane_bombs if bomb.active]

        draw_score(score)
        draw_missed_planes(missed_planes)
        draw_rocket_hit_count(rocket_hit_count)
        #game over logic
        if missed_planes >= max_missed_planes or (big_plane_active and not big_plane.active):
            running = False
            game_over()

        pygame.display.flip()
        pygame.time.Clock().tick(30)

    pygame.quit()
    sys.exit()

main_menu()