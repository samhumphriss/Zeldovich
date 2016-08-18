import micromodules.fileio as io
import micromodules.render as rd
import numpy as np
import glob
import os


if __name__ == "__main__":

    folder = "/gpfs/data/rhgk18/results/b1024_ng256_np256_t300"

    rd.xi_covariance(folder)
