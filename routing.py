
from itertools import combinations

from pysat.formula import WCNF, IDPool
from pysat.card import CardEnc
from pysat.examples.rc2 import RC2

# Problem data
nodes = [1, 2, 3]

c = {
    (1, 2): 5,
    (1, 3): 10,
    (2, 1): 8,
    (2, 3): 2,
    (3, 1): 3,
    (3, 2): 4,
}

# Validate input data
if len(nodes) < 2 or len(nodes) != len(set(nodes)):
    raise ValueError("Nodes must be unique and contain at least two nodes")

for i in nodes:
    for j in nodes:
        if i == j:
            continue

        if (i, j) not in c:
            raise ValueError(f"Missing cost for edge {i} -> {j}")

        if not isinstance(c[i, j], int) or c[i, j] < 0:
            raise ValueError("Edge costs must be non-negative integers")

wcnf = WCNF()
vpool = IDPool()

# x[i, j] is true if the directed edge i -> j is selected
x = {
    (i, j): vpool.id(f"x_{i}_{j}")
    for i in nodes
    for j in nodes
    if i != j
}

# Hard clauses: exactly one outgoing and one incoming edge per node

for i in nodes:
    outgoing = [x[i, j] for j in nodes if j != i]

    # At least one outgoing edge
    wcnf.append(outgoing)

    # At most one outgoing edge
    for a, b in combinations(outgoing, 2):
        wcnf.append([-a, -b])

for j in nodes:
    incoming = [x[i, j] for i in nodes if i != j]

    # At least one incoming edge
    wcnf.append(incoming)

    # At most one incoming edge
    for a, b in combinations(incoming, 2):
        wcnf.append([-a, -b])

# Hard clauses: subtour elimination
# For every proper subset S with |S| >= 2:
# sum(x[i, j] for i, j in S, i != j) <= |S| - 1

for size in range(2, len(nodes)):
    for subset in combinations(nodes, size):
        S = set(subset)

        internal_edges = [
            x[i, j]
            for i in S
            for j in S
            if i != j
        ]

        cnf = CardEnc.atmost(
            lits=internal_edges,
            bound=len(S) - 1,
            vpool=vpool,
        )

        for clause in cnf.clauses:
            wcnf.append(clause)

# Soft clauses: minimize total tour cost
for (i, j), lit in x.items():
    if c[i, j] > 0:
        wcnf.append([-lit], weight=c[i, j])

# Solve the weighted Max-SAT problem
with RC2(wcnf) as solver:
    optimal_route = solver.compute()

    if optimal_route is None:
        raise RuntimeError("No feasible tour found")

    minimum_cost = solver.cost
    selected_literals = set(optimal_route)

selected_edges = {
    (i, j)
    for (i, j), lit in x.items()
    if lit in selected_literals
}

print("Optimal Tour Cost:", minimum_cost)
print("Selected Edges:", sorted(selected_edges))

# Reconstruct the tour, starting from the first node
start = nodes[0]
tour = [start]
current = start

for _ in range(len(nodes) - 1):
    next_nodes = [
        j for i, j in selected_edges
        if i == current
    ]

    if len(next_nodes) != 1:
        raise RuntimeError("Invalid tour: expected one outgoing edge")

    current = next_nodes[0]
    tour.append(current)

if (current, start) not in selected_edges:
    raise RuntimeError("Invalid tour: it does not return to the start node")

tour.append(start)

print("Optimal Tour:", " -> ".join(map(str, tour)))
