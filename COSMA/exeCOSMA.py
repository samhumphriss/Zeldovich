import zeldovich_init as ic
import render as rd
import argparse
import numpy as np
import os
import cic_dens_wrapper as cdw
import spatial_stats as ss
import multiprocessing as mp
import datetime as dt
import time

print "\nAll Numpy errors are currently suppressed."

parser = argparse.ArgumentParser(description='Set up the initial conditions for an N-body simulation given power spectrum data')
parser.add_argument("-b", "--boxsize", type=float, default = 100, help='Define the length of one side of the boundary cube')
parser.add_argument("-g", "--ngrid", type=int, default = 30, help='Define how many grid spaces there should be along each side')
parser.add_argument("-p", "--pkpath", type=str, default = "pk_indra7313.txt", help='Passes the name of the P(k) file used to the code')
parser.add_argument("-z", "--redshift", type=float, default = 0.0, help='Set the initial time step in units of redshift')
parser.add_argument("-r", "--truerand", action='store_true', help='Generates a random seed each time the code is run')
parser.add_argument("-d", "--slicedepth", type=float, default = 2.0, help='Set the depth of field on the 2D cross-sections.')
parser.add_argument("-n", "--nparticles", type=int, default = 30, help='Set the depth of field on the 2D cross-sections.')
parser.add_argument("-x", "--processes", type=int, default = 2, help='Define how many proccesses the code should execute')
parser.add_argument("-xs", "--simnumber", type=int, default = 2, help='Define how many times the simulation will run (MULTIPLE OF PROCESSES)')
args = parser.parse_args()

def ensure_dir(f):
    if not os.path.exists(f):
        os.mkdir(f)

def gather_stats(rshift, pk, bs, ng, tr, n, fname, processes, simnumber, pseed):
    
    for s in range(simnumber/processes):
        simseed = pseed + s
        pos  = ic.main(rshift, pk, bs, ng, trand=tr, seed = simseed)
        dens = cdw.get_dens(pos[0],pos[1],pos[2], ng, bs)
        dens = np.swapaxes(dens, 2, 0)
    
        r, xi=ss.getXi(dens, nrbins=ng/2, boxsize=bs, get2d=False, deconvolve_cic=True, exp_smooth=0.0)

        rp, pi, xi2d=ss.getXi(dens, nrbins=ng/2, boxsize=bs, get2d=True, deconvolve_cic=True, exp_smooth=0.0)

        filename = fname+"/Z"+str(int(rshift))+"_BS"+str(int(bs))+"_NG"+str(int(ng))+"_SEED"+str(pos[6])

#    np.savetxt(filename+"1D.txt", np.array([r, xi]), fmt="%10.5f")
        np.savetxt(filename+"_2D_rp.txt", rp, fmt="%10.5f")
        np.savetxt(filename+"_2D_pi.txt", pi, fmt="%10.5f")
        np.savetxt(filename+"_2D_xi2d.txt", xi2d, fmt="%10.5f")

def submit(rshift, pk, bs, ng, tr):
    #COSMA SUBMIT MODE
    now = dt.datetime.now()    
    fname = "/gpfs/data/rhgk18/results/%s_%s_%sX%s_%s_%s"%(now.hour,now.minute,now.second,now.day,now.month,now.year)

    ensure_dir(fname)

    process_arr = []
    
    masterseed = int(100000*np.random.rand())
    rs = np.random.RandomState(masterseed)

    process_seeds = (100000*rs.rand(args.processes)).astype(int)

    for n in range(args.processes):
        process_arr.append(mp.Process(target=gather_stats, args=(rshift, pk, bs, ng, tr, n, fname, args.processes, args.simnumber, process_seeds[n])))

    for i in process_arr:
        i.start()

    for j in process_arr:
        j.join()

def render(rshift, pk, bs, ng, tr, sd):
    pos  = ic.main(rshift, pk, bs, ng, tr)
    densr = cdw.get_dens(pos[0],pos[1],pos[2], ng, bs)  
    densz = cdw.get_dens(pos[3],pos[4],pos[5], ng, bs)
    rd.full_data_render(pos, densr, densz, pk, sd, bs, ng)
    

base_path = os.getcwd()
pk_path = os.getcwd() + "/pks/" + args.pkpath
pk = ic.import_pk(pk_path)


submit(args.redshift, pk, args.boxsize, args.ngrid, args.truerand)
#render(args.redshift, pk, args.boxsize, args.ngrid, args.truerand, args.slicedepth)
    
    
    
