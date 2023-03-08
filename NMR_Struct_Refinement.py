# Set the variables for various options here
InputFileName = "cefdinir.txt"
UnitCellParam = "cefdinir.unitcell"
NMRExpFile = "cefdinir.shift"
InputFormat = "NOT!fractional" #anything besides 'fractional' does cart
SimRadius_H = 0.1  #in angstroms
SimRadius_C = 0.05
SimRadius_O = 0.05
SimRadius_N = 0.05
SimRadius_S = 0.05
SimRadius_Cl= 0.05
SimRadius_HX= 0 #unless doing proton tunneling, its to separate the H
SimList = []   #Here you have a list of strings where you specify what to refine
# 'H9','C9','C12','C14','N1','O2','O3' are the atoms we mind want to specifically adjust for cefdinir
NumOfSteps = 500
TheMap = (-1.0281, 243.01)
#Nitrogen is -1.0281, 243.01
#Carbon is -1.004, 172.08

from MonteCarloSim import *
from FileIO import *
from Analysis import *

opcode = 2

if opcode == 1:
    unitcell_param = LoadUnitCellParameters(UnitCellParam)
    
    a = unitcell_param[0]
    b = unitcell_param[1]
    c = unitcell_param[2]
    alpha = unitcell_param[3]
    beta = unitcell_param[4]
    gamma = unitcell_param[5]
    SymOps = unitcell_param[6]
    
    cell = ('%BLOCK LATTICE_ABC\n',str(a) + ' ' + str(b) + ' ' + str(c) + '\n',str(alpha) + ' ' + str(beta) + ' ' + str(gamma) + '\n',
            '%ENDBLOCK LATTICE_ABC\n\n', 'fix_all_cell : true\n', "symmetry_generate\n", 'fix_com : false\n',
            "kpoints_mp_spacing : 0.05\n\n")
    param = ('xcfunctional : RPBE\n','opt_strategy : speed\n','task : magres\n','fix_occupancy : true\n',
            'finite_basis_corr : 0\n','elec_energy_tol : 1.0e-10\n','basis_precision : precise\n', 'spin_polarized : false')
    
    OutputParams = (cell, param)
    SimRad = [SimRadius_HX,SimRadius_H,SimRadius_C,SimRadius_O, SimRadius_N, SimRadius_S, SimRadius_Cl]
    parameters = (InputFileName,InputFormat,SimList,NumOfSteps,SimRad, unitcell_param)
    RunMonteCarlo(parameters, OutputParams, True)

# hook up to Castep if desired starting here
if opcode == 2:
    for i in range(NumOfSteps):
        NMRFiles = InputFileName + "." + str(i) + ".magres"
        NMROutput = InputFileName + "." + str(i) + ".nmr"
        ProcessNMROutputFile_Castep(NMRFiles, NMROutput)
    
    FileNum, R2 = FindBestFit(InputFileName, NMRExpFile, NumOfSteps, TheMap, True)
    print("Structure " + str(FileNum)+" has the best fit to the experimental data with R^2 value of " + str(R2) + ".")
    DisplayPoorFits(FileNum, InputFileName, NMRExpFile, TheMap)

    #On line 54 where it says FILENUM, R2, put True, True if you are using slope and intercept
