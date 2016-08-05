import os
import numpy as np

def mkdir(f):
    if not os.path.exists(f):
        os.mkdir(f)

def import_pk(filename):

    pk_path = os.getcwd() + "/pks/" + filename  
    return np.loadtxt(pk_path)

def write_rp(loc, rp):
    fileloc = loc+"/rp.txt"
    if not os.path.exists(fileloc):
        np.savetxt(fileloc, rp)
    
def write_pi(loc, pi):
    fileloc = loc+"/pi.txt"
    if not os.path.exists(fileloc):
        np.savetxt(fileloc, pi)
    
def write_xi2d(loc, xi2d, seed):
    fileloc = loc+"/xi2d_SEED_"+str(seed)+".txt"
    if not os.path.exists(fileloc):
        np.savetxt(fileloc, xi2d)

def import_seedbank(filename):
    seed_path = os.getcwd() + "/seeds/" + filename  
    return np.loadtxt(seed_path)


#---------------------------------------------------
#Unnecessary, identical code to np.loadtxt()
def DEPRECATED_import_pk(filename):
#Takes a txt list and returns a numpy array of P(k)

    pk_path = os.getcwd() + "/pks/" + filename  

    with open(pk_path) as f:
        pk = [line.split() for line in f]
    
    pk_n = np.array(pk).astype(np.float)
    
    return pk_n
