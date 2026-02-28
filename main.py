import pygame
from movement import Worm  # your worm movement file
from hydration import Hydration 

pygame.init()
W, H = 800, 600
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

# Create the worm
worm = Worm("head.png")
camera = pygame.Vector2(0, 0)
camera_smooth = 5

running = True
while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key input
    keys = pygame.key.get_pressed()
    worm.update(dt, keys)

    # Camera follows the worm
    target_cam = worm.segments[0] - pygame.Vector2(W // 2, H // 2)
    camera = camera.lerp(target_cam, camera_smooth * dt)

    # Draw everything
    screen.fill((30, 22, 15))   # background
    worm.draw(screen, camera)   # draw worm
    pygame.display.flip()

pygame.quit()