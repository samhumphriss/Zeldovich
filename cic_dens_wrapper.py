import numpy as N
import cicdens

#Input: particle positions in 3 arrays (x, y, z)
#Each of x, y, and z must be double precision arrays
#We also need the size of the grid to make (density grid will be ngrid x ngrid x ngrid) and the box size
def get_dens(x, y, z, ngrid, boxsize):
    #Just make sure that these are the right data type
    x=x.astype(N.float)
    y=y.astype(N.float)
    z=z.astype(N.float)

    #Number of particles, which needs to be passed into the C code
    nparticles=x.size

    #Initialize the density grid
    dens=N.zeros([ngrid, ngrid, ngrid], dtype=N.float)
    
    #Next we call the C code that computes the Cloud-in-Cell density from the particle positions
    #Pointers are passed using x.ctypes.data and must be of type int64
    #particle positions and density grid must be of type numpy float (which are 64 bit, or double-precision floats)
    #the box size must also be a double precision float. ngrid and nparticles must be integers 
    cicdens.calcd_cic(N.int(ngrid), N.int(nparticles), N.float(boxsize), N.int64(x.ctypes.data), N.int64(y.ctypes.data), N.int64(z.ctypes.data), N.int64(dens.ctypes.data))
    
    #dens now contains the total "mass" (number) of particles in each cell, but we want the overdensity, which is:
    dens=dens/N.mean(dens)-1.0
    
    return dens

#Input: displacement field on the grid in 3 arrays (xp, yp, zp)
#Each of xp, yp, and zp must be double precision arrays
#We also need the size of the grid to make (density grid will be ngrid x ngrid x ngrid) and the box size
#This code assumes the particles are initially on a grid, and it displaces them and computes the final density field all in one go
#If nparticles != ngrid**3, it interpolates the displacement field to the off-grid particles
#Also does redshift space distortions through the "growthrate" parameter, and it assumes the line of sight direction is the x-direction
def disp_to_dens(xp, yp, zp, ngrid, boxsize, nparticles, growthrate):
    #Just make sure that these are the right data type
    xp=xp.astype(N.float)
    yp=yp.astype(N.float)
    zp=zp.astype(N.float)

    #Initialize the density grid
    dens=N.zeros([ngrid, ngrid, ngrid], dtype=N.float)

    cicdens.calcd_zel(N.int(ngrid), N.int64(nparticles), N.float(boxsize), N.float(growthrate), N.int64(xp.ctypes.data), N.int64(yp.ctypes.data), N.int64(zp.ctypes.data), N.int64(dens.ctypes.data))
    
    dens=dens/N.mean(dens)-1.0
    return dens
