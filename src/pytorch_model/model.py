import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
import csv

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#DEVICE = "cpu"
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
    
    


model = mlp_model(in_dim=IN_DIM, num_class=NUM_CLASSES)

try:
    model.load_state_dict(torch.load('saved_model.pth'))
except:
    pass


model = model.to(DEVICE)
loss_fn = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

epochs = 200
print("training started on",DEVICE)
model.train()
for epoch in range(epochs):
    for batch_idx, (inputs, targets) in enumerate(dataloader):
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = loss_fn(outputs.reshape(-1, NUM_CLASSES), targets.reshape(-1))
        loss.backward()
        optimizer.step()
        if batch_idx % 200 == 0:
            print("Loss: ",loss.item())
    if epoch % 50 == 0:
        print("Epoch: ",epoch)
        torch.save(model.state_dict(), 'saved_model.pth')

