#!/usr/bin/env python
# Created by "Thieu" at 13:44, 21/09/2023 ----------%                                                                               
#       Email: nguyenthieu2102@gmail.com            %                                                    
#       Github: https://github.com/thieu1995        %                         
# --------------------------------------------------%

import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


class RBFNWithRegularization:
    def __init__(self, num_centers, regularization_lambda=0.01):
        self.num_centers = num_centers
        self.regularization_lambda = regularization_lambda
        self.centers = None
        self.sigmas = None
        self.weights = None

    def _calculate_rbf(self, x, c, sigma):
        # Radial Basis Function (Gaussian)
        return np.exp(-np.sum((x-c)**2, axis=1) / (2 * sigma**2))

    def train(self, X, y):
        # Randomly initialize centers and sigmas
        self.centers = X[np.random.choice(X.shape[0], self.num_centers, replace=False)]
        self.sigmas = np.ones(self.num_centers)

        # Calculate RBF layer outputs
        RBF_layer = np.zeros((X.shape[0], self.num_centers))
        for i in range(X.shape[0]):
            RBF_layer[i] = self._calculate_rbf(X[i], self.centers, self.sigmas)

        # Solve for weights using ridge regression (L2 regularization)
        I = np.identity(self.num_centers)
        self.weights = np.linalg.inv(RBF_layer.T @ RBF_layer + self.regularization_lambda * I) @ RBF_layer.T @ y

    def predict(self, X):
        if self.centers is None or self.weights is None:
            raise Exception("Model not trained.")

        RBF_layer = np.zeros((X.shape[0], self.num_centers))
        for i in range(X.shape[0]):
            RBF_layer[i] = self._calculate_rbf(X[i], self.centers, self.sigmas)

        return RBF_layer @ self.weights


# Example usage:
if __name__ == "__main__":
    np.random.seed(0)
    # Load the Iris dataset
    iris = load_iris()
    X = iris.data
    y = iris.target

    # Standardize the features
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    num_centers = 10
    regularization_lambda = 0.01
    # Create and train RBFN with regularization
    rbf_with_reg = RBFNWithRegularization(num_centers, regularization_lambda)
    rbf_with_reg.train(X_train, y_train)

    # Predict
    y_pred = rbf_with_reg.predict(X_test)
    # Evaluate the model (you can use various metrics depending on the problem)
    from sklearn.metrics import accuracy_score

    accuracy = accuracy_score(y_test, np.round(y_pred))
    print(f"Accuracy: {accuracy:.2f}")
