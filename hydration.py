import pygame

class HydrationBar:
    def __init__(self, max_value=100, width=200, height=20, x=20, y=20, color=(255,105,180)):
        self.max_value = max_value
        self.current_value = max_value
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.color = color
        self.background_color = (50,50,50)
        self.border_color = (255,255,255)

    def decrease(self, amount):
        self.current_value -= amount
        if self.current_value < 0:
            self.current_value = 0

    def refill(self, amount):
        self.current_value += amount
        if self.current_value > self.max_value:
            self.current_value = self.max_value

    def draw(self, screen):
        # Draw background
        pygame.draw.rect(screen, self.background_color, (self.x, self.y, self.width, self.height))
        # Draw filled portion
        fill_width = self.width * (self.current_value / self.max_value)
        pygame.draw.rect(screen, self.color, (self.x, self.y, fill_width, self.height))
        # Draw border
        pygame.draw.rect(screen, self.border_color, (self.x, self.y, self.width, self.height), 2)