import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("2D Roguelike in Pygame")

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the window with a black background
    window.fill((0, 0, 0))  # RGB (0, 0, 0) is black

    # Example of rendering a simple shape (a white rectangle)
    pygame.draw.rect(window, (255, 255, 255), pygame.Rect(100, 100, 50, 50))

    # Update the display
    pygame.display.flip()

# Clean up and close the game
pygame.quit()
sys.exit()
