"""cmparallel.py. Frank Cleary fcleary@berkeley.edu Jan. 31 2014

Run simulations of dynein motility in parallel.
"""
import multiprocessing
import time
import csv
import os
import numpy as np
import pandas as pd
import functools

from cmfunctions import runtrace

def get_traces(mutant, ratedict, sg,  num_traces=200,
               n_iterations=20000,
               time_step=0.005):
        """Simulate traces of a dynein mutant, return the average
        and standard deviation of the traces.

        Parameters:
        mutant: The name of the mutant
        ratedict: A dictionary containing the rates of relevant
        processes. See run_simulation.py and findrates.py
        sg: A dictionary containing stepping geometry parameters,
        such as the average step size.
        keys in sg:
            distwidth: the s.d. of the stepping distribution
            fwdbias: forward bias of landing site, from partner head, 
            during powerstroke stepping
            tstart:  distance (head to head separation) at which
            tension based stepping begins
            diffstop:  distance (head to head separation) at which
            powerstroke steps stop
            tensionbias:  the average distance, from partner head,
            that a tension stepping head will land
        num_traces: the number of traces to simulate
        n_iterations: the number of iterations in each trace
        time_step: the amount of time represented by each iteration,
        in seconds.
        """
        # create a partial function to passing into map
        rtf_partial = functools.partial(runtrace, ratedict=ratedict, 
                                        stepping_geometry=sg,
                                        time_step=time_step, 
                                        n_iterations=n_iterations)
        randarray = np.random.rand(num_traces, n_iterations)
        stime = time.time()
        pool = multiprocessing.Pool()
        traces = pool.map(rtf_partial, randarray)
        pool.close()
        pool.join()
        print mutant
        print "Took: %0.2f s" % (time.time() - stime)
        speeds = [(trace[0][-1] + trace[1][-1]) / \
                  (2 * time_step * n_iterations)
                  for trace in traces]
        avgspeed = np.mean(speeds)
        stdev = np.std(speeds)
        print "Mean: %0.2f nm/s" % avgspeed
        return avgspeed, stdev

if __name__ == '__main__':
    pass
