import pygame
from movement import Worm
from bar import Hydration, Health
from bg import Background

pygame.init()

# Screen
W, H = 800, 600
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont("Arial", 24)

# Background (CREATE FIRST)
bg = Background(tile_image_path="underground.png", tile_size=32, rows=313, cols=50)

# Now we can calculate world width
world_width = bg.cols * bg.tile_size

# Game objects
hydration = Hydration()
health_bar = Health()

# Perfect center spawn
worm = Worm("head.png", start_pos=(world_width / 2, 0))

# Camera
camera = pygame.Vector2(0, 0)
camera_smooth = 5

# Constants
MAX_MILES = 100
MAX_PIXELS_Y = MAX_MILES * 100  # 100 pixels = 1 mile

red_tint = pygame.Surface((W, H))
red_tint.fill((255, 255, 255))  # Light red tint

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

    head_pos = worm.segments[0]
    
    # --- HARD WORLD BORDERS ---

    # Horizontal border
    head_pos.x = max(0, min(head_pos.x, world_width))

    # Vertical border (0 to 100 miles)
    head_pos.y = max(0, min(head_pos.y, MAX_PIXELS_Y))

    # Update bars
    hydration.update(dt)
    health_bar.update(dt)

    # Camera follow
    target_cam = head_pos - pygame.Vector2(W // 2, H // 2)
    camera = camera.lerp(target_cam, camera_smooth * dt)

    # Clamp camera
    max_camera_x = world_width - W
    max_camera_y = MAX_PIXELS_Y - H

    camera.x = max(0, min(camera.x, max_camera_x))
    camera.y = max(0, min(camera.y, max_camera_y))

    # Draw
    bg.draw(screen, camera)
    worm.draw(screen, camera)
    hydration.draw(screen, camera)
    health_bar.draw(screen, camera)

    # Depth display
    depth_miles = head_pos.y / 100
    
    if depth_miles >= 90:
        hydration.dehydration_rate = 8
        red_tint.fill((255, 50, 50))
    elif depth_miles >= 75:
        hydration.dehydration_rate = 3.25
        red_tint.fill((255, 100, 100))
    elif depth_miles >= 50:
        hydration.dehydration_rate = 2.75
        red_tint.fill((255, 150, 150))
    elif depth_miles >= 25:
        hydration.dehydration_rate = 2
        red_tint.fill((255, 200, 200))

    else:
        hydration.dehydration_rate = 1
        

    text_surface = font.render(f"{round(depth_miles, 1)} miles", True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.bottomright = (W - 10, H - 10)
    screen.blit(text_surface, text_rect)
    
    
    screen.blit(red_tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    pygame.display.flip()
    

pygame.quit()