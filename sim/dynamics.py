import numpy as np


def step_dynamics(x, u, dt):
    """Simple Euler integrator for a 2D double integrator UAV."""
    next_state = x.copy()
    next_state[0:2] = x[0:2] + x[2:4] * dt
    next_state[2:4] = x[2:4] + u * dt
    return next_state
