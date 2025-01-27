import pandas as pd
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, Dataset

#device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
DEVICE = "cpu"
BATCH_SIZE = 32
IN_DIM = 178
NUM_CLASSES = 3

df= pd.read_csv('C:/Users/Hubert/Desktop/Projekty/neurohackaton/neurohackathon/data/Epileptic_Seizure_Recognition.csv')

# Extract features (all columns except the last one or the 'y' column)
X = df.iloc[:, 1:-1].to_numpy()

# Extract labels (the 'y' column)
y = df['y'].to_numpy()


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

class EpilepticSeizureDataset(Dataset):
    def __init__(self, features, labels):
        self.features = torch.tensor(features, dtype=torch.float32).to(DEVICE)  # Convert to torch tensor
        self.labels = torch.tensor(labels-1, dtype=torch.long).to(DEVICE)         # Convert labels to torch tensor

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return self.features[idx], self.labels[idx]

train_dataset = EpilepticSeizureDataset(X_train, y_train)


dataloader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)

class mlp_model(nn.Module):
    def __init__(self, in_dim, num_class):
        super(mlp_model, self).__init__()
        
        self.fc1 = nn.Linear(in_dim, 128)
        self.bn1 = nn.BatchNorm1d(128)
        self.fc2 = nn.Linear(128, 160)
        self.bn2 = nn.BatchNorm1d(160)
        self.fc3 = nn.Linear(160, 80)
        self.bn3 = nn.BatchNorm1d(80)
        self.fc4 = nn.Linear(80, num_class)


    def forward(self, x):
        # Define the forward pass
        x = torch.relu(self.bn1(self.fc1(x)))
        x = torch.relu(self.bn2(self.fc2(x)))
        x = torch.relu(self.bn3(self.fc3(x)))
        x = self.fc4(x)
        return x
    
    
    



def evaluate_model(model, X_test_tensor, y_test_tensor, batch_size=32):
    # Set the model to evaluation mode
    model.eval()

    # Initialize variables to track performance
    correct_preds = 0
    total_preds = 0

    # Disable gradient calculation for inference (saves memory and computations)
    with torch.no_grad():
        class TestDataset(Dataset):
            def __init__(self, features, labels):
                self.labels = labels
                self.labels[labels == 1] = 0
                self.labels[labels == 2] = 1
                self.labels[labels == 3] = 1
                self.labels[labels == 4] = 2
                self.labels[labels == 5] = 2
                self.features = torch.tensor(features, dtype=torch.float32).to(DEVICE)  # Convert to torch tensor
                self.labels = torch.tensor(labels, dtype=torch.long).to(DEVICE)         # Convert labels to torch tensor

            def __len__(self):
                return len(self.labels)

            def __getitem__(self, idx):
                return self.features[idx], self.labels[idx]
        
        test_dataset = TestDataset(X_test_tensor, y_test_tensor)
        test_dataloader = torch.utils.data.DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

        # Iterate through the test dataset
        for inputs, targets in test_dataloader:
            outputs = model(inputs)
            _, predicted = torch.max(outputs, -1)

            correct_preds += (predicted == targets).sum().item()
            total_preds += targets.size(0)

    accuracy = correct_preds / total_preds
    return accuracy

model = mlp_model(IN_DIM, NUM_CLASSES).to(DEVICE)
model.load_state_dict(torch.load('saved_model.pth'))


# Evaluate the model on the test dataset
test_accuracy = evaluate_model(model, X_test, y_test)

# Print the test accuracy
print(f"Test Accuracy: {test_accuracy:.4f}")