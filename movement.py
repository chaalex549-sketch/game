import pygame, math

class Worm:
    def __init__(self, head_img_path, num_segments=15, start_pos=(800, 90), speed=180):
        self.segments = [pygame.Vector2(start_pos) for _ in range(num_segments)]
        self.direction = pygame.Vector2(0,1)
        self.speed = speed
        self.segment_dist = 12
        self.time = 0
        self.head_img = pygame.image.load(head_img_path).convert_alpha()
        self.head_img = pygame.transform.scale(self.head_img, (32,32))

    def update(self, dt, keys):
        self.time += dt
        # Turn
        if keys[pygame.K_a]:
            self.direction.rotate_ip(-180*dt)
        if keys[pygame.K_d]:
            self.direction.rotate_ip(180*dt)
        self.direction = self.direction.normalize()

        # Move head
        self.segments[0] += self.direction * self.speed * dt

        # Body follow
        for i in range(1, len(self.segments)):
            prev = self.segments[i-1]
            cur = self.segments[i]
            vec = prev - cur
            dist = vec.length()
            if dist > self.segment_dist:
                vec.scale_to_length(dist - self.segment_dist)
                self.segments[i] += vec

    def draw(self, screen, camera):
        # Draw body as pink squares
        for i, seg in enumerate(self.segments[1:], start=1):
            perp = pygame.Vector2(-self.direction.y, self.direction.x)
            wiggle = math.sin(self.time*6 + i*0.5)*3
            offset = perp*wiggle
            size = max(20 - i*0.3, 6)
            pygame.draw.rect(
                screen,
                (255,105,180),
                pygame.Rect(
                    seg.x - camera.x - size/2 + offset.x,
                    seg.y - camera.y - size/2 + offset.y,
                    size,
                    size
                )
            )

        # Draw head
        head_screen_x = self.segments[0].x - camera.x
        head_screen_y = self.segments[0].y - camera.y
        angle = math.degrees(math.atan2(-self.direction.y, self.direction.x)) - 90
        rotated_head = pygame.transform.rotate(self.head_img, angle)
        rect = rotated_head.get_rect(center=(head_screen_x, head_screen_y))
        screen.blit(rotated_head, rect)