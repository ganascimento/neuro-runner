import random
import torch
import config
import os
from player import PlayerAgent


class Population:
    def __init__(self):
        self.agents = [PlayerAgent() for _ in range(config.POPULATION_SIZE)]
        self.number_best_agents = int(max(1, config.POPULATION_SIZE * 0.1))
        self.mutation_rate = 0.1

    def evolve(self, generation):
        self.agents.sort(key=lambda agent: agent.fitness, reverse=True)
        survivors = self.agents[: self.number_best_agents]
        self.mutation_rate = max(0.01, 0.1 - (generation * 0.001))

        new_agents = survivors[: self.number_best_agents]
        for _ in range(config.POPULATION_SIZE - self.number_best_agents):
            parent = random.choice(survivors)
            child = parent.clone()
            child.mutate(rate=self.mutation_rate)
            new_agents.append(child)

        self.agents = new_agents

    def save_model(self):
        self.agents.sort(key=lambda agent: agent.fitness, reverse=True)
        agent_to_save = []

        for agent in self.agents[: self.number_best_agents]:
            agent_to_save.append({"model": agent.model.state_dict(), "fitness": agent.fitness})

        data_to_save = {"data": agent_to_save, "mutation_rate": self.mutation_rate}

        torch.save(data_to_save, config.DATA_MODEL_PATH)
        print("Model saved!")

    def load_model(self):
        if not os.path.exists(config.DATA_MODEL_PATH):
            return False

        load_data = torch.load(config.DATA_MODEL_PATH)

        self.mutation_rate = load_data["mutation_rate"]
        base_agents = []
        for data in load_data["data"][: self.number_best_agents]:
            agent = PlayerAgent()
            agent.model.load_state_dict(data["model"])
            agent.fitness = data["fitness"]
            base_agents.append(agent)

        self.agents = base_agents
        print("Model loaded!")

        return True
