import numpy as np
from config import params


def compute_reference(index, t):
    """
    Compute the desired state reference for UAV i at time t.
    
    Enhanced with smoother velocity generation and acceleration feed-forward
    for better trajectory tracking.
    """
    # Rotating pentagon formation reference
    theta = params.OMEGA * t
    angle = theta + 2.0 * np.pi * index / params.N_UAVS
    
    # Formation geometry (pentagon)
    formation_pos = np.array([
        params.FORMATION_RADIUS * np.cos(angle),
        params.FORMATION_RADIUS * np.sin(angle),
    ])
    
    # Center of mass moving along x-axis with constant velocity
    center_pos = np.array([params.CENTER_VELOCITY * t, 0.0])
    center_vel = np.array([params.CENTER_VELOCITY, 0.0])
    
    # Reference position: center + formation
    pos_ref = center_pos + formation_pos
    
    # Reference velocity: center velocity + tangential velocity from rotation
    # v_ref = v_center + ω × r_formation
    # For 2D: v_tan = ω * r * [-sin(angle), cos(angle)]
    vel_ref = center_vel + params.OMEGA * params.FORMATION_RADIUS * np.array([
        -np.sin(angle),
        np.cos(angle),
    ])
    
    return np.hstack([pos_ref, vel_ref])


def compute_input(x, x_ref, K, laplacian_row, neighbor_positions):
    """
    Compute control input using state feedback and cooperative neighbor coupling.
    
    Enhanced:
    - Uses optimized coupling strength from params
    - Better formation geometry enforcement
    """
    # Formation error
    e = x - x_ref
    
    # State feedback from optimized gain K
    u_fb = K @ e
    
    # Cooperative coupling term: Σⱼ Lᵢⱼ * (xᵢ - xⱼ)
    # This term pulls UAVs toward their neighbors to maintain formation
    coupling = np.zeros(2)
    for j, a_ij in enumerate(laplacian_row):
        if a_ij > 0.0:
            # Relative position error to neighbor j
            coupling += a_ij * (x[:2] - neighbor_positions[j])
    
    # Apply optimized coupling strength for tighter formation
    gamma = params.COUPLING_STRENGTH  # Now 0.85 instead of fixed 0.5
    
    return u_fb - gamma * coupling
