import numpy as np
import matplotlib.pyplot as plt
plt.style.use('nuala')
plt.rcParams['xtick.labelsize'] = 22
plt.rcParams['ytick.labelsize'] = 22

import glob

def import_data():
    folder="/gpfs/data/nmccull/zeldovich_out/run180816"
    
    test = np.loadtxt(folder+"/rp_pi.txt")
    rp = test[:,0]
    pi = test[:,1]

    #Monopole
    mono_results = glob.glob(folder+"/with_bao/rs/cf_1d_*")
    mono_test = np.loadtxt(mono_results[0])
    
    mono_arr = np.zeros((len(mono_results), len(mono_test)))

    i = 0
    for r in mono_results:
        temp = np.loadtxt(r)
        mono_arr[i] = temp[:,1]
        i += 1
    
    _2d_results = glob.glob(folder+"/with_bao/rs/cf_2d_*")
    _2d_test    = np.loadtxt(_2d_results[0])

    _2d_arr = np.zeros((len(_2d_results), len(_2d_test), len(_2d_test)))
    
    i = 0
    for r in _2d_results:
        _2d_arr[i] = np.loadtxt(r)
        i += 1
    
    return rp, pi, mono_arr, _2d_arr
     

def render_correlation_spread(rp, pi, m_arr, _2d_arr):
    mono_subset = np.random.permutation(m_arr)
    mono_subset = mono_subset[0:20]
    
    _2d_subset   = np.random.permutation(_2d_arr)
    _2d_subset   = _2d_subset[0:20]

    mono_mean       = np.mean(m_arr  , axis = 0)
    transverse_mean = np.mean(_2d_arr[:,0,:], axis = 0)
    los_mean        = np.mean(_2d_arr[:,:,0], axis = 0)

    plt.figure()
    
    #Monopole
    plt.plot(rp[0:255], mono_mean, color='r', lw=2)

    for i in mono_subset:
        plt.plot(rp[0:255], i, color='r', lw=1, alpha=0.3)

    
    #Transverse 
    plt.plot(rp, transverse_mean, color='b', lw=2)

    for i in _2d_subset:
        plt.plot(rp, i[0,:], color='b', lw=1, alpha=0.3)

    #LoS
    plt.plot(pi, los_mean, color='g', lw=2)

    for i in _2d_subset:
        plt.plot(pi, i[:,0], color='g', lw=1, alpha=0.3)

    monoArtist  = plt.Line2D((0,1),(0,0), color='r', lw=2, ls='-')
    transArtist = plt.Line2D((0,1),(0,0), color='b', lw=2, ls='-')
    losArtist   = plt.Line2D((0,1),(0,0), color='g', lw=2, ls='-')

    plt.axhline(y=0, color='k', lw=2)
    plt.xlabel("$r [Mpc/h]$", size =24)
    plt.ylabel("$\\xi(r)$", size = 28)
    plt.legend([monoArtist, transArtist, losArtist],["Redshift-space Monopole", "Transverse", "Line of Sight"], prop={'size':24})
    plt.axis([20, 180, -0.01, 0.02])
    plt.show()
    
    
if __name__ == "__main__":
    rp, pi, mono_arr, _2d_arr = import_data()
    render_correlation_spread(rp, pi, mono_arr, _2d_arr)
