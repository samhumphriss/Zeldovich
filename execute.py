import zeldovich_init as ic
import numpy as np
import cic_dens_wrapper as cdw

def run_dens(pk, redshift=0, boxsize=512, ngrid=128, trand=True, seed=314159):
    pos  = ic.main(redshift, pk, boxsize=boxsize, ngrid=ngrid, trand=trand, seed=seed)
#    densr = cdw.get_dens(pos[0],pos[1],pos[2], ngrid, boxsize)
    densz = cdw.get_dens(pos[0],pos[1],pos[3], ngrid, boxsize)
    dens = np.swapaxes(densz, 2, 0)
    
    return dens
    
def run_pos(pk, redshift=0, boxsize=512, ngrid=128, trand=True, seed=314159):
    pos  = ic.main(redshift, pk, boxsize, ngrid, trand, seed=seed)
    
    return pos

