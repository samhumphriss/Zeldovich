import zeldovich_init as ic
import argparse
import numpy as np
import cic_dens_wrapper as cdw
import spatial_stats as ss
import micromodules.fileio as io
import execute as exe

#EDIT Notes: seedbank support, 

print "\nAll Numpy errors are currently suppressed."

parser = argparse.ArgumentParser(description='Set up the initial conditions for an N-body simulation given power spectrum data')

parser.add_argument("-b", "--boxsize", type=float, default = 128, help='Define the length of one side of the boundary cube')
parser.add_argument("-g", "--ngrid", type=int, default = 64, help='Define how many grid spaces there should be along each side')
parser.add_argument("-p", "--pkpath", type=str, default = "pk_indra7313.txt", help='Passes the name rof the P(k) file used to the code')
parser.add_argument("-z", "--redshift", type=float, default = 0.0, help='Set the initial time step in units of redshift')
parser.add_argument("-r", "--truerand", action='store_true', help='Generates a random seed each time the code is run')
parser.add_argument("-n", "--nparticles", type=int, default = 30, help='Set the depth of field on the 2D cross-sections.')
parser.add_argument("-f", "--folder", type=str, default = "/BX_GX_ZX_000", help='Give the name of the output folder.')
parser.add_argument("--runindex", type=int, default = -1, help='Should be set to ${LSB_JOBINDEX} if used.')
args = parser.parse_args()

base_folder = "/gpfs/data/rhgk18/results"
sv_folder = base_folder+args.folder
io.mkdir(sv_folder)

pk = io.import_pk(args.pkpath)
s
if args.truerand == False:
    genseed=314159
    print "\nGenerator seed = ", genseed, "\n"
else:
    seedbank = io.import_seedbank('seedbank20k.txt')
    genseed  = int(seedbank[args.runindex])
    print "\nGenerator seed = ", genseed, "\n"

dens = exe.run_dens(pk, args.redshift, args.boxsize, args.ngrid, args.truerand, genseed)

#r, xi=ss.getXi(densz, nrbins=args.ngrid/2, boxsize=args.boxsize, get2d=False, deconvolve_cic=True, exp_smooth=0.0)

rp, pi, xi2d=ss.getXi(dens, nrbins=args.ngrid/2, boxsize=args.boxsize, get2d=True, deconvolve_cic=True, exp_smooth=0.0)

io.write_rp(sv_folder,rp)
io.write_pi(sv_folder,pi)
io.write_xi2d(sv_folder, xi2d, genseed)
    
    
