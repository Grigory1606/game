import os
import random
import sys

import pygame

size = width, height = 600, 800
pygame.init()
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
shots = pygame.sprite.Group()
asteroids = pygame.sprite.Group()


def load_image(name, colorkey=-1):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Ship(pygame.sprite.Sprite):
    image = load_image("spaceship.png")

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Ship.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = pos

    def update(self):
        if pygame.sprite.spritecollideany(self, asteroids):
            self.kill()


class Shot(pygame.sprite.Sprite):
    image = pygame.transform.scale2x(load_image("shot.png"))

    def __init__(self, pos, speed=0):
        super().__init__(all_sprites)
        self.add(shots)
        self.image = Shot.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = pos
        self.speed = speed

    def update(self):
        self.rect = self.rect.move(0, -self.speed)


class Asteroid(pygame.sprite.Sprite):
    image = pygame.transform.scale2x(load_image("asteroid.png"))

    def __init__(self, pos, speed=0):
        super().__init__(all_sprites)
        self.add(asteroids)
        self.image = Asteroid.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = pos
        self.speed = speed

    def update(self):
        if pygame.sprite.spritecollideany(self, shots):
            self.kill()
        else:
            self.rect = self.rect.move(0, self.speed)


def main():
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(pygame.Color('#0f0f2f'))
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(100)
    pygame.quit()


if __name__ == '__main__':
    main()
