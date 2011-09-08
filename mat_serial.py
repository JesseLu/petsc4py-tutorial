# Summary
#     Basic use of matrices in PETSc.
# 
# Description
#     We create both a dense and sparse matrix. 
# 
# For more information, consult the PETSc user manual.
# Also, look at the petsc4py/src/PETSc/Mat.pyx file, especially for a complete listing of 
# matrix types.

import petsc4py
petsc4py.init()
from petsc4py import PETSc

# Create vector to multiply matrices by.
e = PETSc.Vec().createSeq(4) 
e.set(1)
y = PETSc.Vec().createSeq(2) # Put answer here.

# First, we'll create a dense matrix.
# A = PETSc.Mat().create()
# 
# A.setType('dense') # For a list of types, see petsc4py/src/PETSc/Mat.pyx
# A.setSizes([2, 4])
A = PETSc.Mat().createDense([2, 4])

A.setValue(0, 0, 3) # Insert a single value into matrix.
A.setValues([0, 1], [2, 3], [1, 1, 1, 1]) # Insert a 2x2 block of values into the matrix.

A.assemblyBegin() # Assembling the matrix makes it "useable".
A.assemblyEnd()

print 'Values of dense matrix:'
print A.getValues(range(2), range(4)) 

A.mult(e, y)
print 'A * 1 =', y.getArray()


# Next, we'll create a sparse matrix.
# A = PETSc.Mat().create()
# 
# A.setType('aij') # AIJ is PETSc's default sparse matrix format.
# A.setSizes([2, 4])
A = PETSc.Mat().createAIJ([2, 4])

A.setValue(1, 2, -1)
A.setValue(0, 0, -2)

A.assemblyBegin() # Assembling the matrix makes it "useable".
A.assemblyEnd()

print 'Values of sparse matrix:'
print A.getValues(range(2), range(4)) 

A.mult(e, y)
print 'A * 1 =', y.getArray()
