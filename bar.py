import pygame

class Hydration:
    def __init__(self):
        self.hydration = 100
        self.dehydration_rate = 1  # per sec
        self.heal_water = 0.5      # per sec

    def update(self, dt):
        self.hydration -= self.dehydration_rate * dt
        self.hydration = max(self.hydration, 0)

    def drink(self, amount):
        self.hydration += amount * self.heal_water
        self.hydration = min(self.hydration, 100)

    def draw(self, screen, camera):
        bar_width = 200
        bar_height = 20
        x = 10
        y = 10
        fill_width = int(bar_width * (self.hydration / 100))
        # choose color: normal blue, flash red when low
        if self.hydration < 25:
            # alternate every half second
            if (pygame.time.get_ticks() // 500) % 2 == 0:
                fill_color = (255, 0, 0)
            else:
                fill_color = (0, 191, 255)
        else:
            fill_color = (0, 191, 255)
        pygame.draw.rect(screen, (255,255,255), (x, y, bar_width, bar_height), 2)  # border
        pygame.draw.rect(screen, fill_color, (x+2, y+2, fill_width-4, bar_height-4))  # fill

class Health:
    def __init__(self):
        self.health = 100

    def update(self, dt):
        pass  # health doesn’t decrease over time

    def heal(self, amount):
        self.health += amount
        self.health = min(self.health, 100)

    def draw(self, screen, camera):
        bar_width = 200
        bar_height = 20
        x = 10
        y = 40
        fill_width = int(bar_width * (self.health / 100))
        pygame.draw.rect(screen, (255,255,255), (x, y, bar_width, bar_height), 2)  # border
        pygame.draw.rect(screen, (50,205,50), (x+2, y+2, fill_width-4, bar_height-4))  # fill