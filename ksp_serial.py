# Summary
#     Solving a linear system with the KSP package in PETSc.
# 
# Description
#     We create the sparse linear system Ax = b and solve for x. 
#
# For more information, consult the PETSc user manual.
# Also, look at the petsc4py/src/PETSc/Mat.pyx file, especially for a complete listing of 
# matrix types.

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
A = PETSc.Mat().createAIJ([n, n])

# Insert values (the matrix is tridiagonal).
A.setValue(0, 0, 2. - w**2)
for k in range(1, n):
    A.setValue(k, k, 2. - w**2) # Diagonal.
    A.setValue(k-1, k, -1.) # Off-diagonal.
    A.setValue(k, k-1, -1.) # Off-diagonal.

A.assemblyBegin()
A.assemblyEnd()

# Let's solve!
ksp = PETSc.KSP().create()
ksp.setOperators(A)
ksp.setType('cg')
ksp.setFromOptions()
ksp.solve(b, x)

pylab.plot(x.getArray())
pylab.show()

# print A.getValues(range(n), range(n)), b.getArray(), b.norm(), b
