Dynein monte carlo model
Frank Cleary
fcleary@berkeley.edu

collect data with

"python run_simulations.py"

from the code/ directory

This will output to output/ directory

The following parameters were used to define the geometry of the model:
 
distwidth: the s.d. of the stepping distribution for both tension-dependent and powerstroke stepping (16 nm).
fwdbias: forward bias of landing site, in front of non-stepping head, during powerstroke stepping (8 nm).
tstart:  distance (head to head separation) at which tension based stepping begins (12 nm)
diffstop:  distance (head to head separation) at which powerstroke steps stop (20 nm)
tensionbias:  the average distance, from partner head, that a tension stepping head will land (8 nm)
 
Rates, except for powerstroke rates, which are reported ATPase rates, are derived from linear fits to our optical trapping assay. 

atprelease: release of a head from the MT due to ATP binding (powerstroke stepping). From reported ATPase rates.
tstepback: release of a head due to tension when the head leads. Calculated from the average value of the release rates measured under (+)-end directed force.
nodirrelase: release of a head due to weak MT binding. Measured from the y-intercept (0-force value) of the linear fit to release rates measured under (+)-end directed force.
tstepforwint: y-intercept (interhead separation = 0) value of the line defining head release as a function of interhead separation when the head trails
tstepforslope: slope value of the line fit to release rates measured under (-)-end directed force.
