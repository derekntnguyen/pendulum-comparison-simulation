#  -*- coding: utf-8 -*-
'''
P3 Assignment
Derek Nguyen
Created: 2019-02-11
Modified: 2019-02-11
Due: 2019-02-11
'''

# %% codecell
#P3

import numpy as np
import scipy.integrate as integrate
import matplotlib # used to create interactive plots in the Hydrogen package of the Atom IDE
matplotlib.use('Qt5Agg') # used to create interactive plots in the Hydrogen package of the Atom IDE
import matplotlib.pyplot as plt


def pendulum(thetaZero = 30, damp = 0, timeSpan = 20, length = 0.45, gravity = 9.80, wZero = 0):
    '''
    Pendulum Comparison Simulation of a Simple and Real Pendulum
    Uses solve_ivp to integrate a numerical solution for the two first-order ODEs
    Parameter values for the generator depend on the specified:
    thetaZero, float
    damp, float > 0
    timeSpan, float > 0
    length, float > 0
    gravity, float > 0
    wZero, float
    Derek Nguyen
    Created: 02/11/2020
    Last revised: 02/11/2020
    '''
#  Establish Animation time span
    refreshRate = 60 # Hz
    runTimeStep = 1/refreshRate # seconds
    realTimeStep = runTimeStep

    t = np.arange(0, timeSpan, realTimeStep) # t0 and tf in seconds

# Check to ensure that damp, timeSpan, length, and gravity are all positive floats
    if damp < 0:
        raise Exception('Error - damp is a negative value')
    elif damp >= 0:
        pass
    else:
        raise Exception('Error - damp is not a float')

    if timeSpan < 0:
        raise Exception('Error - timeSpan is a negative value')
    elif timeSpan >= 0:
        pass
    else:
        raise Exception('Error - timeSpan is not a float')

    if length < 0:
        raise Exception('Error - length is a negative value')
    elif length >= 0:
        pass
    else:
        raise Exception('Error - length is not a float')

    if gravity < 0:
        raise Exception('Error - gravity is a negative value')
    elif gravity >= 0:
        pass
    else:
        raise Exception('Error - gravity is not a float')

# Convert degrees to radians for variables thetaZero and wZero
    thetaZero_rads = np.radians(thetaZero)
    wZero_rads = np.radians(wZero)

# Calculate the Analytical Solution
    sol_analytical = thetaZero_rads * np.cos(np.sqrt(gravity/length) * t)

# Calculate the Numerical Solution with Jacobian using solve_ivp
    def dydt(t,theta):
        dy = np.array((theta[1], -damp * theta[1] - gravity/length * np.sin(theta[0])))
        return dy
    def jacob(t,theta):
        jacobian = np.array([[0,1],[-np.cos(theta),0]])

    sol_numerical = integrate.solve_ivp(fun = dydt, t_span = [np.min(t), np.max(t)], y0 = [thetaZero_rads, wZero_rads], t_eval = t, jac = jacob)

    theta1 = sol_numerical.y[0,:]

# Plot the Animation of a moving ball and rod utilzing point, and line, and a forloop utilizing the set_data function
    x_analytical = length * np.sin(sol_analytical)
    y_analytical = -length * np.cos(sol_analytical)
    x_numerical = length * np.sin(theta1)
    y_numerical = -length * np.cos(theta1)


    plt.cla() # clear current axes
    plt.axes(xlim = (-2*length,2*length), ylim = (-2*length,length)) # draw x and y limits

    pointa, = plt.plot([], [], 'ro', label = 'Simple')
    pointn, = plt.plot([], [], 'bo', label = 'Real')

    linea, = plt.plot([], [], 'r-', lw = 1)
    linen, = plt.plot([], [], 'b', lw = 1)

    plt.title('Comparing Motions of a Simple and Real Pendulum')
    plt.xlabel('Horizontal Position (m)')
    plt.ylabel('Vertical Position (m)')
    plt.legend()

    for xapoint, yapoint, xnpoint, ynpoint in zip(x_analytical, y_analytical, x_numerical, y_numerical): # forloop to create the animation of moving pendulums
        pointa.set_data(xapoint, yapoint)
        pointn.set_data(xnpoint, ynpoint)
        linea.set_data([0, xapoint], [0, yapoint])
        linen.set_data([0, xnpoint], [0, ynpoint])

        plt.pause(runTimeStep)
