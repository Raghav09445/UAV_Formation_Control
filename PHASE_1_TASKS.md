# Phase 1: Prerequisites & Theory Foundation (Days 1–3)

## Overview
Build the mathematical toolkit. You will not write any simulation code yet — the goal is to be fluent in every symbol in the paper before touching a keyboard.

## Tasks

### Task 1: Graph Theory & Laplacian
- **Duration**: 1 day
- **Type**: Theory
- **Description**: Study L = D − W, eigenvalues, connectivity. Draw the 5-UAV pentagon topology from the paper by hand. Verify λ₁ = 0.
- **Deliverable**: 
  - Hand-drawn diagram of pentagon topology
  - Verification that λ₁ = 0 (notebook or script output)
  - Understanding of why λ₁ = 0 (algebraic connectivity)

**Key Concepts**:
- Adjacency matrix W: captures which UAVs communicate
- Degree matrix D: diagonal matrix with row sums of W
- Laplacian L = D - W: encodes topology structure
- Eigenvalue λ₁ = 0 always (corresponds to constant eigenvector 1)
- λ₂ (algebraic connectivity): > 0 for connected graph

**References**:
- Dong et al. (2015): Multi-agent formation control (TVFT)
- Ren & Beard (2005): Distributed consensus in multi-agent systems

---

### Task 2: Linear Systems & LMI Basics
- **Duration**: 1 day
- **Type**: Theory
- **Description**: Review ẋ = Ax + Bu, stability, Lyapunov V(t) = xᵀPx, Schur complement, MATLAB/Python LMI solvers (cvxpy or YALMIP).
- **Deliverable**: 
  - Notes on Lyapunov stability theory
  - Simple example: solve LMI for P > 0 in a 2×2 A matrix using cvxpy
  - Understand Schur complement and its role in convex LMI formulation

**Key Concepts**:
- Lyapunov stability: if ∃P > 0 s.t. AᵀP + PA < 0, then ẋ = Ax is asymptotically stable
- LMI (Linear Matrix Inequality): Υ < 0 is a convex constraint
- Schur complement: block matrix inequality reduction trick
- cvxpy: Python package for LMI solving via semidefinite programming

**Code to Run**:
```python
import cvxpy as cp
import numpy as np

# Solve for P such that AᵀP + PA < 0
A = np.array([[0, 1], [-2, -3]], dtype=float)
P = cp.Variable((2, 2), PSD=True)
constraint = A.T @ P + P @ A
prob = cp.Problem(cp.Minimize(0), [constraint << 0])
prob.solve()
print("P =\n", P.value)
print("Eigenvalues of A:", np.linalg.eigvals(A))
```

**References**:
- Boyd et al. (1994): Linear Matrix Inequalities in System and Control Theory
- Khalil (2002): Nonlinear Systems, Chapter 4 (Lyapunov stability)

---

### Task 3: Multi-Agent Formation Control
- **Duration**: 0.5 day
- **Type**: Theory
- **Description**: Read Dong et al. (2015) TVFT paper and Ge & Han (2017) static DECM paper — the two direct ancestors of this work.
- **Deliverable**: 
  - 1-page summary of Dong et al. (2015): what is TVFT, why it's useful
  - 1-page summary of Ge & Han (2017): static event-triggered control mechanism
  - Identify key equations and how they connect to the present paper

**Key Questions to Answer**:
1. What does "time-varying formation" mean? Why not fixed formations?
2. What is an "event trigger"? How does it differ from periodic control?
3. How does DECM (dynamic) improve on static event triggers?
4. What is the role of the Laplacian in multi-agent control?

**References**:
- Dong et al. (2015): "Cooperative formation control for multi-agent systems with a time-varying reference"
- Ge & Han (2017): "Distributed formation stabilization via event-triggered communication"

---

### Task 4: Environment Setup
- **Duration**: 0.5 day
- **Type**: Code
- **Description**: Install Python (numpy, scipy, cvxpy, matplotlib, control) or MATLAB + CVX. Create project folder structure: /config, /lmi, /sim, /plots.
- **Deliverable**: 
  - Virtual environment created and activated
  - All packages installed (verify with `pip list`)
  - Folder structure in place (already done!)
  - First script runs without errors

**Steps**:
1. Create virtual environment:
   ```powershell
   cd C:\Users\r3642\UAV formation
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. Install requirements:
   ```powershell
   pip install -r requirements.txt
   ```

3. Verify installation:
   ```python
   python -c "import cvxpy, numpy, scipy, matplotlib; print('All packages OK')"
   ```

4. Test config import:
   ```python
   from config import params
   print(params.L)
   ```

---

### Task 5: Event-Triggered Control Theory
- **Duration**: 0.5 day
- **Type**: Theory
- **Description**: Understand the difference between periodic, static-event, and dynamic-event triggering. Trace Eq. (5)–(6) in the paper step by step.
- **Deliverable**: 
  - 1-page explanation with equations: periodic vs static vs dynamic triggering
  - Diagram showing when broadcasts happen under each scheme
  - Derivation or tracing of Eq. (5)–(6) from the paper

**Key Comparison**:

| Scheme | Broadcast Rule | Pros | Cons |
|--------|---|---|---|
| **Periodic** | Every T seconds | Simple | Wastes bandwidth |
| **Static Event** | When \|eᵢ\| > η | Reduces bandwidth | Threshold is fixed (not adaptive) |
| **Dynamic Event (DECM)** | When f_i(kT) crosses σ_i(kT) | Adapts to convergence, proven stability | More complex to analyze |

**References**:
- Paper Section II.C: Dynamic Event-Triggered Communication Mechanism
- Paper Eq. (5): f_i(kT) = ‖eᵢ(kT)‖² + λ₂⁻¹ ∑_j a_{ij} ‖eⱼ(kT)‖²
- Paper Eq. (6): σᵢ(kT) = σᵢ(0)·(ρ)^k (contracting threshold)

---

## Checklist

- [ ] Task 1: Pentagon topology diagram + Laplacian eigenvalues verified
- [ ] Task 2: Simple LMI example solved with cvxpy
- [ ] Task 3: Summaries of Dong et al. and Ge & Han papers
- [ ] Task 4: Python environment set up and packages installed
- [ ] Task 5: Periodic vs static vs dynamic triggering explained

## Next Steps (Phase 2)

Once Phase 1 is complete, move to **System Modelling (Days 4–6)**:
- Build A, B matrices and verify stabilizability
- Construct the Laplacian from the 5-UAV topology
- Implement formation reference h(t) and center motion r(t)
- Derive compensation term q(t)

---

**Estimated Time**: 3 days
**Type**: Theory + Environment setup
**Outcome**: Mathematical foundation + working Python environment
