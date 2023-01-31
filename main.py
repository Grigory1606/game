import os
import random
import sys

import pygame

size = width, height = 600, 800
FPS = 100

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

    def __init__(self, pos, hp):
        super().__init__(all_sprites)
        self.image = Ship.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = pos
        self.hp = hp
        self.score = 0


class Shot(pygame.sprite.Sprite):
    image = pygame.transform.scale2x(load_image("shot.png"))

    def __init__(self, pos, speed=4):
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

    def __init__(self, pos, speed=2):
        super().__init__(all_sprites)
        self.add(asteroids)
        self.image = Asteroid.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = pos
        self.speed = speed

    def update(self):
        if self.rect.centery > height:
            ship.hp -= 1
            self.kill()
        elif pygame.sprite.spritecollideany(self, shots):
            ship.score += 50
            self.kill()
        else:
            self.rect = self.rect.move(0, self.speed)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Space shooter", "",
                  "Нажмите 1 для выбора лёгкого уровня сложности.",
                  "Нажмите 2 для выбора среднего уровня сложности.",
                  "Нажмите 3 для выбора тяжёлого уровня сложности."]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    clock = pygame.time.Clock()
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    main(2, 1, 1, 5)
                if event.key == pygame.K_2:
                    main(3, 0.7, 0.8, 3)
                if event.key == pygame.K_3:
                    main(4, 0.5, 0.6, 2)
        pygame.display.flip()
        clock.tick(FPS)


def game_over():
    intro_text = ["Вы проиграли!", "",
                  f"Ваш счёт: {ship.score}", ""
                                             "Нажмите ПРОБЕЛ чтобы начать заново."]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    clock = pygame.time.Clock()
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_screen()
        pygame.display.flip()
        clock.tick(FPS)


def main(speed, reload, freq, hp):
    clock = pygame.time.Clock()
    global ship
    ship = Ship((width // 2, height // 1.1), hp)
    font = pygame.font.Font(None, 30)
    string_rendered = font.render(f'Score: {ship.score}   HP: {ship.hp}', 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    running = True
    pygame.key.set_repeat(True)
    s = 0
    while running:
        s += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if ship.rect.left > 0:
                        ship.rect.left -= 1
                if event.key == pygame.K_RIGHT:
                    if ship.rect.right < width:
                        ship.rect.right += 1
        screen.fill(pygame.Color('#0f0f2f'))
        screen.blit(font.render(f'Score: {ship.score}   HP: {ship.hp}', 1, pygame.Color('white')), intro_rect)
        if s % (FPS * 10) == 0:
            ship.score += 100
        if s % (FPS * freq) == 0:
            Asteroid((random.randint(0, width), 0), speed)
        if s % (FPS * reload) == 0:
            Shot((ship.rect.centerx, ship.rect.top - 10))
        all_sprites.update()
        if ship.hp == 0:
            for sprite in all_sprites:
                sprite.kill()
            game_over()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    start_screen()
