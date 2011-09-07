# Summary
#     Creating and using vectors and basic vector operations in PETSc.
# 
# Description
#     Vectors are a basic mathematical building block.
# 
# For a complete list of vector operations, consult the PETSc user manual.
# Also look at the petsc4py/src/PETSc/Vec.pyx file for petsc4py implementation
# details.

import petsc4py
petsc4py.init()
from petsc4py import PETSc

n = 10 # Size of vector.

x = PETSc.Vec().createSeq(n) # Create vector.

# Obtain access to the actual elements of the vector.
x_vals = x.getArray()
for k in range(n):
    x_vals[k] = k # Set elements from 0 to n-1

x.shift(1) # x = x + 1 (add 1 to all elements in x)

print 'Performing various vector operations on x, n =', n

print 'Sum of elements of x =', x.sum()
print 'Dot product with itself =', x.dot(x)
print '1-norm =', x.norm(PETSc.NormType.NORM_1)
print '2-norm =', x.norm()
print 'Infinity-norm =', x.norm(PETSc.NormType.NORM_INFINITY)
print 'Minimum element in x (index, value) =', x.min()
print 'Maximum element in x (index, value) =', x.max()
