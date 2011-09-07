# Demonstrate using vectors and basic vector operations in PETSc.
# For more information, consult the PETSc user manual.

import sys, petsc4py
petsc4py.init(sys.argv)

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
