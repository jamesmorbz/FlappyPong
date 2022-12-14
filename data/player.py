import pygame
from data.metadata import MetaData

class Player(pygame.sprite.DirtySprite):
    def __init__(self, metadata: MetaData):
        pygame.sprite.DirtySprite.__init__(self) # super().__init__()
        self.metadata: MetaData = metadata
        self.dead = False
        self.position = pygame.Vector2()
        self.player_width: int = 38
        self.player_height: int = 51
        self.direction: int = 1
        self.distance: int = 0
        self.coord_y: int = self.metadata.screen_height / 2
        self.coord_x: int = self.metadata.screen_width / 2
        self.gravity: int = -3
        self.jump_height: int = 10
        self.speed: int = 100
        self.right_player_sprite: pygame.image = pygame.image.load(
            "gfx\\right_bird.png"
        ).convert_alpha()
        self.left_player_sprite: pygame.image = pygame.image.load(
            "gfx\\left_bird.png"
        ).convert_alpha()
        self.image: pygame.Surface = self.refresh_sprite()
        self.rect: pygame.rect = self.image.get_rect()
        self.lives = 1
        
    def get_position(self):
        return (self.coord_x, self.coord_y)

    def scale_sprite(self, sprite):
        return pygame.transform.scale(sprite, (self.player_width, self.player_height))

    def get_sprite(self):
        if self.direction == 1:
            return self.right_player_sprite
        if self.direction == -1:
            return self.left_player_sprite

    def lose_a_life(self):
        self.lives = self.lives - 1

    def update(self, dt):
        self.coord_x = (self.direction * (self.speed * dt)) + self.coord_x
        self.coord_y = self.coord_y - ((self.gravity / 10) * 2)

        self.check_window_boundary_collisions()
        self.refresh_sprite()

    def refresh_sprite(self):
        self.image = self.scale_sprite(self.get_sprite())
        return self.image

    def check_window_boundary_collisions(self):
        if self.coord_x > self.metadata.screen_width:
            self.direction = -1

        if self.coord_x < 0:
            self.direction = 1

        if self.coord_y > self.metadata.screen_height:
            self.lose_a_life()
            self.reset_player_position()

    def reset_player_position(self):
        self.coord_y = self.metadata.screen_height / 2
        self.coord_x = self.metadata.screen_width / 2

    def revive_sprite(self):
        self.dead = False
    
    def kill_sprite(self):
        self.dead = True

    def jump(self):
        self.coord_y = self.coord_y - self.jump_height

    def change_speed(self, change):
        self.speed = self.speed + change
    
    def change_gravity(self, change):
        self.gravity = self.gravity + change
    
    def change_jump_height(self, change):
        self.jump_height = self.jump_height + change