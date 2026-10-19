
from pysat.formula import WCNF, IDPool
from pysat.examples.rc2 import RC2

# Problem data
tasks = [1, 2]
processors = [1, 2]

c = {
    (1, 1): 2,
    (1, 2): 5,
    (2, 1): 3,
    (2, 2): 4,
}

# Validate input data
if not tasks or not processors:
    raise ValueError("Tasks and processors must not be empty")

if len(tasks) != len(set(tasks)):
    raise ValueError("Tasks must be unique")

if len(processors) != len(set(processors)):
    raise ValueError("Processors must be unique")

for i in tasks:
    for j in processors:
        if (i, j) not in c:
            raise ValueError(f"Missing cost for task {i}, processor {j}")
        if not isinstance(c[i, j], int) or c[i, j] < 0:
            raise ValueError("Assignment costs must be non-negative integers")

wcnf = WCNF()
vpool = IDPool()

# x[i, j] is true if task i is assigned to processor j
x = {
    (i, j): vpool.id(f"x_{i}_{j}")
    for i in tasks
    for j in processors
}

# Hard clauses: each task is assigned to exactly one processor
for i in tasks:
    # At least one processor
    wcnf.append([x[i, j] for j in processors])

    # At most one processor (pairwise encoding)
    for idx, j1 in enumerate(processors):
        for j2 in processors[idx + 1:]:
            wcnf.append([-x[i, j1], -x[i, j2]])

# Hard clauses: each processor receives at most one task
for j in processors:
    for idx, i in enumerate(tasks):
        for k in tasks[idx + 1:]:
            wcnf.append([-x[i, j], -x[k, j]])

# Soft clauses: minimize total assignment cost
for i in tasks:
    for j in processors:
        if c[i, j] > 0:
            wcnf.append([-x[i, j]], weight=c[i, j])

# Solve the weighted Max-SAT problem
with RC2(wcnf) as solver:
    optimal_assignment = solver.compute()

    if optimal_assignment is None:
        raise RuntimeError("No feasible assignment found")

    minimum_cost = solver.cost
    selected_literals = set(optimal_assignment)

selected_assignments = [
    (i, j)
    for (i, j), lit in x.items()
    if lit in selected_literals
]

print("Minimum Cost:", minimum_cost)
print("Optimal Assignment:")

for i, j in selected_assignments:
    print(f"Task {i} -> Processor {j}, Cost = {c[i, j]}")
