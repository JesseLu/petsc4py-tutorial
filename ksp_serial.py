# Summary
#     Solving a linear system with the KSP package in PETSc.
# 
# Description
#     We create both a sparse linear system (Ax = b) and solve for x. 
#
#     The system we will use is a simple 1D wave equation. Our solution should look like a 
#     sinusoid.
# 
# For more information, consult the PETSc user manual.
# Also, look at the petsc4py/src/PETSc/Mat.pyx file, especially for a complete listing of 
# matrix types.

import petsc4py
petsc4py.init()
from petsc4py import PETSc

n = 10 # Number of grid points.

# Create the DA (grid, basically) for our 1D wave problem. 
da = PETSc.DA().create([n], stencil_width=1) # Create the DA.

# Create the rhs vector b.
b = da.createGlobalVec()
b.setValue(0, 1) # Set value of first element to 1.

print b.getArray(), b.norm(), b
