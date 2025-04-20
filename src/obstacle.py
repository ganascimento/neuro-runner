import config
import random


class Obstacle:
    def __init__(self, add_distance=0, game_run_state=0):
        if game_run_state > 3:
            game_run_state = 3

        self.x = config.SCREEN_WIDTH + add_distance
        self.y = config.GAME_RUN_Y + config.OBSTACLE_SIZE
        self.width = config.OBSTACLE_SIZE * (random.randint(1, game_run_state + 2))
        self.image_type = 1 if random.randint(1, 4) <= 3 else 2
        height_type = random.randint(0, 10)

        if height_type < 6:
            self.height = config.OBSTACLE_SIZE
        elif height_type <= 8:
            self.height = config.OBSTACLE_SIZE * 3
        else:
            self.height = config.OBSTACLE_SIZE * 5
