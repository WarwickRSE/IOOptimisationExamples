import torch.nn as nn
import torch.nn.functional as F

#Image size
_sz = 100

# A basic NN class (from tutorial)
class NeuralNetwork(nn.Module):
    def __init__(self, n_labels):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(3*_sz*_sz, 512), #3 colour channels
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, n_labels),
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

