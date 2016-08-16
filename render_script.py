import micromodules.fileio as io
import micromodules.render as rd
import numpy as np
import glob
import os

folder = "/gpfs/data/rhgk18/results/upd_trial100/bao"
search = "xi2d_*"

results = glob.glob(os.path.join(folder, search))

a = 0
c = 0
for r in results:
    a += np.loadtxt(r)
    c += 1

xi2d_mean = a/c

rp = np.loadtxt(folder+"/rp.txt")
pi = np.loadtxt(folder+"/pi.txt")
#xi2d = np.loadtxt(results[0])

rd.xi2d_slices(rp, pi, xi2d_mean)
