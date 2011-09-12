# Summary
#     Basic use of distributed arrays communication data structures in PETSc.
# 
# Examples
#     Direct solve:
#     $ python da_serial.py -ksp_monitor -ksp_type preonly -pc_type lu
# 
#     Iterative solve:
#     $ python da_serial.py -ksp_monitor -ksp_type bcgs
# 
# Description
#     DAs are extremely useful when working simulations that are discretized
#     on a structured grid. DAs don't actually hold data; instead, they are 
#     templates for distributing and communicating information (matrices and 
#     vectors) across a parallel system.
# 
#     In this example, we set up a simple 2D wave equation with mirror
#     boundary conditions. The solution, given a source at the center of the
#     grid, is solved using a ksp object.
# 
#     Note that this example is uniprocessor only, so there is nothing 
#     "distributed" about the DA. Use this as a stepping stone to working with
#     DAs in a parallel setting.
#
# For more information, consult the PETSc user manual.
# Also, look at the petsc4py/src/PETSc/DA.pyx file.                    

import petsc4py
import sys
petsc4py.init(sys.argv)
from petsc4py import PETSc
from matplotlib import pylab

# Dimensions of the 2D grid.
nx = 101 
ny = 101 

w = 2./10. # Angular frequency of wave (2*pi / period).

# Create the DA.
da = PETSc.DA().create([nx, ny], \
                        stencil_width=1, \
                        boundary_type=('ghosted', 'ghosted')) 

# Create the rhs vector based on the DA. 
b = da.createGlobalVec()
b_val = da.getVecArray(b) # Obtain access to elements of b.
b_val[50, 50] = 1; # Set central value to 1.

# Create (a vector to store) the solution vector.
x = da.createGlobalVec()

# Create the matrix.
A = da.getMatrix('aij')

# Stencil objects make it easy to set the values of the matrix elements.
row = PETSc.Mat.Stencil()
col = PETSc.Mat.Stencil()

# Set matrix elements to correct values.
(i0, i1), (j0, j1) = da.getRanges()
for j in range(j0, j1):
    for i in range(i0, i1):
        row.index = (i, j)
        for index, value in [((i, j), -4 + w**2),
                             ((i-1, j), 1),
                             ((i+1, j), 1),
                             ((i, j-1), 1),
                             ((i, j+1), 1)]:
            col.index = index
            A.setValueStencil(row, col, value) # Sets a single matrix element.
                            
A.assemblyBegin() # Make matrices useable.
A.assemblyEnd()

# Initialize ksp solver.
ksp = PETSc.KSP().create()
ksp.setOperators(A)

# Allow for solver choice to be set from command line with -ksp_type <solver>.
# Recommended option: -ksp_type preonly -pc_type lu
ksp.setFromOptions()
print 'Solving with:', ksp.getType()

# Solve!
ksp.solve(b, x)

# Plot solution, which is wave-like, although boundaries cause reflections.
pylab.contourf(da.getVecArray(x)[:])
pylab.show()
