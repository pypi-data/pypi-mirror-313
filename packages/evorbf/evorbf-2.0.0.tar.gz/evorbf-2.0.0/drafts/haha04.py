#!/usr/bin/env python
# Created by "Thieu" at 13:45, 21/09/2023 ----------%                                                                               
#       Email: nguyenthieu2102@gmail.com            %                                                    
#       Github: https://github.com/thieu1995        %                         
# --------------------------------------------------%

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# Create a custom RBF layer
class RBFLayer(nn.Module):
    def __init__(self, num_centers, sigma=1.0):
        super(RBFLayer, self).__init__()
        self.num_centers = num_centers
        self.sigma = sigma
        self.centers = nn.Parameter(torch.randn(num_centers, 4))  # Adjust the dimension of centers to 4 features

    def forward(self, x):
        x = x.unsqueeze(1)
        return torch.exp(-torch.norm(x - self.centers, dim=2) ** 2 / (2 * self.sigma ** 2))


# Create the RBFN model
class RBFN(nn.Module):
    def __init__(self, num_centers, sigma=1.0):
        super(RBFN, self).__init__()
        self.rbf_layer = RBFLayer(num_centers, sigma)
        self.linear = nn.Linear(num_centers, 1, bias=False)  # Turn off bias

    def forward(self, x):
        x = self.rbf_layer(x)
        x = self.linear(x)
        return x


# Generate synthetic regression data with 4 features
X, y = make_regression(n_samples=100, n_features=4, noise=0.1, random_state=0)
X = StandardScaler().fit_transform(X)
y = StandardScaler().fit_transform(y.reshape(-1, 1)).flatten()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Convert data to PyTorch tensors
X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.float32)
X_test_tensor = torch.tensor(X_test, dtype=torch.float32)

# Initialize and train the RBFN model
num_centers = 10
sigma = 1.0

model = RBFN(num_centers, sigma)
optimizer = optim.Adam(model.parameters(), lr=0.01)
criterion = nn.MSELoss()

# Using named_modules() to get all layers with names
# for name, layer in model.named_modules():
#     print(layer.weights)


# Print out all weights and their names
for name, param in model.named_parameters():
    if param.requires_grad:
        print(name, param.shape)


num_epochs = 1000
for epoch in range(num_epochs):
    optimizer.zero_grad()
    outputs = model(X_train_tensor)
    loss = criterion(outputs, y_train_tensor.unsqueeze(1))
    loss.backward()
    optimizer.step()

# Evaluate the model
with torch.no_grad():
    y_pred_tensor = model(X_test_tensor)
    y_pred = y_pred_tensor.numpy().flatten()

# Plot the results
import matplotlib.pyplot as plt

plt.scatter(X_test[:, 0], y_test, label='True')
plt.scatter(X_test[:, 0], y_pred, label='Predicted')
plt.legend()
plt.xlabel('Feature 1')
plt.ylabel('y')
plt.show()
