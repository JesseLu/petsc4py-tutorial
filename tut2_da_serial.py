# Summary
#     Basic use of distributed arrays communication data structures in PETSc.
# 
# Description
#     DAs are extremely useful when working with a structured grid distributed 
#     across multiple processes. DAs don't actually hold data, they are
#     templates for distributing and communicating information (vectors) across
#     a parallel system.
# 
#     Note that this example is uniprocessor only, so there is nothing 
#     "distributed" about the DA. Use this as a stepping stone to working with
#     DAs in a parallel setting.
#
# For more information, consult the PETSc user manual.
# Also, look at the petsc4py/src/PETSc/DA.pyx file.

import petsc4py
petsc4py.init()
from petsc4py import PETSc

# Dimensions of the 2D grid.
nx = 4
ny = 5 

da = PETSc.DA().create([nx, ny]) # Create the DA.

# Create a vector based on the DA, and obtain access to its elements.
x = da.createGlobalVec()
x_val = da.getVecArray(x)

# Another vector based on the DA.
y = da.createGlobalVec()
y_val = da.getVecArray(y)

# Loop through and set the elements of x and y.
(i0, i1), (j0, j1) = da.getRanges()
for i in range(i0, i1):
    for j in range(j0, j1):
        x_val[i,j] = i;
        y_val[i,j] = j;

# Print out the values of x and y.
print 'x = ...\n', da.getVecArray(x)[:] # One way to do it.
print 'y = ...\n', y_val[:] # This is equivalent.

