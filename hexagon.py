import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
HEX_RADIUS = 100
BALL_RADIUS = 20
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hexagon Bouncing Ball")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

class Ball:
    def __init__(self, color, angle):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.speed = 5
        self.angle = angle
        self.color = color

    def move(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

        # Check collision with walls
        if self.x - BALL_RADIUS <= 0 or self.x + BALL_RADIUS >= WIDTH:
            self.angle = math.pi - self.angle
            self.speed *= 0.9  # Adjust the deceleration factor

        if self.y - BALL_RADIUS <= 0 or self.y + BALL_RADIUS >= HEIGHT:
            self.angle = -self.angle
            self.speed *= 0.9  # Adjust the deceleration factor


    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), BALL_RADIUS)

# Create an initial ball
balls = [Ball(RED, random.uniform(0, 2 * math.pi))]

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move and draw the balls
    for ball in balls:
        ball.move()
        ball.draw()

    # Check if any ball should split into three
    for ball in balls[:]:
        if ball.speed > 20:  # Maximum speed to prevent infinite splitting
            continue

        if ball.x - BALL_RADIUS <= 0 or ball.x + BALL_RADIUS >= WIDTH or \
           ball.y - BALL_RADIUS <= 0 or ball.y + BALL_RADIUS >= HEIGHT:
            angle1 = ball.angle + random.uniform(-math.pi/6, math.pi/6)
            angle2 = ball.angle + math.pi + random.uniform(-math.pi/6, math.pi/6)
            angle3 = ball.angle + 2*math.pi + random.uniform(-math.pi/6, math.pi/6)

            balls.remove(ball)
            balls.extend([Ball(GREEN, angle1), Ball(BLUE, angle2), Ball(RED, angle3)])

    # Draw hexagon
    pygame.draw.polygon(screen, WHITE, [
        (WIDTH // 2 + HEX_RADIUS * math.cos(angle), HEIGHT // 2 + HEX_RADIUS * math.sin(angle))
        for angle in [0, math.pi/3, 2*math.pi/3, 3*math.pi/3, 4*math.pi/3, 5*math.pi/3]
    ], 2)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(FPS)

    # Clear the screen
    screen.fill((0, 0, 0))

# Quit pygame
pygame.quit()
sys.exit()
