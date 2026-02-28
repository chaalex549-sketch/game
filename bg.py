import pygame

class Background:
    def __init__(self, tile_image_path, tile_size=32, rows=50, cols=50):
        self.tile_size = tile_size
        self.rows = rows
        self.cols = cols

        # Load the image for every tile
        self.tile_image = pygame.image.load(tile_image_path).convert_alpha()
        self.tile_image = pygame.transform.scale(self.tile_image, (tile_size, tile_size))

        # Grid: just store tile indices (all 0 since one image)
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

    def draw(self, screen, camera):
        # Draw only visible tiles for efficiency
        start_col = max(int(camera.x // self.tile_size), 0)
        start_row = max(int(camera.y // self.tile_size), 0)
        end_col = min(start_col + (screen.get_width() // self.tile_size) + 2, self.cols)
        end_row = min(start_row + (screen.get_height() // self.tile_size) + 2, self.rows)

        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                rect = pygame.Rect(
                    col*self.tile_size - camera.x,
                    row*self.tile_size - camera.y,
                    self.tile_size,
                    self.tile_size
                )
                screen.blit(self.tile_image, rect)