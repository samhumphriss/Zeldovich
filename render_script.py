import micromodules.fileio as io
import micromodules.render as rd
import numpy as np
import glob
import os


if __name__ == "__main__":
    folder = "/gpfs/data/rhgk18/results/b1024_ng512_np1024"
    search = "xi_*"
    rd.xi_resid(folder, search)
