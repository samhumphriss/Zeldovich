import zeldovich_init as ic
import argparse
import numpy as np
import spatial_stats as ss
import micromodules.fileio as io
import execute as exe
import sys

print "\nAll Numpy errors are currently suppressed."

parser = argparse.ArgumentParser(description='Set up the initial conditions for an N-body simulation given power spectrum data')

parser.add_argument("-b", "--boxsize", type=float, default = 128, help='Define the length of one side of the boundary cube')
parser.add_argument("-g", "--ngrid", type=int, default = 64, help='Define how many grid spaces there should be along each side')
parser.add_argument("-p", "--pkpath", type=str, default = "pk_indra7313.txt", help='Passes the name rof the P(k) file used to the code')
parser.add_argument("-z", "--redshift", type=float, default = 0.0, help='Set the initial time step in units of redshift')
parser.add_argument("-r", "--truerand", action='store_true', help='Generates a random seed each time the code is run')
parser.add_argument("-f", "--folder", type=str, default = "/BX_GX_ZX_000", help='Give the name of the output folder.')
parser.add_argument("--runindex", type=int, default = -1, help='Should be set to ${LSB_JOBINDEX} if used.')
parser.add_argument("-np", "--nparticles", type=int, default = 128, help='Gives the total number of particles within the volume.')
parser.add_argument("-s", "--seedstart", type=int, default=0, help='Set the index from which to begin in the seedbank.')
parser.add_argument("-gr", "--growthrate", type=float, default=0.5, help='Set the relative intensity of the RSD. Set 0 for no RSD.')
args = parser.parse_args()

sv_folder = args.folder

print "Importing pk: ", args.pkpath
pk = io.import_pk(args.pkpath)

print "Importing seed..."
if args.truerand == False:
    genseed=314159
    print "\nGenerator seed = ", genseed, "\n"
else:
    seedbank = io.import_seedbank('seedbank20k.txt')
    genseed  = int(seedbank[args.runindex+args.seedstart])
    print "\nGenerator seed = ", genseed, "\n"

print "Calculating the resulting density grid..."
dens = exe.run_dens(pk, redshift=args.redshift, growthrate=args.growthrate, boxsize=args.boxsize, ngrid=args.ngrid, nparticles=args.nparticles**3, trand=args.truerand, seed=genseed)

print "Calculating the 1D-averaged correlation function..."
r, xi = ss.getXi(dens,nrbins=args.ngrid/2, boxsize=args.boxsize, get2d = False, deconvolve_cic = False, exp_smooth = 0.0)

print "Writing xi to ", sv_folder
io.write_r(sv_folder, r)
io.write_xi(sv_folder, xi, genseed)

print "Calculating the 2D correlation function..."
rp, pi, xi2d = ss.getXi(dens, nrbins = args.ngrid/2, boxsize = args.boxsize, get2d = True, deconvolve_cic = False, exp_smooth = 0.0)

print "Writing xi2d to ", sv_folder
io.write_rp(sv_folder, rp)
io.write_pi(sv_folder, pi)
io.write_xi2d(sv_folder, xi2d, genseed)
    
    
