import numpy as np
import numpy.random as npr
import cmfunctions as cmf
import time
import csv

SIZEFILE = 'sizes.csv'

start_time = time.time()

# number of steps in simulation
n_iterations = 10000

# length of time (in s) of each step
time_step = 0.005

def read_sg(sizefile):
    """Return a dictionary of stepping geometry parameters read from a file.

    SIZEFILE is a csv file with format
    parameter1, value1
    parameter2, value2

    Parameters:
    distwidth: the s.d. of the stepping distribution
    fwdbias: forward bias of landing site, from partner head, 
        during powerstroke stepping
    tstart:  distance (head to head separation) at which tension based 
        stepping begins
    diffstop:  distance (head to head separation) at which powerstroke steps 
        stop
    tensionbias:  the average distance, from partner head, that a tension 
        stepping head will land
    
    Example file:
    distwidth,16
    fwdbias,8
    tstart,12
    diffstop,20
    tensionbias,8
    """
    with open(sizefile, 'rb') as f:
        sizedict = dict(csv.reader(f, delimiter=','))
    for key, value in sizedict.iteritems():
        sizedict[key] = float(value)
    return sizedict


def read_rates(ratefile):
    """Return a dictionary of rates for processes, read from a file.

    ratefile is a csv file with format
    process1, rate1
    process2, rate2

    Processes:
    h1atprelase: release of head1 from the MT due to ATP binding
    h2atprelase: release of head2 from the MT due to ATP binding
    h1tstepback: release of head1 due to tension when head1 leads
    h2tstepback: release of head2 due to tension when head2 leads
    h2nodirrelase: release of head2 due to weak MT binding of head2
    h1stepforwint: y-intercept (interhead separation = 0) value of the line
        definiting head1 release as a funciton of interhead separation when
        head1 trails
    h1tstepforslope: slope value of the line definiting head1 release as a 
        funciton of interhead separation when head1 trails
    h2stepforwint: y-intercept (interhead separation = 0) value of the line
        definiting head2 release as a funciton of interhead separation when
        head2 trails
    h2tstepforslope: slope value of the line definiting head2 release as a 
        funciton of interhead separation when head2 trails
    Example file:
    
    parameter,value
    h1atprelease,8
    h2atprelease,8
    h1tstepback,1.5
    h2tstepback,1.5
    h2nodirrelease,0
    h1tstepforwint,5
    h1tstepforwslope,0.208
    h2tstepforwint,5
    h2tstepforwslope,0.208
    """
    with open(ratefile, 'rb') as f:
        ratedict = dict(csv.reader(f, delimiter=','))
    for key, value in ratedict.iteritems():
        ratedict[key] = float(value)
    return ratedict

def get_data(sizefile='sizes.csv', ratefile='rates.csv'):
    rates = read_rates(ratefile)
    stepping_geometry = read_sg(sizefile)
    speed = []
    for j in range(50):
        final = cmf.runtrace(rates,sg,time_step,n_iterations)
        tracespeed = np.average([final[2], final[3]])/(n_iterations*time_step)
        speed = np.append(speed,tracespeed)
        
    print (time.time() - start_time)
    print ('Average speed ', np.average(speed))
    print ('Speed std ', np.std(speed))
    return [np.average(speed),np.std(speed)]
