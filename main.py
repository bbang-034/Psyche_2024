import pygame
import sys
from tkinter import *
from tkinter import ttk
import random

# Pygame 초기화
pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 화면 크기 설정
screen_width = 790
screen_height = 574

# 게임 제목 설정
pygame.display.set_caption('Pokemon Battle')
background = pygame.image.load('battle_image.png')
background = pygame.transform.scale(background, (screen_width, screen_height))
screen = pygame.display.set_mode((screen_width, screen_height))


class Pokemon:
    def __init__(self, name, type, skills, hp, speed):
        self.name = name
        self.hp = hp
        self.max_hp = hp  # 최대 HP를 저장
        self.type = type
        self.skills = skills
        self.speed = speed
        self.is_hidden = False  # For '껍질에 숨기'
        self.is_sleeping = False  # For '잠자기'
        self.is_yawned = False  # For '하품'

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def attack_target(self, target, move):
        damage = move['power'] + self.attack - target.defense
        if damage < 0:
            damage = 0
        target.take_damage(damage)
        return damage

    def get_skill_power(self, skill_name, opponent_speed):
        for skill in self.skills:
            if skill['name'] == skill_name:
                if skill_name == '일렉트릭볼':
                    power = (self.speed - opponent_speed)
                    return max(0, power)  # Ensure power is not negative
                else:
                    return skill['power']
        return None

    def apply_special_conditions(self, skill_name):
        if skill_name == '껍질에 숨기':
            self.is_hidden = True
        elif skill_name == '잠자기':
            self.is_sleeping = True
        elif skill_name == '하품':
            self.is_yawned = True

    def reset_special_conditions(self):
        self.is_hidden = False
        self.is_sleeping = False
        self.is_yawned = False

    def should_attack_hit(self, skill):
        # Check '껍질에 숨기' condition
        if self.is_hidden and skill['accuracy'] <= 0.6:
            return False
        # Check '잠자기' condition
        if self.is_sleeping and skill['power'] <= 12:
            return False
        # Check '하품' condition
        if self.is_yawned and random.random() >= 0.5:
            return False
        return True



# 포켓몬 예제 생성
pikachu = Pokemon('Pikachu', 100, 55, 40, [{'name': 'Thunderbolt', 'power': 9}, {'name': 'Quick Attack', 'power': 4}])
charmander = Pokemon('Charmander', 100, 52, 43, [{'name': 'Flamethrower', 'power': 9}, {'name': 'Scratch', 'power': 4}])
my_pokemon_image = pygame.image.load('pika.png')
your_pokemon_image = pygame.image.load('mobugi.png')

# 포켓몬 이미지 크기 조정
my_pokemon_image = pygame.transform.scale(my_pokemon_image, (240, 200))
your_pokemon_image = pygame.transform.scale(your_pokemon_image, (140, 155))
my_pokemon_image = pygame.transform.flip(my_pokemon_image, True, False)

font = pygame.font.Font(None, 36)


def draw_text(text, x, y, color=BLACK):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def draw_health_bar(pokemon, x, y, width=200, height=20):
    ratio = pokemon.hp / pokemon.max_hp
    pygame.draw.rect(screen, RED, (x, y, width, height))
    pygame.draw.rect(screen, GREEN, (x, y, width * ratio, height))
    draw_text(f"{pokemon.hp}/{pokemon.max_hp}", x + width - 90, y-2)


def draw_skill_bar(pokemon, x, y):
    for index, move in enumerate(pokemon.moves):
        draw_text(move['name'], x, y + index * 40, BLUE)



def draw_rounded_rect(surface, color, rect, radius):
    pygame.draw.rect(surface, color, (rect[0] + radius, rect[1], rect[2] - 2 * radius, rect[3]))
    pygame.draw.rect(surface, color, (rect[0], rect[1] + radius, rect[2], rect[3] - 2 * radius))
    pygame.draw.circle(surface, color, (rect[0] + radius, rect[1] + radius), radius)
    pygame.draw.circle(surface, color, (rect[0] + rect[2] - radius, rect[1] + radius), radius)
    pygame.draw.circle(surface, color, (rect[0] + radius, rect[1] + rect[3] - radius), radius)
    pygame.draw.circle(surface, color, (rect[0] + rect[2] - radius, rect[1] + rect[3] - radius), radius)


def draw_info_bars():
    # 하단 배경 바 그리기
    draw_rounded_rect(screen, WHITE, (0, 500, screen_width, 74), 20)

    # 플레이어 포켓몬 상태 바 그리기
    draw_health_bar(pikachu, 50, 520)

    # 플레이어 포켓몬 스킬 바 그리기
    draw_skill_bar(pikachu, 50, 540)


def draw_opponent_info():
    # 상대 포켓몬 배경 바 그리기
    draw_rounded_rect(screen, WHITE, (490, 120, 240, 50), 20)

    # 상대 포켓몬 상태 바 그리기
    draw_health_bar(charmander, 510, 135)


def game_loop():
    running = True
    while running:
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 포켓몬 이미지 그리기
        screen.blit(my_pokemon_image, (50, 350))  # Pikachu 이미지 위치
        screen.blit(your_pokemon_image, (520, 180))  # Charmander 이미지 위치

        # 정보 바 그리기
        draw_info_bars()
        draw_opponent_info()

        pygame.display.flip()

    pygame.quit()
    sys.exit()


game_loop()
