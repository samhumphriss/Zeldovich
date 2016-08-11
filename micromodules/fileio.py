import os
import numpy as np
import glob

def mkdir(f):
    if not os.path.exists(f):
        os.makedirs(f)

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

def write_r(loc, r):
    fileloc = loc+"/r.txt"
    if not os.path.exists(fileloc):
        np.savetxt(fileloc, r)

def write_xi(loc, xi, seed):
    fileloc = loc+"/xi_SEED_"+str(seed)+".txt"
    if not os.path.exists(fileloc):
        np.savetxt(fileloc, xi)

def import_seedbank(filename):
    seed_path = os.getcwd() + "/seeds/" + filename  
    return np.loadtxt(seed_path)

def import_pk(filename):
    pk_path = os.getcwd() + "/pks/" + filename  
    return np.loadtxt(pk_path)

def importxi_fromfolder(folder, search):
    search_results = glob.glob(os.path.join(folder, search))

    dtest = np.loadtxt(search_results[0])

    data = np.zeros((len(search_results),len(dtest)))

    for index in range(len(search_results)):
        data[index] = np.loadtxt(search_results[index])

    return data

def importxi2d_fromfolder(folder, search):
    search_results = glob.glob(os.path.join(folder, search))

    dtest = np.loadtxt(search_results[0])

    data = np.zeros((len(search_results),len(dtest)))

    for index in range(len(search_results)):
        data[index] = np.loadtxt(search_results[index])

    return data





#---------------------------------------------------
#Unnecessary, identical code to np.loadtxt()
def DEPRECATED_import_pk(filename):
#Takes a txt list and returns a numpy array of P(k)

    pk_path = os.getcwd() + "/pks/" + filename  

    with open(pk_path) as f:
        pk = [line.split() for line in f]
    
    pk_n = np.array(pk).astype(np.float)
    
    return pk_n
