import numpy as np
from config import params


class DynamicEventTrigger:
    def __init__(self, N, sigma_init, rho, adjacency):
        self.N = N
        self.sigma_init = sigma_init
        self.rho = rho
        self.adjacency = adjacency.astype(float)
        self.step_count = 0
        self.sigmas = np.full(N, sigma_init, dtype=float)

        eigenvalues = np.linalg.eigvals(params.L)
        sorted_eigs = np.sort(np.real(eigenvalues))
        self.lambda2 = float(sorted_eigs[1]) if len(sorted_eigs) > 1 else 1.0

    def update_thresholds(self):
        self.step_count += 1
        self.sigmas = self.sigma_init * (self.rho ** self.step_count)

    def trigger_values(self, errors):
        errors = np.asarray(errors)
        values = np.zeros(self.N, dtype=float)
        for i in range(self.N):
            own_term = np.linalg.norm(errors[i]) ** 2
            neighbor_term = 0.0
            for j in range(self.N):
                if self.adjacency[i, j] > 0.0:
                    neighbor_term += np.linalg.norm(errors[j]) ** 2
            values[i] = own_term + neighbor_term / self.lambda2
        return values

    def check_broadcasts(self, errors):
        values = self.trigger_values(errors)
        broadcasts = values > self.sigmas
        return broadcasts, values
