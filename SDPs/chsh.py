import cvxpy as cp

# Define the number of monomials (operators)
n = 5  # monomials: I (identity), A0, A1, B0, B1

# Create the moment (correlation) matrix Γ as a symmetric positive semidefinite variable
Gamma = cp.Variable((n, n), PSD=True)

# Define the indices for readability
I = 0   # Identity operator
A0 = 1  # Alice's measurement setting 0
A1 = 2  # Alice's measurement setting 1
B0 = 3  # Bob's measurement setting 0
B1 = 4  # Bob's measurement setting 1

# Initialize the list of constraints
constraints = []

# Set the diagonal elements corresponding to the squares of observables to 1
constraints += [Gamma[I, I] == 1]   # ⟨I·I⟩ = 1
constraints += [Gamma[A0, A0] == 1] # ⟨A0·A0⟩ = 1
constraints += [Gamma[A1, A1] == 1] # ⟨A1·A1⟩ = 1
constraints += [Gamma[B0, B0] == 1] # ⟨B0·B0⟩ = 1
constraints += [Gamma[B1, B1] == 1] # ⟨B1·B1⟩ = 1

# Define the Bell expression for the CHSH inequality in terms of Γ entries
# S = ⟨A0·B0⟩ + ⟨A0·B1⟩ + ⟨A1·B0⟩ - ⟨A1·B1⟩
S = Gamma[A0, B0] + Gamma[A0, B1] + Gamma[A1, B0] - Gamma[A1, B1]

# Objective: Maximize the Bell expression S
objective = cp.Maximize(S)

# Set up and solve the optimization problem
prob = cp.Problem(objective, constraints)
prob.solve(solver=cp.SCS)  # 'CVXOPT' is another alternative

# Output the quantum bound of the CHSH inequality
print("Quantum bound of the CHSH inequality:", prob.value)