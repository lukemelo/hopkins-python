############################
##       Luke Melo        ##
## University of Waterloo ##
##     Hopkins Group      ##
##       01/01/2015       ##
##   log_to_gjf_unix.py   ##
##         v1.3           ##
############################
"""
Created on Sun Dec 21 23:27:32 2014

@author: lukemelo

Some text explaining everything goes here
"""

errors = True
#errors = False

#####################################################
# Use optimized/last geometry in *.log files
#lowest_energy = 1
# Backstep n SCF iterations
lowest_energy = 0
# Backstep to initial geometry from *.gjf input
#lowest_energy = 2**32
#####################################################
#####################################################
# Use optimized/last geometry in *.log files
backsteps = 0
# Backstep n SCF iterations
#backsteps = 10
# Backstep to initial geometry from *.gjf input
#backsteps = 2**32
#####################################################

# DFTB Parameters
#link0_cmds = []
#job_keywords = '# opt dftb scf=(maxconventionalcycles=150,xqc)'
#skf_dir = '/home/gaztick/skf/'
#job_title = 'DFTB 4-Aminobenzoic Acid MeOH Clustering'
#gjf_dir = 'DFTB'


## HF Parameters:
#link0_cmds = ['%nosave','%mem=8gb','%nprocs=4']
#job_keywords = '# opt freq rhf/3-21g geom=connectivity'
#job_title = 'HF 4-Aminobenzoic Acid MeOH Clustering'
#gjf_dir = 'HF'

## DFT Parameters:
#link0_cmds = ['%mem=8gb','%nprocs=8']
#job_keywords = '# opt freq b3lyp/6-31+g(d,p)'
#job_title = 'DFT 4-Aminobenzoic Acid MeOH Clustering'
#gjf_dir = 'DFT'

## DFT-GD3 Parameters:
link0_cmds = ['%mem=12gb','%nprocs=8']
job_keywords = '# opt freq b3lyp/6-31+g(d,p) geom=connectivity EmpiricalDispersion=GD3'
job_title = 'DFT-GD3 4-Aminobenzoic Acid MeOH Clustering'
gjf_dir = 'DFT_GD3'


######################################
def dftb_gjfadd(skf_dir,l_atoms):
    """
    Consumes:
    - skf_dir [str]: file directory containing all dftb .skf files
    'C:/G09W/'

    - l_atoms [listof str]: list of all unique atoms in gjf
    ['C','H']

    Produces:
    l_write [listof str]: lines to append to end of # dftb opt gjf input
    ['@C:/G09W/C-C.skf\n','@C:/G09W/C-H.skf\n','@C:/G09W/H-C.skf\n','@C:/G09W/H-H.skf\n']
    """
    l_write = []
    for i in range(len(l_atoms)):
        for j in range(len(l_atoms)):
            line = '@' + skf_dir + l_atoms[i] + '-' + l_atoms[j] + '.skf/N\n'
            if line not in l_write:
                l_write.append(line)
    return l_write
######################################

import os

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
                    
os.system('ls > filedir.csv')
    
fo = open('filedir.csv', 'r')
filenames = fo.readlines()
fo.close
os.system('rm filedir.csv')
print 'Filelist compiled in current directory.'
print 'Processing files in current directory...'

l_norms = []
l_errors = []
d_errors = {}

for i in range(len(filenames)):
    temp = filenames[i].split('.')
    if len(temp) == 2:
        #print temp[0] + '.' + temp[1]
        if temp[1] == 'log\n':
            termination_status = gauss_terminate_line(last20(temp[0]+'.log'))
            if termination_status == 'Normal termination':
                l_norms.append(temp[0]+'.log')
            else:
                l_errors.append(temp[0]+'.log')
		d_errors[temp[0]] = termination_status
               

d_filesort = {}
HF_unsorted = []
## get energies of normally terminated logs                
for i in range(len(l_norms)):
    fo = open(l_norms[i])
    lines = fo.readlines()
    fo.close
    HF = ''
    for line in lines:
        if 'SCF Done:' in line:
            HF = line.split()[4]
    HF_unsorted.append(float(HF))
    d_filesort[float(HF)] = l_norms[i]
    #l_norms[i] = l_norms[i] + ',' + HF + '\n'
    
    #print l_norms[i]
print d_filesort
print HF_unsorted
HF_unsorted.sort()
print HF_unsorted

log_filenames = []
for i in range(len(l_norms)):
    print i
    print d_filesort[HF_unsorted[i]]
    log_filenames.append(d_filesort[HF_unsorted[i]])

# lowest energy implementation
if lowest_energy <= len(log_filenames):
    log_filenames = log_filenames[:lowest_energy]
elif lowest_energy <= 0:
    print 'specify > 0 lowest energy structures'

if errors and lowest_energy > 0:
    log_filenames = log_filenames + l_errors
elif errors:
    log_filenames = l_errors
	
    

    
#for i in range(len(l_errors)):
    #print l_errors[i]
   
######wrt_srt = ''    
######for i in range(len(l_write)):
    ######wrt_srt = wrt_srt + l_write[i]   
######print wrt_srt
    
######fw = open('poo.csv','w')
######fw.writelines(l_write)
######fw.close
######print 'job_summary.csv created in current directory'        



#####################################################################################


## add '\n' to link0_cmds and keywords if parameters are specified
#if 'link0_cmds' in locals():
#    for i in range(len(link0_cmds)):
#        link0_cmds[i] = link0_cmds[i] + '\n'
#if 'keywords' in locals():
#    keywords = keywords + '\n'


if os.path.isdir(gjf_dir):
    os.system('rm '+gjf_dir+'/*.gjf')
os.system('mkdir '+ gjf_dir)


####### Generate a list of log files in current directory to be processed
#######os.system('ls *.log > logs.csv')
#######fo = open('logs.csv')
#######fo = open('filemove.csv')
#######fo = open('job_summary.csv')
######log_filenames = fo.readlines()
######fo.close
######for i in range(len(log_filenames)):
    ######log_filenames[i] = log_filenames[i].split('\n')[0]
#######os.system('rm job_summary.csv')

# For dftb *.skf filename generation
# atom_map[atomic # - 1] --> atomic label [string]
atom_map = ['H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg',
           'Al','Si','P','S','Cl','Ar','K','Ca','Sc','Ti','v','Cr','Mn',
           'Fe','Co','Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr','Rb','Sr',
           'Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn','Sb',
           'Te','I','Xe','Cs','Ba','La','Ce','Pr','Nd','Pm','Sm','Eu','Gd',
           'Tb','Dy','Ho','Er','Tm','Yb','Lu','Hf','Ta','W','Re','Os','Ir',
           'Pt','Au','Hg','Tl','Pb','Bi','Po','At','Rn','Fr','Ra','Ac',
           'Th','Pa','U']

new_filenames = []

if 'link0_cmds' in locals():
    for i in range(len(link0_cmds)):
        link0_cmds[i] = link0_cmds[i] + '\n'


# Loop through each log file in the current directory
for j in range(len(log_filenames)):
    fo = open(log_filenames[j])
    log_lines = fo.readlines()
    fo.close()
    print 'Processing: ' + log_filenames[j]

    # add '\n' to link0_cmds and keywords if parameters are specified

    if 'job_keywords' in locals():
        keywords = job_keywords + '\n'

    index = 0
    try:
        link0_cmds
    except:
        # find link 0 commands
        link0_cmds = []
        link_key_bool = True
        while link_key_bool:
            temp_line = log_lines[index].split('\n')[0]
            if '*****************************' in temp_line:
                index += 4
                while link_key_bool:
                    temp_line = log_lines[index]
                    if temp_line[1] == '%':
                        link0_cmds.append(temp_line[1:])
                        index += 1
                        print
                    elif temp_line[1] == '#':
                        link_key_bool = False
                    else:
                        index += 1
            index += 1

    index= 0
    try:
        keywords
    except:
        # find # keywords
        keywords = ''
        link_key_bool = True
        while link_key_bool:
            temp_line = log_lines[index].split('\n')[0]
            if '*****************************' in temp_line:
                index += 4
                while link_key_bool:
                    temp_line = log_lines[index]
                    if temp_line[1] == '#':
                        keywords = temp_line[1:]
                        link_key_bool = False
                    else:
                        index += 1
            index += 1


    # Setup initial conditions for charge and multiplicity
    charge = 0
    mult = 0
    index = 0
    # get charge and multiplicity information from input
    chrg_mult_bool = True
    while chrg_mult_bool:
        temp_line = log_lines[index].split('\n')[0]
        if 'Multiplicity' in temp_line and 'Charge' in temp_line:
            charge = temp_line.split()[2]
            mult = temp_line.split()[5]
            chrg_mult_bool = False
            geom_start = index + 1
        index += 1

    index=0
    # find the most recent geometry in the log file
    scf_iter = 0
    last_geom_line = []
    init_con_line = 0
    opt_con_lines = []
    for i in range(len(log_lines)):
        temp_line = log_lines[i].split('\n')[0]
        if 'Coordinates (Angstroms)' in temp_line:
            scf_iter += 1
            last_geom_line.append(i)
        elif '!   Optimized Parameters   !' in temp_line:
            opt_con_lines.append(i)
        elif '!    Initial Parameters    !' in temp_line:
            init_con_line = i
    print 'SCF Iterations: ' + str(scf_iter)

    # specify which SCF iteration to extract geometries from
    if backsteps < len(last_geom_line):
        # proceed by 3 lines to the first atom
        geom_start = last_geom_line[-(backsteps+1)] + 3
        backstep_bool = True
    else:
        backstep_bool = False


    # initialize coordinate lists
    atoms = []
    atom_labels = []
    x = []
    y = []
    z = []

    # parse through cartesian coordinates
    geom_bool = True
    while geom_bool:
        temp_line = log_lines[geom_start].split('\n')[0].split()
        if backstep_bool:
            if len(temp_line) == 6:
                atoms.append(temp_line[1])
                atom_labels.append(atom_map[int(temp_line[1])-1])
                x.append(temp_line[-3])
                y.append(temp_line[-2])
                z.append(temp_line[-1])
                geom_start += 1
            else:
                geom_bool = False
        else:
            if len(temp_line) == 4:
                atoms.append(temp_line[0])
                atom_labels.append(atom_map[int(temp_line[0])-1])
                x.append(temp_line[-3] + (8-len(temp_line[-3]))*'0')
                y.append(temp_line[-2] + (8-len(temp_line[-2]))*'0')
                z.append(temp_line[-1] + (8-len(temp_line[-1]))*'0')
                geom_start += 1
            else:
                geom_bool = False

    # generate a cartesian coordinate table
    cart_write = []
    for i in range(len(atoms)):
        temp_line = atoms[i] + '\t' + x[i] + '\t' + y[i] + '\t' + z[i] + '\n'
        cart_write.append(temp_line)

#    print 'Optimized Connectivities: '
#    print opt_con_lines
#    print 'Initial Connectivity: ' + str(init_con_line)
#    print opt_con_lines == []
#    print init_con_line > 0


    con_bool = True
    con_index = 0
    print keywords

    if 'dftb' in job_keywords:
        if 'geom=connectivity' in job_keywords:
            print 'Connectivity should not be specified in DFTB jobs'
            keywords = ''.join(keywords.split(' geom=connectivity'))
            print 'geom=connectivity has been removed from the input keywords'
            print keywords
        if 'freq' in job_keywords:
            print 'Frequency calculations are included in DFTB optimization jobs'
            keywords = ''.join(keywords.split(' freq'))
            print 'freq has been removed from the input keywords'
            print keywords
        con_bool = False



    # obtain
    if 'geom=connectivity' in keywords:
        if opt_con_lines == []:
            if init_con_line == 0:
                print 'No connectivity data found in ' + log_filenames[j]
                con_bool = False
                keywords = ''.join(keywords.split(' geom=connectivity'))
                print 'geom=connectivity has been removed from the input keywords'
            elif init_con_line > 0:
                print 'No optimized connectivity data found in ' + log_filenames[j] + '; using input connectivity'
                con_index = init_con_line
        else:
            con_index = opt_con_lines[-1]
    else:
        con_bool = False

    # create a dictionary of bonds
    d_bonds = {}
    for n in range(len(x)):
        d_bonds[n+1] = []

    # move to the first bond
    con_index += 5
    # parse through connectivity data
    while con_bool:
        temp_line = log_lines[con_index].split('\n')[0].split()
        #print temp_line
        #con_bool = False
        if 'R' in temp_line[2]:
            #print temp_line
            atoms = temp_line[2].split('(')[1].split(')')[0].split(',')
            #print atoms
            d_bonds[int(atoms[0])].append([atoms[1],temp_line[3]])

            con_index += 1
#            if len(temp_line) == 6:
#                atoms.append(temp_line[1])
#                atom_labels.append(atom_map[int(temp_line[1])-1])
#                x.append(temp_line[-3])
#                y.append(temp_line[-2])
#                z.append(temp_line[-1])
#                geom_start += 1
        else:
            con_bool = False

    con_write = ''
    for n in d_bonds.keys():
        con_write = con_write + str(n) + ' '
        for m in d_bonds[n]:
            con_write = con_write + m[0] + ' ' + m[1] + ' '
        con_write = con_write + '\n'
    # continue to write connectivity data

    #print con_write

    # write .gjf files
    new_filenames.append(log_filenames[j][:-4] + '_' + gjf_dir + '_' + str(j+1) + '.gjf')
    fw = open(new_filenames[j],'w')
    fw.writelines(link0_cmds)
    fw.write(keywords)
    fw.write('\n' + job_title + ' ' + str(j+1) + '; by Luke Melo' + '\n')
    fw.write('\n' + charge + ' ' + mult + '\n')
    fw.writelines(cart_write)
    fw.write('\n')
    if 'geom=connectivity' in keywords:
        fw.writelines(con_write)
    if 'dftb' in keywords:
        fw.writelines(dftb_gjfadd(skf_dir,atom_labels))
    fw.writelines(['\n','\n'])
    fw.close()

    print ''


os.system('pwd > f.txt')
f = open('f.txt')
cd = f.readlines()[0].split('\n')[0]
f.close
os.system('rm f.txt')

print cd
for j in range(len(new_filenames)):
    os.system('mv ' + cd + '/' + new_filenames[j]  + ' ' + cd + '/'+gjf_dir+'/')


del link0_cmds
del job_keywords
try:
    del keywords
except:
    pass



