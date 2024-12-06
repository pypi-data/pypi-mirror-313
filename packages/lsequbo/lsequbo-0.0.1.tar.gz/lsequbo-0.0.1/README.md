Solve LSEs using
- classical LU solver
- QUBO formulation minimizing (*A* **x** - **b**) squared with binary representation
- QUBO formulation with gate-based encoding

*A* **x** = **b**

## Structure

1. `poisson` generates *A* and **b** for discrete poisson equation
2. `lsequbo` takes *A* and **b** and creates .ising files for QUBO problems
3. `ising` loads and dumps .ising files

## Output
Problems are labeled upon creation.

lsequbo stores files for each run in the directory `out/label/` by default. Stored are

- `binary-encoding.ising`
- `gate-based-encoding.ising`