import pygame
from movement import Worm  # your worm movement file
from bar import Hydration, Health # your hydration and health bar file

hydration = Hydration()
health_bar = Health()

pygame.init()

font = pygame.font.SysFont("Arial", 24)
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
    hydration.update(dt)
    health_bar.update(dt)
    pos = worm.segments[0]/100

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
    hydration.draw(screen, camera)
    health_bar.draw(screen, camera)
    # Create the text surface
    text_surface = font.render(f"{round(float(pos.y),1)} miles", True, (255,255,255))

    # Get its rect so we can position it
    text_rect = text_surface.get_rect()
    text_rect.bottomright = (W - 10, H - 10)  # 10 pixels from bottom-right

    # Draw the text
    screen.blit(text_surface, text_rect)
    pygame.display.flip()

pygame.quit()