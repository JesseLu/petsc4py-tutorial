# Summary
#     Simulate Maxwell's equations.
# 
# Description

import petsc4py
import sys
petsc4py.init(sys.argv)
from petsc4py import PETSc
from matplotlib import pylab

n = 40
w = 12./10. # Angular frequency of wave (2*pi / period).

# Create the DA.
da = PETSc.DA().create( [n, n, 1], \
                        dof=3, \
                        stencil_width=1, \
                        boundary_type=('ghosted', 'ghosted', 'ghosted')) 

# Create vectors.
b = da.createGlobalVec() # RHS vector (current sources).
b_val = da.getVecArray(b) # Obtain access to elements of b.
b_val[n/2, n/2, 0, 2] = 1; # Define location of point source.

x = da.createGlobalVec() # Solution vector.

# Form the curl matrix.
A = da.getMatrix() # Curl matrix (w.r.t. H-fields).

row = PETSc.Mat.Stencil() # Defines row location of grid element.
col = PETSc.Mat.Stencil() # Defines column location of grid element.

(i0, i1), (j0, j1), (k0, k1) = da.getRanges()
for i in range(i0, i1):
    for j in range(j0, j1):
        for k in range(k0, k1):
            row.index = (i, j, k)

            # x-component.
            row.field = 0
            for field, index, value in [(1, (i, j, k), 1), # dAy/dz.
                                        (1, (i, j, k-1), -1),
                                        (2, (i, j, k), -1), # -dAz/dy. 
                                        (2, (i, j-1, k), 1)]:
                col.field = field
                col.index = index
                A.setValueStencil(row, col, value)

            # y-component.
            row.field = 1
            for field, index, value in [(2, (i, j, k), 1), # dAz/dx.
                                        (2, (i-1, j, k), -1),
                                        (0, (i, j, k), -1), # -dAx/dz. 
                                        (0, (i, j, k-1), 1)]:
                col.field = field
                col.index = index
                A.setValueStencil(row, col, value)

            # z-component.
            row.field = 2
            for field, index, value in [(0, (i, j, k), 1), # dAx/dy.
                                        (0, (i, j-1, k), -1),
                                        (1, (i, j, k), -1), # -dAy/dx. 
                                        (1, (i-1, j, k), 1)]:
                col.field = field
                col.index = index
                A.setValueStencil(row, col, value)

A.assemblyBegin() # Make matrix useable.
A.assemblyEnd()

AT = A.transpose()

A = AT.matMult(A)
A.shift(+w**2)

# Initialize ksp solver.
ksp = PETSc.KSP().create()
ksp.setOperators(A)

# Allow for solver choice to be set from command line with -ksp_type <solver>.
# Recommended option: -ksp_type preonly -pc_type lu
ksp.setFromOptions()
print 'Solving with:', ksp.getType()

# Solve!
ksp.solve(b, x)



pylab.contourf(da.getVecArray(x)[:,:,0,2])
pylab.show()
