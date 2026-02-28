import pygame

class Hydration:
    def bar(self, screen, hydration):
        while hydration > 0:    
            hydration = 100
            max_hydration = 100
            ratio = hydration / max_hydration
            
            pygame.draw.rect(screen, "red", (250, 250, 300, 40))
            pygame.draw.rect(screen, "green", (250, 250, 300 * ratio, 40))


