#!/usr/bin/env python
# Created by "Thieu" at 13:40, 21/09/2023 ----------%                                                                               
#       Email: nguyenthieu2102@gmail.com            %                                                    
#       Github: https://github.com/thieu1995        %                         
# --------------------------------------------------%

import numpy as np


class RBFNWithRegularization:
    def __init__(self, num_centers, sigma=1.0, regularization_lambda=0.01):
        self.num_centers = num_centers
        self.sigma = sigma
        self.regularization_lambda = regularization_lambda
        self.centers = None
        self.weights = None

    def _calculate_rbf(self, x, c):
        # Radial Basis Function (Gaussian)
        return np.exp(-np.linalg.norm(x - c) ** 2 / (2 * self.sigma ** 2))

    def train(self, X, y):
        # Randomly initialize centers
        self.centers = X[np.random.choice(X.shape[0], self.num_centers, replace=False)]

        # Calculate RBF layer outputs
        RBF_layer = np.zeros((X.shape[0], self.num_centers))
        for i in range(X.shape[0]):
            for j in range(self.num_centers):
                RBF_layer[i, j] = self._calculate_rbf(X[i], self.centers[j])

        # Solve for weights using ridge regression (L2 regularization)
        I = np.identity(self.num_centers)
        self.weights = np.linalg.inv(RBF_layer.T @ RBF_layer + self.regularization_lambda * I) @ RBF_layer.T @ y

    def predict(self, X):
        if self.centers is None or self.weights is None:
            raise Exception("Model not trained.")

        RBF_layer = np.zeros((X.shape[0], self.num_centers))
        for i in range(X.shape[0]):
            for j in range(self.num_centers):
                RBF_layer[i, j] = self._calculate_rbf(X[i], self.centers[j])

        return RBF_layer @ self.weights


# Example usage:
if __name__ == "__main__":
    # Generate synthetic data for regression
    np.random.seed(0)
    X_train = np.sort(5 * np.random.rand(80, 1), axis=0)
    y_train = np.sin(X_train).ravel()

    X_test = np.arange(0, 5, 0.01)[:, np.newaxis]

    num_centers = 10
    sigma = 1.0
    regularization_lambda = 0.01

    # Create and train RBFN with regularization
    rbf_with_reg = RBFNWithRegularization(num_centers, sigma, regularization_lambda)
    rbf_with_reg.train(X_train, y_train)

    # Predict
    y_pred = rbf_with_reg.predict(X_test)

    # Plot results
    import matplotlib.pyplot as plt

    plt.figure()
    plt.plot(X_train, y_train, 'ro', label='Training Data')
    plt.plot(X_test, y_pred, 'b-', label='RBFN Prediction')
    plt.legend()
    plt.show()

