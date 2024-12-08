# Adaptive Power Neurons

**Adaptive Power Neurons** is a machine learning model that utilizes adaptive power perceptrons, which are neural units that adjust both their power (degree of polynomial features) and input index dynamically. These perceptrons are used to build layers in a neural network that can handle complex relationships between features and outputs.

The model incorporates polynomial feature expansion, index bias adjustments, and learning rate optimizations to create a highly flexible model for regression and classification tasks.

## Features

- **Adaptive Power Perceptrons**: Each neuron in the network can dynamically adjust its power and input index.
- **Polynomial Feature Expansion**: The model generates polynomial features up to a specified power.
- **Index Bias**: Includes an adjustable index bias that shifts the input features.
- **Layer Support**: The model supports the creation of multi-layer neural networks using adaptive power neurons.
- **Optimizer**: Fine-tune hyperparameters like learning rate, polynomial power, and indexing rate during training.

## Mathematical Formulation

The core of the model is built around the concept of a perceptron that uses polynomial features of input data. Here's a breakdown of the algorithm used:

### 1. Polynomial Feature Expansion

Given an input vector \( x \), we generate polynomial features up to a specified degree \( p \). The polynomial feature vector \( \phi(x) \) is defined as:

\[
\phi(x) = \left[ x^1, x^2, \dots, x^p \right]
\]

Where \( p \) is the maximum power specified for each perceptron (layer).

### 2. Weighted Sum and Activation

For each perceptron in the network, the weighted sum of the polynomial features is computed:

\[
z = w_1 \cdot \phi(x_1) + w_2 \cdot \phi(x_2) + \dots + w_n \cdot \phi(x_n) + b
\]

Where \( w_1, w_2, \dots, w_n \) are the weights of the model, \( b \) is the bias term, and \( \phi(x) \) is the polynomial feature vector. The output of the perceptron is then passed through an activation function (in this case, a step function for binary classification):

\[
\hat{y} = 
\begin{cases} 
1 & \text{if } z \geq 0 \\
0 & \text{if } z < 0
\end{cases}
\]

Where \( \hat{y} \) is the predicted output.

### 3. Loss Function: Mean Squared Error (MSE)

The Mean Squared Error (MSE) loss function is used to evaluate the model's performance. It is calculated as:

\[
\text{MSE} = \frac{1}{N} \sum_{i=1}^{N} \left( y_i - \hat{y}_i \right)^2
\]

Where \( N \) is the number of samples, \( y_i \) is the true output for sample \( i \), and \( \hat{y}_i \) is the predicted output.

### 4. Index Bias and Adjustment

In addition to adjusting the weights and biases, the model includes an adjustable index bias \( \delta \) for each input:

\[
x_{\text{adjusted}} = x + \delta
\]

The model dynamically adjusts the index by a rate determined by the **indexing rate** during training, allowing it to fine-tune the input features for better prediction performance.

### 5. Weight Update Rule

The weights of the model are updated using gradient descent. The gradient of the loss function with respect to the weights is calculated, and the weights are updated as follows:

\[
w_i = w_i - \eta \cdot \frac{\partial \text{MSE}}{\partial w_i}
\]

Where \( \eta \) is the learning rate. Similarly, the bias term \( b \) is updated as:

\[
b = b - \eta \cdot \frac{\partial \text{MSE}}{\partial b}
\]

And the index bias \( \delta \) is updated as:

\[
\delta = \delta - \eta \cdot \frac{\partial \text{MSE}}{\partial \delta}
\]

### 6. Multi-Layer Network

The neural network is built by stacking multiple layers of **Adaptive Power Neurons**. Each layer consists of multiple perceptrons, and the output of one layer serves as the input for the next layer. During training, the parameters (weights, biases, and index bias) of each layer are updated separately using the same gradient descent approach.

## Installation

To install **Adaptive Power Neurons**, follow these steps:

### Install via pip

Clone the repository and run the following command in the terminal:

```bash
pip install adaptive-power-neurons

#Example Usage:
from adaptive_power_neurons import AdaptivePowerNeuron, AdaptivePowerModel, Optimizer
import numpy as np

# Sample data (X: input features, y: target labels)
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([0, 0, 1, 1, 1])

# Create an adaptive power neuron
neuron = AdaptivePowerNeuron(input_dim=1, max_power=3, learning_rate=0.001, indexing_rate=0.01)

# Create a simple neural network with 2 layers
model = AdaptivePowerModel(layers=[neuron, neuron], loss_function="mse")

# Create an optimizer for the model
optimizer = Optimizer(model, learning_rate=0.001)

# Train the model for 20 epochs
model.fit(X, y, epochs=20, optimizer=optimizer)

# Test prediction
test_input = np.array([3])
prediction = model.predict(test_input)
print(f"Prediction for input {test_input}: {prediction}")
