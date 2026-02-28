import pygame
from movement import Worm
from bar import Hydration, Health
from bg import Background
from enemy import EnemySystem
from waterpocket import WaterPocketSystem

pygame.init()

# ---------------- SCREEN ----------------
W, H = 800, 600
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# ---------------- WORLD ----------------
bg = Background(tile_image_path="underground.png",
                tile_size=32,
                rows=313,
                cols=50)

world_width = bg.cols * bg.tile_size

MAX_MILES = 100
MAX_PIXELS_Y = MAX_MILES * 100  # 100 pixels = 1 mile

# ---------------- GAME OBJECTS ----------------
hydration = Hydration()
health_bar = Health()
worm = Worm("head.png", start_pos=(world_width / 2, 0))

enemy_system = EnemySystem()
water_pocket_system = WaterPocketSystem()

# ---------------- CAMERA ----------------
camera = pygame.Vector2(0, 0)
camera_smooth = 5

# ---------------- VISUAL EFFECT ----------------
red_tint = pygame.Surface((W, H))
red_tint.set_alpha(80)

# ---------------- GAME LOOP ----------------
running = True
while running:
    dt = clock.tick(60) / 1000

    # -------- EVENTS --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # -------- INPUT --------
    keys = pygame.key.get_pressed()
    worm.update(dt, keys)

    head_pos = worm.segments[0]

    # -------- HARD WORLD BORDERS --------
    head_pos.x = max(0, min(head_pos.x, world_width))
    head_pos.y = max(0, min(head_pos.y, MAX_PIXELS_Y))

    # -------- UPDATE SYSTEMS --------
    hydration.update(dt)
    health_bar.update(dt)

    enemy_system.update(dt, worm, bg, health_bar)
    water_pocket_system.update(dt, worm, bg, hydration)

    # -------- DEPTH DIFFICULTY --------
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
        red_tint.fill((255, 255, 255))

    # -------- CAMERA --------
    target_cam = head_pos - pygame.Vector2(W // 2, H // 2)
    camera = camera.lerp(target_cam, camera_smooth * dt)

    max_camera_x = world_width - W
    max_camera_y = MAX_PIXELS_Y - H

    camera.x = max(0, min(camera.x, max_camera_x))
    camera.y = max(0, min(camera.y, max_camera_y))

    # -------- DRAW --------
    bg.draw(screen, camera)
    worm.draw(screen, camera)

    enemy_system.draw(screen, camera)
    water_pocket_system.draw(screen, camera)

    hydration.draw(screen, camera)
    health_bar.draw(screen, camera)

    # Depth text
    text_surface = font.render(f"{round(depth_miles, 1)} miles", True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.bottomright = (W - 10, H - 10)
    screen.blit(text_surface, text_rect)

    # victory check
    if depth_miles >= MAX_MILES:
        victory_surface = font.render("VICTORY! 100 miles", True, (255, 215, 0))
        victory_rect = victory_surface.get_rect(center=(W // 2, H // 2))
        screen.blit(victory_surface, victory_rect)
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False
        continue
    
    # Heat tint overlay
    screen.blit(red_tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    if health_bar.health <= 0 or hydration.hydration <= 0:
        game_over_surface = font.render("Game Over", True, (255, 0, 0))
        game_over_rect = game_over_surface.get_rect(center=(W // 2, H // 2))
        screen.blit(game_over_surface, game_over_rect)
        

    pygame.display.flip()


pygame.quit()
