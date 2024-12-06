# How to use
```python
from solver import Solver, SolverType
from pldag import PLDAG

# Setup solver api
solver = Solver(url="http://localhost:9000")

# Setup a pldag model
model = PLDAG()
primitives = ["x", "y", "z"]
root = model.set_and(model.set_primitives(primitives))
solutions = solver.solve(model, [{}], {root: 0j}, SolverType.DEFAULT)
```