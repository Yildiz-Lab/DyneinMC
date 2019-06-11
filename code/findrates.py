"""findrates.py. Frank Cleary fcleary@berkeley.edu Jan. 31 2014
Reads in data from optical trapping experiments on different dynein
mutant monomers and creates a .csv file containing information from
fitting the rates. This file is used to run simulations of dynein
motility.
"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf


def fit(data):
    """Return a linear model of rate to force."""
    model = smf.ols("rate ~ force", data=data).fit()
    return model
    

def findrates(nmperpn=12):
    """Write a csv file containing rates measured from optical
    trapping and published ATPase assays ('atpaserates.csv').

    Parameters:
    nmperpn: The number of nm of interhead separation to cause a 1 pN
    change in interhead tension (the change is assumed to be linear).

    Processes:
    atprelase: release of a head from the MT due to ATP binding
    tstepback: release of a head due to tension when the head leads
    nodirrelase: release of a head due to weak MT binding
    tstepforwint: y-intercept (interhead separation = 0) value of the
    line defining head release as a function of interhead separation
    when the head trails
    tstepforslope: slope value of the line defining head release as
    a function of interhead separation when the head trails
    """    
    atpase = pd.read_csv('../simulations/atpaserates.csv')
    atpase.index = atpase['head']
    atpase = atpase['atpaserate']
    files = os.listdir('../trap_data/')
    files = [f for f in files if f.endswith('.csv')]
    fits = pd.DataFrame()
    for f in files:
        df = pd.read_csv('../trap_data/' + f)
        avgrate = df[df['force'] < 0].mean()['rate']
        model = fit(df[df['force'] > 0])
        nodirr = fit(df[df['force'] < 0]).params.Intercept
        fits[f[:-8]] = model.params.append(
                                      pd.Series({'avgrate': avgrate,
                                                 'nodirr': nodirr})
                                    )
    fits = fits.T
    tensionpernm = 1/float(nmperpn)
    fits['Slope'] = fits['force'] * tensionpernm
    fits = fits[['avgrate', 'nodirr', 'Intercept', 'Slope']]
    rates = fits.join(atpase)
    rates.columns = ['tstepback', 'nodirrelease', 'tstepforwint',
                     'tstepforwslope', 'atprelease']
    rates.to_csv('../simulations/rates.csv', index_label='head')


if __name__ == '__main__':
    findrates()
