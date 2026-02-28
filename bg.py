import pygame

class Background:
    def __init__(self, tile_image_path, tile_size=32, rows=313, cols=50):  # 313 rows ≈ 100 miles
        self.tile_size = tile_size
        self.rows = rows
        self.cols = cols
        self.tile_image = pygame.image.load(tile_image_path).convert_alpha()
        self.tile_image = pygame.transform.scale(self.tile_image, (tile_size, tile_size))

    def draw(self, screen, camera):
        # Determine which tiles are visible
        start_col = max(int(camera.x // self.tile_size), 0)
        start_row = max(int(camera.y // self.tile_size), 0)
        end_col = min(start_col + (screen.get_width() // self.tile_size) + 2, self.cols)
        end_row = start_row + (screen.get_height() // self.tile_size) + 2

        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                # Repeat tiles vertically if the worm goes beyond rows
                tile_y = (row % self.rows) * self.tile_size - camera.y
                tile_x = col * self.tile_size - camera.x
                screen.blit(self.tile_image, (tile_x, tile_y))