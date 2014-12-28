############################
##       Luke Melo        ##
## University of Waterloo ##
##     Hopkins Group      ##
##       11/19/2014       ##
##  connectivity_cage.py  ##
##         v1.0           ##
############################

from math import sqrt

def pyth_dist(l1,l2):
    return sqrt((l1[1]-l2[1])**2 + (l1[2]-l2[2])**2 + (l1[3]-l2[3])**2)

## at this point we need to create an rij matrix, sort this matrix in ascending order of bond length, exclude those > than a thresdhold (ex 2.5), then progressively make larger bonds until atoms are all filled up

def bf_cage_con(geom):
    ## build rij matrix 
    rij = []
    for i in range(natoms):
        new_atom = []
        for j in range(natoms):
            new_atom.append(pyth_dist(geom[i],geom[j]))
        rij.append(new_atom)
    ## longest possible B-B bond length (rij)  
    threshold_bondlength = 2.5
    ## create a list of potential bonds:
    ## example  [bondlength,i,j]
    rij_potential = []
    ## remove F from rij
    for i in range(natoms/2):
        for j in range(natoms/2):
            ## 2*i skips the fluorines
            if rij[2*i][2*j] != 0.0 and rij[2*i][2*j] < threshold_bondlength:
                rij_potential.append([rij[2*i][2*j],2*i,2*j])
    ## sort potential bond lengths in ascending order            
    rij_potential.sort(key=lambda x: x[0])
    ## create a connectivity dictionary for easy porting to .gjf
    # connect B(i) with F(i) (indexes vary by 1) 
    d_bonds = {}
    for i in range(1,natoms+1):
        if i % 2 != 0:
            d_bonds[i] = [i+1]
        else:
            d_bonds[i] = [i-1]
    ## now that borons all have their respective fluorine bonds, begin pairing borons
    ## specify a maximum number of borons bonds (including fluorine):
    max_boron_bonds = 7
    ## start looking at potential bonds in ascending order
    for x in range(len(rij_potential)/2):
        r = rij_potential[2*x][0]
        i = rij_potential[2*x][1]+1
        j = rij_potential[2*x][2]+1
        ## ensure there are not too many bonds on i and j
        if len(d_bonds[i]) < max_boron_bonds and len(d_bonds[j]) < max_boron_bonds:
            d_bonds[i].append(j)
            d_bonds[j].append(i)
    atoms = d_bonds.keys()
    con = '\n'
    for atom in atoms:
        l_bonds = d_bonds[atom]
        s_write = '%g ' % atom
        for i in l_bonds:
            s_write = s_write + str(i) + ' 1.0 '
        con = con + s_write + '\n'
    con = con + '\n\n\n\n\n'        
    return con


    
# read in a cartesian geometry
fo = open('test_car_1.csv','r')
#fo = open('bf_cart.csv','r')
carts = fo.readlines()
fo.close

# clean up the data imported (comma delimitted)
natoms = len(carts)
for i in range(natoms):
    temp = carts[i].split('\n')[0].split(',')
    for j in range(3):
        temp[j] = float(temp[j])
    temp.insert(0,'Atom')
    carts[i] = temp
    print carts[i]
#print filedata_in    
    
    
    
print bf_cage_con(carts) 
    
    
    
    
