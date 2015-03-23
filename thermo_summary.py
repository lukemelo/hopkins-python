############################
##       Luke Melo        ##
## University of Waterloo ##
##     Hopkins Group      ##
##       03/23/2015       ##
##    thermo_summary.py   ##
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
subprocess.call('rm filedir.csv')
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
    ZPE = ''
    TCEn = ''
    TCEnth = ''
    TCGFE = ''
    Sum_ZPEs = ''
    Sum_TEn = ''
    Sum_TEnth = ''
    Sum_ETFE = ''
    for line in lines:
        if 'Zero-point correction=' in line:
            ZPE = line.split()[-2]
        elif 'Thermal correction to Energy=' in line:
            TCEn = line.split()[-1]
        elif 'Thermal correction to Enthalpy=' in line:
            TCEnth = line.split()[-1]            
        elif 'Thermal correction to Gibbs Free Energy=' in line:
            TCGFE = line.split()[-1] 
        elif 'Sum of electronic and zero-point Energies=' in line:
            Sum_ZPEs = line.split()[-1]    
        elif 'Sum of electronic and thermal Energies=' in line:
            Sum_TEn = line.split()[-1]
        elif 'Sum of electronic and thermal Enthalpies=' in line:
            Sum_TEnth = line.split()[-1]
        elif 'Sum of electronic and thermal Free Energies=' in line:
            Sum_ETFE = line.split()[-1]        
            
    l_norms[i] = l_norms[i] + ',' + ZPE + ',' + TCEn + ',' + TCEnth + ',' + TCGFE + ',' + Sum_ZPEs + ',' + Sum_TEn + ',' + Sum_TEnth+ ',' + Sum_ETFE +'\n'
    print l_norms[i]
    #print l_norms[i]

l_write = l_norms + l_errors 
#for i in range(len(l_errors)):
    #print l_errors[i]
   
wrt_srt = 'Filename,Zero-point correction,Thermal correction to Energy,Thermal correction to Enthalpy,Thermal correction to Gibbs Free Energy,Sum of electronic and zero-point Energies,Sum of electronic and thermal Energies,Sum of electronic and thermal Enthalpies,Sum of electronic and thermal Free Energies\n'    
for i in range(len(l_write)):
    wrt_srt = wrt_srt + l_write[i]   
    
fw = open('thermo_job_summary.csv','w')
fw.writelines([wrt_srt])
fw.close
print 'thermo_job_summary.csv created in current directory'            
        
