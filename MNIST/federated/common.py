# common.py
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import datasets, transforms

# Model definition (the same as your SimpleCNN)
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.fc1 = nn.Linear(32 * 14 * 14, 10)
        
    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = self.pool(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        return x

# Data loading function
def load_datasets():
    transform = transforms.ToTensor()
    train_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
    test_dataset = datasets.MNIST(root='./data', train=False, download=True, transform=transform)
    return train_dataset, test_dataset

# Function to partition the training data into `num_clients` parts.
def partition_dataset(dataset, num_clients, client_id):
    total_size = len(dataset)


    # part_size = total_size
    # start = 0
    part_size = total_size // num_clients
    start = client_id * part_size
    # Last client takes any extra samples.
    end = start + part_size if client_id != num_clients - 1 else total_size
    indices = list(range(start, end))
    from torch.utils.data import Subset
    return Subset(dataset, indices)
