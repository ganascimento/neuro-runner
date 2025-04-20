from typing import List
import torch
import config
import random
from brain_nn import BrainNN
from obstacle import Obstacle


class Player:
    def __init__(self):
        self.player_y = config.GAME_RUN_Y
        self.vel_y = 0
        self.gravity = 1
        self.jump_force = -15
        self.score = 0
        self.is_alive = True
        self.color = (random.randint(0, 150), random.randint(0, 255), random.randint(0, 255))
        self.variation_x = random.randint(-25, 25)

    def update(self, jump, obstacles: List[Obstacle]):
        obstacle = self.__get_next_available_obstacle(obstacles)
        if jump and self.player_y >= config.GAME_RUN_Y:
            self.vel_y = self.jump_force

        self.vel_y += self.gravity
        self.player_y += self.vel_y

        if self.player_y >= config.GAME_RUN_Y:
            self.player_y = config.GAME_RUN_Y
            self.vel_y = 0

        self.score += 1

        if self.collided(obstacle):
            self.is_alive = False

    def collided(self, obstacle: Obstacle):
        player_position_start_x = self.get_position()
        player_position_end_x = player_position_start_x + config.AGENT_SIZE
        player_position_start_y = self.player_y - config.AGENT_SIZE
        player_position_end_y = self.player_y

        obstacle_position = obstacle.y - obstacle.height

        overlap_x = player_position_start_x < obstacle.x + obstacle.width and player_position_end_x > obstacle.x
        overlap_y = (
            player_position_start_y < obstacle_position and player_position_end_y > obstacle_position - config.OBSTACLE_SIZE
        )

        return overlap_x and overlap_y

    def get_state(self, obstacles: List[Obstacle], speed: int):
        obstacle = self.__get_next_available_obstacle(obstacles)
        distance = obstacle.x - self.get_position()
        tensor = torch.tensor([distance, speed * 3, obstacle.width, obstacle.height])

        return self.__min_max_scaling(tensor)

    def in_jump(self):
        return self.player_y < config.GAME_RUN_Y

    def get_position(self):
        return config.START_WIDTH + self.variation_x

    def __get_next_available_obstacle(self, obstacles: List[Obstacle]):
        return next(filter(lambda o: o.x + o.width >= self.get_position(), obstacles), obstacles[-1])

    def __min_max_scaling(self, data: torch.Tensor):
        min_val = torch.min(data)
        max_val = torch.max(data)
        return (data - min_val) / (max_val - min_val + 1e-8)


class PlayerAgent:
    def __init__(self):
        self.model = BrainNN()
        self.fitness = 0

    def decide(self, state):
        with torch.no_grad():
            x = torch.tensor(state, dtype=torch.float32)
            output = self.model(x)
            return output.item() > 0.5

    def mutate(self, rate=0.01):
        for param in self.model.parameters():
            if param.requires_grad:
                param.data += torch.randn_like(param) * rate

    def clone(self):
        clone = PlayerAgent()
        clone.model.load_state_dict(self.model.state_dict())
        return clone
