"""DOCSTRING
made in 15/3/2025 (d/m/y)

To do list:

 -

Notes:



"""

# imports

import matplotlib.pyplot as plt
import numpy as np

# functions

def abs_error(datax, datay, a, b):
  error = 0

  for item in range(len(datax)):
    error += abs(datay[item] - (1 / (1 + 2.71828**( -a*(datax[item]-b) ))))

  return error/len(datax)

def logistic_regression(datax, datay, epochs, learning_rate, bias_multiplier, debug=False):

  # (1 / (1 + 2.71828**(-a(datax-b)))) | sigmoid
  a=0
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
      for _ in range(epochs):
        error = abs_error(datax, datay, a, b)
        b += learning_rate*bias_multiplier
        derror = abs_error(datax, datay, a, b)

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
      for _ in range(epochs):
        error = abs_error(datax, datay, a, b)
        a += learning_rate
        derror = abs_error(datax, datay, a, b)

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
      print(f"Training   | {round(a,3):6} | {round(b,3):6} | Error {round(error,3):6} | Epoch {round(mode)}")

  return a, b

# constants

if __name__ == "__main__":
  
  np.random.seed(42)  # For reproducibility
  n_samples = 20
  DATAX = np.array([1,2,3,4,5,6,7,8,9,10])
  DATAY = np.array([0,0,0,0,0,1,1,1,1,1])

  VISUALIZER = []

  count = 0
  while count<len(DATAX):
    VISUALIZER.append(count)
    count += 0.1

  FINAL_VISUALIZER = np.array(VISUALIZER)

  # Main ==========================

  a, b = logistic_regression(DATAX, DATAY, 200, 0.0001, 1000, True)

  # plotting scatter
  plt.scatter(DATAX, DATAY, color='black')  # Plot using only the first feature
  plt.plot(FINAL_VISUALIZER, (1 / (1 + 2.71828**( -a*( FINAL_VISUALIZER - b) ))), color='black') # replace [FINAL_VISUALIZER] with [DATAX] so it uses the same graphing format as the rest

  # texts
  plt.xlabel("X")
  plt.ylabel("Y")
  plt.title("logistic regression", loc='center', fontsize=20, y=1.09)

  # show
  plt.show()