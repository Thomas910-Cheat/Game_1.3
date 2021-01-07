import pygame, random, os


class Settings:
    window_width = 1024
    window_height = 768
    window_border = 10
    amout_enemy = 10
    file_path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(file_path, "images")
    title = "GAME_1.3_KOLEBSKI" 
    
class Background(object):
    def __init__(self, filename):
        self.image = pygame.image.load(os.path.join(Settings.image_path, filename))
        self.image = pygame.transform.scale(self.image, (Settings.window_width, Settings.window_height)).convert()
        self.rect = self.image.get_rect()
        
    def draw(self, screen):
        screen.blit(self.image, self.rect) 


class Einzelkämpfer(pygame.sprite.Sprite):
    def __init__(self, filename):
        super().__init__()
        bitmap = pygame.image.load(os.path.join(Settings.image_path, filename))
        self.image = bitmap.convert_alpha()
        self.image = pygame.transform.scale(self.image, (90, 90)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = (Settings.window_width - 75) // 2
        self.rect.bottom = Settings.window_height - Settings.window_border + 15
        self.direction = 0
        self.speed = 8
        
    def update(self):
        newrect = self.rect.move(self.direction * self.speed, 0)
        if newrect.left <= Settings.window_border:
            self.move_stop()
        if newrect.right >= Settings.window_width - Settings.window_border:
            self.move_stop()
        self.rect.move_ip(self.direction * self.speed, 0)
        
    def move_left(self):
        self.direction = -1
        
    def move_right(self):
        self.direction = 1

    def move_stop(self):
        self.direction = 0

class Stein(pygame.sprite.Sprite):
    def __init__(self, filename, colindex, rowindex):
        super().__init__()
        bitmap = pygame.image.load(os.path.join(Settings.image_path, filename))
        self.image = bitmap.convert_alpha()
        self.image = pygame.transform.scale(self.image, (75, 75)).convert_alpha()
        self.rect = self.image.get_rect()
        self.distance = 28
        newx = Settings.window_border + (self.rect.width + self.distance) * colindex
        newy = Settings.window_border - 15 + (self.rect.height + self.distance) * rowindex
        self.rect.move_ip(newx, newy)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption(Settings.title)
    screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    
    background = Background("wolken.bmp")
    ek = Einzelkämpfer("auto.bmp")
    all_sprites.add(ek)
    enemies = []
    
    for rowindex in range(0, 1):
        for colindex in range(0, Settings.amout_enemy):
            all_sprites.add(Stein("stein.bmp", colindex, rowindex))
    
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    ek.move_left()
                elif event.key == pygame.K_RIGHT:
                    ek.move_right()
                elif event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    ek.move_stop()
                
                    
        ek.update()
        background.draw(screen)
        all_sprites.draw(screen)
        pygame.display.flip()
        
    pygame.quit()
        