"""
Polynomial Regression
=====
  This script implements a polynomial regression model using coordinate descent via numerical differentiation.
  The optimizer used is a custom twist on the traditional gradient descent method.
"""

# imports

import matplotlib.pyplot
import numpy as np
import random

# functions

def abs_error(datax, datay, a, b, c, d):
  error = 0
  
  for item in range(len(datax)):
    error += abs(datay[item] - (a*datax[item]**3 + b*datax[item]**2 + c*datax[item] + d))
    
  return error/len(datax)

def polynomial_regression(datax, datay, epochs, learning_rate, bias_multiplier, debug=False):
  
  # ax^3 + bx^2 + cx + d
  a, b, c, d = 0, 0, 0, 0
  
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
    
    if mode %4 == 3:
      
      for _ in range(epochs):
        error = abs_error(datax, datay, a, b, c, d)
        d += learning_rate*bias_multiplier
        derror = abs_error(datax, datay, a, b, c, d)
        
        slope = derror - error
        d -= learning_rate*bias_multiplier
        
        # if gradient descent is increasing error, break
        if goingdown and goingup:
          break
        
        # positive gradient
        if slope > 0:
          d -= learning_rate*bias_multiplier
          goingdown = True
          
        # positive gradient
        elif slope < 0:
          d += learning_rate*bias_multiplier
          goingup = True
          
    elif mode %4 == 2:
      
      for _ in range(epochs):
        
        error = abs_error(datax, datay, a, b, c, d)
        c += learning_rate
        derror = abs_error(datax, datay, a, b, c, d)
        
        slope = derror - error
        c -= learning_rate
        
        # if gradient descent is increasing error, break
        if goingdown and goingup:
          break
        
        # positive gradient
        if slope > 0:
          c -= learning_rate
          goingdown = True
          
        # positive gradient
        elif slope < 0:
          c += learning_rate
          goingup = True
          
    elif mode %4 == 1:
      
      for _ in range(epochs):
        
        error = abs_error(datax, datay, a, b, c, d)
        b += learning_rate
        derror = abs_error(datax, datay, a, b, c, d)
        
        slope = derror - error
        b -= learning_rate
        
        # if gradient descent is increasing error, break
        if goingdown and goingup:
          break
        
        # positive gradient
        if slope > 0:
          b -= learning_rate
          goingdown = True
          
        # positive gradient
        elif slope < 0:
          b += learning_rate
          goingup = True
          
    elif mode %4 == 0:
      
      for _ in range(epochs):
        
        error = abs_error(datax, datay, a, b, c, d)
        a += learning_rate
        derror = abs_error(datax, datay, a, b, c, d)
        
        slope = derror - error
        a -= learning_rate
        
        # if gradient descent is increasing error, break
        if goingdown and goingup:
          break
        
        # positive gradient
        if slope > 0:
          a -= learning_rate
          goingdown = True
          
        # positive gradient
        elif slope < 0:
          a += learning_rate
          goingup = True
    
    if mode % 100 == 0 and debug:
      print(f"Training   | {round(a,3):6} | {round(b,3):6} | {round(c,3):6} | {round(d,3):6} | Error {round(error,3):6} | Epoch {round(mode)}") 
  
  return a, b, c, d

# constants
if __name__ == "__main__":
    
  A=random.randrange(-2,2) * 1
  B=random.randrange(-25,25) * 1
  C=random.randrange(-25,25) * 1
  D=random.randrange(-25,25)* 1
  RANDOMNESS = 1

  np.random.seed(0) 
  DATAX = np.sort(np.random.rand(50) * 10)
  DATAY = A*DATAX**3 + B*DATAX**2 + C*DATAX + D + np.random.randn(50)*RANDOMNESS

  # Main ==========================

  a, b, c, d = polynomial_regression(DATAX,DATAY,2000,0.0001,1000,True)
  print(f"Validating | {round(A,3):6} | {round(B,3):6} | {round(C,3):6} | {round(D,3):6} |")

  # plotting scatter and the line
  matplotlib.pyplot.scatter(DATAX, DATAY)
  matplotlib.pyplot.plot(DATAX, a*DATAX**3 + b*DATAX**2 + c*DATAX + d, color="black")
  #matplotlib.pyplot.plot(DATAX, A*DATAX**3 + B*DATAX**2 + C*DATAX + D, color="red")

  # texts
  matplotlib.pyplot.xlabel("X")
  matplotlib.pyplot.ylabel("Y")
  matplotlib.pyplot.title("manual polynomial regression", loc='center', fontsize=20)

  # show
  matplotlib.pyplot.show()