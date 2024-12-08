import numpy as np
#Author = Dedeep.v.
#Github_username = Dedeep007

class AdaptivePowerPerceptron:
    """
    A perceptron that adjusts its polynomial feature power and input index dynamically.
    It uses polynomial features and adjusts weights and biases based on the error.
    """
    def __init__(self, input_dim, max_power=3, learning_rate=0.001, indexing_rate=1):
        """
        Initialize the perceptron with specific hyperparameters.

        Parameters:
            input_dim (int): The number of input features.
            max_power (int): The maximum polynomial power for the features.
            learning_rate (float): The learning rate for weight updates.
            indexing_rate (float): The rate at which the input index can adjust.
        """
        self.input_dim = input_dim
        self.max_power = max_power
        self.learning_rate = learning_rate
        self.indexing_rate = indexing_rate
        self.weights = np.random.randn(input_dim * max_power)
        self.bias = np.random.randn()
        self.current_power = 1
        self.current_index_offset = 0  # Index offset (can be fractional)
        self.index_bias = np.random.randn()  # Additional index bias

    def polynomial_features(self, x, power):
        """
        Generate polynomial features up to the specified power.

        Parameters:
            x (float): The input feature.
            power (int): The maximum polynomial power.

        Returns:
            np.ndarray: The generated polynomial features.
        """
        return np.hstack([x**p for p in range(1, power + 1)])

    def interpolate_input(self, x):
        """
        Adjust the input by adding the index offset and index bias.

        Parameters:
            x (float): The input feature.

        Returns:
            float: The adjusted input value.
        """
        idx_adjusted = x + self.current_index_offset + self.index_bias
        return idx_adjusted

    def predict(self, x):
        """
        Make a prediction using the perceptron.

        Parameters:
            x (float): The input feature.

        Returns:
            int: The predicted class (0 or 1).
        """
        x_adjusted = self.interpolate_input(x)
        poly_x = self.polynomial_features(x_adjusted, self.current_power)
        linear_output = np.dot(poly_x, self.weights[:len(poly_x)]) + self.bias
        return 1 if linear_output >= 0 else 0

    def update_weights(self, x, y):
        """
        Update the weights and biases based on the error.

        Parameters:
            x (float): The input feature.
            y (int): The target label.
        """
        best_power = self.current_power
        best_index_offset = self.current_index_offset
        min_loss = float('inf')

        for power in range(1, self.max_power + 1):
            for offset in [-self.indexing_rate, 0, self.indexing_rate]:
                temp_index_offset = self.current_index_offset + offset
                x_adjusted = x + temp_index_offset + self.index_bias
                poly_x = self.polynomial_features(x_adjusted, power)
                prediction = 1 if np.dot(poly_x, self.weights[:len(poly_x)]) + self.bias >= 0 else 0
                error = y - prediction
                loss = error ** 2

                if loss < min_loss:
                    min_loss = loss
                    best_power = power
                    best_index_offset = temp_index_offset

        self.current_power = best_power
        self.current_index_offset = best_index_offset

        x_adjusted = x + self.current_index_offset + self.index_bias
        poly_x = self.polynomial_features(x_adjusted, self.current_power)
        prediction = self.predict(x)
        error = y - prediction

        self.weights[:len(poly_x)] += self.learning_rate * error * poly_x
        self.bias += self.learning_rate * error
        self.index_bias += self.learning_rate * error * 1  # Adjust index_bias dynamically


class Optimizer:
    """
    An optimizer class that allows the adjustment of learning rate, power, and indexing power during training.
    """
    def __init__(self, learning_rate=0.001, max_power=3, indexing_rate=0.1):
        """
        Initialize the optimizer.

        Parameters:
            learning_rate (float): The global learning rate for all layers.
            max_power (int): The global max power for polynomial features.
            indexing_rate (float): The global indexing rate.
        """
        self.learning_rate = learning_rate
        self.max_power = max_power
        self.indexing_rate = indexing_rate

    def apply_optimizer(self, perceptron, layer_avg_params):
        """
        Apply optimizer settings to the given perceptron based on the average parameters of the layer.

        Parameters:
            perceptron (AdaptivePowerPerceptron): The perceptron to which the optimizer will apply settings.
            layer_avg_params (dict): The average parameters of the layer to match with the optimizer settings.
        """
        # Apply a weighted adjustment of the optimizer's parameters to match layer average
        perceptron.learning_rate = (self.learning_rate + layer_avg_params['learning_rate']) / 2
        perceptron.max_power = (self.max_power + layer_avg_params['max_power']) / 2
        perceptron.indexing_rate = (self.indexing_rate + layer_avg_params['indexing_rate']) / 2


class AdaptivePowerNeurons:
    """
    A neural network model using layers of AdaptivePowerPerceptrons.
    This model can have multiple layers of perceptrons, and the optimizer can be used to adjust
    hyperparameters dynamically.
    """
    def __init__(self):
        """
        Initialize the AdaptivePowerNeurons model.
        """
        self.layers = []
        self.optimizer = None

    def add_layer(self, num_perceptrons, input_dim, max_power, learning_rate, indexing_rate):
        """
        Add a layer of perceptrons to the model.

        Parameters:
            num_perceptrons (int): Number of perceptrons in the layer.
            input_dim (int): Number of input dimensions.
            max_power (int): Maximum polynomial power for perceptron features.
            learning_rate (float): Learning rate for this layer.
            indexing_rate (float): Indexing rate for this layer.
        """
        layer = [
            AdaptivePowerPerceptron(input_dim, max_power, learning_rate, indexing_rate)
            for _ in range(num_perceptrons)
        ]
        self.layers.append({'perceptrons': layer, 'learning_rate': learning_rate, 'max_power': max_power, 'indexing_rate': indexing_rate})

    def set_optimizer(self, optimizer):
        """
        Set the optimizer for the model.

        Parameters:
            optimizer (Optimizer): The optimizer object.
        """
        self.optimizer = optimizer
        for layer in self.layers:
            # Calculate the average parameters of the layer
            layer_avg_params = {
                'learning_rate': np.mean([p.learning_rate for p in layer['perceptrons']]),
                'max_power': np.mean([p.max_power for p in layer['perceptrons']]),
                'indexing_rate': np.mean([p.indexing_rate for p in layer['perceptrons']])
            }
            for perceptron in layer['perceptrons']:
                self.optimizer.apply_optimizer(perceptron, layer_avg_params)

    def predict(self, X):
        """
        Predict the output for a given input.

        Parameters:
            X (array-like): Input data.

        Returns:
            np.ndarray: Model predictions for the input data.
        """
        for layer in self.layers:
            new_X = []
            for xi in X:
                layer_output = [perceptron.predict(xi) for perceptron in layer['perceptrons']]
                new_X.append(layer_output)
            X = np.array(new_X)
        return X

    def fit(self, X, y, epochs=10):
        """
        Train the model on the given data.

        Parameters:
            X (array-like): Input data.
            y (array-like): Target labels.
            epochs (int): Number of epochs for training.
        """
        for epoch in range(epochs):
            for layer in self.layers:
                for perceptron in layer['perceptrons']:
                    for xi, yi in zip(X, y):
                        perceptron.update_weights(xi, yi)
            loss = self.calculate_loss(X, y)
            print(f"Epoch {epoch + 1}/{epochs}, Loss: {loss}")

    def calculate_loss(self, X, y):
        """
        Calculate the mean squared error (MSE) loss.

        Parameters:
            X (array-like): Input data.
            y (array-like): Target labels.

        Returns:
            float: Loss value.
        """
        total_loss = 0
        for xi, yi in zip(X, y):
            prediction = self.predict([xi])
            total_loss += (yi - prediction[0][0]) ** 2
        return total_loss / len(y)
