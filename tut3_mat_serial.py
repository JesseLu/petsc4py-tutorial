# Summary
#     Basic use of matrices in PETSc.
# 
# For more information, consult the PETSc user manual.
# Also, look at the petsc4py/src/PETSc/DA.pyx file.

import petsc4py
petsc4py.init()
from petsc4py import PETSc

# Create matrix
A = PETSc.Mat().create()
A.setType('dense')
A.setSizes([2, 4])
A.setValue(0, 0, 3)
A.assemblyBegin()
A.assemblyEnd()
A.view()
print A.getValues(range(2), range(4))
