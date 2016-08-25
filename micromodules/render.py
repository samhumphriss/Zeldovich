import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.colors import LogNorm
from itertools import product, combinations
import glob
import os
import numpy as np
import spatial_stats as ss

def xi2d_fromfile(folder, seed):
    rp = np.loadtxt(folder+"/rp.txt")
    pi = np.loadtxt(folder+"/pi.txt")
    xi2d = np.loadtxt(folder+"/xi2d_SEED_"+str(seed)+".txt")

    plt.figure()
    plt.pcolormesh(rp, pi, np.arcsinh(300*xi2d), cmap = 'magma')
    plt.axes().set_aspect('equal')
    plt.show()

def xi2d_slices(folder, search):
    results = glob.glob(os.path.join(folder, search))

    a = 0
    c = 0
    for r in results:
        a += np.loadtxt(r)
        c += 1

    xi2d = a/c

    rp = np.loadtxt(folder+"/rp.txt")
    pi = np.loadtxt(folder+"/pi.txt")
    #Prunes data above rp = 200 Mpc
    rp_ind = np.where(rp<201.0)
    rp = rp[rp_ind]
    pi = pi[rp_ind]
    xi2d = xi2d[0:rp_ind[0].max()+1, 0:rp_ind[0].max()+1]

    fig0 = plt.figure()
    ax1 = fig0.add_subplot(221, aspect='equal')
    ax1.pcolormesh(rp, pi, np.arcsinh(300*xi2d), cmap = 'magma')
    ax1.axis([3,200,3,200])
    ax1.set_title("2D Correlation Plot")
    ax1.set_xlabel("$R_p$ /Mpc")
    ax1.set_ylabel("$\\Pi$ /Mpc")

    ax2 = fig0.add_subplot(223)
    ax2.plot(rp, rp**2*xi2d[:,0])
    ax2.set_xlabel("$\\Pi$ /Mpc")
    ax2.set_ylabel("$R^2\\xi(R)$")
    ax2.set_title("Line-of-sight")   

    ax3 = fig0.add_subplot(224)
    ax3.plot(pi, pi**2*xi2d[0,:])
    ax3.set_xlabel("$R_p$ /Mpc")
    ax3.set_ylabel("$R^2\\xi(R)$")
    ax3.set_title("Tranverse")

    plt.show()


def xi_covariance(folder, search):

    b_results = glob.glob(os.path.join(folder+"/bao", search))
    
    b_test = np.loadtxt(b_results[0])
    b_arr = np.zeros((len(b_results),len(b_test)))
    
    for ind in range(len(b_results)):
        b_arr[ind] = np.loadtxt(b_results[ind])

    n_results = glob.glob(os.path.join(folder+"/nobao", search))
    
    n_test = np.loadtxt(n_results[0])
    n_arr = np.zeros((len(n_results),len(n_test)))
    
    for ind in range(len(n_results)):
        n_arr[ind] = np.loadtxt(n_results[ind])
    
    b_covar = np.cov(b_arr, rowvar=False)
    n_covar = np.cov(n_arr, rowvar=False)
    b_corr  = np.corrcoef(b_arr, rowvar=False)
    n_corr  = np.corrcoef(n_arr, rowvar=False)

    r = np.loadtxt(folder+"/bao/r.txt")

    r_ind = np.where(r<200.0)
    r = r[r_ind]
    b_corr = b_corr[0:r_ind[0].max()+1, 0:r_ind[0].max()+1]
    n_corr = n_corr[0:r_ind[0].max()+1, 0:r_ind[0].max()+1] 
    b_covar= b_covar[0:r_ind[0].max()+1, 0:r_ind[0].max()+1]
    n_covar= n_covar[0:r_ind[0].max()+1, 0:r_ind[0].max()+1] 

    fig0 = plt.figure()

    ax1 = fig0.add_subplot(121, aspect='equal')
    divider = make_axes_locatable(ax1)
    cax = divider.append_axes("right", size="5%", pad=0.05)

    ax1.axhline(y=107, xmin=0, xmax=200, c='k', alpha=0.7)
    ax1.axvline(x=107, ymin=0, ymax=200, c='k', alpha=0.7)

    col1 = ax1.pcolormesh(r,r,b_corr, vmin=b_corr.min(), vmax=b_corr.max(),  cmap='rainbow')
    plt.colorbar(col1, cax = cax)
    ax1.set_title('With BAO')
    ax1.set_xlabel("$R$")
    ax1.set_ylabel("$R$")
    ax1.text(20, 109, 'BAO', color='k', alpha=0.7)

    ax2 = fig0.add_subplot(122, aspect='equal')
    divider = make_axes_locatable(ax2)
    cax = divider.append_axes("right", size="5%", pad=0.05)

    ax2.axhline(y=107, xmin=0, xmax=200,c= 'k', alpha=0.7)
    ax2.axvline(x=107, ymin=0, ymax=200, c='k', alpha=0.7)

    col2 = ax2.pcolormesh(r,r,n_corr, vmin=b_corr.min(), vmax=b_corr.max(), cmap='rainbow')
    plt.colorbar(col2, cax = cax)
    ax2.set_title('Without BAO')
    ax2.set_xlabel("$R$")
    ax2.set_ylabel("$R$")
    ax2.text(20, 109, 'BAO', color='k', alpha=0.7)


    fig0.suptitle("Comparing the Pearson matrices of the 1D averaged correlation function with and without BAO")
    plt.show()


def xi2d_covariance(folder):
    search = "xi2d_*"

    b_results = glob.glob(os.path.join(folder+"/bao", search))
    b_test = np.loadtxt(b_results[0])

    trials = len(b_results)
    dim = len(b_test)
    b_arr = np.zeros((trials, dim, dim))
    c = 0

    for r in b_results:
        b_arr[c] = np.loadtxt(r)
        c += 1


    n_results = glob.glob(os.path.join(folder+"/nobao", search))
    n_test = np.loadtxt(n_results[0])

    n_arr = np.zeros((len(n_results),len(n_test)))
    c = 0
    for r in n_results:
        n_arr[c] = np.loadtxt(r)
        c += 1

    covar = np.cov(b_xi2d, n_xi2d)
    corr  = np.corrcoef(n_xi2d, b_xi2d)
    return covar

def xi_resid(folder, search):
    fig0 = plt.figure(0)

    frame1 = fig0.add_axes((.1,.3,.8,.6))
    frame2 = fig0.add_axes((.1,.1,.8,.2))

    #Plot
    results = glob.glob(os.path.join(folder+"/nobao", search))
    r = np.loadtxt(folder+"/nobao/r.txt")
    test = np.loadtxt(results[0])
   
    r_ind = np.where(r<=200.0)
    r = r[r_ind]

    arr = np.zeros((len(results),len(test)))
    
    for ind in range(len(results)):
        arr[ind] = np.loadtxt(results[ind])

    subset = np.random.permutation(arr)
    subset = subset[0:20]

    arr_mean = np.mean(arr, axis=0)
    frame1.plot(r, r**2*arr_mean[r_ind], linewidth = 2.5, color='k')

    for sub in subset:
        frame1.plot(r, r**2*sub[r_ind], alpha=0.4)
    
    frame1.set_xticklabels([])
    frame1.set_yticks(range(-10, 60, 10))
    frame1.set_ylabel("$\\xi (R)$", rotation = 90, size=16)
    frame1.set_title("Resultant Correlation Function (300 trials): Angular Average")
    frame1.axvline(x=107, ymin=-20,ymax=70, color='k')
    frame1.text(107, 45, "BAO", rotation=270, alpha=0.7, color='k')
    frame1.grid()

    std = np.std(arr, axis = 0)
    std = std[r_ind]
    nstd = -std
    frame2.plot(r, r**2*std, 'r--')
    frame2.plot(r, r**2*nstd, 'r--')
    frame2.axhline(y=0, xmin=0, xmax=200, color='k', alpha=0.5, lw = 1)
    frame2.set_yticks([-2,-1,0,1,2])
    frame2.set_xlabel("$R /Mpc$", size=16)
    frame2.set_ylabel("Standard Deviation", rotation = 90, size=13)
    frame2.axvline(x=107, ymin=-4, ymax=4, color='k')
    frame2.grid()

    plt.show()



def import_data(folder, search, cutoff):

    results = glob.glob(os.path.join(folder, search))
    test = np.loadtxt(results[0])

    if search == "xi_*":
        r = np.loadtxt(folder+"/r.txt")
    
        r_ind = np.where(r <= cutoff)
        r = r[r_ind]

        arr = np.zeros((len(results),len(test)))
    
        for ind in range(len(results)):
            arr[ind] = np.loadtxt(results[ind])
            
        arr = arr[:, r_ind[0]]
        return r, arr
    
    if search == "xi2d_*":
        rp = np.loadtxt(folder+"/rp.txt")
        pi = np.loadtxt(folder+"/pi.txt")
   
        rp_ind = np.where(rp<=cutoff)
        rp = rp[rp_ind]
        pi = pi[rp_ind]

        arr = np.zeros((len(results), len(test), len(test)))
    
        for ind in range(len(results)):
            arr[ind] = np.loadtxt(results[ind])

        rp = rp[rp_ind]
        pi = pi[rp_ind]
        arr = arr[0:rp_ind[0].max()+1, 0:rp_ind[0].max()+1]
        return rp, pi, arr
    
    return -42

def meeting_plot(folder):
    print "meeting_plot()"
    plt.figure()
    
    bao_fol  = folder+"/bao"
    nbao_fol = folder+"/nobao"

    xi_search   = "xi_*"
    xi2d_search = "xi2d_*"

    print "importing xi..."
    r, xi_arr_bao  = import_data( bao_fol, xi_search, 200)
    r, xi_arr_nbao = import_data(nbao_fol, xi_search, 200)

    
#    print "importing xi2d..."
#    rp, pi, xi2d_arr_bao  = import_data( bao_fol, xi2d_search, 200)
#    rp, pi, xi2d_arr_nbao = import_data(nbao_fol, xi2d_search, 200)

    #Angular Average (/w RSD)
    print "calculating angular average /w RSD..."
    m_xi_bao  = np.mean(xi_arr_bao, axis = 0)
    m_xi_nbao = np.mean(xi_arr_nbao, axis = 0)
#    print "shape m_xi, ", str(np.shape(m_xi_bao))

    print "plotting..."
    plt.plot(r, r**2*m_xi_bao, label='m_xi_rsd_bao')
    plt.plot(r, r**2*m_xi_nbao, label='m_xi_rsd_nbao')

    #Angular Average (w/o RSD)

    #Transverse

    #Line of Sight
    
    plt.legend(['m_xi_rsd_bao', 'm_xi_rsd_nbao'], ['Mean $\\xi (R)$, RSD, BAO','Mean $\\xi (R)$, RSD, No BAO'])
    plt.show()






def xi_mean(folder):
    search = "xi_*"

    b_results = glob.glob(os.path.join(folder+"/bao", search))
    
    b_test = np.loadtxt(b_results[0])
    b_arr = np.zeros((len(b_results),len(b_test)))
    
    for ind in range(len(b_results)):
        b_arr[ind] = np.loadtxt(b_results[ind])

    subset = np.random.permutation(b_arr)
    subset = subset[0:50]
    
    r = np.loadtxt(folder+"/bao/r.txt")
    
    r_ind = np.where(r<=200.0)
    r = r[r_ind]
 
    fig0 = plt.figure()
    ax1 = fig0.add_subplot(121)

    for sub in subset:
        ax1.plot(r, r**2*sub[r_ind], alpha = 0.7)
         
    xi_mean = np.mean(b_arr, axis = 0)
    xi_stderr = np.std(b_arr, axis = 0)

    ax1.errorbar(r, r**2*xi_mean[r_ind], yerr=r**2*xi_stderr[r_ind], color='k', alpha=0.7)
    ax1.set_xlabel("$R$ /Mpc")
    ax1.set_ylabel("$R^2\\xi(R)$")

    ax2 = fig0.add_subplot(122)

    n_results = glob.glob(os.path.join(folder+"/nobao", search))
    
    n_test = np.loadtxt(n_results[0])
    n_arr = np.zeros((len(n_results),len(n_test)))
    
    for ind in range(len(n_results)):
        n_arr[ind] = np.loadtxt(n_results[ind])

    subset = np.random.permutation(n_arr)
    subset = subset[0:10]
 
    ax1 = fig0.add_subplot(121)

    for sub in subset:
        ax2.plot(r, r**2*sub[r_ind], alpha = 0.7)

    xi_mean = np.mean(n_arr, axis = 0)
    xi_stderr = np.std(n_arr, axis = 0)

    ax2.errorbar(r, r**2*xi_mean[r_ind], yerr=r**2*xi_stderr[r_ind], color='k', alpha=0.7)
    ax2.set_xlabel("$R$ /Mpc")
    ax2.set_ylabel("$R^2\\xi(R)$")

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
