"""run_simulation.py. Frank Cleary fcleary@berkeley.edu Jan. 31 2014

A master script for the dynein simulation model. The "main" function,
run_simulation, reads in pairs of heads (representing different
mutants) from mutants.csv. The names of these heads are matched
with rates calculated from optical trap data, and simulations are run.

Will also compare the results with experiment and plot the results.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import cmparallel as cmp
import findrates


def run_simulation(num_traces=200, n_iterations=20000,
                   time_step=0.005, nmperpn=12):
    """Run simulated dynein traces.

    Determines rates from optical trap data using findrates.findrates,
    reads in mutants to simulation from mutants.csv, and stepping
    geometry from sizes.csv.

    Parameters:
    num_traces: The number of traces to simulate for each mutant
    n_iterations: The number of iterations in each trace
    time_step: the amount of time represented by each iteration
    """
    findrates.findrates(nmperpn)  # generate rates from trap data
    rates = pd.read_csv('../simulations/rates.csv')
    mutants = pd.read_csv('../simulations/mutants.csv')
    rates = rates.set_index('head')
    rates = rates.T
    mutants = mutants.set_index('mutant')
    mutants = mutants.T
    sg = pd.read_csv('../simulations/sizes.csv', header=None,
                     index_col=0) 
    sg = sg[1].to_dict()

    results = pd.DataFrame()
    for col in mutants.columns:
        ratedict = {}
        for head in mutants.index:
            r = rates[mutants.loc[head, col]].to_dict()
            r = {head + k: v for k, v in r.iteritems()}
            ratedict.update(r)
        mean, sd = cmp.get_traces(col, ratedict, sg,
                                  num_traces=num_traces,
                                  n_iterations=n_iterations,
                                  time_step=time_step)
        results[col] = pd.Series({'simMean': mean, 'simS.D.': sd})
    return results

def compare_results(results):
    """Return a DataFrame comparing results of a simulation (results)
    to experimental data read in from a file.

    Parameters:
    results: A DataFrame with simulation results, i.e. the return
    value of run_simulation()
    """
    experiment = pd.read_csv('../experiment/speed_sd.csv')
    experiment.set_index('mutant', inplace=True)
    experiment = experiment.T
    comp = results.T.join(experiment.T)
    return comp

def plot_results(comp):
    """Produce a plot comparing the results of the simulation to
    experimental results.

    Parameters:
    comp: A DataFrame, such as that generated by compare_results()
    """
    plt.bar(np.arange(1.2, 7), comp['exMean'], align='center',
            width=.4, yerr=comp['exS.D.'], ecolor='k',
            label='Experiment')
    plt.bar(np.arange(.8, 6), comp['simMean'], align='center',
            width=.4, color='red', yerr=comp['simS.D.'], ecolor='k',
            label='Simulation')
    plt.ylabel(r'Speed $nm/s$', size='x-large')
    plt.xlabel('Mutant')
    plt.legend()
    plt.xticks(xrange(1,7), comp.index, rotation=90, size='large')
    plt.tight_layout()
    plt.savefig('../output/comparison.png', dpi=600)
    plt.savefig('../output/comparison.eps', dpi=600)

if __name__ == '__main__':
    np.random.seed(424)
    results = run_simulation(num_traces=200, n_iterations=20000,
                            time_step=0.005)
    results.to_csv('../output/results.csv')
    comp = compare_results(results)
    plot_results(comp)