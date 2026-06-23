"""
Configuration and system parameters for UAV Formation Control
Dynamic Event-Triggered Communication Mechanism (DECM) + Time-Varying Formation Tracking (TVFT)
"""

import numpy as np

# ============================================================================
# SYSTEM PARAMETERS
# ============================================================================

# Number of UAVs
N_UAVS = 5

# Sampling period (seconds)
T_s = 0.05

# Simulation time (seconds)
T_sim = 50.0

# ============================================================================
# DYNAMIC MODEL (Double Integrator)
# ============================================================================
# ẋᵢ = Axᵢ + Buᵢ + d_i(t)
# where xᵢ = [pos_x, pos_y, vel_x, vel_y]ᵀ (4D state per UAV)

# State-space matrices (Kronecker product: I₂ ⊗ [0,1; 0,0])
A = np.array([
    [0, 0, 1, 0],
    [0, 0, 0, 1],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
], dtype=float)

# Input matrix (I₂ ⊗ [0; 1])
B = np.array([
    [0],
    [0],
    [1],
    [0]
], dtype=float)  # Shape: (4, 1) per UAV

# System is repeated for each UAV independently
# Full augmented system would be (4N) × (4N)

# ============================================================================
# FORMATION TOPOLOGY (5-UAV Pentagon)
# ============================================================================
# Adjacency matrix W (from paper Fig. 1)
# Pentagon: each UAV connected to neighbors
W = np.array([
    [0, 1, 0, 0, 1],
    [1, 0, 1, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 1, 0, 1],
    [1, 0, 0, 1, 0]
], dtype=float)

# Degree matrix D
D = np.diag(np.sum(W, axis=1))

# Laplacian matrix L = D - W
L = D - W

# ============================================================================
# FORMATION REFERENCE (Rotating Pentagon)
# ============================================================================

# Formation radius (meters)
FORMATION_RADIUS = 1.0

# Angular velocity (rad/s)
OMEGA = 0.5

# Center position (moving reference)
# r(t) = [x_c(t), y_c(t)]ᵀ
CENTER_VELOCITY = 0.3  # m/s (constant velocity in x)

# ============================================================================
# EVENT-TRIGGERED CONTROL PARAMETERS
# ============================================================================

# Initial dynamic threshold σ(0)
# Optimized: Higher value = fewer broadcasts initially, but still maintains stability
SIGMA_INIT = 0.7  # Increased from 0.5 for better bandwidth efficiency

# Contraction rate ρ (Eq. 6: σᵢ(kT) contracts as system converges)
# Optimized: Lower value = faster threshold decay = more events as errors reduce
RHO = 0.92  # Decreased from 0.95 for adaptive trigger behavior

# Event trigger threshold η (relative to communication threshold)
ETA_SCALE = 1.0

# Coupling strength for formation cohesion (0-1.0)
# Higher = tighter formation, better inter-UAV coordination
COUPLING_STRENGTH = 0.85  # Increased from 0.5 for tighter geometry

# ============================================================================
# DISTURBANCE PARAMETERS (Enhancement: Optional)
# ============================================================================

# Enable disturbance observer
USE_DISTURBANCE = False

# Wind disturbance amplitude (m/s²)
DISTURBANCE_AMPLITUDE = 0.1

# Wind disturbance period (seconds)
DISTURBANCE_PERIOD = 10.0

# ============================================================================
# ACTUATOR SATURATION (Enhancement: Optional)
# ============================================================================

# Enable actuator saturation
USE_SATURATION = False

# Maximum control input magnitude (m/s²)
U_MAX = 2.0

# ============================================================================
# COMMUNICATION DELAY (Enhancement: Optional)
# ============================================================================

# Enable communication delays
USE_DELAY = False

# Maximum delay (seconds)
TAU_MAX = 0.1

# ============================================================================
# LMI SOLVER PARAMETERS
# ============================================================================

# Feasibility tolerance for cvxpy
LMI_TOLERANCE = 1e-6

# Verbosity of cvxpy solver
LMI_VERBOSE = False

# ============================================================================
# SIMULATION OUTPUT
# ============================================================================

# Save plots to this directory
PLOT_DIR = "./plots"

# Save data to this directory
DATA_DIR = "./data"

# Plotting frequency (plot every N timesteps)
PLOT_FREQ = 10

print("[Config] System initialized:")
print(f"  UAVs: {N_UAVS}")
print(f"  Sampling period: {T_s} s")
print(f"  Simulation time: {T_sim} s")
print(f"  Formation radius: {FORMATION_RADIUS} m")
print(f"  Laplacian eigenvalues: {np.linalg.eigvalsh(L)}")
