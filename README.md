ls_structure project documentation

The aim of this code is to use the Zeldovich approximation to generate an initial set of 
conditions for an n-body simulation from a given power spectrum (referred to hereafter as a pk)


Folder names in all capitals should NOT be accessed at runtime for either read/write use.

Folder breakdown (Alphabetically):
- CBUILD:
    Simple storage folder for the code that generates the cicdens.so hybrid python / C module.
    Should not be needed at runtime.

- CORDELIA:
    Contains the necessary files to run a multitude of serial simulations as per the Cordelia
    model. The two files should be copied into the main folder and renamed to replace
    exeMAIN.py and queue_script_main.sh.

- COSMA:
    Similar to CORDELIA, however this folder is less likely to be required as it contains
    an ungodly amount of unnecessary, unwieldy code. Cordelia is probably nicer in every way.

- dump:
    The output folder for all .out and .err files generated at runtime.

- micromodules: 
    Contains all miscellaneous modules that are not required for the actual process of 
    simulation. IO and Pyplot rendering modules are contained herein.

- pks:
    Contains any pk files in a .txt format. The default file is pk_indra7313.txt.

- results:
    Should contain image results gathered from the actual simulations however the purpose of
    this folder is not overly well defined, I'm just slightly sure that it is necessary.

- seeds:
    Will contain a number of different numpy seed arrays. This is intended to allow for
    troubleshooting and easier to use pseudo-random generation however this is not needed
    explicitly yet.
    


File breakdown (Alphabetically):
- cicdens.so:
    A C/Python hybrid module that is accessed by cic_dens_wrapper.py. This code runs the cloud 
    in cell method of calculating the density grid from the final particle positios. Should
    never need to be called explicitly, instead, being only accessed from the wrapper code.
    
- cic_dens_wrapper.py:
    This module interfaces between the exeMAIN.py simulation handler and the cicdens.so cloud-in
    -cell algorithm. Contains a single function that returns the density grid and is very easy
    to use.

- exeMAIN.py:
    The brains of the outfit. exeMAIN is the highest level code and calls upon the other modules
    in sequence to run the full simulation and statistical calculation. Running different versions
    of this code allows for execution on different HPC queues, with CORDELIA and COSMA being the
    main ones. In terms of the design of the whole simulation, all necessary code should be run
    with a single call to exeMAIN.

- queue_script_main.sh:
    This batch script should submit HPC jobs to the supercomputer. This code should vary depending
    on the job required and should not always be required.

- README.txt:
    "ls_structure project documentation. The aim of this code is to use the Zeldovich approximation
     to generate an initial set of conditions for an n-body simulation from a given power spe..."

- spatial_stats.py:
    An arkane monstrosity that carries out the calculation of the 1D and 2D correlation function from
    a given density grid.

- zeldovich_init.py:
    Generates an initially distorted particle position grid using the zeldovich approximation by
    taking a pk and some other parameters such as boxsize and grid resolution.


