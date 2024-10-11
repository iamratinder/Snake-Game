import pygame
import random
import os


pygame.init()
pygame.mixer.init()

# colors 
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)

screen_width = 1000
screen_height = 700
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Welcome Image
img = pygame.image.load('SnakeGame/pictures/image.png')
img = pygame.transform.scale(img, (screen_width, screen_height)).convert_alpha()

# Background Image
bgimg2 = pygame.image.load('SnakeGame/pictures/image2.png')
bgimg2 = pygame.transform.scale(bgimg2, (screen_width, screen_height)).convert_alpha()

# GameOver Image
overimg = pygame.image.load('SnakeGame/pictures/over.png')
overimg = pygame.transform.scale(overimg, (screen_width, screen_height)).convert_alpha()

clock = pygame.time.Clock()  # defining clock

# game title
pygame.display.set_caption('Snake Game')
pygame.display.update()


font = pygame.font.SysFont(None, 55)       # none means taking the default system font
font_score = pygame.font.SysFont(None, 95)       

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, (x,y))



def plot_snake(gameWindow, color, snk_lst, snake_size):
    for x,y in snk_lst:
        pygame.draw.rect(gameWindow, color,(x, y, snake_size, snake_size),  border_radius=15)      # ploting the snake


def welcome():

    while True:
        gameWindow.blit(img, (0,0))
        # text_screen('Welcome to Snakes!', black, screen_width/2, screen_height/2)
        # text_screen('(Press Space Bar to play)', black, screen_width/2, screen_height/1.5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    
                    pygame.mixer.music.stop()
                    gameLoop()
        pygame.display.update()
        clock.tick(60)

def gameLoop():

    # game specific variables
    exit_game = False
    gameOver = False

    # check if highscore file exists
    if (not os.path.exists('SnakeGame/highScore.txt')):
        with open('SnakeGame/highScore.txt', 'w') as f:
            f.write('0')

    with open('SnakeGame/highScore.txt', 'r') as f:
        highscore = f.read()

    snake_x = 45        # initial position of snake (x vch kina age h (left ton))
    snake_y = 55        # initial position of snake (y vch kina age h (right ton))
    velocity_x = 0      # initial velocity in x
    velocity_y = 0      # initial velocity in y
    snake_size = 30  # size of snake rectangle
    food_radius = 10

    food_x = random.randint(20, int(screen_width/1.5))  # generates random no. bw 20 to screen_width/1.5
    food_y = random.randint(20, int(screen_height/1.5)) # generates random no. bw 20 to screen_height/1.5

    score = 0
    init_velocity = 5


    FPS = 30

    snk_lst = []
    snake_length = 1

    while not exit_game:

        if gameOver:

            gameWindow.blit(overimg, (0,0))
            screen_text = font_score.render(str(score), True, black)
            gameWindow.blit(screen_text, (screen_width/1.8, screen_height/1.26))

            with open('SnakeGame/highScore.txt', 'w') as f:
                f.write(str(highscore))

            # gameWindow.fill(white)
            # text_screen(str(score), black, screen_width/1.7, screen_height/1.2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        
                        pygame.mixer.music.load('SnakeGame/Sounds/intro.mp3')
                        pygame.mixer.music.play()
                        welcome()

        else :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:

                    if velocity_x == 0:
                        if event.key == pygame.K_RIGHT:
                            velocity_x = init_velocity
                            velocity_y = 0

                        if event.key == pygame.K_LEFT:
                            velocity_x = -init_velocity
                            velocity_y = 0

                    if velocity_y == 0:
                        if event.key == pygame.K_UP:
                            velocity_y = -init_velocity
                            velocity_x = 0

                        if event.key == pygame.K_DOWN:
                            velocity_y = init_velocity
                            velocity_x = 0

                    if event.key == pygame.K_LCTRL:
                        score+=10

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_lst.append(head)
            

            if (abs(head[0] - food_x) < 20 and abs(head[1] - food_y) < 20):    # not exactly overlapping but very very close proximity (bcz overlapping may be very rare)
                
                pygame.mixer.music.load('SnakeGame/Sounds/beep.mp3')
                pygame.mixer.music.play()
                
                score+=10
                if score > int(highscore): highscore = score
                food_x = random.randint(20, int(screen_width/1.5))  
                food_y = random.randint(50, int(screen_height/1.5))
                snake_length += 5

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y




            gameWindow.blit(bgimg2, (0,0))
            text_screen("Score : " + str(score) + "     High Score : " + str(highscore), white, 13, 15)

            if len(snk_lst) > snake_length:
                del snk_lst[0]

            if head in snk_lst[:-1]:     # if head is at the same place as any previous element(position) in list
                pygame.mixer.music.load('SnakeGame/Sounds/over.wav')
                pygame.mixer.music.play()
                gameOver = True
            
            plot_snake(gameWindow, green, snk_lst, snake_size)
            # pygame.draw.rect(gameWindow, green, (snake_x, snake_y, snake_size, snake_size))      # ploting the snake
            pygame.draw.circle(gameWindow, red, (food_x, food_y), food_radius)                # ploting the food
        
            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                pygame.mixer.music.load('SnakeGame/Sounds/over.wav')
                pygame.mixer.music.play()
                gameOver = True

        
        pygame.display.update()
        clock.tick(FPS)

pygame.mixer.music.load('SnakeGame/Sounds/intro.mp3')
pygame.mixer.music.play(-1)
welcome()

pygame.quit()
quit()