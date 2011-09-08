# Summary
#     Solving a linear system with the KSP package in PETSc.
# 
# Description
#     We create the sparse linear system Ax = b and solve for x. Different solvers can be
#     used by including the option -ksp_type <solver>. Also, include the -ksp_monitor option
#     to monitor progress.
# 
#     In particular, compare results from the following solvers:
#         python ksp_serial.py -ksp_monitor -ksp_type chebychev
#         python ksp_serial.py -ksp_monitor -ksp_type cg
#
# For more information, consult the PETSc user manual.

import petsc4py
import sys
from matplotlib import pylab
petsc4py.init(sys.argv)
from petsc4py import PETSc

n = 100 # Size of grid.
w = 6./10. # Angular frequency of wave (2*pi / period).

# Create the rhs vector b.
b = PETSc.Vec().createSeq(n) 
b.setValue(0, 1) # Set value of first element to 1.

# Create solution vector x.
x = PETSc.Vec().createSeq(n)

# Create the wave equation matrix.
A = PETSc.Mat().createAIJ([n, n], nnz=3) # nnz=3 since the matrix will be tridiagonal.

# Insert values (the matrix is tridiagonal).
A.setValue(0, 0, 2. - w**2)
for k in range(1, n):
    A.setValue(k, k, 2. - w**2) # Diagonal.
    A.setValue(k-1, k, -1.) # Off-diagonal.
    A.setValue(k, k-1, -1.) # Off-diagonal.

A.assemblyBegin() # Make matrices useable.
A.assemblyEnd()

# Initialize ksp solver.
ksp = PETSc.KSP().create()
ksp.setOperators(A)

# Allow for solver choice to be set from command line with -ksp_type <solver>.
ksp.setFromOptions()
print 'Solving with:', ksp.getType()

# Solve!
ksp.solve(b, x)

# Print results.
print 'Converged in', ksp.getIterationNumber(), 'iterations.'

# # Use this to plot the solution (should look like a sinusoid).
# pylab.plot(x.getArray())
# pylab.show()
