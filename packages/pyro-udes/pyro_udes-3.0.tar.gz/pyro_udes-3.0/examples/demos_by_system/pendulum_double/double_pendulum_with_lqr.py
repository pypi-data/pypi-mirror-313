#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 11:51:18 2020

@author: alex
"""

import numpy as np

from pyro.dynamic.pendulum      import DoublePendulum
from pyro.analysis.costfunction import QuadraticCostFunction
from pyro.dynamic.statespace    import linearize
from pyro.control.lqr           import synthesize_lqr_controller


# Non-linear model
sys = DoublePendulum()
    
# Linear model
ss  = linearize( sys , 0.01 )

# Cost function
cf  = QuadraticCostFunction.from_sys( sys )
cf.R[0,0] = 1000
cf.R[1,1] = 10000

# LQR controller
ctl = synthesize_lqr_controller( ss , cf )

# Simulation Closed-Loop Non-linear with LQR controller
cl_sys = ctl + sys
cl_sys.x0 = np.array([0.4,0,0,0])
cl_sys.compute_trajectory()
cl_sys.plot_trajectory('xu')
cl_sys.animate_simulation()