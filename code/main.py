from settings import * 
from snake import Snake
from apple import Apple

class Main:
    def __init__(self):

        # init
        pygame.init()
        pygame.display.set_caption('Snake Game')
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.bg_rects = [pygame.Rect((col + int(row%2==0))*CELL_SIZE,row*CELL_SIZE, CELL_SIZE, CELL_SIZE) for col in range(0, COLS, 2) for row in range(ROWS)]

        # snake
        self.snake = Snake()

        # apple
        self.apple = Apple(self.snake)

        # updates

        self.update_event = pygame.event.custom_type()

        pygame.time.set_timer(self.update_event, 200)
        self.game_active = False

        # audio
        self.crunch_sound = pygame.mixer.Sound(join('..', 'audio', 'crunch.wav'))
        self.bg_sound = pygame.mixer.Sound(join('..', 'audio', 'Arcade.ogg'))
        self.bg_sound.play(-1).set_volume(0.5)
        self.game_over = pygame.mixer.Sound(join('..', 'audio', 'game_over.mp3'))

    def draw_rects(self):
        self.display_surface.fill(DARK_GREEN)
        for rect in self.bg_rects:
            pygame.draw.rect(self.display_surface, LIGHT_GREEN, rect)
    
    def draw_shadow(self):
        shadow_surf = pygame.Surface(self.display_surface.get_size())
        shadow_surf.fill((0,255,0))
        shadow_surf.set_colorkey((0,255,0))
        shadow_surf.blit(self.apple.scale_surf, self.apple.scale_rect.topleft + SHADOW_SIZE)
        for surf, rect in self.snake.draw_data:
            shadow_surf.blit(surf, rect.topleft + SHADOW_SIZE)
        mask = pygame.mask.from_surface(shadow_surf)
        mask.invert()
        shadow_surf = mask.to_surface()
        shadow_surf.set_colorkey((255, 255, 255, 0.5))
        shadow_surf.set_alpha(SHADOW_OPACITY)
        self.display_surface.blit(shadow_surf, (0,0))
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] and self.snake.direction.x != -1:
            self.snake.direction = pygame.Vector2(1, 0)
        if keys[pygame.K_LEFT] and self.snake.direction.x != 1:
            self.snake.direction = pygame.Vector2(-1, 0)
        if keys[pygame.K_UP] and self.snake.direction.y != 1:
            self.snake.direction = pygame.Vector2(0, -1)
        if keys[pygame.K_DOWN] and self.snake.direction.y != -1:
            self.snake.direction = pygame.Vector2(0, 1)
        
    
    def collision(self): 
        # apple
        if self.snake.body[0] == self.apple.pos:
            self.crunch_sound.play()
            self.snake.has_eaten = True
            self.apple.set_pos()
        # game over
        
        if self.snake.body[0] in self.snake.body[1:] or not 0 <= self.snake.body[0].x < COLS or not 0 <= self.snake.body[0].y < ROWS:
            self.game_over.play()
            self.snake.reset()
            self.game_active = False
        
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == self.update_event and self.game_active:
                    self.snake.update()
                if event.type == pygame.KEYDOWN and not self.game_active:
                    self.game_active = True
                
                
                self.draw_rects()
                self.draw_shadow()
                self.snake.draw()
                self.apple.draw()
                
                self.input()
                self.collision()                
                pygame.display.update()
                

if __name__ == "__main__":
    main = Main()
    main.run()