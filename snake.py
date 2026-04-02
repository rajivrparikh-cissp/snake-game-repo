import pygame
import random
import sys
import asyncio

# Initialize pygame
pygame.init()

# Setup display
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
GOLD = (255, 215, 0)

# Clock for controlling game speed
clock = pygame.time.Clock()
snake_block = 20
snake_speed = 15

# Fonts
# Provide fallbacks if the chosen fonts are not available on all systems
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def your_score(score):
    value = score_font.render("Score: " + str(score), True, WHITE)
    screen.blit(value, [0, 0])

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], snake_block, snake_block])

def message(msg, color, y_displace=0):
    mesg = font_style.render(msg, True, color)
    text_rect = mesg.get_rect(center=(width / 2, height / 2 + y_displace))
    screen.blit(mesg, text_rect)

async def gameLoop():
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
    foody = round(random.randrange(0, height - snake_block) / 20.0) * 20.0
    golden_foodx = None
    golden_foody = None
    golden_timer = 0

    while not game_over:

        while game_close == True:
            screen.fill(BLACK)
            message("You Lost! Press C to Play Again or Q to Quit", RED, -30)
            your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
                        return
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
            
            await asyncio.sleep(0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        # Boundary rules
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True
            
        x1 += x1_change
        y1 += y1_change
        screen.fill(BLACK)
        
        # Draw food
        pygame.draw.rect(screen, RED, [foodx, foody, snake_block, snake_block])
        
        # Manage Golden Apple spawning
        if golden_foodx is None and random.randint(1, 150) == 1:
            golden_foodx = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
            golden_foody = round(random.randrange(0, height - snake_block) / 20.0) * 20.0
            golden_timer = 60 # Stays for 60 frames
            
        if golden_foodx is not None:
            pygame.draw.rect(screen, GOLD, [golden_foodx, golden_foody, snake_block, snake_block])
            golden_timer -= 1
            if golden_timer <= 0:
                golden_foodx = None
                golden_foody = None
        
        # Manage snake length and position
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Check self-collision
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        your_score(Length_of_snake - 1)

        pygame.display.update()

        # Check if food eaten
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(0, height - snake_block) / 20.0) * 20.0
            Length_of_snake += 1

        # Check if golden apple eaten
        if golden_foodx is not None and x1 == golden_foodx and y1 == golden_foody:
            Length_of_snake += 5
            golden_foodx = None
            golden_foody = None

        clock.tick(snake_speed)
        await asyncio.sleep(0)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    asyncio.run(gameLoop())
