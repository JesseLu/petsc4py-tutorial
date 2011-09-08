# Summary
#     Creating and using vectors and basic vector operations in PETSc.
# 
# Description
#     Vectors are a basic mathematical building block.
# 
# For a complete list of vector operations, consult the PETSc user manual.
# Also look at the petsc4py/src/PETSc/Vec.pyx file for petsc4py implementation
# details.

import sys
import petsc4py
petsc4py.init(sys.argv)
from petsc4py import PETSc

n = 10 # Size of vector.

# x = PETSc.Vec().create() # Create vector the long way.
# x.setSizes(n) 
# x.setType('seq') # 'seq' means sequential vector.
# 
# x.assemblyBegin() # Needed in order to work on vector.
# x.assemblyEnd()

x = PETSc.Vec().createSeq(n) # Faster way to create a sequential vector.

x.setValues(range(n), range(n)) # x = [0 1 ... 9]
x.shift(1) # x = x + 1 (add 1 to all elements in x)

print 'Performing various vector operations on x =', x.getArray() 

print 'Sum of elements of x =', x.sum()
print 'Dot product with itself =', x.dot(x)
print '1-norm =', x.norm(PETSc.NormType.NORM_1)
print '2-norm =', x.norm()
print 'Infinity-norm =', x.norm(PETSc.NormType.NORM_INFINITY)
print 'Minimum element in x (index, value) =', x.min()
print 'Maximum element in x (index, value) =', x.max()
