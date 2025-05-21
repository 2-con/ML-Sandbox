"""DOCSTRING
made in 15/3/2025 (d/m/y)

To do list:

 -

Notes:



"""

# imports

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# functions

def abs_error_3d(datax1, datax2, datay, a, b, c):
  error = 0

  for item in range(len(datax1)):
    error += abs(datay[item] - (a * datax1[item] + b * datax2[item] + c))

  return error/len(datax1)

def linear_regression_3d(datax1, datax2, datay, epochs, learning_rate, bias_multiplier, debug=False):

  a=0
  b=0
  c=0

  goingdown_a = False
  goingup_a = False
  goingdown_b = False
  goingup_b = False
  goingdown_c = False
  goingup_c = False

  error = 0
  derror = 0
  slope = 0

  mode = 0

  for _ in range(epochs):
    mode += 1
    goingdown_a = False
    goingup_a = False
    goingdown_b = False
    goingup_b = False
    goingdown_c = False
    goingup_c = False

    if mode % 3 == 0:
      for _ in range(epochs):
        error = abs_error_3d(datax1, datax2, datay, a, b, c)
        c += learning_rate * bias_multiplier
        derror = abs_error_3d(datax1, datax2, datay, a, b, c)

        slope = derror - error
        c -= learning_rate * bias_multiplier

        if goingdown_c and goingup_c:
          break

        if slope > 0:
          c -= learning_rate * bias_multiplier
          goingdown_c = True
        elif slope < 0:
          c += learning_rate * bias_multiplier
          goingup_c = True

    elif mode % 3 == 1:
      for _ in range(epochs):
        error = abs_error_3d(datax1, datax2, datay, a, b, c)
        a += learning_rate
        derror = abs_error_3d(datax1, datax2, datay, a, b, c)

        slope = derror - error
        a -= learning_rate

        if goingdown_a and goingup_a:
          break

        if slope > 0:
          a -= learning_rate
          goingdown_a = True
        elif slope < 0:
          a += learning_rate
          goingup_a = True

    else:
      for _ in range(epochs):
        error = abs_error_3d(datax1, datax2, datay, a, b, c)
        b += learning_rate
        derror = abs_error_3d(datax1, datax2, datay, a, b, c)

        slope = derror - error
        b -= learning_rate

        if goingdown_b and goingup_b:
          break

        if slope > 0:
          b -= learning_rate
          goingdown_b = True
        elif slope < 0:
          b += learning_rate
          goingup_b = True

    if mode % 100 == 0 and debug:
      print(f"Training   | {round(a,3):6} | {round(b,3):6} | {round(c,3):6} | Error {round(error,3):6} | Epoch {round(mode)}")

  return a, b, c

# constants

np.random.seed(42)
n_samples = 50
DATAX1 = np.sort(np.random.rand(n_samples) * 10)
DATAX2 = np.sort(np.random.rand(n_samples) * 10)
DATAY = 2 * DATAX1 + 3 * DATAX2 + 5 + np.random.randn(n_samples) * 5

# Main ==========================

a, b, c = linear_regression_3d(DATAX1, DATAX2, DATAY, 1000, 0.0001, 1000, True)

# plotting scatter 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(DATAX1, DATAX2, DATAY, color='black')

# Create a meshgrid for the regression plane
x1_range = np.linspace(min(DATAX1), max(DATAX1), 10)
x2_range = np.linspace(min(DATAX2), max(DATAX2), 10)
X1, X2 = np.meshgrid(x1_range, x2_range)
Y = a * X1 + b * X2 + c
ax.plot_surface(X1, X2, Y, color='red', alpha=0.5)

# texts
ax.set_xlabel("X1")
ax.set_ylabel("X2")
ax.set_zlabel("Y")
ax.set_title("3D Linear Regression", loc='center', fontsize=20, y=1.09)

# show
plt.show()