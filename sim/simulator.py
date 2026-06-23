import numpy as np
from config import params
from lmi.lmi_solve import solve_event_triggered_lmi
from lmi.controller import compute_reference, compute_input
from sim.dynamics import step_dynamics
from sim.decm import DynamicEventTrigger


def initialize_states():
    states = np.zeros((params.N_UAVS, 4), dtype=float)
    for i in range(params.N_UAVS):
        angle = 2.0 * np.pi * i / params.N_UAVS
        states[i, 0:2] = params.FORMATION_RADIUS * np.array([np.cos(angle), np.sin(angle)])
        states[i, 2:4] = 0.0
    return states


def run_simulation():
    # Use optimized event-triggered LMI for better trajectory smoothness
    K, _ = solve_event_triggered_lmi()
    dt = params.T_s
    steps = int(params.T_sim / dt) + 1

    states = initialize_states()
    last_broadcast_positions = states[:, 0:2].copy()
    estimators = last_broadcast_positions.copy()
    broadcast_counts = np.zeros(params.N_UAVS, dtype=int)

    history_positions = np.zeros((steps, params.N_UAVS, 2), dtype=float)
    history_centers = np.zeros((steps, 2), dtype=float)
    history_event_values = np.zeros((steps, params.N_UAVS), dtype=float)
    history_broadcasts = np.zeros((steps, params.N_UAVS), dtype=bool)

    trigger = DynamicEventTrigger(params.N_UAVS, params.SIGMA_INIT, params.RHO, params.W)

    for step in range(steps):
        t = step * dt
        center = np.array([params.CENTER_VELOCITY * t, 0.0])
        history_centers[step] = center

        errors = states[:, 0:2] - last_broadcast_positions
        broadcasts, values = trigger.check_broadcasts(errors)
        history_event_values[step] = values
        history_broadcasts[step] = broadcasts

        for i in range(params.N_UAVS):
            if broadcasts[i]:
                estimators[i] = states[i, 0:2].copy()
                last_broadcast_positions[i] = states[i, 0:2].copy()
                broadcast_counts[i] += 1

        next_states = states.copy()
        for i in range(params.N_UAVS):
            x_ref = compute_reference(i, t)
            u = compute_input(states[i], x_ref, K, params.W[i], estimators)
            next_states[i] = step_dynamics(states[i], u, dt)

        states = next_states
        history_positions[step] = states[:, 0:2]
        trigger.update_thresholds()

    total_actual_broadcasts = int(history_broadcasts.sum())
    periodic_broadcasts = params.N_UAVS * steps
    reduction_percent = 100.0 * (1.0 - total_actual_broadcasts / periodic_broadcasts)
    average_broadcasts = np.mean(broadcast_counts)
    broadcast_per_step = np.sum(history_broadcasts, axis=1)

    print("Simulation summary:")
    print(f"  Total steps: {steps}")
    print(f"  Periodic broadcast baseline: {periodic_broadcasts}")
    print(f"  DECM actual broadcasts: {total_actual_broadcasts}")
    print(f"  Bandwidth reduction: {reduction_percent:.1f}%")
    print(f"  Average broadcasts per UAV: {average_broadcasts:.1f}")
    print(f"  Average broadcasts per step: {np.mean(broadcast_per_step):.2f}")

    # Note: Plotting removed for Flask compatibility (runs in background thread)
    # All visualization now happens in the browser via dashboard.html + Plotly.js
    
    return history_positions, history_centers, broadcast_counts, history_broadcasts


if __name__ == "__main__":
    run_simulation()
