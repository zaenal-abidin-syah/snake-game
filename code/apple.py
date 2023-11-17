from settings import *
from random import choice
from math import sin
class Apple:
    def __init__(self, snake):
        self.pos = pygame.Vector2()
        self.display_surface = pygame.display.get_surface()
        self.snake = snake
        self.set_pos()
        self.surf = pygame.image.load(join("..", "graphics", "apple.png")).convert_alpha()
        self.scale_surf = self.surf.copy()
        self.scale_rect = self.scale_surf.get_rect(center=(self.pos.x * CELL_SIZE + CELL_SIZE / 2, self.pos.y * CELL_SIZE + CELL_SIZE / 2))
        

    
    def set_pos(self):
        available_pos = [pygame.Vector2(col, row) for col in range(COLS)  for row in range(ROWS) if (pygame.Vector2(col, row) not in self.snake.body)]
        self.pos = choice(available_pos)

    def draw(self):
        # print(self.pos.y * CELL_SIZE + 40, self.pos.y)
        # rect = pygame.Rect(self.pos.x * CELL_SIZE, self.pos.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        # pygame.draw.rect(self.display_surface ,'blue', rect)
        # self.display_surface.blit(self.surf, rect)
        scale = 1.4+sin(pygame.time.get_ticks() / 200)/3
        self.scale_surf = pygame.transform.smoothscale_by(self.surf, scale)
        self.scale_rect = self.scale_surf.get_rect(center=(self.pos.x * CELL_SIZE + CELL_SIZE / 2, self.pos.y * CELL_SIZE + CELL_SIZE / 2))
        self.display_surface.blit(self.scale_surf, self.scale_rect)