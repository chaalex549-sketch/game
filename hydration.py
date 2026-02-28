import pygame

class Hydration:
    def __init__(self):
        self.hydration = 100
        self.dehydration_rate = 1 # per sec 
        self.heal_water = 0.5 # per sec
        self.update = self.update
        self.hydration = self.hydration
        self.drink = self.drink
        self.draw = self.draw
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
        pygame.draw.rect(screen, (255,255,255), (x, y, bar_width, bar_height), 2)
        pygame.draw.rect(screen, (0,191,255), (x+2, y+2, fill_width-4, bar_height-4))
