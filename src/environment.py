import pygame
import config
from typing import List
from pygame import Surface
from obstacle import Obstacle
from player import Player


class Environment:
    def __init__(self, screen: Surface):
        self.screen = screen
        self.start_x = config.SCREEN_WIDTH
        self.start_y = config.SCREEN_HEIGHT - config.OBSTACLE_SIZE
        self.amount_x = int(config.SCREEN_WIDTH / config.OBSTACLE_SIZE)
        self.font = pygame.font.Font(None, 18)
        self.rect_save_button = pygame.Rect(config.SCREEN_WIDTH - 250, 5, 90, 30)
        self.rect_load_button = pygame.Rect(config.SCREEN_WIDTH - 150, 5, 90, 30)

        self.__load_images()

    def build(self):
        self.screen.blit(self.background_img, (0, 0))

        for i in range(self.amount_x):
            for y in range(3):
                image = self.terrain_img if y < 2 else self.grass_img
                self.screen.blit(image, (i * config.OBSTACLE_SIZE, self.start_y - y * config.OBSTACLE_SIZE))

        self.draw_save_button()
        self.draw_load_button()

    def draw_obstacle(self, obstacles: List[Obstacle]):
        for obstacle in obstacles:
            amount_obstacles = int(obstacle.width / config.OBSTACLE_SIZE)
            image = self.grass_img if obstacle.image_type == 1 else self.grass2_img

            for i in range(amount_obstacles):
                self.screen.blit(image, (obstacle.x + i * config.OBSTACLE_SIZE, obstacle.y - obstacle.height))

    def draw_player(self, player: Player):
        pygame.draw.circle(self.screen, player.color, (player.get_position(), player.player_y), 4)
        self.screen.blit(self.player_img, (player.get_position(), player.player_y))

    def draw_save_button(self):
        pygame.draw.rect(self.screen, (220, 20, 60), self.rect_save_button, border_radius=5)
        text_surface = self.font.render("Save model", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect_save_button.center)
        self.screen.blit(text_surface, text_rect)

    def draw_load_button(self):
        pygame.draw.rect(self.screen, (65, 105, 225), self.rect_load_button, border_radius=5)
        text_surface = self.font.render("Load model", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect_load_button.center)
        self.screen.blit(text_surface, text_rect)

    def __load_images(self):
        self.terrain_img = pygame.image.load(f"{config.DEFAULT_PATH_IMG_GAME}/terrain.png")
        self.background_img = pygame.image.load(f"{config.DEFAULT_PATH_IMG_GAME}/background.png")
        self.grass_img = pygame.image.load(f"{config.DEFAULT_PATH_IMG_GAME}/grass.png")
        self.grass2_img = pygame.image.load(f"{config.DEFAULT_PATH_IMG_GAME}/grass2.png")
        self.player_img = pygame.image.load(f"{config.DEFAULT_PATH_IMG_GAME}/player.png")
