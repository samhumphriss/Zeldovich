import numpy as np
import matplotlib.pyplot as plt
plt.style.use('nuala')
plt.rcParams['xtick.labelsize'] = 22
plt.rcParams['ytick.labelsize'] = 22

import matplotlib.patches as mpatches
import glob

def import_data():
    folder="/gpfs/data/nmccull/zeldovich_out/run180816"
    
    test = np.loadtxt(folder+"/rp_pi.txt")
    rp = test[:,0]
    pi = test[:,1]

    #Monopole Redshift BAO
    monors_results_b = glob.glob(folder+"/with_bao/rs/cf_1d_*")
    monors_test_b = np.loadtxt(monors_results_b[0])
    
    monors_arr_b = np.zeros((len(monors_results_b), len(monors_test_b)))

    i = 0
    for r in monors_results_b:
        temp = np.loadtxt(r)
        monors_arr_b[i] = temp[:,1]
        i += 1

    #2D BAO
    _2d_results_b = glob.glob(folder+"/with_bao/rs/cf_2d_*")
    _2d_test_b    = np.loadtxt(_2d_results_b[0])

    _2d_arr_b = np.zeros((len(_2d_results_b), len(_2d_test_b), len(_2d_test_b)))
    
    i = 0
    for r in _2d_results_b:
        _2d_arr_b[i] = np.loadtxt(r)
        i += 1
    
    #Monopole Redshift No BAO
    monors_results_nb = glob.glob(folder+"/no_bao/rs/cf_1d_*")
    monors_test_nb = np.loadtxt(monors_results_nb[0])
    
    monors_arr_nb = np.zeros((len(monors_results_nb), len(monors_test_nb)))

    i = 0
    for r in monors_results_nb:
        temp = np.loadtxt(r)
        monors_arr_nb[i] = temp[:,1]
        i += 1

    #2D No BAO
    _2d_results_nb = glob.glob(folder+"/no_bao/rs/cf_2d_*")
    _2d_test_nb    = np.loadtxt(_2d_results_nb[0])

    _2d_arr_nb = np.zeros((len(_2d_results_nb), len(_2d_test_nb), len(_2d_test_nb)))
    
    i = 0
    for r in _2d_results_nb:
        _2d_arr_nb[i] = np.loadtxt(r)
        i += 1
    
    return rp, pi, monors_arr_b, monors_arr_nb, _2d_arr_b, _2d_arr_nb

def render_correlation_mean(rp, pi, monors_b, monors_nb, twod_b, twod_nb):
    #Monopole RS BAO  
    mono_rs_b_m   = np.mean(monors_b, axis=0)
    mono_rs_b_err = np.std(monors_b, axis=0)/np.sqrt(len(monors_b)) 

    #Monopole RS NBAO  
    mono_rs_nb_m   = np.mean(monors_nb, axis=0)
    mono_rs_nb_err = np.std(monors_nb, axis=0)/np.sqrt(len(monors_nb))   

    #2D Mean + Error
    twod_b_m   = np.mean(twod_b, axis=0)
    twod_b_err = np.std(twod_b, axis=0)/np.sqrt(len(twod_b))

    twod_nb_m   = np.mean(twod_nb, axis=0)
    twod_nb_err = np.std(twod_nb, axis=0)/np.sqrt(len(twod_nb))
 
    #Transverse BAO
    trans_b_m   = twod_b_m[0,:]
    trans_b_err = twod_b_err[0,:] 

    #Transverse NBAO
    trans_nb_m   = twod_nb_m[0,:]
    trans_nb_err = twod_nb_err[0,:] 

    #LoS BAO
    los_b_m   = twod_b_m[:,0]
    los_b_err = twod_b_err[:,0] 

    #LoS NBAO
    los_nb_m   = twod_nb_m[:,0]
    los_nb_err = twod_nb_err[:,0] 

    #Render
    plt.figure()
    
    p_mrs_b   = plt.plot(rp[0:255], mono_rs_b_m, color='r', lw=2)
    p_trans_b = plt.plot(rp, trans_b_m, color='b', lw=2)
    p_los_b   = plt.plot(pi, los_b_m, color='g', lw=2)

    p_mrs_nb   = plt.plot(rp[0:255], mono_rs_nb_m, color='r', ls='--', lw=2)
    p_trans_nb = plt.plot(rp, trans_nb_m, color='b', ls='--', lw=2)
    p_los_nb   = plt.plot(pi, los_nb_m, color='g', ls='--', lw=2)

    f_mrs_b = plt.fill_between(rp[0:255], mono_rs_b_m-mono_rs_b_err, mono_rs_b_m+mono_rs_b_err, alpha=0.2, color='r')
    f_trans_b = plt.fill_between(rp, trans_b_m-trans_b_err, trans_b_m+trans_b_err, alpha=0.2, color='b')
    f_los_b = plt.fill_between(pi, los_b_m-los_b_err, los_b_m+los_b_err, alpha=0.2, color='g')

    f_mrs_nb = plt.fill_between(rp[0:255], mono_rs_nb_m-mono_rs_nb_err, mono_rs_nb_m+mono_rs_nb_err, alpha=0.2, color='r')
    f_trans_nb = plt.fill_between(rp, trans_nb_m-trans_nb_err, trans_nb_m+trans_nb_err, alpha=0.2, color='b')
    f_los_nb = plt.fill_between(pi, los_nb_m-los_nb_err, los_nb_m+los_nb_err, alpha=0.2, color='g')
    
    plt.axhline(y=0, color='k')
    plt.xlabel("$r [Mpc/h]$", size=24)
    plt.ylabel("$\\xi(r)$", size=28)
    plt.axis([20,180, -0.01, 0.02])

    monoredsArtist = mpatches.Patch(color='r')
    transArtist    = mpatches.Patch(color='b')
    losArtist      = mpatches.Patch(color='g')
    baoArtist      = plt.Line2D((0,1),(0,0),color='k',ls='-')
    nbaoArtist     = plt.Line2D((0,1),(0,0),color='k',ls='--')

    plt.legend([monoredsArtist,transArtist,losArtist,baoArtist,nbaoArtist],["Redshift-space Monopole", "Transverse", "Line of Sight", "With BAO", "Without BAO"], prop={'size':24},loc=1)
    plt.show()

if __name__ == "__main__": 
    rp, pi, monors_arr_b, monors_arr_nb, _2d_arr_b, _2d_arr_nb = import_data()
    render_correlation_mean(rp, pi, monors_arr_b, monors_arr_nb, _2d_arr_b, _2d_arr_nb)

