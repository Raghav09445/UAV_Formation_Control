# Phase 1: Prerequisites & Theory Foundation--

## Overview
Build the mathematical toolkit. 

## Tasks

### Task 1: Graph Theory & Laplacian
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
- λ₂ (algebraic connectivity): > 0 for connectivity--

### Task 2: Linear Systems & LMI Basics
- **Type**: Theory
- **Description**: Review ẋ = Ax + Bu, stability, Lyapunov V(t) = xᵀPx, Schur complement, MATLAB/Python LMI solvers (cvxpy or YALMIP).
- **Deliverable**: 
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
`

---

### Task 3: Multi-Agent Formation Control
- **Type**: Theory

**Key Questions to Answer**:
1. What does "time-varying formation" mean? Why not fixed formations?
2. What is an "event trigger"? How does it differ from periodic control?
3. How does DECM (dynamic) improve on static event triggers?
4. What is the role of the Laplacian in multi-agent control?


---

### Task 4: Environment Setup
- **Type**: Code
- **Description**: Install Python (numpy, scipy, cvxpy, matplotlib, control) or MATLAB + CVX. Create project folder structure: /config, /lmi, /sim, /plots.
- **Deliverable**: 
  - Virtual environment created and activated
  - All packages installed (verify with `pip list`)
  - Folder structure in place (already done!)
  - First script runs without errors

**Steps**:
1. Create virtual environment:
   ``
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
- **Type**: Theory
- **Description**: Understand the difference between periodic, static-event, and dynamic-event triggering.


**Key Comparison**:

| Scheme | Broadcast Rule | Pros | Cons |
|--------|---|---|---|
| **Periodic** | Every T seconds | Simple | Wastes bandwidth |
| **Static Event** | When \|eᵢ\| > η | Reduces bandwidth | Threshold is fixed (not adaptive) |
| **Dynamic Event (DECM)** | When f_i(kT) crosses σ_i(kT) | Adapts to convergence, proven stability | More complex to analyze |



---

## Checklist

- [ ] Task 1: Pentagon topology diagram + Laplacian eigenvalues verified
- [ ] Task 2: Simple LMI example solved with cvxpy
- [ ] Task 3: Summaries of Dong et al. and Ge & Han papers
- [ ] Task 4: Python environment set up and packages installed
- [ ] Task 5: Periodic vs static vs dynamic triggering explained

## Next Steps (Phase 2)

- Build A, B matrices and verify stabilizability
- Construct the Laplacian from the 5-UAV topology
- Implement formation reference h(t) and center motion r(t)
- Derive compensation term q(t)

---


**Type**: Theory + Environment setup
**Outcome**: Mathematical foundation + working Python environment
