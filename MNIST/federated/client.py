# client.py
import torch
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F
import flwr as fl
import random  # For poisoning
from common import SimpleCNN, load_datasets, partition_dataset
from torch.utils.data import DataLoader
from sklearn.metrics import precision_score, recall_score, f1_score

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
        optimizer = optim.SGD(self.model.parameters(), lr=0.03)
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
        loss_total, correct, total = 0.0, 0, 0
        preds_all, labels_all = [], []

        with torch.no_grad():
            for data, target in self.test_loader:
                output = self.model(data)
                loss_total += self.criterion(output, target).item() * data.size(0)

                preds = output.argmax(dim=1)
                preds_all.extend(preds.cpu().numpy())
                labels_all.extend(target.cpu().numpy())

                total   += target.size(0)
                correct += (preds == target).sum().item()

        # ------------- metrics -------------
        loss     = loss_total / total
        accuracy = correct / total
        precision = precision_score(labels_all, preds_all, average="macro", zero_division=0)
        recall    = recall_score   (labels_all, preds_all, average="macro", zero_division=0)
        f1        = f1_score       (labels_all, preds_all, average="macro", zero_division=0)

        # everything goes back in the "metrics" dict
        return loss, total, {
            "accuracy":  accuracy,
            "precision": precision,
            "recall":    recall,
            "f1":        f1,
        }

if __name__ == "__main__":
    import sys
    # Expect client_id as command-line argument (0,1,...,4 for 5 clients)
    if len(sys.argv) != 2:
        print("Usage: python client.py <client_id>")
        exit(1)
    client_id = int(sys.argv[1])
    
    # Load datasets
    train_dataset, test_dataset = load_datasets()
    
    # Partition the train dataset for this client
    num_clients = 5
    train_subset = partition_dataset(train_dataset, num_clients, client_id)

    # Poison x% of the training labels
    poison_fraction = 0
    # replace labels in-place
    # Poison exactly poison_fraction of THIS client’s local examples
    subset_indices = train_subset.indices
    k = int(poison_fraction * len(subset_indices))
    for idx in random.sample(subset_indices, k):
        train_dataset.targets[idx] = random.randint(0, 9)
    
    train_loader = DataLoader(train_subset, batch_size=64, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=64)
    
    # Create model and Flower client instance
    model = SimpleCNN()
    client = MnistClient(model, train_loader, test_loader, local_epochs=1)
    
    # Start Flower client (assuming the server is running at localhost:8080)
    fl.client.start_numpy_client(server_address="127.0.0.1:8080", client=client)
