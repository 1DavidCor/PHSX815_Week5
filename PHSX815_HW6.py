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

#Set help flag to print flags
if '-h' in sys.argv:
    p = sys.argv.index('-h')
    print("Flags:")
    print("-num_intervals [# of intervals for trapezoid rule approx, int]")
    print("-int_bound_l [left integration bound, float]")
    print("-int_bound_r [right integration bound, float]")
    print("-anSol_trap [analytical solution to integral  f(x) from [a, b], float]")
    print("-anSol_cheby [analytical solution to integral f(p)/sqrt(1-p^2) from [-1, 1] where p = (a+b)/2 + ((b-a)/2)*x , float]")
    sys.exit()

# Number of sub-intervals from user input
if '-num_intervals' in sys.argv:
    p = sys.argv.index('-num_intervals')
    num_intervals = int(sys.argv[p+1])
    
### Method 1: Trapezoid Rule

#set integration bounds from user input
if '-int_bound_l' in sys.argv:
    p = sys.argv.index('-int_bound_l')
    a = float(sys.argv[p+1])
    
if '-int_bound_r' in sys.argv:
    p = sys.argv.index('-int_bound_r')
    b = float(sys.argv[p+1])

#Write out the analytical solutions
if '-anSol_trap' in sys.argv:
    p = sys.argv.index('-anSol_trap')
    anSol_trap = float(sys.argv[p+1])
    
if '-anSol_cheby' in sys.argv:
    p = sys.argv.index('-anSol_cheby')
    anSol_cheby = float(sys.argv[p+1])
    

#anSol_cheby = 3*np.pi/2. #analytical solution for chebyshev-gauss quadrature i.e. int f(p)/sqrt(1-p^2) from [-1, 1] p = (a+b)/2 + ((b-a)/2)*x (change of variables using bounds [a, b])
#anSol_trap = 2. #analytical solution for integral of f(x) from [a, b]

#Integrate!!! Define a function:
def func(x):
    return x*x*x + 3*x*x

def integrate_trap(num_intervals):
    #initialize "integral" i.e. sum of trapezoid areas
    integral = 0
    for i in range(1, num_intervals+1):
        #interval size h
        h = (b-a) / num_intervals
        f0 = func(a + h* (i - 1))
        f1 = func(a + h * i)
        trap = (f0 + f1)
        integral = integral + trap
    return (h/2)*integral

# Repeat for different number of sub-intervals 
integral_arr = []   
for j in range(1, num_intervals + 1): 
    integral = integrate_trap(j)
    integral_arr = np.append(integral_arr, integral)

#print(integral_arr)


### Method 2: Gaussian Quadrature

def changeOfInterval(a,b,x):
    return (a+b)/2 + ((b-a)/2)*x


def integral_gauss_quad(num_evals):
    #before using gaussian quadrature rules, we must change the interval from [0, 25] to [-1, 1]
    #int sqrt(x) on the closed interval [0, 25] becomes int 25/2 * sqrt(25x/2 + 25/2) dx; THIS = f(x_i) in approx.
    #introduce Chebyshev weight funciton to use Chebyshev-Gauss quadrature approximation: w(x) = (1-x^2)^(-1/2)
    #This integral is then approximated by sum from i = 1 to n of 2)(w_i * f(x_i)) where x_i = cos((2i - 1) / 2n * pi) and w_i = pi/n this is what this function will compute
    
    integral = 0
    w = np.pi / (num_evals+1)
    for i in range(1, num_evals+2):
       # w_i = np.pi / num_evals
        x_i = -np.cos(((i-1) + 1/2)*np.pi/(num_evals+1))
       # x_i = np.cos((2*(i-1) - 1) / (2 *(num_evals+1)) * np.pi)
#        f_x_i = 25/2 * np.sqrt((25*x_i / 2) + 25/2)
        phi_i = changeOfInterval(a,b,x_i)
        f_x_i = func(phi_i)
        integral = integral + f_x_i
        
    return ((b-a)/2)*w*integral

integral_arr_gauss = []   
for j in range(0, num_intervals+1): 
    integral = integral_gauss_quad(j)
    integral_arr_gauss = np.append(integral_arr_gauss, integral)
    
#plot integral approx as a function of num_intervals
plt.figure()
plt.title("Numerical Integration: Trapezoid Rule + Chebyshev-Gauss Quadrature")
plt.xlabel("Number of sub-intervals")
plt.ylabel("Calculated Integral Value")
plt.axhline(anSol_cheby, color = "b", linestyle='--',label = "analytical chebyshev") #analytical answer
plt.axhline(anSol_trap, color = "r", linestyle='--', label = "analytical trapezoidal") #analytical answer
plt.plot(np.linspace(0, num_intervals, integral_arr.size), integral_arr, color = "r", label = "Trapezoid approx") #trapezoid
plt.plot(np.linspace(0, num_intervals, integral_arr.size+1), integral_arr_gauss, color = "b", label = "Chebyshev-Gauss")
plt.legend()
plt.show()
