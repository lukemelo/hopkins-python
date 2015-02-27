############################
##       Luke Melo        ##
## University of Waterloo ##
##     Hopkins Group      ##
##       11/24/2014       ##
##     cpc_summary.py     ##
##         v1.0           ##
############################

import subprocess


def last20(log_filename):
    """
     Obtains the last 20 lines of a gaussian .log file with log_filename
     
     Consumes:
     - log_filename - Str: filename of the gaussian log file
     
     Produces:
     - last20_lines - (listof Str): last 20 lines of the gaussian file
    """
    fo = open(log_filename, "rw+")
    lines = fo.readlines()
    last20_lines = lines[-20:]
    #for i in range(len(last20_lines)):
        #print last20_lines[i]
    return last20_lines
        
        
def gauss_terminate_line(l_last20):
    """
     Loop through the last 20 lines of a .log file to check for standard error
     messages. The keywords here for error identification are:
     - 'Normal termination': geometry optimization converged
     - 'link 9999': geometry optimization has not converged
     - 'walltime': file has exceeded allowed runtime on SHARCNET servers
     - 'NtrErr': asking for information that isnt there (in .chk)
     
     Consumes:
     - l_last20 - (listof Str): last 20 lines of a .log file
     
     Produces:
     - terminate_status - Str: lreturns a string representing a specific error
    """
    
    terminate_status = ''
    for i in range(len(l_last20)):
        if 'Normal termination' in l_last20[i]:
            terminate_status = 'Normal termination'
        elif 'link 9999' in l_last20[i]:
            terminate_status = 'Link 9999 error'    
        elif 'FormBX had a problem' in l_last20[i]:
            terminate_status = 'FormBX had a problem'
        elif 'galloc: could not allocate memory' in l_last20[i]:
            terminate_status = 'galloc: could not allocate memory'
        elif 'Error termination via Lnk1e in /disc30/g98/l716.exe.' in l_last20[i]:
            terminate_status = 'Conversion from Z-matrix to cartesian coordinates failed'      
        elif 'Convergence failure -- run terminated.' in l_last20[i]:
            terminate_status = 'Conversion from Z-matrix to cartesian coordinates failed'
        elif 'termination in NtrErr' in l_last20[i]:
            terminate_status = 'NtrErr FileIO'
        elif 'walltime' in l_last20[i] and 'WARNING' not in l_last20[i]:
            terminate_status = 'Walltime error'    
    
    if terminate_status == '':
        return 'error check file'
    else:
        return terminate_status
            
            
subprocess.call(['ls > filedir.csv'],shell=True)
    
fo = open('filedir.csv', 'r')
filenames = fo.readlines()
fo.close
print 'filedir.csv created in current directory.'
print 'Processing files in current directory...'

l_norms = []
l_errors = []

for i in range(len(filenames)):
    temp = filenames[i].split('.')
    if len(temp) == 2:
        #print temp[0] + '.' + temp[1]
        if temp[1] == 'log\n':
            termination_status = gauss_terminate_line(last20(temp[0]+'.log'))
            if termination_status == 'Normal termination':
                l_norms.append(temp[0]+'.log')
            else:
                l_errors.append(temp[0]+'.log'+','+termination_status+'\n')
    
                
                
## get energies of normally terminated logs                
for i in range(len(l_norms)):
    fo = open(l_norms[i])
    lines = fo.readlines()
    fo.close
    HF = ''
    cce = ''
    bsse = ''
    som = ''
    ce_raw = ''
    ce_corr = ''
    for line in lines:
        if 'SCF Done:' in line:
            HF = line.split()[4]
        elif 'Counterpoise corrected energy' in line:
            cce = line.split()[-1]
        elif 'BSSE energy' in line:
            bsse = line.split()[-1]            
        elif 'sum of monomers' in line:
            som = line.split()[-1] 
        elif '(raw)' in line:
            ce_raw = line.split()[-3]             
        elif '(corrected)' in line:
            ce_corr = line.split()[-3]        
            
    l_norms[i] = l_norms[i] + ',' + HF + ',' + cce + ',' + bsse + ',' + som + ',' + ce_raw + ',' + ce_corr +'\n'
    print l_norms[i]
    #print l_norms[i]

l_write = l_norms + l_errors 
#for i in range(len(l_errors)):
    #print l_errors[i]
   
wrt_srt = 'Filename,HF Energy,Counterpoise Corrected Energy,BSSE Energy,Sum of Momomers,Raw Complexation Energy [kcal/mole],Corrected Complexation Energy [kcal/mole]\n'    
for i in range(len(l_write)):
    wrt_srt = wrt_srt + l_write[i]   
    
fw = open('cpc_job_summary.csv','w')
fw.writelines([wrt_srt])
fw.close
print 'job_summary.csv created in current directory'            
        
