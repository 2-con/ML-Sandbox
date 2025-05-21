"""DOCSTRING
made in 30/3/2025 (d/m/y)

To do list:

 - 
 
Notes:



"""

# imports

import math

# classes

class sequential:
  def __init__(self, *args):
    self.layers = args
    
  def propagate(self, input:list) -> list:
    
    for item in input:
      if type(item) not in (list, tuple):
        raise TypeError("Input must be a 2d array/list")
      
      for elements in item:
        if type(elements) not in (int, float):
          raise TypeError("Convolutional neural networks only process numbers")
    
    for layer in self.layers:
      
      answer = [] # final answer
      
      # if its a convolutional layer, apply the kernel and activation function
      if type(layer) == convolution:
        
        # iterate over all layers
        for a in range( len(input) - (len(layer.kernel) - 1) ):
          
          layer_output = []
          
          # iterate over all the elements in the layer
          for b in range( len(input[a]) - (len(layer.kernel[0]) - 1) ):
            dot_product = 0
            
            # iterate over the kernel layers
            for c in range(len(layer.kernel)):
              
              # iterate over the kernel elements
              for d in range(len(layer.kernel[c])):
                
                # apply the kernel to the input
                dot_product += layer.kernel[c][d] * input[a+c][b+d]
            
            layer_output.append(ACTIVATION[layer.activation](dot_product))
          
          answer.append(layer_output[:])
      
      # lastly, if its a maxpooling layer, apply the maxpooling function
      elif type(layer) == maxpooling:
        
        # iterate over all the layers
        for a in range(0, len(input), layer.stride):
          
          layer_output = []
          
          # iterate over all the elements in the layer
          for b in range(0, len(input[a]), layer.stride):
            pool = []
            
            # control the vertical
            for c in range(layer.size):
              
              # control the horizontal
              for d in range(layer.size):
                
                if a+c < len(input) and b+d < len(input[a]):
                  pool.append(input[a+c][b+d])
            
            layer_output.append( max(pool) )
          
          answer.append(layer_output[:])
      
      # same thing but average it out
      elif type(layer) == meanpooling:
        # iterate over all the layers
        for a in range(0, len(input), layer.stride):
          
          layer_output = []
          
          # iterate over all the elements in the layer
          for b in range(0, len(input[a]), layer.stride):
            pool = []
            
            # control the vertical
            for c in range(layer.size):
              
              # control the horizontal
              for d in range(layer.size):
                
                if a+c < len(input) and b+d < len(input[a]):
                  pool.append(input[a+c][b+d])
            
            layer_output.append( sum(pool) / len(pool) )
          
          answer.append(layer_output[:])
      
      elif type(layer) == reshape:
        
        # pool everything
        pile = []
        for row in input:
          for item in row:
            pile.append(item)
        
        height = layer.height
        width = layer.width
        
        if height < 0:
          height = len(pile) // abs(width)
        
        if width < 0:
          width = len(pile) // abs(height)
        
        # reshape the pile
        answer = []
        for a in range(height):
          row = []
          for b in range(width):
            try:
              row.append(pile[0])
              pile.pop(0)
            except:
              raise ValueError(f"Cannot reshape a {len(input[0])}x{len(input)} matrix to a {width}x{height} matrix")
          
          answer.append(row[:])
      
      # if its something else, raise an error
      else:
        raise TypeError("Invalid layer type")
      
      input = answer[:]
      
    return answer

  def add(self, layer):
    self.layers.append(layer)
      
class convolution:
  def __init__(self, kernel:list, activation:str, **kwargs):
    """
    kernel        (list or lists) : the kernel to apply
    activation    (string)        : the activation function
    learnable     (boolean)       : whether or not the kernel is learnable
    learning_rate (float)         : the learning rate
    ----------
    Activation functions    : 'relu' 'softplus' 'mish' 'swish' 'leaky_relu' 'elu' 'gelu' 'selu' 'reeu' 'linear'
    Normalisation functions : 'binary_step' 'softsign' 'sigmoid' 'tanh' 'softmax' 'argmax'
    """
    self.kernel = kernel
    self.activation = activation
    self.extra = kwargs

class maxpooling:
  def __init__(self, matrix_size:int, stride:int):
    self.size = matrix_size
    self.stride = stride
    
class meanpooling:
  def __init__(self, matrix_size:int, stride:int):
    self.size = matrix_size
    self.stride = stride

class reshape:
  def __init__(self, xlength:int, ylength:int):
    self.width = xlength
    self.height = ylength

# functions

if True:
  """
  summary:
    a nice place to store all the functions. it kinda gets messy if i cant collapse the function
    and just makes life easier for me.
  """
  
  # normalization functions
  def sigmoid(x):
    return 1 / (1 + math.exp(-x))
  
  def tanh(x):
    return math.tanh(x)

  def binary_step(x):
    return 1 if x >= 0 else 0
  
  def softsign(x):
    return x / (1 + abs(x))
  
  def softmax(x):
    exp_x = [math.exp(i) for i in x]
    return [i / sum(exp_x) for i in exp_x]
  
  def argmax(x):
    return x.index(max(x))
  
  # rectifiers
  
  def ReLU(x):
    return max(0,x)

  def softplus(x):
    return math.log(1 + math.exp(x))

  def mish(x):
    return x * math.tanh(math.log(1 + math.exp(x)))

  def swish(x):
    return x * sigmoid(x)

  def leaky_ReLU(x, alpha=0.01):
    return max(alpha * x, x)

  def ELU(x, alpha=1.0):
    return min(alpha * (math.exp(x) - 1), ReLU(x))

  def GELU(x):
    return (x * (1 + math.tanh(math.sqrt(2 / math.pi) * (x + 0.044715 * x**3))))/2

  def SELU(x, alpha=1.67326, scale=1.0507):
    return scale * (x if x > 0 else alpha * (math.exp(x) - 1))

  def Linear(x):
    return x
  
  def ReEU(x):
    return min(math.exp(x),max(1,x+1))

def display(image: list) -> None:
  
  for row in image:
    for pixel in row:
      if pixel > 0.01:
        print("■", end=" ")
        
      elif pixel < -0.01:
        print("□", end=" ")
        
      else:
        print("•", end=" ")
    print()

def numerical_display(image: list) -> None:
  
  for row in image:
    for pixel in row:
      print(pixel, end=" ")
    print()
# constants

ACTIVATION = {
  # rectifiers
  'relu': ReLU,
  'softplus': softplus,
  'mish': mish,
  'swish': swish,
  'leaky_relu': leaky_ReLU,
  'elu': ELU,
  'gelu': GELU,
  'selu': SELU,
  'reeu': ReEU,
  'linear': Linear,
  
  # normalization functions
  'binary_step': binary_step,
  'softsign': softsign,
  'sigmoid': sigmoid,
  'tanh': tanh,
  
  'softmax': softmax,
  'argmax': argmax,
}

# Main ==========================

if __name__ == '__main__':
  model = sequential(
    convolution(kernel=[[-1,-1,-1],
                        [-1, 8,-1],
                        [-1,-1,-1]], activation='relu'),
  )

  image1 = (
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  )

  print("Original image:")
  display(image1)

  print("-----------------")
  print("convoluted image:")
  display(model.propagate(image1))