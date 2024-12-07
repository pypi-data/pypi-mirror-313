# -*- coding: utf-8 -*-
"""
Created on Sun May 12 16:34:44 2019

@author: Alexandre
"""

###############################################################################
import numpy as np
###############################################################################
from pyro.dynamic  import manipulator
from pyro.control  import nonlinear
###############################################################################

sys = manipulator.TwoLinkManipulator()

ctl  = nonlinear.ComputedTorqueController( sys )

# Target
ctl.rbar = np.array([0,0])

closed_loop_robot = ctl + sys
    
closed_loop_robot.x0 = np.array([3.14,+1,0,0])
    
closed_loop_robot.compute_trajectory( 5 )
closed_loop_robot.plot_trajectory('x')
closed_loop_robot.plot_trajectory('u')
closed_loop_robot.animate_simulation()