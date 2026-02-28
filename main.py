import pygame
from movement import Worm        # your worm movement file
from bar import Hydration, Health  # hydration and health bars
from bg import Background

pygame.init()

# Screen
W, H = 800, 600
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

# Font for depth text
font = pygame.font.SysFont("Arial", 24)

# Game objects
hydration = Hydration()
health_bar = Health()
worm = Worm("head.png", start_pos=(400, 0))  # spawn at top middle

# Grid background with image tiles
bg = Background(tile_image_path="underground.png", tile_size=32, rows=100, cols=50)

# Camera
camera = pygame.Vector2(0, 0)
camera_smooth = 5

running = True
while running:
    dt = clock.tick(60) / 1000

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Input
    keys = pygame.key.get_pressed()
    worm.update(dt, keys)

    # Clamp worm inside the grid world
    head_pos = worm.segments[0]
    head_pos.x = max(0, min(head_pos.x, bg.cols * bg.tile_size))
    head_pos.y = max(0, min(head_pos.y, bg.rows * bg.tile_size))

    # Update hydration and health
    hydration.update(dt)
    health_bar.update(dt)

    # Camera follows worm
    target_cam = head_pos - pygame.Vector2(W // 2, H // 2)
    camera = camera.lerp(target_cam, camera_smooth * dt)

    # Clamp camera so it never shows empty space
    max_camera_x = bg.cols * bg.tile_size - W
    max_camera_y = bg.rows * bg.tile_size - H
    camera.x = max(0, min(camera.x, max_camera_x))
    camera.y = max(0, min(camera.y, max_camera_y))

    # Draw everything
    bg.draw(screen, camera)          # draw background tiles
    worm.draw(screen, camera)        # draw worm
    hydration.draw(screen, camera)   # draw hydration
    health_bar.draw(screen, camera)  # draw health

    # Depth text bottom-right
    text_surface = font.render(f"{round(head_pos.y / 100, 1)} miles", True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.bottomright = (W - 10, H - 10)
    screen.blit(text_surface, text_rect)

    pygame.display.flip()

pygame.quit()