import pygame
import random


class Enemy:
    def __init__(self, spawn_pos):
        self.position = pygame.Vector2(spawn_pos)
        self.size = 36
        self.speed = random.randint(60, 120)
        self.color = (180, 40, 40)

        self.damage = 8
        self.attack_delay = 0.8
        self.attack_timer = 0

        self.rect = pygame.Rect(
            self.position.x,
            self.position.y,
            self.size,
            self.size
        )

        # Load enemy image
        try:
            self.image = pygame.image.load("enemy1.png").convert_alpha()
        except FileNotFoundError:
            # Create placeholder enemy image if file not found
            self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.rect(self.image, self.color, (0, 0, self.size, self.size))
        
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

    def update(self, dt, worm):
        # movement toward the player's head only; damage is handled by the system
        player_pos = worm.segments[0]  # note: keep for direction calculation
        direction = player_pos - self.position

        if direction.length() > 0:
            direction = direction.normalize()
            self.position += direction * self.speed * dt

        # update bounding box and cooldown timer
        self.rect.topleft = self.position
        if self.attack_timer > 0:
            self.attack_timer -= dt

    def draw(self, screen, camera):
        screen_x = self.position.x - camera.x
        screen_y = self.position.y - camera.y
        screen.blit(self.image, (screen_x, screen_y))


class EnemySystem:
    def __init__(self):
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_rate = 2.5
        self.max_enemies = 20

    def update(self, dt, worm, bg, health_bar):
        self.spawn_timer += dt

        if self.spawn_timer >= self.spawn_rate and len(self.enemies) < self.max_enemies:
            self.spawn_timer = 0

            world_width = bg.cols * bg.tile_size
            world_height = bg.rows * bg.tile_size

            x = random.randint(0, world_width)
            y = worm.segments[0].y + random.randint(400, 800)
            y = min(y, world_height - 50)

            self.enemies.append(Enemy((x, y)))

        # constants for damage percentages (based on max health = 100)
        HEAD_DAMAGE_PCT = 0.10
        BODY_DAMAGE_PCT = 0.02

        for enemy in self.enemies[:]:
            enemy.update(dt, worm)  # position and timer

            player_pos = worm.segments[0]
            head_rect = pygame.Rect(player_pos.x, player_pos.y, 32, 32)

            # head collision (10% damage)
            if enemy.rect.colliderect(head_rect):
                if enemy.attack_timer <= 0:
                    health_bar.health -= 100 * HEAD_DAMAGE_PCT
                    health_bar.health = max(health_bar.health, 0)
                    enemy.attack_timer = enemy.attack_delay

            # body collisions; enemy dies and deals 2% damage
            hit_body = False
            for body_seg in worm.segments[1:]:
                seg_rect = pygame.Rect(body_seg.x, body_seg.y, 32, 32)
                if enemy.rect.colliderect(seg_rect):
                    health_bar.health -= 100 * BODY_DAMAGE_PCT
                    health_bar.health = max(health_bar.health, 0)
                    self.enemies.remove(enemy)
                    hit_body = True
                    break

            if hit_body:
                continue

            # remove enemies that fall far above the player (out of range)
            if enemy.position.y < worm.segments[0].y - 1200:
                self.enemies.remove(enemy)

    def draw(self, screen, camera):
        for enemy in self.enemies:
            enemy.draw(screen, camera)