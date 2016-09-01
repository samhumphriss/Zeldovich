import numpy as np
import scipy.interpolate as ip
import multiprocessing as mp
import time
from numpy.random import seed as NumSeed

np.seterr(all='ignore')

def make_gauss_init(pkinit, boxsize=100.0, ngrid=100, seed=314159, exactpk=True, smw=2.0):
    
    #mathematical artifact of Fourier transform, possibly incorrect? (ngrid+1)/2)
    thirdim = ngrid/2+1
    
    
    #inverse(?) of the cell size (in 2pi)
    kmin = 2*np.pi/np.float(boxsize)
    
    #shape of k grid
    sk = (ngrid,ngrid,thirdim)
    
    #No clue. it represents the grid, but the method / definition is non-trivial.
    a = np.fromfunction(lambda x,y,z:x, sk).astype(np.float)
    a[np.where(a > ngrid/2)] -= ngrid
    b=np.transpose(a, (1, 0, 2))
    c = np.fromfunction(lambda x,y,z:z, sk).astype(np.float)
    c[np.where(c > ngrid/2)] -= ngrid
    
    #From this, a/b/c = x/y/z but why are 3x10x10x6 arrays necessary?
    kgrid = kmin*np.sqrt(a**2+b**2+c**2).astype(np.float)
    a = 0
    b = 0
    c = 0
    #K-space is a bitch.
    
    
    #self-explanatory
    rs = np.random.RandomState(seed)
    
    #What are these complex numbers representing?
    if (exactpk):
        dk = np.exp(2j*np.pi*rs.rand(ngrid*ngrid*(thirdim))).reshape(sk).astype(np.complex64)
    else:
        dk = np.empty(sk,dtype=np.complex64)
        dk.real = rs.normal(size=ngrid*ngrid*(thirdim)).reshape(sk).astype(np.float32)
        dk.imag = rs.normal(size=ngrid*ngrid*(thirdim)).reshape(sk).astype(np.float32)
        dk /= np.sqrt(2.0)
    #This section provides a unit length, random(?) phase complex number associated with
    #each point on the grid.
    
    #Gaussian filter
    filt=np.exp(-kgrid**2*smw**2)
    
    #interpolate power spectrum to approximate at non-keyed values.
    pkinterp=ip.interp1d(pkinit[:,0], pkinit[:,1])
    
    #Pk undefined at 0, so this provides an explicit exception.
    if (kgrid[0,0,0]==0):
        dk[0,0,0]=0
        wn0=np.where(kgrid!=0)
        
        #The mathematics? 
        dk[wn0] *= np.sqrt(filt[wn0]*pkinterp(kgrid[wn0]))*ngrid**3/boxsize**1.5   
    #Why is this if statement necessary? We know the P(k) will be undefined.
    else:
        dk *= np.sqrt(filt*pkinterp(kgrid.flatten())).reshape(sk)*ngrid**3/boxsize**1.5
        
    dk=nyquist(dk)
    return dk
    
def get_disp(dens, boxsize=100.0, ngrid=100):
    
    cell_len=np.float(boxsize)/np.float(ngrid)
    thirdim=ngrid/2+1
    kmin = 2*np.pi/np.float(boxsize)
    sk = (ngrid,ngrid,thirdim)  


    #Hello darkness, my old friend. (Same k-space issues)
    a = np.fromfunction(lambda x,y,z:x, sk).astype(np.float)
    a[np.where(a > ngrid/2)] -= ngrid
    b=np.transpose(a, (1, 0, 2))
    c = np.fromfunction(lambda x,y,z:z, sk).astype(np.float)
    c[np.where(c > ngrid/2)] -= ngrid
  
    xp=-1j*dens*a/(a**2+b**2+c**2)/kmin
    yp=-1j*dens*b/(a**2+b**2+c**2)/kmin
    zp=-1j*dens*c/(a**2+b**2+c**2)/kmin
    
    xp[0,0,0]=0.
    yp[0,0,0]=0.
    zp[0,0,0]=0.
    
    a=0
    b=0
    c=0
    
    xp = nyquist(xp)
    yp = nyquist(yp)
    zp = nyquist(zp)
    
    xp=np.fft.irfftn(xp)
    yp=np.fft.irfftn(yp)
    zp=np.fft.irfftn(zp)
    
    return xp, yp, zp
    

#Returns the updated positions of all of the particles.
def get_pos(fx, fy, fz, redshift, boxsize=100.0, ngrid=100):

    #xyz-space cell length
    cell_len=np.float(boxsize)/np.float(ngrid)

    
    #setup particles on a uniform grid in xyz
    sk = (ngrid,ngrid,ngrid)
    
    #This abc stuff is confusing to me in k or xyz apparently
    a = np.fromfunction(lambda x,y,z:x+0.5, sk).astype(np.float)
    b = np.fromfunction(lambda x,y,z:y+0.5, sk).astype(np.float)
    c = np.fromfunction(lambda x,y,z:z+0.5, sk).astype(np.float)
    a=cell_len*a.flatten()
    b=cell_len*b.flatten()
    c=cell_len*c.flatten()
    
    #change in time, given by the growth function
    d1=growthfunc(1./(1+redshift))/growthfunc(1.)
    
    #Scaled displacements by time.
    x=fx*d1
    y=fy*d1
    z=fz*d1
    
    #assuming ngrid=nparticles, displace particles from the grid
    a+=x.flatten()
    b+=y.flatten()
    c+=z.flatten()
    
    #periodic boundary conditions
    a[np.where(a<0)]+=boxsize
    a[np.where(a>boxsize)]-=boxsize
    b[np.where(b<0)]+=boxsize
    b[np.where(b>boxsize)]-=boxsize
    c[np.where(c<0)]+=boxsize
    c[np.where(c>boxsize)]-=boxsize
    return a, b, c
    
    
def redshift_dist(x, redshift, xp):

    #Assumes that observations are made along the x-axis  
    x = x.flatten()
    
    d1=growthfunc(1./(1+redshift))/growthfunc(1.)
    
    x += xp.flatten()*0.5*d1
     
    return x


#cosmological growth function. Unsure of where this comes from?
def growthfunc(a, omega_m=0.289796, omega_l=0.710204):
    da=a/10000.
    integral = 0.
    
    #manual, definite integration
    for i in range(10000):
        aa=(i+1)*da
        integral+=da/((aa*np.sqrt(omega_m/(aa**3)+omega_l))**3)
    return 5*omega_m/2*np.sqrt(omega_m/a**3+omega_l)*integral

# ensuring arrays are hermitian
def nyquist(xp):
    ngrid=xp.shape[0]
    xp[ngrid/2+1:,1:,0]= np.conj(np.fliplr(np.flipud(xp[1:ngrid/2,1:,0])))
    xp[ngrid/2+1:,0,0] = np.conj(xp[ngrid/2-1:0:-1,0,0])
    xp[0,ngrid/2+1:,0] = np.conj(xp[0,ngrid/2-1:0:-1,0])
    xp[ngrid/2,ngrid/2+1:,0] = np.conj(xp[ngrid/2,ngrid/2-1:0:-1,0])
    
    xp[ngrid/2+1:,1:,ngrid/2]= np.conj(np.fliplr(np.flipud(xp[1:ngrid/2,1:,ngrid/2])))
    xp[ngrid/2+1:,0,ngrid/2] = np.conj(xp[ngrid/2-1:0:-1,0,ngrid/2])
    xp[0,ngrid/2+1:,ngrid/2] = np.conj(xp[0,ngrid/2-1:0:-1,ngrid/2])
    xp[ngrid/2,ngrid/2+1:,ngrid/2] = np.conj(xp[ngrid/2,ngrid/2-1:0:-1,ngrid/2])
    return xp
