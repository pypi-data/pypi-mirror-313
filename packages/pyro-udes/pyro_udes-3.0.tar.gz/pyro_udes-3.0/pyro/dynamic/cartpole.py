# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 13:07:39 2018

@author: nvidia
"""
###############################################################################
import numpy as np
###############################################################################
from pyro.dynamic import mechanical
from pyro.dynamic import system
###############################################################################


###############################################################################
        
class RotatingCartPole( mechanical.MechanicalSystem ):
    """ 

    """
    
    ############################
    def __init__(self):
        """ """
               
        # initialize standard params
        mechanical.MechanicalSystem.__init__( self, 2)
        
        # Name
        self.name = 'Rotating Cart Pole'
        
        # dynamic/kinematic params
        self.l1  = 1 
        self.l2  = 1
        
        self.m2  = 1
        
        self.I1 = 1.0
        self.I2 = 0.1
        
        self.gravity = 9.81
        
        self.d1 = 0.1
        self.d2 = 0.1
        
        #plotting params
        self.is_3d = True
        
        
    ##############################
    def trig(self, q ):
        """ 
        Compute cos and sin usefull in other computation 
        ------------------------------------------------
        
        """
        
        c1  = np.cos( q[0] )
        s1  = np.sin( q[0] )
        c2  = np.cos( q[1] )
        s2  = np.sin( q[1] )
        
        return [c1,s1,c2,s2]
        
    
    ###########################################################################
    def H(self, q ):
        """ 
        Inertia matrix 
        ----------------------------------
        dim( H ) = ( dof , dof )
        
        such that --> Kinetic Energy = 0.5 * dq^T * H(q) * dq
        
        """  
        
        [c1,s1,c2,s2] = self.trig( q )
        
        H = np.zeros((2,2))
        
        H[0,0] = self.m2 * self.l1 ** 2 + self.I1
        H[1,0] = self.m2 * self.l1 * self.l2 * c2
        H[0,1] = H[1,0]
        H[1,1] = self.m2 * self.l2 ** 2 + self.I2
        
        return H
    
    
    ###########################################################################
    def C(self, q , dq ):
        """ 
        Corriolis and Centrifugal Matrix 
        ------------------------------------
        dim( C ) = ( dof , dof )
        
        such that --> d H / dt =  C + C^T
        
        
        """ 
        
        [c1,s1,c2,s2] = self.trig( q )
        
        C = np.zeros((2,2))
        
        C[0,0] = 0
        C[1,0] = 0
        C[0,1] = - self.m2 * self.l1 * self.l2 * s2 * dq[1]
        C[1,1] = 0

        return C
    
    ###########################################################################
    def B(self, q ):
        """ 
        Actuator Matrix  : dof x m
        """
        
        B = np.diag( np.ones( self.dof ) ) #  identity matrix
        
        return B
    
    
    ###########################################################################
    def g(self, q ):
        """ 
        Gravitationnal forces vector : dof x 1
        """
        
        [c1,s1,c2,s2] = self.trig( q )
        
        G = np.zeros(2)
        
        G[0] = 0
        G[1] = - self.m2 * self.gravity * self.l2 * s2
        
        return G
    
        
    ###########################################################################
    def d(self, q , dq ):
        """ 
        State-dependent dissipative forces : dof x 1
        """
        
        D = np.zeros((2,2))
        
        D[0,0] = self.d1
        D[1,0] = 0
        D[0,1] = 0
        D[1,1] = self.d2
        
        d = np.dot( D , dq )
        
        return d
    
        
    ###########################################################################
    # Graphical output
    ###########################################################################
    
    ###########################################################################
    def forward_kinematic_domain(self, q ):
        """ 
        """
        l = 2
        
        domain  = [ (-l,l) , (-l,l) , (-l,l) ]#  
                
        return domain
    
    
    ###########################################################################
    def forward_kinematic_lines(self, q ):
        """ 
        Compute points p = [x;y;z] positions given config q 
        ----------------------------------------------------
        - points of interest for ploting
        
        Outpus:
        lines_pts = [] : a list of array (n_pts x 3) for each lines
        
        """
        
        lines_pts = [] # list of array (n_pts x 3) for each lines
        lines_style = []
        lines_color = []
        
        ###############################
        # ground line
        ###############################
        
        pts      = np.zeros(( 5 , 3 ))
        pts[0,:] = np.array([-1,-1,-1])
        pts[1,:] = np.array([-1,+1,-1])
        pts[2,:] = np.array([+1,+1,-1])
        pts[3,:] = np.array([+1,-1,-1])
        pts[4,:] = np.array([-1,-1,-1])
        
        lines_pts.append( pts )
        lines_style.append( '-' )
        lines_color.append( 'k' )
        
        ###########################
        # pendulum kinematic
        ###########################
        
        pts      = np.zeros(( 4 , 3 ))
        
        [c1,s1,c2,s2] = self.trig( q )
        
        pts[0,0] = 0
        pts[0,1] = 0
        pts[0,2] = -1
        
        pts[1,0] = 0
        pts[1,1] = 0
        pts[1,2] = 0
        
        pts[2,0] = self.l1 * s1
        pts[2,1] = -(self.l1 * c1)
        pts[2,2] = 0
        
        pts[3,0] = self.l1 * s1   + self.l2 * s2 * c1
        pts[3,1] = - (self.l1 * c1   - self.l2 * s2 * s1)
        pts[3,2] = 0              + self.l2 * c2

        
        lines_pts.append( pts )
        lines_style.append( 'o-' )
        lines_color.append( 'b' )
                
        return lines_pts , lines_style , lines_color
    
    
    
###############################################################################
        
class UnderActuatedRotatingCartPole( RotatingCartPole ):
    
    ############################
    def __init__(self):
        """ """
        
        # Degree of Freedom
        dof      = 2
        self.dof = dof 
        
        # Dimensions
        n = dof * 2 
        m = 1  
        p = dof * 2
        
        # initialize standard params
        system.ContinuousDynamicSystem.__init__(self, n, m, p)
        
        # Labels, bounds and units
        self.x_ub[0] = + np.pi * 2
        self.x_lb[0] = - np.pi * 2
        self.state_label[0] = 'Angle '+ str(1)
        self.state_units[0] = '[rad]'
        self.x_ub[1] = + np.pi * 2
        self.x_lb[1] = - np.pi * 2
        self.state_label[1] = 'Angle '+ str(2)
        self.state_units[1] = '[rad]'
            
        # joint velocity states
        self.x_ub[2] = + np.pi * 2
        self.x_lb[2] = - np.pi * 2
        self.state_label[2] = 'Velocity ' + str(1)
        self.state_units[2] = '[rad/sec]'
        self.x_ub[3] = + np.pi * 2
        self.x_lb[3] = - np.pi * 2
        self.state_label[3] = 'Velocity ' + str(2)
        self.state_units[3] = '[rad/sec]'
        
        #actuators
        self.u_ub[0] = + 5
        self.u_lb[0] = - 5
        self.input_label[0] = 'Torque ' + str(1)
        self.input_units[0] ='[Nm]'
        
        # Name
        self.name = 'Underactuated Rotating Cart Pole'
        
        # dynamic/kinematic params
        self.l1  = 1 
        self.l2  = 1
        
        self.m2  = 1
        
        self.I1 = 1.0
        self.I2 = 0.1
        
        self.gravity = 9.81
        
        self.d1 = 0.1
        self.d2 = 0.1
        
        #plotting params
        self.is_3d = True
    
    
    ###########################################################################
    def B(self, q ):
        """ 
        Actuator Matrix  : dof x m
        """
        
        B = np.zeros((2,1))
        
        B[0] = 1
        B[1] = 0
        
        return B
   
    
   
###############################################################################
### Linear Cartpole
###############################################################################
    
class CartPole(mechanical.MechanicalSystem):
    """ Cart with unactuated pole.
    Attributes
    ----------
    l (float): Length of pole rod. Only used for display.
    lcg (float): Distance to center of gravity pole.
    m1 (float): Mass of the cart.
    m2 (float): Mass of the pole (point mass at center of gravity).
    
    Author: Jean-Gabriel Mercier , Winter 2023
    """
    
    ###########################################################################
    def __init__(self):
        
        mechanical.MechanicalSystem.__init__(self, dof=2, actuators=1)
        
        self.name = 'Cart Pole'
        
        self.state_label[0] = 'x'
        self.state_label[2] = 'dx'
        self.state_units[0] = '[m]'
        self.state_units[2] = '[m/s]'
        
        self.input_label[0] = 'F'
        self.input_units[0] = '[N]'
        
        self.u_lb[0] = -10
        self.u_ub[0] = +10
        
        # kinematic
        self.l = 3
        self.lcg = 0.5

        # dynamic
        self.m1 = 1
        self.m2 = 0.1
        self.gravity = 9.81
        
        
    ###########################################################################
    def trig(self, q):
        
        return [np.cos(q), np.sin(q)]
    
    
    ###########################################################################
    def H(self, q):
        """
        Inertia matrix -> dim( H ) = ( dof , dof ), such that --> Kinetic Energy = 0.5 * dq^T * H(q) * dq
        ----------------------------------
        """
        
        H = np.zeros((self.dof, self.dof))
        
        theta = q[1]
        
        H[0, 0] = self.m1 + self.m2
        H[1, 0] = self.m2 * self.lcg * np.cos(theta)
        H[0, 1] = H[1, 0]
        H[1, 1] = self.m2 * self.lcg ** 2
        
        return H
    
    
    ###########################################################################
    def C(self, q, dq):
        """
        Corriolis and Centrifugal Matrix -> dim( C ) = ( dof , dof ) such that --> d H / dt =  C + C^T
        ------------------------------------
        """
        
        theta = q[1]
        theta_dot = dq[1]
        
        C = np.zeros((self.dof, self.dof))
        
        C[0, 1] = -self.m2 * self.lcg * np.sin(theta) * theta_dot
        
        return C
    
    
    ###########################################################################
    def B(self, q):
        # Actuator Matrix  : dof x m
        
        B = np.zeros((self.dof, 1))
        
        B[0] = 1
        
        return B
    
    ###########################################################################
    def g(self, q):
        # Gravitationnal forces vector : dof x 1
        
        g = np.zeros(self.dof)
        theta = q[1]
        [c1, s1] = self.trig(theta)
        
        # theta = 0 pointing downward, incrementing anti-clockwise,
        # to map it theta = 0 pointing upward, incrementing clockwise
        # sin(pi - (-theta)) = sin(-theta) = -sin(theta)
        
        g[1] = self.m2 * self.gravity * self.lcg * s1
        
        return g
    
    
    ###########################################################################
    def d(self, q, dq):
        # State-dependent dissipative forces : dof x 1
        
        d = np.zeros(self.dof)
        
        return d
    

    ###########################################################################
    # Graphical output
    ###########################################################################
    
    def forward_kinematic_domain(self, q):
        l = 5
        return [(-l, l), (-l, l), (-l, l)]
    
    
    ###########################################################################
    def forward_kinematic_lines(self, q):
        """
        Compute points p = [x;y;z] positions given config q
        ----------------------------------------------------
        - points of interest for ploting
        Outpus:
        lines_pts = [] : a list of array (n_pts x 3) for each lines
        """

        lines_pts = []  # list of array (n_pts x 3) for each lines
        lines_style = []
        lines_color = []

        # ground line
        pts = np.zeros((2, 3))
        pts[0, :] = np.array([-10, 0, 0])
        pts[1, :] = np.array([+10, 0, 0])

        lines_pts.append(pts)
        lines_style.append('--')
        lines_color.append('k')

        # cart
        cart_length = 2.5
        cart_heigth = 1.5
        pts = np.zeros((5, 3))
        pts[0, :] = np.array([q[0] - cart_length/2, 0, 0])
        pts[1, :] = np.array([q[0] - cart_length/2, cart_heigth, 0])
        pts[2, :] = np.array([q[0] + cart_length/2, cart_heigth, 0])
        pts[3, :] = np.array([q[0] + cart_length/2, 0, 0])
        pts[4, :] = np.array([q[0] - cart_length/2, 0, 0])
        lines_pts.append(pts)
        lines_style.append('-')
        lines_color.append('k')

        # wheels
        pts = np.zeros((2, 3))
        pts[0, :] = np.array([q[0] - cart_length / 4, 0, 0])
        pts[1, :] = np.array([q[0] + cart_length / 4, 0, 0])
        lines_pts.append(pts)
        lines_style.append('o-')
        lines_color.append('k')

        # pendulum
        pts = np.zeros((2, 3))
        pts[0, :] = np.array([q[0], cart_heigth/2, 0])
        [c1, s1] = self.trig(q[1])
        pts[1, :] = pts[0, :] + np.array([s1 * self.l, -c1 * self.l, 0])
        lines_pts.append(pts)
        lines_style.append('o-')
        lines_color.append('b')

        return lines_pts, lines_style, lines_color

    ###########################################################################
    def forward_kinematic_lines_plus(self, x, u, t):
        
        # Display force
        lines_pts = []  # list of array (n_pts x 3) for each lines
        lines_style = []
        lines_color = []

        # Force
        f = u[0]  # Force amplitude
        f_pos = (f > 0)
        max_amplitude = 10.0 / self.u_ub[0]
        cart_length = 2.5
        cart_heigth = 1.5

        if abs(f) > (self.u_ub[0] * 0.02):
            pts = np.zeros((2, 3))
            if f_pos:
                # Draw line
                pts[1, :] = np.array([x[0] - cart_length / 2, cart_heigth/2, 0])
                pts[0, :] = np.array([x[0] - cart_length / 2 - f * max_amplitude, cart_heigth/2, 0])
            else:
                # Draw line
                pts[0, :] = np.array([x[0] + cart_length / 2, cart_heigth / 2, 0])
                pts[1, :] = np.array([x[0] + cart_length / 2 - f * max_amplitude, cart_heigth / 2, 0])

            lines_pts.append(pts)
            lines_style.append('-')
            lines_color.append('r')

            # Draw Arrow
            pts = np.zeros((3, 3))
            if f_pos:
                pts[1, :] = np.array([x[0] - cart_length / 2, cart_heigth/2, 0])
                pts[0, :] = pts[1, :] + [-0.1,0.1,0]
                pts[2, :] = pts[1, :] + [-0.1,-0.1,0]
            else:
                pts[1, :] = np.array([x[0] + cart_length / 2, cart_heigth / 2, 0])
                pts[0, :] = pts[1, :] + [0.1,0.1,0]
                pts[2, :] = pts[1, :] + [0.1,-0.1,0]

            lines_pts.append(pts)
            lines_style.append('-')
            lines_color.append('r')

        else:

            pts = np.zeros((3, 3))

            lines_pts.append(pts)
            lines_style.append('-')
            lines_color.append('r')

            lines_pts.append(pts)
            lines_style.append('-')
            lines_color.append('r')

        return lines_pts, lines_style, lines_color
    

##############################################################################
        
        
        
'''
#################################################################
##################          Main                         ########
#################################################################
'''


if __name__ == "__main__":     
    """ MAIN TEST """
    
    sys = UnderActuatedRotatingCartPole()
    sys.x0 = np.array([0,0.1,0,0])
    #sys.show3(np.array([0.3,0.2]))
    ani1 = sys.animate_simulation( is_3d = True)
    
    sys2 = CartPole()
    sys2.x0      = np.array([0,0.1,0,0])
    sys2.ubar[0] = 2.0
    #sys.show3(np.array([0.3,0.2]))
    ani2 = sys2.animate_simulation()