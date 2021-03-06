# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 16:28:29 2021

@author: d338c921
"""

#Use rejection sampling to sample from a distribution and visulaize the target distribution, proposal distribution, and random samples. Try to do one of the following:
#Choose a non-trivial (not uniform, not piecewise-linear) function defined on the interval [0,1]. Using a uniform distribution (or something better matching target function) sample your target function using rejection sampling. Visualize the results (ideally at each step of the procedure)
#OR Sample random points in a closed 2D or 3D space (NOT just a circle) using rejection sampling and visualize the results. Try to make the density "not uniform" in some way over the domain of points (ex. a 3D sphere of ellipse)

#Option #1:
    
import numpy as np
import matplotlib.pyplot as plt

    
#Choose a non trivial function (f(x) = 4x^4 + 3x^3 + 2x^2 + x); construct it to be plotted later
#f = np.poly1d([4, 3, 2, 1, 0]) ###LAME
#create x (input) array
x = np.linspace(0, 1, 1000)
f = (np.sin(20*x))**2 ### WAY more interesting to look at; if you change f, make sure to ALSO change in the sorting conditional statement LINE 57

#Sample from a uniform distribution; need an x and a y sample over region [0,1] U [0,1]
N = 10000
x_sample = np.random.uniform(0, 1, size = N)
y_sample = np.random.uniform(0, 1, size = N)

#create plot
plt.figure()
plt.title("Rejection Sampling")
plt.xlim(0,1)
plt.ylim(0,1)
plt.xlabel("x")
plt.ylabel("f(x)")
plt.plot(x, f, color = "b", linewidth = 3, label = "f(x)")

#reject/accept
accept = 0 #initiate accept counter

# for i in range(N):
# #Test if a point (x_i, y_i) is less than (x_i, f(x_i)); count # of "accepts"; seperate accepts vs. rejects to be plotted in different colors
#     if (y_sample[i] < f(x_sample[i])):
#         accept = accept + 1 #add one to accept counter for an accept
#         plt.scatter(x_sample[i], y_sample[i], color = "g", marker = ".") #plot accepts in green
#     else:
#         plt.scatter(x_sample[i], y_sample[i], color = "r", marker = ".") #plot rejects in red

###VERY SLOW!!! Maybe if I DON'T plot in a loop...just sort
x_accept = []
y_accept = []
x_reject = []
y_reject = []

for i in range(N):
#Test if a point (x_i, y_i) is less than (x_i, f(x_i)); count # of "accepts"; seperate accepts vs. rejects to be plotted in different colors
    if (y_sample[i] < (np.sin(20 * x_sample[i]))**2):
        accept = accept + 1 #add one to accept counter for an accept
        x_accept = np.append(x_accept, x_sample[i])
        y_accept = np.append(y_accept, y_sample[i])
    else:
        x_reject = np.append(x_reject, x_sample[i])
        y_reject = np.append(y_reject, y_sample[i])

plt.scatter(x_accept, y_accept, color = "g", marker = ".", label = "accepts")
plt.scatter(x_reject, y_reject, color = "r", marker = ".", label = "rejects")
plt.legend()

### Much faster to sort in a loop AND THEN plot

print("Sample Size: N = " + str(N) + "\n")
print("Number of accepts " + str(accept) + "\n")
print("Number of rejects: " + str(N - accept) + "\n")
print("Number of accepts / N : " + str(accept / N) + "\n")
