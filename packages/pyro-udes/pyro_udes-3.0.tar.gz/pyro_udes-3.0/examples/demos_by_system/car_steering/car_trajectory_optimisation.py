#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 08:27:06 2021

@author: alex
"""

import numpy as np

from pyro.dynamic.vehicle_steering                 import KinematicCarModel
from pyro.planning.trajectoryoptimisation import DirectCollocationTrajectoryOptimisation


sys = KinematicCarModel()

# Constraints
sys.x_ub = np.array([ 10, 2, 1.5])
sys.x_lb = np.array([-10,-1,-1.5])
sys.u_ub = np.array([ 10, 0.5])
sys.u_lb = np.array([-10, -0.5])

# Cost function
sys.cost_function.Q[0,0] = 1
sys.cost_function.Q[1,1] = 1
sys.cost_function.Q[2,2] = 10
sys.cost_function.R[0,0] = 1
sys.cost_function.R[1,1] = 1000

planner = DirectCollocationTrajectoryOptimisation( sys , 0.1, 20)

#PArking
planner.x_start = np.array([-0,1,0])
planner.x_goal  = np.array([ 0,0,0])

planner.maxiter = 1000
# planner.ini
planner.compute_optimal_trajectory()
# planner.show_solution()
planner.animate_solution()

