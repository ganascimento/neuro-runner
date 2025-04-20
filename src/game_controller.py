import random
from typing import List
from obstacle import Obstacle
import config
import math


class GameController:
    def __init__(self):
        self.obstacles: List[Obstacle]
        self.distance_traveled = 0
        self.last_distance = 0
        self.build()

    def reset(self):
        self.distance_traveled = 0
        self.last_distance = 0
        self.build()

    def build(self):
        self.obstacles = []
        rand_value = random.randint(1, 3)
        amount_obstacles = 1 if rand_value < 3 else 2
        game_run_state = self.__get_game_run_state()

        for i in range(amount_obstacles):
            add_distance = i * (config.SCREEN_WIDTH / 2)
            self.obstacles.append(Obstacle(add_distance, game_run_state))

    def next(self):
        finded_obstacles = list(filter(lambda obstacle: obstacle.x > -obstacle.width, self.obstacles))

        if not finded_obstacles:
            self.build()

        return self.obstacles

    def has_avaible(self):
        return any(obstacle.x > -20 for obstacle in self.obstacles)

    def update(self, speed: int):
        self.distance_traveled += speed

        for obstacle in self.obstacles:
            obstacle.x -= speed

    def clear(self):
        self.obstacles = []

    def get_speed(self, speed: int):
        if speed == 10:
            return speed

        add_speed = math.floor((self.distance_traveled - self.last_distance) / config.DISTANCE_CHANGE_SPEED)
        if add_speed > 0:
            self.last_distance += config.DISTANCE_CHANGE_SPEED

        return speed + add_speed

    def __get_game_run_state(self):
        if self.distance_traveled == 0:
            return 0

        return math.floor(self.distance_traveled / (config.DISTANCE_CHANGE_SPEED + config.INCREMENT_TO_CHANGE_GAME_SPEED))
