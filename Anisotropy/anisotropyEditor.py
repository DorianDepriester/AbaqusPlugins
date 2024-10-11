from abaqusConstants import *
from abaqus import *
import __main__
import material

def applyAnisotropy(Cc=(), Ch=(), CtetA=(), CtetB=(), CtriA=(), CtriB=(), Co=(), 
                    symmetry='', modelName='', material=''):
    Cdict=dict()
    Cdict['Cubic']=Cc
    Cdict['Hexagonal']=Ch
    Cdict['Tetragonal (A)']=CtetA
    Cdict['Tetragonal (B)']=CtetB
    Cdict['Trigonal (A)']=CtriA
    Cdict['Trigonal (B)']=CtriB
    Cdict['Orthorombic']=Co
    Cl=[]
    C=Cdict[symmetry]
    if len(C)==0:
        raise Exception('Fill in the {} tab above before applying this symmetry.'.format(symmetry))
    for row in C:
        C11=C12=C13=C14=C15=C16=0
        C22=C23=C24=C25=C26=0
        C33=C34=C35=C36=0
        C44=C45=C46=0
        C55=C56=0
        C66=0
        if symmetry=='Cubic':
            C11, C44, C12=row
            C22=C33=C11
            C13=C23=C12
            C55=C66=C44
        elif symmetry=='Hexagonal':
            C11, C33, C44, C12, C13=row
            C22=C11
            C23=C13
            C55=C44
            C66=(C11-C12)/2
        elif symmetry=='Tetragonal (A)':
            C11, C33, C44, C66, C12, C13, C16=row
            C22=C11
            C23=C13
            C55=C44
            C26=-C16
        elif symmetry=='Tetragonal (B)':
            C11, C33, C44, C66, C12, C13=row
            C22=C11
            C23=C13
            C55=C44
        elif symmetry=='Trigonal (A)':
            C11, C33, C44, C12, C13, C14, C15=row
            C22=C11
            C23=C13
            C55=C44
            C24=-C14
            C25=-C15
            C46=C25
            C56=C14
            C66=(C11-C12)/2
        elif symmetry=='Trigonal (B)':
            C11, C33, C44, C12, C13, C14=row
            C22=C11
            C23=C13
            C55=C44
            C24=-C14
            C56=C14
            C66=(C11-C12)/2
        else: # Orthorombic
            C11, C22, C33, C44, C55, C66, C12, C13, C23=row

            
        Ci=(C11, C12, C22, C13, C23, C33, C16, C26, C36, C66, C15, C25, C35, C56, C55, C14, C24, C34, C46, C45, C44)
        Cl.append(Ci)
    
    if len(Cl)==1:
        tempDep=OFF
    else:
        tempDep=ON
    mdb.models[modelName].materials[material].Elastic(type=ANISOTROPIC, 
                                                      temperatureDependency=tempDep,
                                                      table=tuple(Cl))