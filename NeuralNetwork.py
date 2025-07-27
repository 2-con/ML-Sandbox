"""
NeuralNetwork
=====
  The earliest version of (what would become) PyNet. Although a similar version of this code is archived into PyNet as "FlashNet", that version has been heavily modified and is not the same as this one.
  This code is a simple neural network implementation that uses a ReLU activation function and the traditional optimization method of backpropagation.
  It is designed to be a basic example of how neural networks can be implemented in Python.
"""

import random
import math

if True:
  """
  summary:
    a nice place to store all the functions. it kinda gets messy if i cant collapse the function
    and just makes life easier for me.
  """

  # ReLU ###############################################################
  def ReLU(x):
    return max(0,x)

  def ReLU_derivative(x):
    return 1 if x > 0 else 0

  # sigmoid ############################################################
  def sigmoid(x):
    if x < -10.0:
      return 0.0
    elif x > 10.0:
      return 1.0
    else:
      return 1 / (1 + math.exp(-x))

  def sigmoid_derivative(x):
    return sigmoid(x) * (1 - sigmoid(x))

  # softplus ###########################################################
  def softplus(x):
    if x > 10:
      return x
    elif x < -10:
      return 0
    else:
      return math.log(1 + math.exp(x))

  def softplus_derivative(x):
    if x > 10:
      return 1
    elif x < -10:
      return 0
    else:
      return 1 / (1 + math.exp(-x))

  # Mish ############################################################### BROKEN
  def mish(x):
    return x * math.tanh(math.log(1 + math.exp(x))) if x < 5 else x

  def mish_derivative(x):
    return 1 + mish(x) * (1 - mish(x))

  # tanh ###############################################################
  def tanh(x):
    return math.tanh(x)

  def tanh_derivative(x):
    return 1 - math.tanh(x)**2

  # arctan #############################################################
  def arctan(x):
    return math.atan(x)

  def arctan_derivative(x):
    return 1 / (1 + x**2)

  # swish ###############################################################
  def swish(x):
    return x * sigmoid(x)

  def swish_derivative(x):
    return swish(x) + sigmoid(x) * (1 - swish(x))

  # leaky ReLU #########################################################
  def leaky_ReLU(x, alpha=0.01):
    return x if x > 0 else alpha * x

  def leaky_ReLU_derivative(x, alpha=0.01):
    return 1 if x > 0 else alpha

  # ELU ################################################################
  def ELU(x, alpha=1.0):
    if x > 0:
      return x

    elif x < -10:
      return -alpha

    else:
      return alpha * (math.exp(x) - 1)

  def ELU_derivative(x, alpha=1.0):
    if x > 0:
      return 1

    elif x < -10:
      return 0

    else:
      return alpha * math.exp(x)

  # GELU ############################################################## BROKEN
  def GELU(x):
    return 0.5 * x * (1 + math.tanh(math.sqrt(2 / math.pi) * (x + 0.044715 * x**3)))

  def GELU_derivative(x):
    cdf = 0.5 * (1.0 + math.tanh(math.sqrt(2 / math.pi) * (x + 0.044715 * x**3)))
    pdf = math.sqrt(2 / math.pi) * (1 + 3 * 0.044715 * x**2) * (1 - cdf**2)
    return cdf + x * pdf

  # SELU ##############################################################
  def SELU(x, alpha=1.67326, scale=1.0507):
    if x > 10:
      return scale * x

    elif x < -10:
      return scale * -alpha

    else:
      return scale * (x if x > 0 else alpha * (math.exp(x) - 1))

  def SELU_derivative(x, alpha=1.67326, scale=1.0507):
    if x > 0:
      return scale

    elif x < -10:
      return 0

    else:
      return scale * (1 if x > 0 else alpha * math.exp(x))

def enumerated_list(number,list_length) -> list:
  answer = [0 for _ in range(list_length)]
  
  for i in range(list_length):
    if i == number:
      answer[i] = 1
  
  return answer


################################################################################################
#                                           Main code                                          #
################################################################################################


def initialize(*args: int) -> list:
  """
  Initializes a neural network with the specified layer sizes

  Args:
    *args: controls the number of neurons per layer

  Returns:
    A list of lists representing the neural network, where each inner list represents a layer,
    and each layer contains dictionaries representing neurons with 'weights' and 'bias' keys
  """

  network = []  # list of layers

  for a in range(len(args)-1):
    layer = []

    for _ in range(args[a+1]):
      neuron = {
        'weights': [random.uniform(0.1, 1) for _ in range(args[a])],
        'bias': random.uniform(-1, 1)
      }
      layer.append(neuron)
    network.append(layer)

  return network

def propagate(model: list, input_layer) -> tuple[list, list]:
  """
  propagate through the network

  Args:
    model:       The neural network model (list of layers)
    input_layer: The input values for the first layer

  Returns:
    A tuple containing:
      activations[-1]: The output of the last layer
      
      A tuple containing:
        activations:   A list of activations for each layer
        weighted_sums: A list of weighted sums for each layer
  """
  
  current_input = input_layer[:] # copy the input layer, because it will be modified.
  activations = [current_input] # list of layer outputs
  weighted_sums = [] # all of the weighted sums 

  for layer in model:
    layer_output = []
    layer_weighted_sums = []

    for neuron in layer:
      weighted = 0

      for weight, input_value in zip(neuron['weights'], current_input):
        weighted += weight * input_value
      weighted += neuron['bias']

      layer_weighted_sums.append(weighted)
      layer_output.append( ReLU(weighted) )

    activations.append(layer_output[:]) #copy to prevent aliasing.
    current_input = layer_output[:] #copy to prevent aliasing.
    weighted_sums.append(layer_weighted_sums[:])
  
  #return the very last layer (output) and the activations
  return activations[-1], (activations, weighted_sums)

def backpropegate(network: list, results: list, target: list) -> list:
  """
  backpropagates to calculate the error gradients for each neuron, bassically giving
  a number on how much to nudge the weights of each neuron

  Args:
    network: The neural network model
    results: A tuple containing activations and weighted sums from the forward pass
    target:  The target output values

  Returns:
    A list containing:
      lists of errors for each neuron in the layer
  """
  
  activations, weighted_sums = results # unpack the results
  errors = [([0.0] * len(layer)) for layer in network] # initialize list
  output_errors = [target[i] - activations[-1][i] for i in range(len(target))]
  errors[-1] = [error * ReLU_derivative(weightedsum) for error, weightedsum in zip(output_errors, weighted_sums[-1])]

  # goes backwards from the input
  for reversed_layer_index in reversed(range(len(network) - 1)):
    layer = network[reversed_layer_index]
    next_layer_errors = errors[reversed_layer_index + 1]
    current_errors = []

    # goes over all the enuron in the layer
    for neuron_index, neuron in enumerate(layer):

      # goes over the all the neurons in the previous layer
      error = sum(next_neuron['weights'][neuron_index] * next_error for next_neuron, next_error in zip(network[reversed_layer_index + 1], next_layer_errors))
      error *= ReLU_derivative(weighted_sums[reversed_layer_index][neuron_index])# derivative goes here
      current_errors.append(error)
      
    errors[reversed_layer_index] = current_errors[:]
  return errors

def update(network: list, activations: list, error: list, learning_rate: float) -> None:
  """
  Updates the weights and biases of the network

  Args:
    network:       The neural network model
    activations:   The activations from forward propagation
    error:         The error gradients from backpropagation
    learning_rate: The learning rate
  """
  #print(f"Network layer sizes: {[len(layer) for layer in network]}") # debug print

  # iterate over layers
  for layer_index in range(len(network)):
    
    # iterate over each neuron
    for neuron_index, neuron in enumerate(network[layer_index]):
      
      # iterate over each weights
      for weight_index in range(len(neuron['weights'])):
        neuron['weights'][weight_index] += learning_rate * error[layer_index][neuron_index] * activations[layer_index][weight_index]
      
      # bias
      neuron['bias'] += learning_rate * error[layer_index][neuron_index]


################################################################################################
#                          universal, works for both situations                                #
################################################################################################


def train(network: list, training_data, learning_rate: float, epochs: int, **debug):
  """
  Summary:
    trains the network over epochs given

  Args:
    network:       list of layers, which is a list of neurons
    training_data: the dataset that will be used to train the model, must be an iterable containing iterables containing the inputs (iterable) and the targets(iterable).
    learning_rate: learning rate
    epochs:        how many rounds of training the network will get
    debug:         show stats? how often?
  """

  for epoch in range(epochs):
    overall_error = 0

    for batch in training_data:
      output, activations = propagate(network, batch[0])
      error = backpropegate(network, activations, batch[1])
      update(network, activations[0], error, learning_rate)

      for output_index in range(len(batch[1])):
        overall_error += sum((target - output)**2 for target, output in zip(batch[1], output))

    if debug['debug'] and (epoch % debug['regularity'] == 0):
      print(f"Epoch {epoch:5} | Error {round(overall_error/len(training_data), debug['decimals'])}")

# main ----------------------------------------------------------------

if __name__ == "__main__":
  
  network = initialize(2, 3, 1)
  training_data = [
    ([0, 0], [0]),
    ([1, 0], [1]),
    ([0, 1], [1]),
    ([1, 1], [0])
  ]
  learning_rate = 0.05
  epochs = 10000

  train(network, training_data, learning_rate, epochs, debug=True, regularity=500, decimals=2, model='custom')
  print()
  # Test the trained network
  for inputs, target in training_data:

    output, _ = propagate(network, inputs)
    print(f"Input: {inputs} | Output {round(output[0],3):5} | Target {target} ")