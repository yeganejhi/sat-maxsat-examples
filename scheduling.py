
from itertools import combinations

from pysat.formula import WCNF, IDPool

# Problem data
tasks = [1, 2]
d = {
    1: 2,
    2: 3,
}
T_max = 10
precedence_relations = [(1, 2)]

# Validate input data
if not tasks or len(tasks) != len(set(tasks)):
    raise ValueError("Tasks must be non-empty and unique")

if not isinstance(T_max, int) or T_max <= 0:
    raise ValueError("T_max must be a positive integer")

for i in tasks:
    if i not in d:
        raise ValueError(f"Missing duration for task {i}")

    if not isinstance(d[i], int) or d[i] <= 0:
        raise ValueError(f"Duration of task {i} must be a positive integer")

    if d[i] > T_max:
        raise ValueError(
            f"Task {i} has duration greater than T_max"
        )

for i, j in precedence_relations:
    if i not in tasks or j not in tasks:
        raise ValueError(f"Unknown task in precedence relation {(i, j)}")
    if i == j:
        raise ValueError("A task cannot precede itself")

wcnf = WCNF()
vpool = IDPool()

# x[i, t] is true if task i starts at time t
# Valid start times: 0, ..., T_max - d[i]
x = {
    (i, t): vpool.id(f"x_{i}_{t}")
    for i in tasks
    for t in range(T_max - d[i] + 1)
}

# Hard clauses: exactly one start time per task
for i in tasks:
    times_i = range(T_max - d[i] + 1)

    # At least one start time
    wcnf.append([x[i, t] for t in times_i])

    # At most one start time (pairwise encoding)
    for t1, t2 in combinations(times_i, 2):
        wcnf.append([-x[i, t1], -x[i, t2]])

# Hard clauses: precedence constraints
# If task i precedes task j, j cannot start before i finishes.
for i, j in precedence_relations:
    for t in range(T_max - d[i] + 1):
        for t_prime in range(T_max - d[j] + 1):
            if t_prime < t + d[i]:
                wcnf.append([-x[i, t], -x[j, t_prime]])

# Hard clauses: no overlap on a single processor
for i, k in combinations(tasks, 2):
    for t in range(T_max - d[i] + 1):
        for t_prime in range(T_max - d[k] + 1):
            overlaps = (
                t < t_prime + d[k]
                and t_prime < t + d[i]
            )

            if overlaps:
                wcnf.append([-x[i, t], -x[k, t_prime]])

# Soft clauses: minimize the sum of start times
for (i, t), lit in x.items():
    if t > 0:
        wcnf.append([-lit], weight=t)

# Export the weighted CNF formula
output_file = "scheduling.wcnf"
wcnf.to_file(output_file)

print(f"Wrote {output_file}")
print(f"Number of variables: {vpool.top}")
print(f"Number of hard clauses: {len(wcnf.hard)}")
print(f"Number of soft clauses: {len(wcnf.soft)}")
