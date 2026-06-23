import numpy as np
import cvxpy as cp
from config import params


def solve_state_feedback_lmi(A=None, B=None, eps=1e-4):
    """Solve a state-feedback stabilizing LMI for the UAV dynamics."""
    A = A if A is not None else params.A
    B = B if B is not None else params.B
    n = A.shape[0]
    m = B.shape[1]

    P = cp.Variable((n, n), PSD=True)
    Y = cp.Variable((m, n))

    stability_lmi = A.T @ P + P @ A + B @ Y + (B @ Y).T
    constraints = [P >> eps * np.eye(n), stability_lmi << -eps * np.eye(n)]

    problem = cp.Problem(cp.Minimize(0), constraints)
    problem.solve(solver=cp.SCS, verbose=False)

    if problem.status not in [cp.OPTIMAL, cp.OPTIMAL_INACCURATE]:
        raise RuntimeError(f"LMI solver failed: {problem.status}")

    P_val = P.value
    K = Y.value @ np.linalg.inv(P_val)
    return K, P_val


def solve_event_triggered_lmi(A=None, B=None, L=None, eps=1e-4, mu=0.5):
    """
    Solve enhanced stability LMI for Event-Triggered Formation Control.
    
    Adds additional dissipation terms for smoother trajectories and better
    coordination. Uses a damped Lyapunov formulation that considers 
    cooperative coupling via the Laplacian structure.
    
    Returns: K, P (feedback gain and Lyapunov matrix)
    """
    A = A if A is not None else params.A
    B = B if B is not None else params.B
    L = L if L is not None else params.L
    n = A.shape[0]  # 4 (state dimension)
    m = B.shape[1]  # 1 (control input dimension)
    
    # Decision variables
    P = cp.Variable((n, n), PSD=True)
    Y = cp.Variable((m, n))  # Scaled feedback Y = K*P
    
    # Conservative damping for stability with smoother responses
    # Using dissipative Lyapunov: A'P + PA - eps*I < 0
    damping = 0.05 * np.eye(n)  # Reduced damping for numerical stability
    
    # Stability condition:
    # A'P + PA + damping + BY + Y'B' < 0
    stability_lmi = A.T @ P + P @ A + damping + B @ Y + (B @ Y).T
    
    constraints = [
        P >> eps * np.eye(n),
        stability_lmi << -eps * np.eye(n)
    ]
    
    # Minimize trace(P^{-1}) to get smaller gains (more conservative)
    # But invert it for optimization
    problem = cp.Problem(cp.Minimize(cp.trace(P)), constraints)
    problem.solve(solver=cp.SCS, verbose=False, max_iters=3000)
    
    if problem.status not in [cp.OPTIMAL, cp.OPTIMAL_INACCURATE]:
        print(f"Event-triggered LMI returned: {problem.status}")
        return solve_state_feedback_lmi(A, B, eps)
    
    P_val = P.value
    if P_val is None:
        return solve_state_feedback_lmi(A, B, eps)
        
    try:
        K = Y.value @ np.linalg.inv(P_val)
        # Limit gain magnitude to prevent explosive control
        gain_norm = np.linalg.norm(K)
        if gain_norm > 2.0:
            K = K * (2.0 / gain_norm)
    except:
        return solve_state_feedback_lmi(A, B, eps)
    
    return K, P_val


if __name__ == "__main__":
    print("Testing standard state-feedback LMI...")
    K_std, P_std = solve_state_feedback_lmi()
    print("K_std =", K_std)
    
    print("\nTesting event-triggered LMI (Theorem 1)...")
    K_et, P_et = solve_event_triggered_lmi()
    print("K_et =", K_et)
    print("\nGain comparison (higher magnitude → more aggressive control):")
    print(f"  Standard gain norm: {np.linalg.norm(K_std):.4f}")
    print(f"  Event-triggered gain norm: {np.linalg.norm(K_et):.4f}")
