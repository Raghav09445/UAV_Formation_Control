import matplotlib.pyplot as plt
import numpy as np


def plot_results(
    time,
    positions,
    centers,
    broadcast_counts,
    broadcasts,
    total_broadcasts,
    periodic_broadcasts,
    reduction_percent,
    broadcast_per_step,
):
    N = positions.shape[1]

    fig, axs = plt.subplots(4, 1, figsize=(10, 14))

    for i in range(N):
        axs[0].plot(time, positions[:, i, 0], label=f'UAV {i+1} x')
        axs[0].plot(time, positions[:, i, 1], linestyle='--', label=f'UAV {i+1} y')
    axs[0].set_title('UAV Position Trajectories')
    axs[0].set_xlabel('Time [s]')
    axs[0].set_ylabel('Position [m]')
    axs[0].legend(loc='upper right', fontsize='small')
    axs[0].grid(True)

    for i in range(N):
        axs[1].plot(time, positions[:, i, 0] - centers[:, 0], label=f'UAV {i+1} x error')
        axs[1].plot(time, positions[:, i, 1] - centers[:, 1], linestyle='--', label=f'UAV {i+1} y error')
    axs[1].set_title('Relative Formation Error to Center')
    axs[1].set_xlabel('Time [s]')
    axs[1].set_ylabel('Error [m]')
    axs[1].legend(loc='upper right', fontsize='small')
    axs[1].grid(True)

    axs[2].plot(time, broadcast_per_step, color='tab:orange')
    axs[2].set_title('Number of Broadcasts per Time Step')
    axs[2].set_xlabel('Time [s]')
    axs[2].set_ylabel('Broadcasts')
    axs[2].grid(True)

    axs[3].bar(np.arange(N) + 1, broadcast_counts, color='tab:green')
    axs[3].set_title('Total Broadcast Count Per UAV')
    axs[3].set_xlabel('UAV Index')
    axs[3].set_ylabel('Total Broadcasts')
    axs[3].grid(True)

    plt.tight_layout()
    # plt.show()  # Disabled for Flask backend - use web dashboard instead
    plt.close('all')

    # Broadcast event matrix plot (visualization moved to web dashboard)
    # plt.figure(figsize=(10, 4))
    # plt.imshow(broadcasts.T, aspect='auto', cmap='Greys', interpolation='none')
    # plt.title('Broadcast Event Matrix (UAVs × Time Steps)')
    # plt.xlabel('Time Step')
    # plt.ylabel('UAV Index')
    # plt.colorbar(label='Broadcast (True=1, False=0)')
    # plt.show()

    # Bandwidth comparison plot (visualization moved to web dashboard)
    # plt.figure(figsize=(10, 4))
    # plt.bar(['Periodic', 'DECM'], [periodic_broadcasts, total_broadcasts], color=['gray', 'tab:blue'])
    # plt.title(f'Bandwidth Comparison: {reduction_percent:.1f}% Reduction')
    # plt.ylabel('Total Broadcasts')
    # plt.show()
