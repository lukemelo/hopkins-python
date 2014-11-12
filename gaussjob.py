############################
##       Luke Melo        ##
## University of Waterloo ##
##     Hopkins Group      ##
##       09/26/2014       ##
##      gaussjob.py       ##
##         v1.0           ##
############################

class gaussjob:
    """
     A simple public storage class representing a gaussian job on SHARCNET
     Fields: jobid - int: a unique job identification
             queue - str: private queue label
             state - str: current job status, 'D', 'Q', or 'R'
             ncpus - int: number of cpu cores used for calculation
             nodes - str: specific node calculation was run on
             time  - str: duration of time spent in current state
             command - str: program command (usually 'g09')
             filename - str: filename
             last20 - (listof str): last 20 lines in the gaussian output file contained in a list
    """
    
    # Examples omitted
    
    ## Produces an inmate with the given id, name and sentence in years.
    ## If not provided, default sentence is 10 years.
    def __init__(self, jobid='', state='', filename='', last20=[], walltime = False):
        self.jobid = jobid
        self.state = state
        self.filename = filename
        self.last20 = last20
	self.walltime = walltime
    
    ## __repr__: Inmate -> String
    ## Produces a string listing the number, name and sentence of self.
    def __repr__(self):
        return "JobID: " + str(self.jobid) + ", " + \
               "State: " + self.state + ", " + \
               "Filename: " + self.filename + ", " + \
               "Walltime Status: " + str(self.walltime)
    
    ## __eq__: Inmate Inmate -> Boolean
    ## Produces True iff self and other represent the same prisoner.
    def __eq__(self, other):
        return self.jobid == other.jobid and self.filename == other.filename
        
    ## __ne__: Inmate Inmate -> Boolean
    ## Produces True iff self and other represent different prisoners.
    def __ne__(self, other):
        return not(self.jobid == other.jobid and self.filename == other.filename)
