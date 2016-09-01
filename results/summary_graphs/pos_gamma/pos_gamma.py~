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

    f03 = f03arr[:,:,0]

    #f035
    f035result = glob.glob(folder+"/run_f0.35/with_bao/rs/cf_2d_*")
    f035test   = np.loadtxt(f035result[0])

    f035arr  = np.zeros((len(f035result), len(f035test), len(f035test)))
    
    i = 0
    for r in f035result:
        f035arr[i] = np.loadtxt(r)
        i += 1

    f035 = f035arr[:,:,0]

    #f04
    f04result = glob.glob(folder+"/run_f0.4/with_bao/rs/cf_2d_*")
    f04test   = np.loadtxt(f04result[0])

    f04arr  = np.zeros((len(f04result), len(f04test), len(f04test)))
    
    i = 0
    for r in f04result:
        f04arr[i] = np.loadtxt(r)
        i += 1

    f04 = f04arr[:,:,0]
    
    #f045
    f045result = glob.glob(folder+"/run_f0.45/with_bao/rs/cf_2d_*")
    f045test   = np.loadtxt(f045result[0])

    f045arr  = np.zeros((len(f045result), len(f045test), len(f045test)))
    
    i = 0
    for r in f045result:
        f045arr[i] = np.loadtxt(r)
        i += 1

    f045 = f045arr[:,:,0]
    
    #f05
    f05result = glob.glob(folder+"/run_f0.5/with_bao/rs/cf_2d_*")
    f05test   = np.loadtxt(f05result[0])

    f05arr  = np.zeros((len(f05result), len(f05test), len(f05test)))
    
    i = 0
    for r in f05result:
        f05arr[i] = np.loadtxt(r)
        i += 1

    f05 = f05arr[:,:,0]

    #f055
    f055result = glob.glob(folder+"/run_f0.55/with_bao/rs/cf_2d_*")
    f055test   = np.loadtxt(f055result[0])

    f055arr  = np.zeros((len(f055result), len(f055test), len(f055test)))
    
    i = 0
    for r in f055result:
        f055arr[i] = np.loadtxt(r)
        i += 1

    f055 = f055arr[:,:,0]

    #f06
    f06result = glob.glob(folder+"/run_f0.6/with_bao/rs/cf_2d_*")
    f06test   = np.loadtxt(f06result[0])

    f06arr  = np.zeros((len(f06result), len(f06test), len(f06test)))
    
    i = 0
    for r in f06result:
        f06arr[i] = np.loadtxt(r)
        i += 1

    f06 = f06arr[:,:,0]

    return pi, f03, f035, f04, f045, f05, f055, f06

def min_search(pi, xi):
    ind = np.where((pi>20)&(pi<90))
    return np.sum(pi[ind]*(xi[ind]-1))/np.sum((xi[ind]-1))   

def calc_pos(pi, r_arr):
    min_array = []

    for r in r_arr:
        min_array.append(min_search(pi, r))
    
    min_array = np.array(min_array)
    pos_mean = np.mean(min_array)
    pos_err  = np.std(min_array)

    return pos_mean, pos_err

def render_pos_gamma(pi, f03, f035, f04, f045, f05, f055, f06):
    f03_m, f03_err = calc_pos(pi, f03)
    f035_m, f035_err = calc_pos(pi, f035)
    f04_m, f04_err = calc_pos(pi, f04)
    f045_m, f045_err = calc_pos(pi, f045)
    f05_m, f05_err = calc_pos(pi, f05)
    f055_m, f055_err = calc_pos(pi, f055)
    f06_m, f06_err = calc_pos(pi, f06)

    gamma    = np.array([0.925, 0.806, 0.704, 0.613, 0.532, 0.459, 0.392])
    positions = np.array([f03_m, f035_m, f04_m, f045_m, f05_m, f055_m, f06_m])
    errors    = np.array([f03_err, f035_err, f04_err, f045_err, f05_err, f055_err, f06_err])
    plt.figure()
    
    plt.plot(gamma, positions)
    plt.grid()
    plt.show()

if __name__ == "__main__":
    pi, f03, f035, f04, f045, f05, f055, f06 = import_data()
