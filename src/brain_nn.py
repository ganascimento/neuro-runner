import torch
import torch.nn as nn


class BrainNN(nn.Module):
    def __init__(self, input_size=4, hidden_size=6, output_size=1):
        r"""The expected input data is:

        Args:
            - Distance to next obstacle
            - Speed
            - Obstacle width
            - Obstacle Y position"""

        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.sigmoid(self.fc2(x))
        return x
