import pygame
from pygame.sprite import Sprite
import random

class Alien(Sprite):

    def __init__(self,ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        screen_width = self.screen.get_rect().width
        screen_height = self.screen.get_rect().height
        self.rect.x = random.randint(0, max(10, screen_width - self.rect.width - 10))
        self.rect.y = random.randint(
            self.settings.alien_spawn_area_top,
            min(self.settings.alien_spawn_area_bottom, screen_height - self.rect.height - 50)
        )
        self.direction = random.choice([-1,1])
        self.speed = random.uniform(
            self.settings.alien_min_speed,
            self.settings.alien_max_speed
        )
        self.direction = random.choice([-1, 1])
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        self.rect.x += self.settings.alien_speed*self.settings.fleet_direction
        self.rect.x = int(self.x)
        if random.random() < 0.005:
            self.direction *= -1

        if random.random() < 0.01:
            self.y += random.uniform(-2,2)
            self.rect.y = int(self.y)

        if self.rect.top < 0:
            self.rect.top = 0
            self.y = float(self.rect.y)

        if self.check_edges():
            self.direction *= -1

class RandomAlien(Alien):
    def __init__(self,ai_game):
        super().__init__(ai_game)
        self.behaviour = random.choice(['normal','zigzag','dive'])
        self.vertical_speed = 0

    def update(self):
        if self.behaviour == 'normal':
            super().update()

        elif self.behaviour == 'zigzag':
            self.x += self.speed * self.direction
            self.y += random.uniform(-1, 1) * 2
            self.rect.x = int(self.x)
            self.rect.y = int(self.y)

        elif self.behaviour == 'dive':
            self.x += self.speed * self.direction * 0.5
            self.y += self.speed * 2  # 向下移动更快
            self.rect.x = int(self.x)
            self.rect.y = int(self.y)

        if self.check_edges():
            self.direction *= -1









