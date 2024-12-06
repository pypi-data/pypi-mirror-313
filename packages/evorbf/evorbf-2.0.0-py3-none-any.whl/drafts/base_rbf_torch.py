#!/usr/bin/env python
# Created by "Thieu" at 15:50, 21/09/2023 ----------%                                                                               
#       Email: nguyenthieu2102@gmail.com            %                                                    
#       Github: https://github.com/thieu1995        %                         
# --------------------------------------------------%

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
from sklearn.datasets import make_regression, load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from torch.utils.data import TensorDataset, DataLoader


class RBFN(nn.Module):
    """Radial Basis Function
    Build based on this paper: http://evo-ml.com/ibrahim/publications/10.1007s00521-016-2559-2.pdf
    """
    def __init__(self, n_output, centers, sigmas=(1.0, ), centers_learnable=False, sigmas_learnable=False):
        super(RBFN, self).__init__()
        # Perform K-means clustering to find centers
        self.n_centers = len(centers)
        # self.kmeans = KMeans(n_clusters=num_centers, random_state=0).fit(X_train)
        self.centers = nn.Parameter(torch.tensor(centers, dtype=torch.float32), requires_grad=centers_learnable)
        self.sigmas = nn.Parameter(torch.tensor(sigmas, dtype=torch.float32), requires_grad=sigmas_learnable)
        # Create linear output layer
        self.linear = nn.Linear(self.n_centers, n_output, bias=False)  # Turn off bias

    def forward(self, x):
        x = x.unsqueeze(1)
        rbf = torch.exp(-torch.norm(x - self.centers, dim=2) ** 2 / (2 * self.sigmas ** 2))
        output = self.linear(rbf)
        return output


class GradientRbfn01:
    """
    This class defines the general RBF model that:
        + use non-linear Gaussian function
        + use Gradient-based
        + have no regulation term
    """
    def __init__(self, center_finder="kmean", n_centers=5):
        self.center_finder = center_finder
        self.n_centers = n_centers
        self.network, self.loss_train, self.weights = None, None, None

    @staticmethod
    def calculate_centers(X, method="kmean", n_clusters=5):
        if method == "kmean":
            kobj = KMeans(n_clusters=n_clusters, init='random', random_state=11).fit(X)
            return kobj.cluster_centers_
        elif method == "random":
            return X[np.random.choice(len(X), n_clusters, replace=False)]

    def fit(self, X, y, epoch=1000, batch_size=32):
        centers = self.calculate_centers(X, method="random", n_clusters=5)
        sigmas = np.ones(len(centers))
        self.network = RBFN(n_output=1, centers=centers, sigmas=sigmas, centers_learnable=False, sigmas_learnable=True)
        optimizer = optim.Adam(self.network.parameters(), lr=0.01)
        criterion = nn.MSELoss()

        # Create TensorDatasets
        train_dataset = TensorDataset(torch.tensor(X, dtype=torch.float32), torch.tensor(y, dtype=torch.float32))
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

        for idx_epoch in range(epoch):
            total_loss = 0.0
            for batch_x, batch_y in train_loader:
                optimizer.zero_grad()
                outputs = self.network(batch_x)
                loss = criterion(outputs, batch_y.unsqueeze(1))
                total_loss += loss.item()
                loss.backward()
                optimizer.step()
            average_loss = total_loss / len(train_loader)
            print(f"Epoch [{idx_epoch + 1}/{epoch}] - Average Loss: {average_loss:.4f}")

    def predict(self, X):
        self.network.eval()
        test_tensor = torch.tensor(X, dtype=torch.float32)
        with torch.no_grad():
            return self.network(test_tensor).numpy()


class GradientRbfn02:
    """
    This class defines the general RBF model that:
        + use non-linear Gaussian function
        + use Gradient-based
        + have regulation term
    """
    def __init__(self, center_finder="kmean", n_centers=5):
        self.center_finder = center_finder
        self.n_centers = n_centers
        self.network, self.loss_train, self.weights = None, None, None

    @staticmethod
    def calculate_centers(X, method="kmean", n_clusters=5):
        if method == "kmean":
            kobj = KMeans(n_clusters=n_clusters, init='random', random_state=11).fit(X)
            return kobj.cluster_centers_
        elif method == "random":
            return X[np.random.choice(len(X), n_clusters, replace=False)]

    def custom_loss(self, outputs, targets, original_loss, model, lambda_reg):
        # Calculate the original loss (e.g., MSE)
        original_loss = original_loss(outputs, targets)
        # Calculate the L2 regularization term
        regularization_loss = 0.0
        for param in model.parameters():
            if param.requires_grad:
                regularization_loss += torch.norm(param, p=2) ** 2  # L2 norm
        # Combine the original loss and regularization term
        return original_loss + lambda_reg * regularization_loss  # Adjust lambda_reg as needed

    def fit(self, X, y, epoch=1000, batch_size=32):
        centers = self.calculate_centers(X, method="random", n_clusters=5)
        sigmas = np.ones(len(centers))
        self.network = RBFN(n_output=1, centers=centers, sigmas=sigmas, centers_learnable=False, sigmas_learnable=True)
        optimizer = optim.Adam(self.network.parameters(), lr=0.01, weight_decay=0.001)  # Adjust weight_decay as needed
        lambda_reg = 0.001       # Regularization Weight, Regularization Strength
        criterion = nn.MSELoss()

        # Create TensorDatasets
        train_dataset = TensorDataset(torch.tensor(X, dtype=torch.float32), torch.tensor(y, dtype=torch.float32))
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

        for idx_epoch in range(epoch):
            total_loss = 0.0
            for batch_x, batch_y in train_loader:
                optimizer.zero_grad()
                outputs = self.network(batch_x)
                loss = self.custom_loss(outputs, batch_y.unsqueeze(1), criterion, self.network, lambda_reg)
                total_loss += loss.item()
                loss.backward()
                optimizer.step()
            average_loss = total_loss / len(train_loader)
            print(f"Epoch [{idx_epoch + 1}/{epoch}] - Average Loss: {average_loss:.4f}")

    def predict(self, X):
        self.network.eval()
        test_tensor = torch.tensor(X, dtype=torch.float32)
        with torch.no_grad():
            return self.network(test_tensor).numpy()


# np.random.seed(0)
# # Load the Iris dataset
# iris = load_iris()
# X = iris.data
# y = iris.target
#
# # Standardize the features
# scaler = StandardScaler()
# X = scaler.fit_transform(X)
# # Split the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Generate synthetic regression data
X, y = make_regression(n_samples=1000, n_features=4, noise=0.1, random_state=0)
X = StandardScaler().fit_transform(X)
y = StandardScaler().fit_transform(y.reshape(-1, 1)).flatten()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialize and train the RBFN model
model = GradientRbfn01("kmean", n_centers=10)
model.fit(X_train, y_train, epoch=1000)
y_pred = model.predict(X_test)
print(model.network.centers.detach().numpy())
print(model.network.sigmas.detach().numpy())

from permetrics import RegressionMetric, ClassificationMetric

metric = RegressionMetric(y_test, y_pred)
print(metric.get_metrics_by_list_names(["MSE", "RMSE", "R2", "NSE", "KGE", "MAPE"]))


# import numpy as np
# from evorbf import get_dataset, MhaRbfRegressor
#
#
# data = get_dataset("Diabetes")
# data.split_train_test(test_size=0.2, random_state=2)
# print(data.X_train.shape, data.X_test.shape)
#
# data.X_train, scaler_X = data.scale(data.X_train, scaling_methods="standard")
# data.X_test = scaler_X.transform(data.X_test)
#
# data.y_train, scaler_y = data.scale(data.y_train, scaling_methods="standard")
# data.y_test = scaler_y.transform(np.reshape(data.y_test, (-1, 1)))
#
# # Initialize and train the RBFN model
# model = GradientRbfn01("kmean", n_centers=10)
# model.fit(data.X_train, data.y_train, epoch=1000)
# y_pred = model.predict(data.X_test)
#
# from permetrics import RegressionMetric, ClassificationMetric
#
# metric = RegressionMetric(data.y_test, y_pred)
# print(metric.get_metrics_by_list_names(["MSE", "RMSE", "R2S", "NSE", "KGE", "MAPE"]))
