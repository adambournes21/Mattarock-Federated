# client.py
import torch
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F
import flwr as fl
import random  # For poisoning
from common import SimpleCNN, load_datasets, partition_dataset
from torch.utils.data import DataLoader

# Flower client class that uses the NumPyClient interface
class MnistClient(fl.client.NumPyClient):
    def __init__(self, model, train_loader, test_loader, local_epochs=1):
        self.model = model
        self.train_loader = train_loader
        self.test_loader = test_loader
        self.local_epochs = local_epochs
        self.criterion = nn.CrossEntropyLoss()

    def get_parameters(self, config=None):
        # Return model parameters as a list of NumPy arrays.
        return [val.cpu().numpy() for _, val in self.model.state_dict().items()]

    def set_parameters(self, parameters):
        # Set model parameters from a list of NumPy arrays.
        state_dict = self.model.state_dict()
        for key, param in zip(state_dict.keys(), parameters):
            state_dict[key] = torch.tensor(param)
        self.model.load_state_dict(state_dict)

    def fit(self, parameters, config):
        self.set_parameters(parameters)
        self.model.train()
        optimizer = optim.Adam(self.model.parameters(), lr=0.01)
        # Local training loop
        for _ in range(self.local_epochs):
            for data, target in self.train_loader:
                optimizer.zero_grad()
                output = self.model(data)
                loss = self.criterion(output, target)
                loss.backward()
                optimizer.step()
        return self.get_parameters(), len(self.train_loader.dataset), {}

    def evaluate(self, parameters, config):
        self.set_parameters(parameters)
        self.model.eval()
        loss_total = 0
        correct = 0
        total = 0
        with torch.no_grad():
            for data, target in self.test_loader:
                output = self.model(data)
                loss = self.criterion(output, target)
                loss_total += loss.item() * data.size(0)
                _, predicted = torch.max(output, 1)
                total += target.size(0)
                correct += (predicted == target).sum().item()
        loss_avg = loss_total / total
        accuracy = correct / total
        # Print the evaluation metrics
        print(f"Test Loss: {loss_avg:.4f} | Test Accuracy: {accuracy * 100:.2f}%")
        return loss_avg, len(self.test_loader.dataset), {"accuracy": accuracy}

if __name__ == "__main__":
    import sys
    # Expect client_id as command-line argument (0,1,...,4 for 5 clients)
    if len(sys.argv) != 2:
        print("Usage: python client.py <client_id>")
        exit(1)
    client_id = int(sys.argv[1])
    
    # Load datasets
    train_dataset, test_dataset = load_datasets()
    
    # Poison 10% of the training labels
    poison_fraction = 0.25
    num_poisoned = int(poison_fraction * len(train_dataset))
    all_indices = list(range(len(train_dataset)))
    poisoned_indices = random.sample(all_indices, num_poisoned)
    for idx in poisoned_indices:
        # Overwrite the label with a random digit between 0 and 9
        train_dataset.targets[idx] = random.randint(0, 9)
    
    # Partition the train dataset for this client
    num_clients = 5
    train_subset = partition_dataset(train_dataset, num_clients, client_id)

    train_loader = DataLoader(train_subset, batch_size=64, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=64)
    
    # Create model and Flower client instance
    model = SimpleCNN()
    client = MnistClient(model, train_loader, test_loader, local_epochs=1)
    
    # Start Flower client (assuming the server is running at localhost:8080)
    fl.client.start_numpy_client(server_address="127.0.0.1:8080", client=client)
