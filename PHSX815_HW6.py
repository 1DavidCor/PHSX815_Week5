# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 19:47:23 2021

@author: d338c921
"""

import sys
import numpy as np
import matplotlib.pyplot as plt

# - Choose a function on a closed interval (the function *cannot* be a low order polynomial, but need not be too complicated). Choose a function that you can calculate the integral for analytically.

# - Implement *two different* numerical integration methods, one with fixed interval sizes, one with Gaussian quadrature, to integrate this function. These don't need to be of very high order. You should write your code such that you can change the number of sub-intervals (and number of evaluation points).

# - Compare the difference between the two numerical integrals, and their difference with the correct/analytic answer, as a function of the number sub-intervals. Is the difference between the two estimates a good indicator of the actual error?

### NUMERICAL INTEGRATION ###
#x = np.linspace(0, 25, 1000)
#f = np.sqrt(x) #use the function f(x) = sqrt(x) on the closed interval [0, 25]
#Indefinite Integral = (2/3)x**(3/2) + C
#Definite integral on [0, 25] = 250/3 = 83.3333

# Number of sub-intervals from user input
if '-num_intervals' in sys.argv:
    p = sys.argv.index('-num_intervals')
    num_intervals = int(sys.argv[p+1])
    
# Number of evaluation points (for Gaussian quadrature) from user input
if '-num_evals' in sys.argv:
    p = sys.argv.index('-num_evals')
    num_evals = int(sys.argv[p+1])

### Method 1: Trapezoid Rule

#Integrate!!! Define a function:

def integrate_trap(num_intervals):
    #initialize "integral" i.e. sum of trapezoid areas
    integral = 0
    for i in range(1, num_intervals):
        #interval size h
        h = 25 / num_intervals
        f0 = np.sqrt(h* (i - 1))
        f1 = np.sqrt(h * i)
        trap = 0.5 * h * (f0 + f1)
        integral = integral + trap
  
    return integral

# Repeat for different number of sub-intervals???    
integral_arr = []   
for j in range(1, num_intervals + 1): 
    integral = integrate_trap(j)
    integral_arr = np.append(integral_arr, integral)

#print(integral_arr)


### Method 2: Gaussian Quadrature

def integral_gauss_quad(num_evals):
    #before using gaussian quadrature rules, we must change the interval from [0, 25] to [-1, 1]
    #int sqrt(x) on the closed interval [0, 25] becomes int 25/2 * sqrt(25x/2 + 25/2) dx; THIS = f(x_i) in approx.
    #introduce Chebyshev weight funciton to use Chebyshev-Gauss quadrature approximation: w(x) = (1-x^2)^(-1/2)
    #This integral is then approximated by sum from i = 1 to n of 2)(w_i * f(x_i)) where x_i = cos((2i - 1) / 2n * pi) and w_i = pi/n this is what this function will compute
    
    integral = 0
    
    for i in range(1, num_evals):
        w_i = np.pi / num_evals
        x_i = np.cos((2*i - 1) / (2 * num_evals) * np.pi)
        f_x_i = 25/2 * np.sqrt((25*x_i / 2) + 25/2)
        integral = integral + w_i * f_x_i
        
    return integral

integral_arr_gauss = []   
for j in range(1, num_intervals + 1): 
    integral = integral_gauss_quad(j)
    integral_arr_gauss = np.append(integral_arr_gauss, integral)

#plot integral approx as a function of num_intervals
plt.figure()
plt.title("Numerical Integration: Trapezoid Rule + Chebyshev-Gauss Quadrature")
plt.xlabel("Number of sub-intervals")
plt.ylabel("Calculated Integral Value")
plt.axhline(250/3, color = "g", label = "analytical") #analytical answer
plt.plot(np.linspace(0, num_intervals, integral_arr.size), integral_arr, color = "r", label = "Trapezoid approx") #trapezoid
plt.plot(np.linspace(0, num_intervals, integral_arr.size), integral_arr_gauss, color = "b", label = "Chebyshev-Gauss")
plt.legend()
plt.show()