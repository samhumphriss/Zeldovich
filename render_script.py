import micromodules.fileio as io
import micromodules.render as rd
import numpy as np
import glob
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def import_data(folder, search, cutoff):

    results = glob.glob(os.path.join(folder, search))
    test = np.loadtxt(results[0])

    if search == "xi_*":
        r = np.loadtxt(folder+"/r.txt")
        arr = np.zeros((len(results),len(test)))
    
        for ind in range(len(results)):
            arr[ind] = np.loadtxt(results[ind])

        return r, arr
    
    if search == "xi2d_*":
        rp = np.loadtxt(folder+"/rp.txt")
        pi = np.loadtxt(folder+"/pi.txt")
        arr = np.zeros((len(results), len(test), len(test)))
    
        for ind in range(len(results)):
            arr[ind] = np.loadtxt(results[ind])

        return rp, pi, arr
    
    return -42

def meeting_plot(folder):
    print "meeting_plot()"
    plt.figure()
    
    bao_fol  = folder+"/bao"
    nbao_fol = folder+"/nobao"

    xi_search   = "xi_*"
    xi2d_search = "xi2d_*"

    print "importing xirsd..."
    r, xi_rsd_bao  = import_data( bao_fol, xi_search, 200)
    r, xi_rsd_nbao = import_data(nbao_fol, xi_search, 200)
    
    real_fol = "/gpfs/data/rhgk18/results/R_b1024_ng512_np1024"

    print "importing xireal..."
    r, xi_real_bao = import_data( real_fol+"/bao", xi_search, 200)
    r, xi_real_nbao= import_data( real_fol+"/nobao", xi_search, 200)
    

    #Angular Average (/w RSD)
    print "calculating angular average /w RSD..."
    m_xi_bao_rsd   = np.mean(xi_rsd_bao, axis = 0)
    xi_bao_rsd_err = np.std(xi_rsd_bao, axis = 0)/np.sqrt(len(xi_rsd_bao))

    m_xi_nbao_rsd   = np.mean(xi_rsd_nbao, axis = 0)
    xi_nbao_rsd_err = np.std(xi_rsd_nbao, axis = 0)/np.sqrt(len(xi_rsd_nbao))


    print "plotting..."
#    p1  = plt.errorbar(r, r**2*m_xi_bao_rsd, yerr=r**2*xi_bao_rsd_err ,label='RSD, BAO', color = 'r', linestyle='-')
    p1  = plt.plot(r, m_xi_bao_rsd, label='RSD, BAO', color = 'r', linestyle='-')
    p1e = plt.fill_between(r, m_xi_bao_rsd-xi_bao_rsd_err, m_xi_bao_rsd+xi_bao_rsd_err, alpha=0.2, color='r')
#    p2  = plt.errorbar(r, r**2*m_xi_nbao_rsd, yerr=r**2*xi_nbao_rsd_err, label='RSD, No BAO', color='r', linestyle='--')
    p2  = plt.plot(r, m_xi_nbao_rsd, label='RSD, No BAO', color='r', linestyle='--')
    p2e = plt.fill_between(r, m_xi_nbao_rsd-xi_nbao_rsd_err, m_xi_nbao_rsd+xi_nbao_rsd_err, alpha=0.2, color='r')


    #Angular Average (w/o RSD)
    print "calculating angular average w/o RSD..."
    m_xi_bao_real  = np.mean(xi_real_bao, axis = 0)
    xi_bao_real_err = np.std(xi_real_bao, axis = 0)/np.sqrt(len(xi_real_bao))

    m_xi_nbao_real = np.mean(xi_real_nbao, axis = 0)
    xi_nbao_real_err = np.std(xi_real_nbao, axis = 0)/np.sqrt(len(xi_real_nbao))

    print "plotting..."
    p3  = plt.plot(r, m_xi_bao_real, 'b-', label='Real, BAO')
    p3e = plt.fill_between(r, m_xi_bao_real-xi_bao_real_err, m_xi_bao_real+xi_bao_real_err, alpha=0.2, color='b')

    p4  = plt.plot(r, m_xi_nbao_real, 'b--', label='Real, No BAO')
    p4e = plt.fill_between(r, m_xi_nbao_real-xi_nbao_real_err, m_xi_nbao_real+xi_nbao_real_err, alpha=0.2, color='b')

    if True:
        print "importing xi2d..."
        rp, pi, xi2d_rsd_bao  = import_data( bao_fol, xi2d_search, 200)
        rp, pi, xi2d_rsd_nbao = import_data(nbao_fol, xi2d_search, 200)

        print "calculating the mean 2D correlation function..."
        m_xi2d_bao_rsd  = np.mean(xi2d_rsd_bao , axis = 0)
        xi2d_bao_rsd_err= np.std(xi2d_rsd_bao, axis = 0)/np.sqrt(len(xi2d_rsd_bao))
        m_xi2d_nbao_rsd = np.mean(xi2d_rsd_nbao, axis = 0)
        xi2d_nbao_rsd_err= np.std(xi2d_rsd_bao, axis = 0)/np.sqrt(len(xi2d_rsd_nbao))   

        #Transverse
        print "plotting..."
#        p5 = plt.errorbar(rp, rp**2*m_xi2d_bao_rsd[:,0], yerr=rp**2*xi2d_bao_rsd_err[:,0], label="XI2D Transverse, RSD, BAO", color='g', linestyle='-')
        p5 = plt.plot(rp, m_xi2d_bao_rsd[:,0], label="XI2D Transverse, RSD, BAO", color='g', linestyle='-')
        p5e = plt.fill_between(rp, m_xi2d_bao_rsd[:,0]-xi2d_bao_rsd_err[:,0], m_xi2d_bao_rsd[:,0]+xi2d_bao_rsd_err[:,0], alpha=0.2, color='g')

        p6 = plt.plot(rp, m_xi2d_nbao_rsd[:,0], label="XI2D Transverse, RSD, No BAO", color='g', linestyle='--')
        p6e = plt.fill_between(rp, m_xi2d_nbao_rsd[:,0]-xi2d_nbao_rsd_err[:,0], m_xi2d_nbao_rsd[:,0]+xi2d_nbao_rsd_err[:,0], alpha=0.2, color='g')
#        p6 = plt.errorbar(rp, rp**2*m_xi2d_nbao_rsd[:,0], yerr=rp**2*xi2d_nbao_rsd_err[:,0], label="XI2D Transverse, RSD, No BAO", color='g', linestyle='--')

        #Line of Sight
#        p7 = plt.errorbar(pi, pi**2*m_xi2d_bao_rsd[0,:], yerr=pi**2*xi2d_bao_rsd_err[0,:], label ="XI2D LoS, RSD, BAO", color='c', linestyle='-')
        p7 = plt.plot(pi, m_xi2d_bao_rsd[0,:],label="XI2D LoS, RSD, BAO",color='c',linestyle='-')
        p7e = plt.fill_between(pi, m_xi2d_bao_rsd[0,:]-xi2d_bao_rsd_err[0,:], m_xi2d_bao_rsd[0,:]+xi2d_bao_rsd_err[0,:], alpha=0.2, color='c')

        p8 = plt.plot(pi, m_xi2d_nbao_rsd[0,:],label="XI2D LoS, RSD, No BAO",color='c',linestyle='--')
        p8e = plt.fill_between(pi, m_xi2d_nbao_rsd[0,:]-xi2d_nbao_rsd_err[0,:], m_xi2d_nbao_rsd[0,:]+xi2d_nbao_rsd_err[0,:], alpha=0.2, color='c')
#        p8 = plt.errorbar(pi, pi**2*m_xi2d_nbao_rsd[0,:], yerr=pi**2*xi2d_nbao_rsd_err[0,:], label="XI2D LoS, RSD, No BAO", color='c', linestyle='--')

    rsdArtist  = mpatches.Patch(color='red')
    realArtist = mpatches.Patch(color='blue')
    transArtist= mpatches.Patch(color='cyan')
    losArtist  = mpatches.Patch(color='green')
    baoArtist  = plt.Line2D((0,1),(0,0), color='k', linestyle='-')
    nbaoArtist = plt.Line2D((0,1),(0,0), color='k', linestyle='--')

    plt.xlabel("$R [Mpc/h]$", size = 16)
    plt.ylabel("$\\xi (R)$", size = 16)
    plt.title("Correllation function for Real and Redshift space, with and without the BAO")
    plt.legend([rsdArtist, realArtist, transArtist, losArtist, baoArtist, nbaoArtist], ["Redshift Space", "Real Space", "Redshift Space Transverse", "Redshift Space Line of Sight", "With BAO", "Without BAO"], prop={'size':13})
    plt.axis([30,200,-0.007,0.01])
    plt.show()

#--------------------------------------------------------------------------------
#=================================================================================
#---------------------------------------------------------------------------------

def meeting_plot_xidiff_unscale(folder):
    print "xidiff_unscale()"
    plt.figure()
    
    bao_fol  = folder+"/bao"
    nbao_fol = folder+"/nobao"
#    bao_fol  = folder+"/with_bao"
#    nbao_fol = folder+"/no_bao"

    xi_search   = "xi_*"
    xi2d_search = "xi2d_*"
#    xi_search   = "cf_1d*"
#    xi2d_search = "cf_2d*"

    print "importing xirsd..."
    r, xi_rsd_bao  = import_data( bao_fol, xi_search, 200)
    r, xi_rsd_nbao = import_data(nbao_fol, xi_search, 200)
    
    real_fol = "/gpfs/data/rhgk18/results/R_b1024_ng512_np1024"

    print "importing xireal..."
    r, xi_real_bao = import_data( real_fol+"/bao", xi_search, 200)
    r, xi_real_nbao= import_data( real_fol+"/nobao", xi_search, 200)
    

    #Angular Average (/w RSD)
    print "calculating angular average /w RSD..."
    xi_rsd_diff     = xi_rsd_bao-xi_rsd_nbao
    m_xi_rsd_diff   = np.mean(xi_rsd_diff, axis=0)
    xi_rsd_diff_err = np.std(xi_rsd_diff, axis = 0)/np.sqrt(len(xi_rsd_diff))


    print "plotting..."

    p1  = plt.plot(r, m_xi_rsd_diff, label='RSD', color = 'r', linestyle='-')
    p1e = plt.fill_between(r, m_xi_rsd_diff-xi_rsd_diff_err, m_xi_rsd_diff+xi_rsd_diff_err, alpha=0.2, color='r')



    #Angular Average (w/o RSD)
    print "calculating angular average w/o RSD..."
    xi_real_diff     = xi_real_bao-xi_real_nbao
    m_xi_real_diff   = np.mean(xi_real_diff, axis=0)
    xi_real_diff_err = np.std(xi_real_diff, axis = 0)/np.sqrt(len(xi_real_diff))


    print "plotting..."
    p2  = plt.plot(r, m_xi_real_diff, 'b-', label='Real')
    p2e = plt.fill_between(r, m_xi_real_diff-xi_real_diff_err, m_xi_real_diff+xi_real_diff_err, alpha=0.2, color='b')


    if True:
        print "importing xi2d..."
#        temp_ = np.loadtxt(folder+"/rp_pi.txt")
#        rp = temp_[:,0]
#        pi = temp_[:,1]

        rp, pi, xi2d_rsd_bao  = import_data( bao_fol, xi2d_search, 200)
        rp, pi, xi2d_rsd_nbao = import_data(nbao_fol, xi2d_search, 200)

        print "calculating the mean 2D correlation function..."
        xi2d_rsd_diff    = xi2d_rsd_bao-xi2d_rsd_nbao
        m_xi2d_rsd_diff  = np.mean(xi2d_rsd_diff, axis=0)
        xi2d_rsd_diff_err= np.std(xi2d_rsd_diff, axis = 0)/np.sqrt(len(xi2d_rsd_diff))
 

        #Transverse
        print "plotting..."
        p3 = plt.plot(rp, m_xi2d_rsd_diff[:,0], label="XI2D LoS, RSD", color='g', linestyle='-')
        p3e = plt.fill_between(rp, m_xi2d_rsd_diff[:,0]-xi2d_rsd_diff_err[:,0], m_xi2d_rsd_diff[:,0]+xi2d_rsd_diff_err[:,0], alpha=0.2, color='g')


        #Line of Sight
        p7 = plt.plot(pi, m_xi2d_rsd_diff[0,:],label="XI2D Transverse, RSD, BAO",color='c',linestyle='-')
        p7e = plt.fill_between(pi, m_xi2d_rsd_diff[0,:]-xi2d_rsd_diff_err[0,:], m_xi2d_rsd_diff[0,:]+xi2d_rsd_diff_err[0,:], alpha=0.2, color='c')

    plt.axhline(y=0, xmin=0, xmax=130, color='k', alpha=0.5)
    rsdArtist  = mpatches.Patch(color='red')
    realArtist = mpatches.Patch(color='blue')
    transArtist= mpatches.Patch(color='cyan')
    losArtist  = mpatches.Patch(color='green')
    baoArtist  = plt.Line2D((0,1),(0,0), color='k', linestyle='-')
    nbaoArtist = plt.Line2D((0,1),(0,0), color='k', linestyle='--')

    plt.xlabel("$R [Mpc/h]$", size = 16)
    plt.ylabel("$\\Delta \\xi (R)$", size = 16)
    plt.title("$\\langle\\xi_{bao}-\\xi_{no bao}\\rangle$")
    plt.legend([rsdArtist, realArtist, transArtist, losArtist, baoArtist, nbaoArtist], ["Redshift Space", "Real Space", "Redshift Space Transverse", "Redshift Space Line of Sight"], prop={'size':10}, loc=2)
    plt.axis([0,150,-0.01,0.01])
    plt.show()

#--------------------------------------------------------------------------------
#=================================================================================
#---------------------------------------------------------------------------------

def meeting_plot_xidiff(folder):
    print "xi_scale()"
    plt.figure()
    
    bao_fol  = folder+"/bao"
    nbao_fol = folder+"/nobao"
#    bao_fol  = folder+"/with_bao"
#    nbao_fol = folder+"/no_bao"

    xi_search   = "xi_*"
    xi2d_search = "xi2d_*"
#    xi_search   = "cf_1d*"
#    xi2d_search = "cf_2d*"

    print "importing xirsd..."
    r, xi_rsd_bao  = import_data( bao_fol, xi_search, 200)
    r, xi_rsd_nbao = import_data(nbao_fol, xi_search, 200)
    
    real_fol = "/gpfs/data/rhgk18/results/R_b1024_ng512_np1024"

    print "importing xireal..."
    r, xi_real_bao = import_data( real_fol+"/bao", xi_search, 200)
    r, xi_real_nbao= import_data( real_fol+"/nobao", xi_search, 200)
    

    #Angular Average (/w RSD)
    print "calculating angular average /w RSD..."
    xi_rsd_diff     = xi_rsd_bao-xi_rsd_nbao
    m_xi_rsd_diff   = np.mean(xi_rsd_diff, axis=0)
    xi_rsd_diff_err = np.std(xi_rsd_diff, axis = 0)/np.sqrt(len(xi_rsd_diff))


    print "plotting..."

    p1  = plt.plot(r, r**2*m_xi_rsd_diff, label='RSD', color = 'r', linestyle='-')
    p1e = plt.fill_between(r, r**2*(m_xi_rsd_diff-xi_rsd_diff_err), r**2*(m_xi_rsd_diff+xi_rsd_diff_err), alpha=0.2, color='r')



    #Angular Average (w/o RSD)
    print "calculating angular average w/o RSD..."
    xi_real_diff     = xi_real_bao-xi_real_nbao
    m_xi_real_diff   = np.mean(xi_real_diff, axis=0)
    xi_real_diff_err = np.std(xi_real_diff, axis = 0)/np.sqrt(len(xi_real_diff))


    print "plotting..."
    p2  = plt.plot(r, r**2*m_xi_real_diff, 'b-', label='Real')
    p2e = plt.fill_between(r, r**2*(m_xi_real_diff-xi_real_diff_err), r**2*(m_xi_real_diff+xi_real_diff_err), alpha=0.2, color='b')


    if True:
        print "importing xi2d..."
#        temp_ = np.loadtxt(folder+"/rp_pi.txt")
#        rp = temp_[:,0]
#        pi = temp_[:,1]

        rp, pi, xi2d_rsd_bao  = import_data( bao_fol, xi2d_search, 200)
        rp, pi, xi2d_rsd_nbao = import_data(nbao_fol, xi2d_search, 200)

        print "calculating the mean 2D correlation function..."
        xi2d_rsd_diff    = xi2d_rsd_bao-xi2d_rsd_nbao
        m_xi2d_rsd_diff  = np.mean(xi2d_rsd_diff, axis=0)
        xi2d_rsd_diff_err= np.std(xi2d_rsd_diff, axis = 0)/np.sqrt(len(xi2d_rsd_diff))
 

        #Transverse
        print "plotting..."
        p3 = plt.plot(rp, rp**2*m_xi2d_rsd_diff[:,0], label="XI2D LoS, RSD", color='g', linestyle='-')
        p3e = plt.fill_between(rp, rp**2*(m_xi2d_rsd_diff[:,0]-xi2d_rsd_diff_err[:,0]), rp**2*(m_xi2d_rsd_diff[:,0]+xi2d_rsd_diff_err[:,0]), alpha=0.2, color='g')


        #Line of Sight
        p7 = plt.plot(pi, pi**2*m_xi2d_rsd_diff[0,:],label="XI2D Transverse, RSD, BAO",color='c',linestyle='-')
        p7e = plt.fill_between(pi, pi**2*(m_xi2d_rsd_diff[0,:]-xi2d_rsd_diff_err[0,:]), pi**2*(m_xi2d_rsd_diff[0,:]+xi2d_rsd_diff_err[0,:]), alpha=0.2, color='c')


    rsdArtist  = mpatches.Patch(color='red')
    realArtist = mpatches.Patch(color='blue')
    transArtist= mpatches.Patch(color='cyan')
    losArtist  = mpatches.Patch(color='green')
    baoArtist  = plt.Line2D((0,1),(0,0), color='k', linestyle='-')
    nbaoArtist = plt.Line2D((0,1),(0,0), color='k', linestyle='--')

    plt.axhline(y=0, xmin=0, xmax=200, color='k', alpha=0.5)
    plt.xlabel("$R [Mpc/h]$", size = 16)
    plt.ylabel("$R^2\\Delta\\xi (R)$", size = 16)
    plt.title("$\\langle\\xi_{bao}-\\xi_{no bao}\\rangle$")
    plt.legend([rsdArtist, realArtist, transArtist, losArtist, baoArtist, nbaoArtist], ["Redshift Space", "Real Space", "Redshift Space Transverse", "Redshift Space Line of Sight"], prop={'size':10})
#    plt.axis([0,250,-60,80])
    plt.show()


def meeting_plot_scale(folder):
    print "meeting_plot_scale()"
    plt.figure()
    
    bao_fol  = folder+"/bao"
    nbao_fol = folder+"/nobao"
#    bao_fol  = folder+"/with_bao"
#    nbao_fol = folder+"/no_bao"

    xi_search   = "xi_*"
    xi2d_search = "xi2d_*"
#    xi_search   = "cf_1d*"
#    xi2d_search = "cf_2d*"

    print "importing xirsd..."
    r, xi_rsd_bao  = import_data( bao_fol, xi_search, 200)
    r, xi_rsd_nbao = import_data(nbao_fol, xi_search, 200)
    
    real_fol = "/gpfs/data/rhgk18/results/R_b1024_ng512_np1024"

    print "importing xireal..."
    r, xi_real_bao = import_data( real_fol+"/bao", xi_search, 200)
    r, xi_real_nbao= import_data( real_fol+"/nobao", xi_search, 200)
    

    #Angular Average (/w RSD)
    print "calculating angular average /w RSD..."
    m_xi_bao_rsd   = np.mean(xi_rsd_bao, axis = 0)
    xi_bao_rsd_err = np.std(xi_rsd_bao, axis = 0)/np.sqrt(len(xi_rsd_bao))

    m_xi_nbao_rsd   = np.mean(xi_rsd_nbao, axis = 0)
    xi_nbao_rsd_err = np.std(xi_rsd_nbao, axis = 0)/np.sqrt(len(xi_rsd_nbao))


    print "plotting..."
#    p1  = plt.errorbar(r, r**2*m_xi_bao_rsd, yerr=r**2*xi_bao_rsd_err ,label='RSD, BAO', color = 'r', linestyle='-')
    p1  = plt.plot(r, r**2*m_xi_bao_rsd, label='RSD, BAO', color = 'r', linestyle='-')
    p1e = plt.fill_between(r, r**2*(m_xi_bao_rsd-xi_bao_rsd_err), r**2*(m_xi_bao_rsd+xi_bao_rsd_err), alpha=0.2, color='r')
#    p2  = plt.errorbar(r, r**2*m_xi_nbao_rsd, yerr=r**2*xi_nbao_rsd_err, label='RSD, No BAO', color='r', linestyle='--')
    p2  = plt.plot(r, r**2*m_xi_nbao_rsd, label='RSD, No BAO', color='r', linestyle='--')
    p2e = plt.fill_between(r, r**2*(m_xi_nbao_rsd-xi_nbao_rsd_err), r**2*(m_xi_nbao_rsd+xi_nbao_rsd_err), alpha=0.2, color='r')


    #Angular Average (w/o RSD)
    print "calculating angular average w/o RSD..."
    m_xi_bao_real  = np.mean(xi_real_bao, axis = 0)
    xi_bao_real_err = np.std(xi_real_bao, axis = 0)/np.sqrt(len(xi_real_bao))

    m_xi_nbao_real = np.mean(xi_real_nbao, axis = 0)
    xi_nbao_real_err = np.std(xi_real_nbao, axis = 0)/np.sqrt(len(xi_real_nbao))

    print "plotting..."
    p3  = plt.plot(r, r**2*m_xi_bao_real, 'b-', label='Real, BAO')
    p3e = plt.fill_between(r, r**2*(m_xi_bao_real-xi_bao_real_err), r**2*(m_xi_bao_real+xi_bao_real_err), alpha=0.2, color='b')

    p4  = plt.plot(r, r**2*m_xi_nbao_real, 'b--', label='Real, No BAO')
    p4e = plt.fill_between(r, r**2*(m_xi_nbao_real-xi_nbao_real_err), r**2*(m_xi_nbao_real+xi_nbao_real_err), alpha=0.2, color='b')

    if True:
        print "importing xi2d..."
#        temp_ = np.loadtxt(folder+"/rp_pi.txt")
#        rp = temp_[:,0]
#        pi = temp_[:,1]

        rp, pi, xi2d_rsd_bao  = import_data( bao_fol, xi2d_search, 200)
        rp, pi, xi2d_rsd_nbao = import_data(nbao_fol, xi2d_search, 200)

        print "calculating the mean 2D correlation function..."
        m_xi2d_bao_rsd  = np.mean(xi2d_rsd_bao , axis = 0)
        xi2d_bao_rsd_err= np.std(xi2d_rsd_bao, axis = 0)/np.sqrt(len(xi2d_rsd_bao))
        m_xi2d_nbao_rsd = np.mean(xi2d_rsd_nbao, axis = 0)
        xi2d_nbao_rsd_err= np.std(xi2d_rsd_bao, axis = 0)/np.sqrt(len(xi2d_rsd_nbao))   

        #Transverse
        print "plotting..."
        p5 = plt.plot(rp, rp**2*m_xi2d_bao_rsd[:,0], label="XI2D LoS, RSD, BAO", color='g', linestyle='-')
        p5e = plt.fill_between(rp, rp**2*(m_xi2d_bao_rsd[:,0]-xi2d_bao_rsd_err[:,0]), rp**2*(m_xi2d_bao_rsd[:,0]+xi2d_bao_rsd_err[:,0]), alpha=0.2, color='g')

        p6 = plt.plot(rp, rp**2*m_xi2d_nbao_rsd[:,0], label="XI2D LoS, RSD, No BAO", color='g', linestyle='--')
        p6e = plt.fill_between(rp, rp**2*(m_xi2d_nbao_rsd[:,0]-xi2d_nbao_rsd_err[:,0]), rp**2*(m_xi2d_nbao_rsd[:,0]+xi2d_nbao_rsd_err[:,0]), alpha=0.2, color='g')


        #Line of Sight
        p7 = plt.plot(pi, pi**2*m_xi2d_bao_rsd[0,:],label="XI2D Transverse, RSD, BAO",color='c',linestyle='-')
        p7e = plt.fill_between(pi, pi**2*(m_xi2d_bao_rsd[0,:]-xi2d_bao_rsd_err[0,:]), pi**2*(m_xi2d_bao_rsd[0,:]+xi2d_bao_rsd_err[0,:]), alpha=0.2, color='c')

        p8 = plt.plot(pi, pi**2*m_xi2d_nbao_rsd[0,:],label="XI2D Transverse, RSD, No BAO",color='c',linestyle='--')
        p8e = plt.fill_between(pi, pi**2*(m_xi2d_nbao_rsd[0,:]-xi2d_nbao_rsd_err[0,:]), pi**2*(m_xi2d_nbao_rsd[0,:]+xi2d_nbao_rsd_err[0,:]), alpha=0.2, color='c')

    rsdArtist  = mpatches.Patch(color='red')
    realArtist = mpatches.Patch(color='blue')
    transArtist= mpatches.Patch(color='cyan')
    losArtist  = mpatches.Patch(color='green')
    baoArtist  = plt.Line2D((0,1),(0,0), color='k', linestyle='-')
    nbaoArtist = plt.Line2D((0,1),(0,0), color='k', linestyle='--')

    plt.xlabel("$R [Mpc/h]$", size = 16)
    plt.ylabel("$R^2\\xi (R)$", size = 16)
    plt.title("Scaled Correllation function for Real and Redshift space, with and without the BAO")
    plt.legend([rsdArtist, realArtist, transArtist, losArtist, baoArtist, nbaoArtist], ["Redshift Space", "Real Space", "Redshift Space Transverse", "Redshift Space Line of Sight", "With BAO", "Without BAO"], prop={'size':10})
    plt.axis([30,200,-60,80])
    plt.show()


if __name__ == "__main__":

    folder = "/gpfs/data/rhgk18/results/b1024_ng512_np1024"

    meeting_plot_xidiff(folder)
