# UAV Formation Control — Dynamic Event-Triggered Communication

A 20-day implementation roadmap for **Dynamic Event-Triggered Communication Mechanism (DECM) + Time-Varying Formation Tracking (TVFT)** for multi-agent UAV systems.

## Project Overview

This project implements the controller from:
> **"Dynamic Event-Triggered Formation Control for UAVs with Time-Varying Reference"**  
> *Xiang et al., IEEE IECON 2023*

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

## 6-Phase Roadmap

| Phase | Days | Title | Focus |
|-------|------|-------|-------|
| **1** | 1–3 | Prerequisites & Theory | Graph theory, LMI basics, control theory |
| **2** | 4–6 | System Modelling | Build A, B, L matrices; formation reference |
| **3** | 7–9 | Controller Design & LMI | Formulate and solve Theorem 1 (Eq. 22–23) |
| **4** | 10–13 | Parameter Tuning | Validate stability, adjust σ(0) and ρ |
| **5** | 14–15 | Stability Validation | Reproduce Table II & Fig. 2–5 from paper |
| **6** | 16–20 | Simulation + Enhancements | Full-scale sim + 3 enhancements (saturation, delay, disturbance) |

---

## Getting Started

### 1. Set Up Python Environment

```powershell
cd C:\Users\r3642\UAV formation
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

**Estimated**: 3 days for Phase 1

---

## Key Files by Phase

### Phase 1 (Theory)
- `PHASE_1_TASKS.md` — 5 tasks with deliverables

### Phase 2 (System Modelling)
- `config/params.py` — System matrices, topology, formation reference
- `PHASE_2_TASKS.md` (to be created)

### Phase 3 (Controller Design)
- `lmi/lmi_solve.py` — Solve the LMI for K, Φ, Ω (Theorem 1)
- `lmi/controller.py` — Implement feedback law u = Kx + q

### Phase 4 (Parameter Tuning)
- Jupyter notebook: tune σ(0), ρ, and other gains

### Phase 5 (Stability Validation)
- Scripts to reproduce paper's Table II (trigger probabilities)
- Figures 2–5 (trajectories, formation, bandwidth savings)

### Phase 6 (Full Simulation + Enhancements)
- `sim/simulator.py` — 20-second closed-loop simulation
- 3 enhancements: actuator saturation, comm delays, disturbance observer

---

## LMI Formulation (Paper Theorem 1)

The core of the project is solving the block LMI in **Equations (22)–(23)**:

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

### From Paper (Table II, Fig. 2–5)
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

## Enhancement Extensions

After the core project, three enhancements deepen the work:

1. **Actuator Saturation** (Days 14–15) — Easy
   - Add ‖uᵢ‖ ≤ u_max constraint
   - Anti-windup compensator
   - Re-solve LMI with saturation bounds

2. **Communication Delays** (Days 16–17) — Medium
   - Replace state sharing with delayed data: xⱼ(t − τ)
   - Re-derive LMI with delay-dependent stability (Jensen's inequality)
   - Tune max delay τ_max

3. **Disturbance Observer** (Days 18–20) — Medium
   - Finite-time disturbance observer (FTDO)
   - Estimate wind gusts and drag online
   - Feedback compensation into control law

---

## References

### Core Paper
- **Xiang et al. (2023)**. "Dynamic Event-Triggered Formation Control for UAVs..."  
  IEEE IECON 2023 · Northwestern Polytechnical University

### Foundational Works
- Dong et al. (2015). "Cooperative formation control for multi-agent systems..."  
- Ge & Han (2017). "Distributed formation stabilization via event-triggered communication"  
- Ren & Beard (2005). "Consensus seeking in multiagent systems..."

### Mathematical Tools
- Boyd et al. (1994). "Linear Matrix Inequalities in System and Control Theory"  
- Khalil (2002). "Nonlinear Systems" (Lyapunov stability)

### Software
- **cvxpy**: Python convex optimization package  
- **NumPy/SciPy**: Numerical linear algebra  
- **Matplotlib**: Visualization

---

## Contact & Notes

- **Date Started**: June 15, 2026
- **Estimated Duration**: 20 days
- **Status**: Phase 1 (Theory Foundation)

Each phase builds on the previous; skip no steps. Theory (Phase 1) foundations are critical for understanding the controller design (Phase 3) and debugging the simulation (Phase 6).

---

**Next**: Open `PHASE_1_TASKS.md` and begin Task 1 (Graph Theory & Laplacian).
