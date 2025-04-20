from typing import List
import pygame
import config
from environment import Environment
from game_controller import GameController
from obstacle import Obstacle
from player import Player, PlayerAgent
from population import Population


class Game:
    def __init__(self):
        self.speed = config.DEFAULT_SPEED
        self.running = False
        self.generations = 0
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)

        self.population = Population()
        self.game_controller = GameController()
        self.environment = Environment(self.screen)

    def play(self):
        while self.generations < config.MAX_GENERATIONS:
            self.__reset()
            self.view()

            self.generations += 1
            self.population.evolve(self.generations)

        print(f"Treinamento concluído após {self.generations} gerações.")
        pygame.quit()

    def view(self):
        players = [Player() for _ in range(config.POPULATION_SIZE)]
        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                self.__handle_event(event)

            self.environment.build()
            next_obstacles = self.__update()
            self.__show_text(players)

            for _, (agent, player) in enumerate(zip(self.population.agents, players)):
                if player.is_alive:
                    self.__player_action(player, agent, next_obstacles)
                    self.environment.draw_player(player)
                    agent.fitness = player.score

            pygame.display.flip()  # Update screen
            self.clock.tick(60)

            has_alive = any(player.is_alive for player in players)
            if not has_alive:
                self.running = False

    def __update(self):
        self.environment.draw_obstacle(self.game_controller.obstacles)
        self.game_controller.update(self.speed)
        self.speed = self.game_controller.get_speed(self.speed)
        return self.game_controller.next()

    def __reset(self):
        self.game_controller.reset()
        self.speed = config.DEFAULT_SPEED

    def __player_action(self, player: Player, agent: PlayerAgent, next_obstacles: List[Obstacle]):
        jump = False
        if not player.in_jump():
            state = player.get_state(next_obstacles, self.speed)
            jump = agent.decide(state)
        player.update(jump, next_obstacles)

    def __show_text(self, players):
        text = self.font.render(
            f"GEN: {self.generations} - Agents: {len(list(filter(lambda p: p.is_alive, players)))} - Speed: {self.speed} - Distance: {self.game_controller.distance_traveled}",
            True,
            (0, 0, 0),
        )
        self.screen.blit(text, (10, 10))

    def __handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.environment.rect_save_button.collidepoint(event.pos):
                self.population.save_model()

            if self.environment.rect_load_button.collidepoint(event.pos):
                if self.population.load_model():
                    self.running = False
