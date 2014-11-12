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
    def __init__(self, jobid, queue, state, ncpus, nodes, time, command, filename, last20=[]):
        self.jobid = jobid
        self.queue = queue
        self.state = state
        self.ncpus = ncpus
        self.nodes = nodes
        self.time = time
        self.command = command
        self.filename = filename
        self.last20 = last20
    
    ## __repr__: Inmate -> String
    ## Produces a string listing the number, name and sentence of self.
    def __repr__(self):
        return "JobID: " + str(self.jobid) + ", " + \
               "Queue: " + self.queue + ", " + \
               "State: " + self.state + ", " + \
               "# CPUs: " + str(self.ncpus) + ", " + \
               "Nodes: " + self.nodes + ", " + \
               "Time: " + self.time + ", " + \
               "Command: " + self.command + ", " + \
               "Filename: " + self.filename
    
    ## __eq__: Inmate Inmate -> Boolean
    ## Produces True iff self and other represent the same prisoner.
    def __eq__(self, other):
        return self.jobid == other.jobid and self.filename == other.filename
        
    ## __ne__: Inmate Inmate -> Boolean
    ## Produces True iff self and other represent different prisoners.
    def __ne__(self, other):
        return not(self.jobid == other.jobid and self.filename == other.filename)
