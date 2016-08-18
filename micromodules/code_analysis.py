import numpy as np
import glob
import os
import re

def read_dump(folder, search):
    search_results = glob.glob(os.path.join(folder, search))

    time   = np.zeros(len(search_results))
    memory = np.zeros(len(search_results))

    count = 0
    for result_ in search_results:
        file_ = open(result_, 'r')
        for line_ in file_:
            if 'CPU time' in line_:
                t_ = re.findall("\d+\.\d+", line_)
                time[count] = float(t_[0])

            if 'Max Memory' in line_:
                m_ = re.findall("\d+", line_)
                memory[count] = int(m_[0])
        count += 1
    return time, memory

if __name__ == "__main__":
    folder = "/cosma/home/durham/rhgk18/ls_structure/dump/b256_ng256_np256"
    search = "zeldovich*.out"

    time, memory = read_dump(folder, search)
    
    print "\nMemory Usage:"
    print "Mean : ", str(np.mean(memory))
    print "Max  : ", str(memory.max()), "\n"

    print "Execution Time:"
    print "Mean : ", str(np.mean(time))
    print "Max  : ", str(time.max())
