import numpy as np
from eqc_models.base import ConstrainedQuadraticModel, QuadraticModel
from eqc_models.solvers import Dirac3CloudSolver
import logging

logging.basicConfig(level=logging.INFO)
ALPHA = 30
n = 4
m = 3
np.random.seed(21)
obj = -10 + 20 * np.random.random((n,))

print(obj)

A = np.array([[1, 1, 0, 0],
              [0, 0, -1, 1],
              [1, 1, 0, 1]])
b = np.array([2, 0, 5]).T
J = np.zeros((n, n))
model = ConstrainedQuadraticModel(obj, J, A, b)
R = 8
model.upper_bound = np.array([R, R, R, R])
model.penalty_multiplier = ALPHA
Pl, Pq = model.penalties
offset = model.penalty_multiplier * model.offset
print(Pl)
print(Pq)
print(offset)
solver = Dirac3CloudSolver()
response = solver.solve(model, num_samples=5, relaxation_schedule=1)
results = response["results"]
print("Solution")
print(results["solutions"][0])
print("Meets constraints:", (A@results["solutions"][0]==b).all())
for i in range(len(results["energies"])):
    x = np.array(results["solutions"][i][:n])
    print(i, x.T@obj, results["energies"][i])
# test the relaxed model
resposne = solver.solve(model, num_samples=5, sum_constraint=R, solution_precision=None, relaxation_schedule=1)
results = response["results"]
print("Relaxed Solution")
print(results["solutions"][0])
print("Meets constraints:", (A@results["solutions"][0]==b).all())
for i in range(len(results["energies"])):
    x = np.array(results["solutions"][i][:n])
    print(i, x.T@obj, results["energies"][i])# since the dual of a minimization problem is maximization, and we can only minimize, make it negative
AT = A.T
# add negative variables for the duals since the
# equality constraints imply free variables
# add slacks to make the constraints into A^Tz>=c
AT = np.hstack([AT, -1*AT,  -1*np.eye(n)])
# Ax=b implies z is free
# AT(z-R/2)>=c
dual_obj = np.zeros((2*m+n,))
dual_obj[:m] = -1*b.T
dual_obj[m:2*m] = b.T
c = obj.T
J = np.zeros((2*m+n, 2*m+n), dtype=np.float64)
dualmodel = ConstrainedQuadraticModel(dual_obj, J, AT, c)
dualmodel.upper_bound = R * np.ones((dual_obj.shape[0],))
dualmodel.machine_slacks = 1
dualmodel.penalty_multiplier = ALPHA
response = solver.solve(dualmodel, sum_constraint=R, num_samples=5, solution_precision=None, relaxation_schedule=1)
results = response["results"]
offset = dualmodel.penalty_multiplier * dualmodel.offset
print("Solution")
print(results["solutions"][0])
print("Meets constraints:", (AT@results["solutions"][0][:-1]==c).all())
for i in range(len(results["energies"])):
    z = np.array(results["solutions"][i][:-1])
    val = z.T@dual_obj
    print(i, val, results["energies"][i])

