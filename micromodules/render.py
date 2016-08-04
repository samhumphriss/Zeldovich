import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.colors import LogNorm
from itertools import product, combinations
import numpy as np
import spatial_stats as ss

#result = ic.main(args.redshift, pk, boxsize=args.boxsize, ngrid=args.ngrid, trand=args.truerand)

def xi2d_fromfile(folder, seed):
    rp = np.loadtxt(folder+"/rp.txt")
    pi = np.loadtxt(folder+"/pi.txt")
    xi2d = np.loadtxt(folder+"/xi2d_SEED_"+str(seed)+".txt")

    plt.figure()
    plt.plot(rp, pi, np.arcsinh(300*xi2d), cmap = 'magma')
    plt.axes().set_aspect('equal')
    plt.show()


def pk_render(pk):
    plt.figure()
    
    plt.loglog(pk[:,0], pk[:,1], 'g-')
    plt.show()

def full_data_render(result, densr, densz, pk, slice_depth, boxsize, ngrid):

    #Runtime Parameters
    bs = boxsize
    sp = boxsize/2
    sd = slice_depth
    dg = ngrid

    fig0 = plt.figure()
    
    #3D Slice Boundary Render
    ax1 = fig0.add_subplot(231, projection = "3d")
    
    X = result[0]
    Y = result[1]
    Z = result[2]
    
    rs = np.random.RandomState(123456)
    X = np.random.permutation(X)
    
    rs = np.random.RandomState(123456)
    Y = np.random.permutation(Y)
    
    rs = np.random.RandomState(123456)
    Z =np.random.permutation(Z)
    
    ax1.plot(X[:4000],Y[:4000], Z[:4000], 'bo', markersize = 1)   
    

    
    x = np.linspace(0, bs, 30)
    y = np.linspace(sp, sp+sd, 10)
    z = np.linspace(0, bs, 30)

    x1,z1= np.meshgrid(x,z)
    y11 = np.ones_like(x1)*sp
    y12 = np.ones_like(x1)*(sp+sd)
    x2,y2= np.meshgrid(x,y)
    z21 = np.ones_like(x2)*0
    z22 = np.ones_like(x2)*bs
    y3,z3= np.meshgrid(y,z)
    x31 = np.ones_like(y3)*0
    x32 = np.ones_like(y3)*bs
    
    ax1.plot_wireframe(x1, y11, z1, color='r', rstride=1, cstride=1, alpha=0.5)
    ax1.plot_wireframe(x1, y12, z1, color='r', rstride=1, cstride=1, alpha=0.5)
    ax1.plot_wireframe(x2, y2, z21, color='r', rstride=1, cstride=1, alpha=0.5)
    ax1.plot_wireframe(x2, y2, z22, color='r', rstride=1, cstride=1, alpha=0.5)
    ax1.plot_wireframe(x31, y3, z3, color='r', rstride=1, cstride=1, alpha=0.5)
    ax1.plot_wireframe(x32, y3, z3, color='r', rstride=1, cstride=1, alpha=0.5)
    
    ax1.set_xlabel("X /MPc")
    ax1.set_ylabel("Y /Mpc")
    ax1.set_zlabel("Z /Mpc")
    ax1.set_title("Full-Volume Render")


    #Real Space Cross-section, PLOT2                                  
    indices = []
    for a in xrange(len(result[1])):
    	if(result[1][a] > sp and result[1][a] < sp + sd):
        	indices.append(a)
    
    x = result[0][indices]
    z = result[2][indices]
    
    ax2 = fig0.add_subplot(232)
    ax2.plot(x,z, 'bo', markersize = 1)
    ax2.set_title("XZ / Real Space")
    ax2.set_xlabel("X /MPc")
    ax2.set_ylabel("Z /MPc")
    ax2.set_xlim([0,bs])
    ax2.set_ylim([0,bs])

    #+++++++++++++++++++++
    densitycutoff = -0.8
    #+++++++++++++++++++++

    #Real Space Density Map, PLOT 3
    x, z = np.mgrid[0:dg+1,0:dg+1]
               
    dr = densr[:,int(dg*float(sp)/float(bs)),:]
    dp = np.log10(1+dr)
    
    ind = np.where(np.isnan(dp))
    dp[ind] = densitycutoff
    

    z_min, z_max = densitycutoff, np.max(dp)

    ax3 = fig0.add_subplot(233)
    colax3 = ax3.pcolor(x*bs/dg, z*bs/dg, dp, cmap='magma', vmin=z_min, vmax=z_max)
    cbar3 = fig0.colorbar(colax3)
    cbar3.set_ticks([densitycutoff,0,z_max])
    cbar3.set_ticklabels([r"$\rho$ = -$\infty$", r"$\rho$ = 0", r"$\rho$ = "+ str(np.around(z_max, 3))])
    
    
    #POWER SPECTRUM, PLOT 4
    ax4  = fig0.add_subplot(234)
    ax4.loglog(pk[:,0], pk[:,1], 'g-')
    ax4.set_xlabel("Wavenumber, k")
    ax4.set_ylabel("Power, P(k)")
    ax4.set_title("Power Spectrum")
    

    #Z-Space Cross-section, PLOT 5                                 
    indices = []
    for a in xrange(len(result[1])):
    	if(result[4][a] > sp and result[4][a] < sp + sd):
        	indices.append(a)
    
    x = result[3][indices]
    z = result[5][indices]
    
    ax5 = fig0.add_subplot(235)
    ax5.plot(x,z, 'bo', markersize = 1)
    ax5.set_title("XZ / Redshift Space")
    ax5.set_xlabel("X /MPc")
    ax5.set_ylabel("Z /MPc")
    ax5.set_xlim([0,bs])
    ax5.set_ylim([0,bs])


    #Z-Space Density Map, PLOT 6
    x, z = np.mgrid[0:dg+1,0:dg+1]
               
    dz = densz[:,int(dg*float(sp)/float(bs)),:]
    dzp = np.log10(1+dz)

    ind = np.where(np.isnan(dzp))
    dzp[ind] = densitycutoff

    z_min, z_max = densitycutoff, np.max(dzp)

    ax6 = fig0.add_subplot(236)
    colax6 = ax6.pcolor(x*bs/dg, z*bs/dg, dzp, cmap='magma', vmin=z_min, vmax=z_max)
    cbar6 = fig0.colorbar(colax6)
    cbar6.set_ticks([densitycutoff,0,z_max])
    cbar6.set_ticklabels([r"$\rho$ = -$\infty$", r"$\rho$ = 0", r"$\rho$ = "+ str(np.around(z_max, 3))])

    #Correlation Function
    fig1 = plt.figure()
    ax6 = fig1.add_subplot(211)

    #Makes the density grid compatible with SS
    dens = np.swapaxes(densr, 2, 0)

    r, xi=ss.getXi(dens, nrbins=dg/2, boxsize=bs, get2d=False, deconvolve_cic=True, exp_smooth=0.0)
    ax6.plot(r, r**2*xi)

    ax7 = fig1.add_subplot(212)

    rp, pi, xi2d=ss.getXi(dens, nrbins=dg/2, boxsize=bs, get2d=True, deconvolve_cic=True, exp_smooth=0.0)

    colax = ax7.pcolormesh(rp, pi, np.arcsinh(xi2d*300.0), cmap='magma')
    ax7.set_xlim([0, bs/2])
    ax7.set_ylim([0, bs/2])
    fig1.colorbar(colax)
    plt.show()

if "__name__" == "__main__":
    plt.show()
