import sys
import torch
import torch.optim as optim
import torch.nn as nn
import flwr as fl
from torch.utils.data import DataLoader
from torchvision import transforms
import random
from common import ImageWoofDataset, partition_dataset, CustomResNet18
from sklearn.metrics import precision_score, recall_score, f1_score

class ImageWoofClient(fl.client.NumPyClient):
    def __init__(self, model, train_loader, val_loader, device, local_epochs=1):
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.device = device
        self.local_epochs = local_epochs
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.SGD(self.model.parameters(), lr=0.003)
        
    def get_parameters(self, config=None):
        return [val.cpu().numpy() for val in self.model.state_dict().values()]
    
    def set_parameters(self, parameters):
        state_dict = self.model.state_dict()
        for key, param in zip(state_dict.keys(), parameters):
            state_dict[key] = torch.tensor(param)
        self.model.load_state_dict(state_dict)
    
    def fit(self, parameters, config):
        self.set_parameters(parameters)
        self.model.train()
        for _ in range(self.local_epochs):
            for images, labels in self.train_loader:
                images, labels = images.to(self.device), labels.to(self.device)
                self.optimizer.zero_grad()
                outputs = self.model(images)
                loss = self.criterion(outputs, labels)
                loss.backward()
                self.optimizer.step()
        return self.get_parameters(), len(self.train_loader.dataset), {"train_loss": loss.item()}
    
    def evaluate(self, parameters, config):
        self.set_parameters(parameters)
        self.model.eval()
        total_loss, correct, total = 0.0, 0, 0
        all_labels = []
        all_preds = []

        with torch.no_grad():
            for images, labels in self.val_loader:
                images, labels = images.to(self.device), labels.to(self.device)
                outputs = self.model(images)
                loss = self.criterion(outputs, labels)
                total_loss += loss.item() * images.size(0)
                preds = outputs.argmax(dim=1)
                correct += (preds == labels).sum().item()
                total += labels.size(0)

                all_labels.extend(labels.cpu().numpy())
                all_preds.extend(preds.cpu().numpy())

        avg_loss = total_loss / total if total > 0 else 0.0
        accuracy = correct / total if total > 0 else 0.0
        precision = precision_score(all_labels, all_preds, average="macro")
        recall = recall_score(all_labels, all_preds, average="macro")
        f1 = f1_score(all_labels, all_preds, average="macro")

        print(
            f"Test Loss: {avg_loss:.4f} | "
            f"Test Accuracy: {accuracy*100:.2f}% | "
            f"Test Precision: {precision:.4f} | "
            f"Test Recall: {recall:.4f} | "
            f"Test F1: {f1:.4f}"
        )
        return avg_loss, total, {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1,
        }

def main():
    if len(sys.argv) != 2:
        print("Usage: python client.py <client_id>")
        sys.exit(1)
    client_id = int(sys.argv[1])
    num_clients = 5

    # Define image transforms.
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
    ])
    
    # Paths to your ImageWoof dataset.
    csv_file = "../imagewoof2-160/noisy_imagewoof.csv"
    root_dir = "../imagewoof2-160"
    
    # Create training and validation datasets.
    train_dataset = ImageWoofDataset(
        csv_file=csv_file,
        root_dir=root_dir,
        label_column="noisy_labels_0",
        transform=transform,
        split="train",
        poisoned_data_pct=0.0
    )
    val_dataset = ImageWoofDataset(
        csv_file=csv_file,
        root_dir=root_dir,
        label_column="noisy_labels_0",
        transform=transform,
        split="val",
        poisoned_data_pct=0.0
    )
    
    print("Number of training images:", len(train_dataset))
    print("Number of validation images:", len(val_dataset))
    
    # Partition the training dataset for this client.
    train_subset = partition_dataset(train_dataset, num_clients, client_id)
    
    # Create DataLoaders.
    train_loader = DataLoader(train_subset, batch_size=32, shuffle=True, num_workers=4)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False, num_workers=4)
    
    # Device selection.
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Create a model instance using the number of classes from the train dataset.
    model = CustomResNet18(num_classes=train_dataset.num_classes).to(device)
    
    # Create the Flower client.
    client = ImageWoofClient(model, train_loader, val_loader, device, local_epochs=1)
    
    # Start the Flower client (assuming the server is running at localhost:8080).
    fl.client.start_numpy_client(server_address="127.0.0.1:8080", client=client)

if __name__ == "__main__":
    main()
