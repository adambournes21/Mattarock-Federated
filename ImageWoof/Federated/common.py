import os
import pandas as pd
import random
from PIL import Image
from torch.utils.data import Dataset, Subset
import torch.nn as nn
import torchvision.models as models


class ImageWoofDataset(Dataset):
    def __init__(
        self,
        csv_file,
        root_dir,
        label_column='noisy_labels_0',
        transform=None,
        split='train',
        poisoned_data_pct=0.0,
        seed=42
    ):
        # Load metadata
        self.df = pd.read_csv(csv_file)

        # Split train vs val
        if split == 'train':
            self.df = self.df[self.df['is_valid'] == False].reset_index(drop=True)
        else:
            self.df = self.df[self.df['is_valid'] == True].reset_index(drop=True)

        self.root_dir = root_dir
        self.label_column = label_column
        self.transform = transform
        self.split = split
        self.poisoned_data_pct = poisoned_data_pct

        # Map synset labels to integers
        synsets = self.df[self.label_column].unique()
        self.synset_to_idx = {synset: idx for idx, synset in enumerate(synsets)}
        self.num_classes = len(self.synset_to_idx)

        # Pre-select which indices to poison (only for training)
        if self.split == 'train' and self.poisoned_data_pct > 0.0:
            total = len(self.df)
            n_poison = int(total * self.poisoned_data_pct)
            all_indices = list(range(total))
            random.seed(seed)
            random.shuffle(all_indices)
            self._poisoned_idx = set(all_indices[:n_poison])
        else:
            self._poisoned_idx = set()

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        # Load image and original label
        row = self.df.iloc[idx]
        img_path = os.path.join(self.root_dir, row['path'])
        image = Image.open(img_path).convert("RGB")
        label = self.synset_to_idx[row[self.label_column]]

        # If this index was marked as poisoned, assign a random label
        if self.split == 'train' and idx in self._poisoned_idx:
            label = random.randint(0, self.num_classes - 1)

        if self.transform:
            image = self.transform(image)

        return image, label


def partition_dataset(dataset, num_clients, client_id):
    total = len(dataset)
    indices = list(range(total))
    random.shuffle(indices)
    part_size = total // num_clients
    start = client_id * part_size
    end = start + part_size if client_id != num_clients - 1 else total
    return Subset(dataset, indices[start:end])


class CustomResNet18(nn.Module):
    def __init__(self, num_classes: int):
        super(CustomResNet18, self).__init__()
        # Load pretrained ResNet18
        self.resnet = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        num_features = self.resnet.fc.in_features
        # Replace final layer
        self.resnet.fc = nn.Linear(num_features, num_classes)

    def forward(self, x):
        return self.resnet(x)
