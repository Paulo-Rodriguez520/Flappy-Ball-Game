import pygame
import sys
import random
import math

# Constants
WIDTH = 800
HEIGHT = 600
CIRCLE_SIZE = 25
GRAVITY = 0.00075
SIZE_INCREASE = 5  # Amount by which the circle size increases when eating stardust
SIZE_DECREASE = 5  # Amount by which the circle size decreases when jumping
MAX_SIZE = 150  # Maximum size of the circle


class Circle:
    def __init__(self, x, y, color, x_velocity=0, y_velocity=0):
        self.x = x
        self.y = y
        self.size = CIRCLE_SIZE
        self.color = color
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.jump_pressed = False  # Flag to track if jump key is pressed
        self.jumps = 0

    def x_movement(self):
        if self.x - self.size <= 0:
            self.x_velocity = abs(self.x_velocity)  # Reverse the direction of movement
            self.x = self.size  # Set the circle's x position to the radius
        elif self.x + self.size >= WIDTH:
            self.x_velocity = -abs(self.x_velocity)  # Reverse the direction of movement
            self.x = WIDTH - self.size  # Set the circle's x position to the right edge - radius
        self.x += self.x_velocity

    def apply_gravity(self):
        self.y_velocity += GRAVITY
        self.y += self.y_velocity

    def jump(self):
        if not self.jump_pressed:
            self.y_velocity = -0.4
            self.jump_pressed = True
            self.size -= SIZE_DECREASE  # Decrease size when jumping
            if self.size < 0:
                self.size = 0
            self.jumps += 1

    def reset_jump(self):
        self.jump_pressed = False

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.size)


class Stardust:
    def __init__(self, x, y, radius, color, y_velocity=1):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.y_velocity = y_velocity

    def move(self):
        self.y += 0.1

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)


class Counter:
    def __init__(self, font_size=24, font_color=(255, 255, 255)):
        self.eaten = 0
        self.jumps = 0
        self.size = CIRCLE_SIZE
        self.font = pygame.font.Font(None, font_size)
        self.color = font_color

    def increase_eaten(self):
        self.eaten += 1

    def increase_jumps(self):
        self.jumps += 1

    def increase_size(self, size):
        self.size = size

    def draw(self, surface, x, y):
        text_eaten = self.font.render(f"Eaten: {self.eaten}", True, self.color)
        text_jumps = self.font.render(f"Jumps: {self.jumps}", True, self.color)
        surface.blit(text_eaten, (x, y))
        surface.blit(text_jumps, (x, y + 30))


# Initialize Pygame
pygame.init()

# Set up the window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")

# Set up the circle
circle_color = (255, 209, 220)  # Pink
circle_x = (WIDTH - CIRCLE_SIZE) // 2
circle_y = (HEIGHT - CIRCLE_SIZE) // 2
circle_x_velocity = 0.2
circle_y_velocity = 0
circle = Circle(circle_x, circle_y, circle_color, circle_x_velocity, circle_y_velocity)

# List to hold stardust particles
stardust_particles = []

# Create a counter
counter = Counter()

def reset():
    global circle, stardust_particles, counter
    circle = Circle((WIDTH - CIRCLE_SIZE) // 2, (HEIGHT - CIRCLE_SIZE) // 2, (255, 209, 220), 0.2, 0)
    stardust_particles = []
    counter = Counter()

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle spacebar press (jump)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                circle.jump()
                counter.increase_jumps()

        # Handle spacebar release (reset jump flag)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                circle.reset_jump()

    # Apply gravity to the circle
    circle.x_movement()
    circle.apply_gravity()

    # Check if the entire circle is below the bottom of the screen
    if circle.y - circle.size >= HEIGHT:
        reset()

    # Check if the circle has reached the maximum size
    if circle.size >= MAX_SIZE:
        # Display "You Won" message
        font = pygame.font.Font(None, 36)
        text = font.render("You Won!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        window.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)  # Wait for 2 seconds
        reset()  # Reset the game

    # Clear the screen
    window.fill((0, 0, 0))  # Fill with black

    # Generate stardust particles randomly
    if random.randint(0, 800) < 5:  # Adjust probability as needed
        stardust_x = random.randint(0, WIDTH)
        stardust_y = 0  # Start at y=0
        stardust_radius = 5
        stardust_y_velocity = 0.5
        stardust_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Random color
        stardust_particles.append(Stardust(stardust_x, stardust_y, stardust_radius, stardust_color, stardust_y_velocity))

    # Move and draw all stardust particles
    for stardust_particle in stardust_particles:
        stardust_particle.move()
        stardust_particle.draw(window)

        # Check for collision with the circle
        distance = math.sqrt((circle.x - stardust_particle.x) ** 2 + (circle.y - stardust_particle.y) ** 2)
        if distance < circle.size + stardust_particle.radius:
            stardust_particles.remove(stardust_particle)
            counter.increase_eaten()
            circle.size += SIZE_INCREASE  # Increase size when eating stardust
            counter.increase_size(circle.size)

    # Draw the circle
    circle.draw(window)

    # Draw the counter
    counter.draw(window, 10, 10)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
