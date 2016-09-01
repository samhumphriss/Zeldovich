import numpy as np
import matplotlib.pyplot as plt
import glob

def import_data():
    folder="/gpfs/data/nmccull/zeldovich_out/"

    tmp       = np.loadtxt(folder+"/run_f0.3/rp_pi.txt")
    rp        = tmp[:,0]
    pi        = tmp[:,1]

    #f03
    f03result = glob.glob(folder+"/run_f0.3/with_bao/rs/cf_2d_*")
    f03test   = np.loadtxt(f03result[0])

    f03arr  = np.zeros((len(f03result), len(f03test), len(f03test)))
    
    i = 0
    for r in f03result:
        f03arr[i] = np.loadtxt(r)
        i += 1

    #f035
    f035result = glob.glob(folder+"/run_f0.35/with_bao/rs/cf_2d_*")
    f035test   = np.loadtxt(f035result[0])

    f035arr  = np.zeros((len(f035result), len(f035test), len(f035test)))
    
    i = 0
    for r in f035result:
        f035arr[i] = np.loadtxt(r)
        i += 1

    #f04
    f04result = glob.glob(folder+"/run_f0.4/with_bao/rs/cf_2d_*")
    f04test   = np.loadtxt(f04result[0])

    f04arr  = np.zeros((len(f04result), len(f04test), len(f04test)))
    
    i = 0
    for r in f04result:
        f04arr[i] = np.loadtxt(r)
        i += 1
    
    #f045
    f045result = glob.glob(folder+"/run_f0.45/with_bao/rs/cf_2d_*")
    f045test   = np.loadtxt(f045result[0])

    f045arr  = np.zeros((len(f045result), len(f045test), len(f045test)))
    
    i = 0
    for r in f045result:
        f045arr[i] = np.loadtxt(r)
        i += 1
    
    #f05
    f05result = glob.glob(folder+"/run_f0.5/with_bao/rs/cf_2d_*")
    f05test   = np.loadtxt(f05result[0])

    f05arr  = np.zeros((len(f05result), len(f05test), len(f05test)))
    
    i = 0
    for r in f05result:
        f05arr[i] = np.loadtxt(r)
        i += 1

    #f055
    f055result = glob.glob(folder+"/run_f0.55/with_bao/rs/cf_2d_*")
    f055test   = np.loadtxt(f055result[0])

    f055arr  = np.zeros((len(f055result), len(f055test), len(f055test)))
    
    i = 0
    for r in f055result:
        f055arr[i] = np.loadtxt(r)
        i += 1

    #f06
    f06result = glob.glob(folder+"/run_f0.6/with_bao/rs/cf_2d_*")
    f06test   = np.loadtxt(f06result[0])

    f06arr  = np.zeros((len(f06result), len(f06test), len(f06test)))
    
    i = 0
    for r in f06result:
        f06arr[i] = np.loadtxt(r)
        i += 1

    return pi, f03arr, f035arr, f04arr, f045arr, f05arr, f055arr, f06arr
     

def render_gamma_variance(pi, g0925, g0806, g0704, g0613, g0532, g0459, g0392):
    g1_m = np.mean(g0925[:,:,0], axis=0)
    g2_m = np.mean(g0806[:,:,0], axis=0)
    g3_m = np.mean(g0704[:,:,0], axis=0)
    g4_m = np.mean(g0613[:,:,0], axis=0)
    g5_m = np.mean(g0532[:,:,0], axis=0)
    g6_m = np.mean(g0459[:,:,0], axis=0)
    g7_m = np.mean(g0392[:,:,0], axis=0)

    g1_err = np.std(g0925[:,:,0], axis=0)/np.sqrt(len(g0925))
    g2_err = np.std(g0806[:,:,0], axis=0)/np.sqrt(len(g0806))
    g3_err = np.std(g0704[:,:,0], axis=0)/np.sqrt(len(g0704))
    g4_err = np.std(g0613[:,:,0], axis=0)/np.sqrt(len(g0613))
    g5_err = np.std(g0532[:,:,0], axis=0)/np.sqrt(len(g0532))
    g6_err = np.std(g0459[:,:,0], axis=0)/np.sqrt(len(g0459))
    g7_err = np.std(g0392[:,:,0], axis=0)/np.sqrt(len(g0392))


    plt.figure()

    cmap = plt.cm.rainbow
    carr =[cmap(i) for i in np.linspace(0,0.9, 7)]
    p1 = plt.plot(pi, g1_m, color=carr[0])
    p2 = plt.plot(pi, g2_m, color=carr[1])
    p3 = plt.plot(pi, g3_m, color=carr[2])
    p4 = plt.plot(pi, g4_m, color=carr[3])
    p5 = plt.plot(pi, g5_m, color=carr[4])
    p6 = plt.plot(pi, g6_m, color=carr[5])
    p7 = plt.plot(pi, g7_m, color=carr[6])

    f1 = plt.fill_between(pi, g1_m-g1_err, g1_m+g1_err, color=carr[0], alpha=0.2)
    f2 = plt.fill_between(pi, g2_m-g2_err, g2_m+g2_err, color=carr[1], alpha=0.2)
    f3 = plt.fill_between(pi, g3_m-g3_err, g3_m+g3_err, color=carr[2], alpha=0.2)
    f4 = plt.fill_between(pi, g4_m-g4_err, g4_m+g4_err, color=carr[3], alpha=0.2)
    f5 = plt.fill_between(pi, g5_m-g5_err, g5_m+g5_err, color=carr[4], alpha=0.2)
    f6 = plt.fill_between(pi, g6_m-g6_err, g6_m+g6_err, color=carr[5], alpha=0.2)
    f7 = plt.fill_between(pi, g7_m-g7_err, g7_m+g7_err, color=carr[6], alpha=0.2)
    plt.grid()
    
    f = [0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6]
    g = np.array([0.925, 0.806, 0.704, 0.613, 0.532, 0.459, 0.392])
    plt.axhline(y=0, color='k')
    plt.xlabel("$R [Mpc]$",size=24)
    plt.ylabel("$\\xi(R)$",size=24)
    plt.axis([20,180,-0.015, 0.01])
    sm = plt.cm.ScalarMappable(cmap='rainbow', norm =plt.Normalize(vmin=0.3, vmax=0.6))
    sm._A = []
    cb = plt.colorbar(sm)
    cb.set_label(r'$\gamma$', rotation=270, labelpad=30, size = 24)
    cb.set_ticks(f)
    cb.ax.set_yticklabels(['%.2f'%g[i] for i in np.arange(g.size)])
#    plt.legend()
    plt.show()
        

if __name__ == "__main__":
    pi, f03, f035, f04, f045, f05, f055, f06 = import_data()
    g0925, g0806, g0704, g0613, g0532, g0459, g0392 = f03, f035, f04, f045, f05, f055, f06


    render_gamma_variance(pi, g0925, g0806, g0704, g0613, g0532, g0459, g0392)
    
    
