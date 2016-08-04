class timer:
    """
    Timer class, designed to provide a portable method of timing specific sections of code
    within a given function. Multiple clocks can be started and stopped at different points
    and a final breakdown of the proportions of the runtime can be printed.
    """

    fclock = 0
    times = []
    
    def __init__(self):
        pass

    def start_fclock(self):
        self.fclock = time.time()
        print "Initialising function clock.\n"
    
    def stop_fclock(self):
        self.fclock = time.time() - self.fclock

    def start_clock(self, number):
        self.times.append(time.time())
        print "Initialising clock #" + str(len(self.times)-1) + ".\n"

    def stop_clock(self, number):
        if(number >= len(self.times) or number < 0):
            print "ERROR: CLOCK #" + str(number) + " IS UNINITIALISED."
        else:
            self.times[number] = time.time() - self.times[number]


    def print_diag(self):

        remainder = 100.0

        print "Fclock: " + str(np.round(self.fclock,5)) + "\n"
        print "Clock Timing Data:"

        for n in range(len(self.times)):
            print "Clock #" + str(n) + ": " + str(np.round(self.times[n],5)) + "  (" + str(np.round(self.times[n]/self.fclock*100, 5)) + "%)"
            remainder -= self.times[n]/self.fclock*100           
        
        print "\nTotal recorded time: " + str(np.round(100-remainder, 5)) + "%\n"

if "__name__" == "__main__":
    print "Timer class. Import module."
