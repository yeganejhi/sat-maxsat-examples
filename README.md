# Modeling and Solving Combinatorial Optimization Problems Using SAT/Max-SAT

**Author:** Yegane Jahanbani

This repository contains Python implementations of selected combinatorial optimization problems using Boolean satisfiability (SAT) and weighted partial Max-SAT (Max-SAT).

The examples illustrate how optimization problems can be represented using hard and weighted soft clauses and solved using PySAT.

## Problems

### 1. Assignment Problem

**File:** `assignment.py`

Assigns tasks to processors while minimizing the total assignment cost.

- Each task must be assigned to exactly one processor.
- Each processor can receive at most one task.
- Assignment costs are represented by weighted soft clauses.
- The RC2 solver computes an optimal solution.

For the included example, the expected minimum cost is **6**.

### 2. Scheduling Problem

**File:** `scheduling.py`

Models a single-processor scheduling problem with task durations and precedence constraints.

- Each task must have exactly one start time.
- Tasks must satisfy the specified precedence relations.
- Tasks cannot overlap on the single processor.
- The objective is to minimize the sum of task start times.

The script generates a weighted CNF file named `scheduling.wcnf`. It does not solve the instance directly. The exported WCNF file can be solved with RC2 or with a standalone Max-SAT solver such as LMHS.

For the included example (`d = {1: 2, 2: 3}`, `T_max = 10`, precedence `1 -> 2`), the expected optimal solution starts task 1 at time 0 and task 2 at time 2, giving an optimal objective value (sum of start times) of **2**.

### 3. Traveling Salesperson Problem (TSP)

**File:** `routing.py`

Models a directed traveling salesperson problem with edge costs.

- Each node must have exactly one incoming and one outgoing edge.
- Subtour elimination constraints enforce a single tour.
- Edge costs are represented by weighted soft clauses.
- The RC2 solver computes an optimal tour.

For the included example, the expected optimal tour cost is **10**, with the tour:

`1 -> 2 -> 3 -> 1`

## Requirements

- Python 3.9 or later
- `python-sat`

Install the dependency with:

```bash
python -m pip install -r requirements.txt
```

## Running the Examples

Run each script from the repository directory:

```bash
python assignment.py
python scheduling.py
python routing.py
```

The assignment and routing scripts solve their respective instances using RC2. The scheduling script exports the WCNF formula to `scheduling.wcnf`.

## Technical Notes

- Hard clauses represent mandatory feasibility constraints.
- Weighted soft clauses encode minimization objectives: selecting a decision incurs the corresponding penalty.
- Assignment and routing costs are assumed to be positive integers.
- The scheduling objective minimizes the sum of start times, not the makespan.
- The routing implementation uses explicit subtour elimination constraints and is intended for small illustrative instances.
- The examples use small, predefined instances for educational and methodological demonstration.

## Reproducibility

The input data and model parameters are defined directly in each Python script. The expected objective values above refer to the included example instances.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.