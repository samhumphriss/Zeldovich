import numpy as np
import matplotlib.pyplot as plt
import glob

def import_data():
    folder = "/gpfs/data/nmccull/zeldovich_out/run_f0.6"

    tmp = np.loadtxt(folder+"/rp_pi.txt")
    pi = tmp[:,1]

    results = glob.glob(folder+"/with_bao/rs/cf_2d_*")
    test = np.loadtxt(results[0])

    arr = np.zeros((len(results), len(test), len(test)))    

    i = 0
    for r in results:
        arr[i] = np.loadtxt(r)
        i += 1

    los_arr = arr[:,:,0]
    
    return pi, los_arr

def min_search(low, high, pi, xi):
    ind = np.where((pi>low)&(pi<high))
    return np.sum(pi[ind]*(xi[ind]))/np.sum(xi[ind])

def render_trough_hunt(pi, los_arr):
    subset = np.random.permutation(los_arr)
    subset = subset[0:10]

    plt.figure()
    #cmap = plt.cm.rainbow
    #carr = [cmap(i) for i in np.linspace(0, 0.9, 10)]
    carr = []
    i = 0
    for s in subset:
        a = plt.plot(pi, s, lw=1)
        xi = min_search(40, 100, pi, s**10)
        plt.axvline(x=xi, color=a[0].get_color(), lw=1.5, ls='--')
        i += 1


    plt.grid()
    plt.axhline(y=0, color='k')
    plt.xlabel("$R [Mpc/h]$", size=24)
    plt.ylabel("$\\xi(R)$", size=24)
    plt.axis([20, 180, -0.015, 0.01])

    realiseArtist = plt.Line2D((0,1),(0,0), color='k', lw=1, ls='-')
    posArtist     = plt.Line2D((0,1),(0,0), color='k', lw=1.5, ls='--')

    plt.legend([realiseArtist, posArtist],["Individual Realisation ($\\gamma = 0.392$)", "Calculated Position of Minimum"], prop={'size':18}, loc=1)
    plt.show()

if __name__ == "__main__":
    pi, los_arr = import_data()
    render_trough_hunt(pi, los_arr)
