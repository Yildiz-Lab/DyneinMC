import numpy as np


def whichrear(head1, head2):
    """Return 1 if head 1 is in the rear, 2 if head 2"""
    if head1 < head2:
        return 1
    else:
        return 2


def atpstep(stepping_geometry, fixedhead):
    """Return fixedhead plus a number drawn from a random distribution
    with mean fwdbias and standard deviation distwidth.
    """
    return fixedhead + \
           np.random.normal(stepping_geometry['fwdbias'],
                            stepping_geometry['distwidth'])


def tstep(stepping_geometry, fixedhead, rearstep=True):
    """Return fixedhead plus a number drawn from a random distribution
    with mean bias and standard deviation distwidth.
    """
    sign = -1 * ((rearstep - 1) * 2 + 1)
    return fixedhead + \
           np.random.normal(sign * stepping_geometry['tensionbias'],
                            stepping_geometry['distwidth'])

    
def calc_lims(ratedict, time_step, ihs):
    """Return an dict, lims dict where lims[process] is an interval on
    [0, 1) such that lims[process][1] - lims[process][0] = probability
    that process will occur in time time_step and the intervals do not
    intersect for different processes.
    """
    lims = {}
    startpoint = 0

    # fill in values for all the rates that are not functions of ihs
    for key, value in ratedict.iteritems():
        if not 'tstepforw' in key:
            probability = 1 - np.exp(-time_step * value)
            lims[key] = (startpoint, startpoint + probability)
            startpoint += probability
    # fill in the rates for tension stepping of the rear head
    for head in ['h1', 'h2']:
        rate = ratedict[head + 'tstepforwint'] + \
               ratedict[head + 'tstepforwslope'] * ihs
        probability = 1 - np.exp(-time_step * rate)
        lims[head + 'tstepforw'] = (startpoint,
                                    startpoint + probability)
        startpoint += probability
    return lims

def occurs(r, limtuple):
    """Return true if r is in between the first and second values of
    limtuple, else false.
    """
    return r >= limtuple[0] and r < limtuple[1]

def runtrace(rands, ratedict={}, stepping_geometry={}, 
             time_step=0, n_iterations=0):
    """Run the simulation

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
    head1 = 16
    head2 = -16

    track1 = np.zeros(n_iterations + 1)
    track2 = np.zeros(n_iterations + 1)
    track1[0] = head1
    track2[0] = head2
    ihs = np.abs(head1 - head2)
    lims = calc_lims(ratedict, time_step, ihs)
    rand_array = rands

    for i in xrange(1, n_iterations + 1):
        r = rand_array[i-1]
            
        if ihs != np.abs(head1 - head2):
            ihs = np.abs(head1 - head2)
            lims = calc_lims(ratedict, time_step, ihs)

        if max(lims.values())[1] > .9:
            print("Limits > .9, reduce time step")
            return
        if r > max(lims.values())[1]:
            track1[i] = head1
            track2[i] = head2
            continue
        
        rear = whichrear(head1,head2)

        if ihs > stepping_geometry['tstart']:
            tension = True
        else:
            tension = False

        # biased diffusion stepping
        if ihs < stepping_geometry['diffstop']:
            if occurs(r, lims['h1atprelease']):
                head1 = atpstep(stepping_geometry, fixedhead=head2)
            elif occurs(r, lims['h2atprelease']):
                head2 = atpstep(stepping_geometry, fixedhead=head1)

        if tension:
            if rear == 1:
                # head1 in rear, tension stepping
                if occurs(r, lims['h1tstepforw']):
                    head1 = tstep(stepping_geometry, fixedhead=head2)
                # head2 in front, tension stepping
                elif occurs(r, lims['h2tstepback']):
                    head2 = tstep(stepping_geometry, fixedhead=head1,
                                  rearstep=False)
            elif rear == 2:
               # head2 in rear, tension stepping
               if occurs(r, lims['h2tstepforw']):
                   head2 = tstep(stepping_geometry, fixedhead=head1)
               # head1 in front, tension stepping
               elif occurs(r, lims['h1tstepback']):
                   head1 = tstep(stepping_geometry, fixedhead=head2,
                                 rearstep=False)
        # head2 non-directional stepping
        elif occurs(r, lims['h2nodirrelease']):
            head2 = head1 + \
                    np.random.normal(0,
                                     stepping_geometry['distwidth'])
        elif occurs(r, lims['h1nodirrelease']):
            head1 = head2 + \
                    np.random.normal(0,
                                     stepping_geometry['distwidth'])

        track1[i] = head1
        track2[i] = head2

##    plt.plot(track1)
##    plt.plot(track2)
##    plt.show(block=False)

    return track1, track2
