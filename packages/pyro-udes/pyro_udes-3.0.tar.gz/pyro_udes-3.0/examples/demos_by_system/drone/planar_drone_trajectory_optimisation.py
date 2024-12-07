#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 08:27:06 2021

@author: alex
"""

import numpy as np

from pyro.dynamic.drone                   import Drone2D
from pyro.planning.trajectoryoptimisation import DirectCollocationTrajectoryOptimisation


sys = Drone2D()

sys.u_ub = np.array([10.0, 10.0])

planner = DirectCollocationTrajectoryOptimisation( sys )

planner.x_start = np.array([-5,0,0,0,0,0])
planner.x_goal  = np.array([0,0,0,0,0,0])

planner.maxiter = 200
planner.init_dynamic_plot()
planner.compute_optimal_trajectory()
# planner.show_solution()
planner.animate_solution()

