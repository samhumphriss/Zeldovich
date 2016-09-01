import matplotlib.pyplot as plt
plt.style.use('nuala')
plt.rcParams['xtick.labelsize'] = 22
plt.rcParams['ytick.labelsize'] = 22

import numpy as np
import zeldovich_init as zi
import cic_dens_wrapper as cdw

def zeldovich_data():
    pkinit = np.loadtxt("/cosma/home/durham/rhgk18/ls_structure/pks/wig.txt")

    dk_field   = zi.make_gauss_init(pkinit)
    xp, yp, zp = zi.get_disp(dk_field)
    x, y, z    = zi.get_pos(xp, yp, zp, 0.0)
    xr         = zi.redshift_dist(x, 0.0, xp)
    densrs     = cdw.disp_to_dens(xp, yp, zp, 100, 100, 100**3, 0.5) #last parameter growthrate, 0.0 = real space
    densreal   = cdw.disp_to_dens(xp, yp, zp, 100, 100, 100**3, 0.0)

    return x, xr, y, z, densrs, densreal
    
def render_real_pos(x, y, z):

    indices = []
    for a in xrange(len(y)):
    	if(y[a] > 50 and y[a] <= 51):
        	indices.append(a)
    
    x = x[indices]
    z = z[indices]
    
    plt.figure()
    plt.axes().set_aspect('equal')
    plt.plot(z,x, 'bo', markersize = 1)
    plt.xlabel("X [$MPc/h$]", size=24)
    plt.ylabel("Z [$MPc/h$]", size=24)
    plt.xlim([0,100])
    plt.ylim([0,100])
    plt.show()

def render_rs_pos(x, y, z):

    indices = []
    for a in xrange(len(y)):
    	if(y[a] > 50 and y[a] <= 51):
        	indices.append(a)
    
    x = x[indices]
    z = z[indices]
    
    plt.figure()
    plt.axes().set_aspect('equal')
    plt.plot(z,x, 'bo', markersize = 1)
    plt.xlabel("X [$MPc/h$]", size=24)
    plt.ylabel("Z [$MPc/h$]", size=24)
    plt.xlim([0,100])
    plt.ylim([0,100])
    plt.show()

def render_rs_dens(densrs):
    
    densitycutoff = -0.8

    x, z = np.mgrid[0:100+1,0:100+1]
               
    dr = densrs[:,50,:]
    dp = np.log10(1+dr)
    
    ind = np.where(np.isnan(dp))
    dp[ind] = densitycutoff
    

    z_min, z_max = densitycutoff, np.max(dp)

    fig0 = plt.figure()
    colax2 = plt.pcolormesh(z, x, dp, cmap='magma', vmin=z_min, vmax=z_max)
    cbar2 = fig0.colorbar(colax2)
    cbar2.set_ticks([densitycutoff,0,z_max])
    cbar2.set_ticklabels([r"$\delta$ = -$\infty$", r"$\delta$ = 0", r"$\delta$ = "+ str(np.around(z_max, 3))])
    cbar2.ax.tick_params(labelsize=24)
    plt.xlabel("$X [$Mpc/h$]$", size=24)
    plt.ylabel("$Z [$Mpc/h$]$", size=24)
    plt.show()

def render_real_dens(densreal):
    
    densitycutoff = -0.8

    x, z = np.mgrid[0:100+1,0:100+1]
               
    dr = densreal[:,50,:]
    dp = np.log10(1+dr)
    
    ind = np.where(np.isnan(dp))
    dp[ind] = densitycutoff
    

    z_min, z_max = densitycutoff, np.max(dp)

    fig0 = plt.figure()
    colax2 = plt.pcolormesh(z, x, dp, cmap='magma', vmin=z_min, vmax=z_max)
    cbar2 = fig0.colorbar(colax2)
    cbar2.set_ticks([densitycutoff,0,z_max])
    cbar2.set_ticklabels([r"$\delta$ = -$\infty$", r"$\delta$ = 0", r"$\delta$ = "+ str(np.around(z_max, 3))])
    cbar2.ax.tick_params(labelsize=24)
    plt.xlabel("$X [$Mpc/h$]$", size=24)
    plt.ylabel("$Z [$Mpc/h$]$", size=24)
    plt.show()


if __name__ == "__main__":
    x, xr, y, z, densrs, densreal = zeldovich_data()
    render_real_pos(x, y, z)
    render_real_dens(densreal)
    render_rs_pos(xr, y, z)
    render_rs_dens(densrs)



