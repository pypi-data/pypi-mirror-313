import pygame
import random

def obstacles_game():
    class Sprite():
        def __init__(self, x, y, speed, width, height, color):
            self.x = x
            self.y = y
            self.speed = speed
            self.width = width
            self.height = height
            self.color = color
            self.direction = random.choice(['up', 'down', 'left', 'right'])

        def draw(self, mw):
            pygame.draw.rect(mw, self.color, (self.x, self.y, self.width, self.height))

        def draw_circle(self, mw):
            #pygame.draw.circle(mw, self.color, (self.x, self.y), radius)
            pygame.draw.ellipse(mw, self.color, (self.x, self.y, self.width, self.height))

        def make_step(self):
            if self.direction == 'up':
                self.y -= self.speed
            if self.direction == 'down':
                self.y += self.speed
            if self.direction == 'left':
                self.x -= self.speed
            if self.direction == 'right':
                self.x += self.speed

        def reach_boarders(self):
            if self.y > 700:
                self.direction = 'up'
            if self.y < 0:
                self.direction = 'down'
            if self.x > 700:
                self.direction = 'left'
            if self.x < 0:
                self.direction = 'right'

        def is_collide(self, other, dist):
            if self.x > other.x - dist and self.x < other.x + dist:
                if self.y > other.y - dist and self.y < other.y + dist:
                    return True
        
    class Label():
        def __init__(self, x, y, fontsize, color):
            self.x = x
            self.y = y
            self.font = pygame.font.Font(None, fontsize)
            self.color = color

        def draw_text(self, text):
            textbox = self.font.render(text, True, self.color)
            window.blit(textbox, (self.x, self.y))

    # Initialize Pygame
    pygame.init()

    # Set Command Variables
    score = 0
    checkscore = 0
    checkpoint_set = False
    
    lost = False
    window = pygame.display.set_mode((700, 700))
    clock = pygame.time.Clock()   
    background = (220, 220, 220)

    # Setting up Sprites
    player = Sprite(x=350, y=350, speed=30, width=20, height=20, color=(0, 0, 255))
    target = Sprite(x=random.randint(50, 650), y=random.randint(50, 650), speed=0, width=20, height=20, color=(0, 255, 0))
    obstacles = [Sprite(x=random.randint(50, 650), y=random.randint(50, 650), speed=5, width=20, height=20, color=(255, 0, 0)) for _ in range(3)]
    checkpoint = Sprite(x=player.x + 2.5, y=player.y + 2.5, speed=0, width=15, height=15, color=(50, 255, 50))

    # Set Window Title
    pygame.display.set_caption('Obstacles Game')
    
    # The Game Loop
    running = True
    while running:
        window.fill(background)

        # Draw Player
        player.draw(window)

        # Draw Target
        target.draw_circle(window)

        # Draw Checkpoint
        if checkpoint_set == True:
            checkpoint.draw(window)

        # Draw the TextBox
        if lost == False:
            writer = Label(x=20, y=20, fontsize=30, color=(0, 128, 0))
            writer.draw_text(text=f'Score: {score}')

            writer = Label(x=20, y=45, fontsize=30, color=(0, 128, 0))
            writer.draw_text(text=f'Checkpoints: {checkscore//3}')
        else:
            writer = Label(x=270, y=270, fontsize=60, color=(0, 0, 0))
            writer.draw_text(text='You lost!')

            writer = Label(x=290, y=320, fontsize=50, color=(0, 0, 0))
            writer.draw_text(text=f'Score: {score}')

        for obstacle in obstacles:
            obstacle.draw(window)                               # Draw Obstacles
            obstacle.reach_boarders()                           # Check if obstacles are in the boarders
            obstacle.make_step()                                # Move the obstacles

        if player.is_collide(target, 30) == True:
            target.x = random.randint(50, 650)
            target.y = random.randint(50, 650)
            obstacles.append(Sprite(x=random.randint(50, 650), y=random.randint(50, 650), speed=5, width=20, height=20, color=(255, 0, 0)))
            score += 1
            checkscore += 1

        for obstacle in obstacles:
            if player.is_collide(obstacle, 25) == True:
                if checkpoint_set == True:
                    window.fill((50, 255, 50))
                    checkpoint_set = False
                    player.x = checkpoint.x
                    player.y = checkpoint.y
                else:
                    lost = True
                    background = (255, 50, 50)
                    player.speed = 0
                    player.color = (220, 220, 220)
                    target.color = (220, 220, 220)
                    if checkpoint_set == True:
                        checkpoint.color = (220, 220, 220)
                    for obstacle in obstacles:
                        obstacle.speed = 0
                        obstacle.color = (220, 220, 220)

        # Keyboard Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.direction = 'up'
                    player.make_step()
                if event.key == pygame.K_DOWN:
                    player.direction = 'down'
                    player.make_step()
                if event.key == pygame.K_LEFT:
                    player.direction = 'left'
                    player.make_step()
                if event.key == pygame.K_RIGHT:
                    player.direction = 'right'
                    player.make_step()
                if event.key == pygame.K_r:
                    if lost == True:
                        # Setting up Sprites
                        player = Sprite(x=350, y=350, speed=30, width=20, height=20, color=(0, 0, 255))
                        target = Sprite(x=random.randint(50, 650), y=random.randint(50, 650), speed=0, width=20, height=20, color=(0, 255, 0))
                        obstacles = [Sprite(x=random.randint(50, 650), y=random.randint(50, 650), speed=5, width=20, height=20, color=(255, 0, 0)) for _ in range(3)]
                        # Set Command Variables
                        score = 0
                        checkscore = 0
                        lost = False   
                        background = (220, 220, 220)
                if event.key == pygame.K_SPACE:
                    if checkscore >= 3:
                        checkscore -= 3
                        checkpoint_set = True
                        checkpoint.x = player.x + 2.5
                        checkpoint.y = player.y + 2.5

        # Update Display
        pygame.display.update()

        # Tick Rate (48 FPS)
        clock.tick(48)

    # Quit Game
    pygame.quit()
obstacles_game()