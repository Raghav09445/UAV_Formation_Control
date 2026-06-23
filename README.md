# UAV Formation Control — Dynamic Event-Triggered Communication

Roadmap for **Dynamic Event-Triggered Communication Mechanism (DECM) + Time-Varying Formation Tracking (TVFT)** for multi-agent UAV systems.

## Project Overview



### What This Does
- **5 UAVs** maintain a rotating pentagon formation (radius 1 m)
- **Formation tracks** a moving center (0.3 m/s constant velocity)
- **DECM mechanism** reduces communication bandwidth by ~50% vs. periodic sampling
- **Proven Lyapunov stability** via Linear Matrix Inequalities (LMI)

### Key Innovation
Instead of broadcasting every 50 ms (periodic), each UAV broadcasts **only when a dynamic threshold is crossed**. The threshold itself shrinks over time as the formation converges, balancing performance and communication load.

---

## Project Structure

```
UAV formation/
├── config/                 # System parameters and configuration
│   ├── params.py          # Main config file (num UAVs, sampling rate, etc.)
│   └── __init__.py
├── lmi/                    # LMI solver and controller design
│   ├── lmi_solve.py       # Formulate and solve the LMI (Theorem 1)
│   ├── controller.py      # Controller implementation
│   └── __init__.py
├── sim/                    # Simulation engine
│   ├── simulator.py       # Main simulation loop
│   ├── dynamics.py        # UAV dynamics (double integrator + DECM)
│   ├── decm.py            # Event-triggered mechanism
│   └── __init__.py
├── plots/                  # Post-processing and visualization
│   ├── plotter.py         # Generate figures (formation, bandwidth, convergence)
│   └── __init__.py
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── PHASE_1_TASKS.md       # Phase 1 checklist (theory foundation)
```

---



---

## Getting Started

### 1. Set Up Python Environment

```powershell
cd C:\Users\Username\UAV formation
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Verify Installation

```python
python -c "from config import params; print(params.N_UAVS, params.L)"
```

Should output:
```
5
[[ 2. -1.  0.  0. -1.]
 [-1.  2. -1.  0.  0.]
 [ 0. -1.  2. -1.  0.]
 [ 0.  0. -1.  2. -1.]
 [-1.  0.  0. -1.  2.]]
```

### 3. Start Phase 1

Open `PHASE_1_TASKS.md` and work through the 5 theory tasks:
1. Graph theory & Laplacian
2. Linear systems & LMI basics
3. Multi-agent formation control (paper review)
4. Environment setup ✓ (already done)
5. Event-triggered control theory



---

## Key Files by Phase

### Phase 1 (Theory)
- `PHASE_1_TASKS.md` — 5 tasks with deliverables

### Phase 2 (System Modelling)
- `config/params.py` — System matrices, topology, formation reference


### Phase 3 (Controller Design)
- `lmi/lmi_solve.py` — Solve the LMI for K, Φ, Ω (Theorem 1)
- `lmi/controller.py` — Implement feedback law u = Kx + q

### Phase 4 (Parameter Tuning)
- Jupyter notebook: tune σ(0), ρ, and other gains

### Phase 5 (Stability Validation)
- Figures-(trajectories, formation, bandwidth savings)

### Phase 6 (Full Simulation + Enhancements)
- `sim/simulator.py` — 20-second closed-loop simulation


---

## LMI Formulation 

The core of the project is solving the block LMI. 

Find P̃, Q̃, R̃, Φ̃, Ω̃, S̃, K̃ such that:

$$\Upsilon = \begin{bmatrix}
\Upsilon_{11} & \Upsilon_{12} & \Upsilon_{13} \\
* & \Upsilon_{22} & 0 \\
* & * & -R̃
\end{bmatrix} < 0$$

with constraints on σ(0) ∈ [0, 1) and ρ > 0.

This ensures:
- **Closed-loop stability** of the formation error dynamics
- **Convergence** to the moving reference
- **Proof** that DECM triggers reduce bandwidth without sacrificing stability

Implementation: **`lmi/lmi_solve.py`** uses cvxpy to solve this feasibility problem.

---

## Expected Results

- **5 UAVs** converge to rotating pentagon (radius 1 m, ω = 0.5 rad/s)
- **Center tracks** reference trajectory at 0.3 m/s
- **Trigger probabilities**: 38.5–62.5% (∼50% bandwidth savings)
- **Lyapunov convergence** guaranteed by LMI feasibility
- **All eigenvalues** of closed-loop system in left-half plane

### What You Will Produce
- Trajectory plots of all 5 UAVs
- Formation shape evolution over time
- Communication event histogram (broadcasts per second)
- Bandwidth usage: periodic vs. DECM
- Convergence plots: formation error → 0

---


---

## References

### Core Paper
- **Xiang et al. (2023)**. "Dynamic Event-Triggered Formation Control for UAVs..."  
  IEEE IECON 2023 · Northwestern Polytechnical University

### Foundational Works
- Dong et al. (2015). "Cooperative formation control for multi-agent systems..."  
- Ge & Han (2017). "Distributed formation stabilization via event-triggered communication"  
- Ren & Beard (2005). "Consensus seeking in multiagent systems..."



### Software
- **cvxpy**: Python convex optimization package  
- **NumPy/SciPy**: Numerical linear algebra  
- **Matplotlib**: Visualization

---



Each phase builds on the previous; skip no steps. Theory (Phase 1) foundations are critical for understanding the controller design (Phase 3) and debugging the simulation (Phase 6).

---

