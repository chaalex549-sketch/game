import pygame
import random


class WaterPocket:
    def __init__(self, spawn_pos):
        self.position = pygame.Vector2(spawn_pos)
        self.size = 20
        self.color = (0, 191, 255)  # cyan
        self.hydration_restore = 30  # restore 30% of max hydration
        
        self.rect = pygame.Rect(
            self.position.x,
            self.position.y,
            self.size,
            self.size
        )

    def update(self):
        self.rect.topleft = self.position

    def draw(self, screen, camera):
        screen_x = self.position.x - camera.x
        screen_y = self.position.y - camera.y
        pygame.draw.circle(
            screen,
            self.color,
            (screen_x + self.size // 2, screen_y + self.size // 2),
            self.size // 2
        )


class WaterPocketSystem:
    def __init__(self):
        self.pockets = []
        self.spawn_timer = 0
        self.spawn_rate = 5.0  # spawn every 5 seconds
        self.max_pockets = 15

    def update(self, dt, worm, bg, hydration):
        self.spawn_timer += dt

        if self.spawn_timer >= self.spawn_rate and len(self.pockets) < self.max_pockets:
            self.spawn_timer = 0

            world_width = bg.cols * bg.tile_size
            world_height = bg.rows * bg.tile_size

            x = random.randint(0, world_width)
            y = worm.segments[0].y + random.randint(400, 800)
            y = min(y, world_height - 50)

            self.pockets.append(WaterPocket((x, y)))

        # Check collision with worm head
        player_pos = worm.segments[0]
        head_rect = pygame.Rect(player_pos.x, player_pos.y, 32, 32)

        for pocket in self.pockets[:]:
            pocket.update()
            
            if pocket.rect.colliderect(head_rect):
                hydration.hydration += pocket.hydration_restore
                hydration.hydration = min(hydration.hydration, 100)
                self.pockets.remove(pocket)
            elif pocket.position.y < worm.segments[0].y - 1200:
                # remove pockets that fall far above the player
                self.pockets.remove(pocket)

    def draw(self, screen, camera):
        for pocket in self.pockets:
            pocket.draw(screen, camera)
