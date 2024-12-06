#!/usr/bin/env python
# Created by "Thieu" at 16:26, 21/09/2023 ----------%                                                                               
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
from sklearn.cluster import KMeans

# Create a custom RBF layer with fixed centers
class RBFLayer(nn.Module):
    def __init__(self, centers, sigma=1.0):
        super(RBFLayer, self).__init__()
        self.centers = nn.Parameter(torch.tensor(centers, dtype=torch.float32), requires_grad=False)    # Use fixed centers
        self.sigma = sigma

    def forward(self, x):
        x = x.unsqueeze(1)
        return torch.exp(-torch.norm(x - self.centers, dim=2) ** 2 / (2 * self.sigma ** 2))

# Create the RBFN model with K-means selected centers
class RBFN(nn.Module):
    def __init__(self, centers, sigma=1.0):
        super(RBFN, self).__init__()
        self.rbf_layer = RBFLayer(centers, sigma)
        self.linear = nn.Linear(len(centers), 1, bias=False)  # Turn off bias

    def forward(self, x):
        x = self.rbf_layer(x)
        x = self.linear(x)
        return x

# Generate synthetic regression data
X, y = make_regression(n_samples=100, n_features=4, noise=0.1, random_state=0)
X = StandardScaler().fit_transform(X)
y = StandardScaler().fit_transform(y.reshape(-1, 1)).flatten()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Perform K-means clustering to find centers
num_centers = 10
kmeans = KMeans(n_clusters=num_centers, random_state=0).fit(X_train)
centers = kmeans.cluster_centers_

# Convert data to PyTorch tensors
X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.float32)
X_test_tensor = torch.tensor(X_test, dtype=torch.float32)

# Initialize and train the RBFN model with fixed centers
sigma = 1.0

rbfn_model = RBFN(centers, sigma)
optimizer = optim.Adam(rbfn_model.parameters(), lr=0.01)
criterion = nn.MSELoss()

num_epochs = 1000
for epoch in range(num_epochs):
    optimizer.zero_grad()
    outputs = rbfn_model(X_train_tensor)
    loss = criterion(outputs, y_train_tensor.unsqueeze(1))
    loss.backward()
    optimizer.step()

# Evaluate the model
with torch.no_grad():
    y_pred_tensor = rbfn_model(X_test_tensor)
    y_pred = y_pred_tensor.numpy().flatten()

# Plot the results
import matplotlib.pyplot as plt
plt.scatter(X_test[:, 0], y_test, label='True')
plt.scatter(X_test[:, 0], y_pred, label='Predicted')
plt.legend()
plt.xlabel('Feature 1')
plt.ylabel('y')
plt.show()

