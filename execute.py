import zeldovich_init as ic
import numpy as np
import cic_dens_wrapper as cdw

def run_dens(pk, redshift=0.0, growthrate=0.5, boxsize=1024, ngrid=256, nparticles=512**3, trand=True, seed=314159):

    dens0 = ic.make_gauss_init(pk, boxsize=boxsize, ngrid=ngrid, seed=seed, exactpk=True)

    fx, fy, fz = ic.get_disp(dens0, boxsize=boxsize, ngrid=ngrid)

    dens = cdw.disp_to_dens(fx, fy, fz, ngrid, boxsize, nparticles, growthrate)

    return dens
    

def run_pos(pk, redshift=0, boxsize=512, ngrid=128, trand=True, seed=314159):
    pos  = ic.main(redshift, pk, boxsize, ngrid, trand, seed=seed)
    
    return pos

