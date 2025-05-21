"""DOCSTRING
made in 15/3/2025 (d/m/y)

To do list:

 - 
 
Notes:

linear regression lmao

"""

# imports

import matplotlib.pyplot
import numpy as np
import random

# functions

def abs_error(datax, datay, m, b):
  error = 0
  
  for item in range(len(datax)):
    error += abs(datay[item] - (m*datax[item] + b))
    
  return error/len(datax)

def linear_regression(datax, datay, epochs, learning_rate, bias_multiplier, debug=False):
  
  # y=mx+b
  m=0
  b=0
  
  goingdown = False # is currently increasing the value
  goingup = False # is currently decreasing the value
  
  error = 0 # current error
  derror = 0 # error if we change it a bit
  slope = 0 # slope (derivative)
  
  mode = 0
  
  for _ in range(epochs):
    mode += 1
    goingdown = False
    goingup = False
    
    if mode %2 == 0:
      
      # calculate B
      for _ in range(epochs):
        
        error = abs_error(datax, datay, m, b)
        b += learning_rate*bias_multiplier
        derror = abs_error(datax, datay, m, b)
        
        slope = derror - error
        b -= learning_rate*bias_multiplier
        
        # if gradient descent is increasing error, break
        if goingdown and goingup:
          break
        
        # positive gradient
        if slope > 0:
          b -= learning_rate*bias_multiplier
          goingdown = True
          
        # positive gradient
        elif slope < 0:
          b += learning_rate*bias_multiplier
          goingup = True
    
    else:
      # calculate M
      for _ in range(epochs):
        
        error = abs_error(datax, datay, m, b)
        m += learning_rate
        derror = abs_error(datax, datay, m, b)
        
        slope = derror - error
        m -= learning_rate
        
        # if gradient descent is increasing error, break
        if goingdown and goingup:
          break
        
        # positive gradient
        if slope > 0:
          m -= learning_rate
          goingdown = True
          
        # positive gradient
        elif slope < 0:
          m += learning_rate
          goingup = True
    
    if mode % 100 == 0 and debug:
      print(f"Training   | {round(m,3):6} | {round(b,3):6} | Error {round(error,3):6} | Epoch {round(mode)}")    
       
  return m, b

# constants

if __name__ == "__main__":
  M = random.randint(0,10)
  B = random.randint(-50,50)
  RANDOMNESS = 2.5

  np.random.seed(0) 
  DATAX = np.sort(np.random.rand(50) * 10) 
  DATAY = M*DATAX + B + np.random.randn(50)*RANDOMNESS
  # Main ==========================

  m,b = linear_regression(DATAX, DATAY, 1000, 0.0001, 10000, True)
  print(f"Validating | {round(M,3):6} | {round(B,3):6} |")

  # plotting scatter and the line
  matplotlib.pyplot.scatter(DATAX, DATAY)
  matplotlib.pyplot.plot(DATAX, m*DATAX+b, color='black')
  #matplotlib.pyplot.plot(DATAX, M*DATAX + B, color='red')

  # texts
  matplotlib.pyplot.xlabel("X")
  matplotlib.pyplot.ylabel("Y")
  matplotlib.pyplot.title("manual linear regression", loc='center', fontsize=20, y=1.09)
  matplotlib.pyplot.title(f"regression: {m}x+{b} | error = {abs_error(DATAX, DATAY, m, b)}", loc='left', fontsize=10, y=1.0)

  # show
  matplotlib.pyplot.show()