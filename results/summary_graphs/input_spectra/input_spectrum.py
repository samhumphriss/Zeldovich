import matplotlib.pyplot as plt
plt.style.use('nuala')
plt.rcParams['xtick.labelsize'] = 18
plt.rcParams['ytick.labelsize'] = 18

import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset


def import_pk(name, loc="/cosma/home/durham/rhgk18/ls_structure/pks"):
    pk = loc+"/"+name
    return np.loadtxt(pk)
    
def render_input_spectrum():

    folder = "/cosma/home/durham/rhgk18/ls_structure/pks"
    bao    = folder+"/wig.txt"
    nbao   = folder+"/nowig.txt"

    pkbao  = np.loadtxt(bao)
    pknbao = np.loadtxt(nbao)

    fig, ax = plt.subplots()

    ax.loglog(pkbao[:,0]  ,pkbao[:,1]  , color='r', label='With BAO')
    ax.loglog(pknbao[:,0] ,pknbao[:,1] , color='b', label='Without BAO')
    ax.set_xlabel("Wavenumber, $k$ [$h/Mpc$]", size=28)
    ax.set_ylabel("Power, $P(k)$ [$(Mpc/h)^3$]", size=28)
    ax.legend(prop={'size':28})
    
    axins = zoomed_inset_axes(ax, 5, loc=3)
    axins.loglog(pkbao[:,0]  ,pkbao[:,1]  , color='r', label='iWith BAO')
    axins.loglog(pknbao[:,0] ,pknbao[:,1] , color='b', label='iWithout BAO')

    x1, x2, y1, y2 = 0.02, 0.1, 5000, 30000
    axins.set_xlim(x1, x2)
    axins.set_ylim(y1, y2)

    plt.xticks(visible=False)
    plt.yticks(visible=False)

    mark_inset(ax, axins, loc1=2, loc2=1, fc="none", ec="0.5")

    
    plt.show()

if __name__ == "__main__":
    render_input_spectrum()
    
