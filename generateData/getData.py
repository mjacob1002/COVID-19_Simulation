import os
import sys
import numpy as np
import pandas as pd

from ICUV_spatial_periodic import ICUSpatialPeriodic

# a dictionary that maps type of vaccination strategy to number
typeVax = {
"StandardVax" : 0,
"AgeVax" : 1,
"MovementVax":2,
"SpreadingVax" : 3,
"NoVax": 0
}



def genSigma(p):
    # assume sample size is 200
    return (p*(1-p)/ 200)**.5

def runSims(fileName, simType):
    S0 = 999
    E0 = 0
    I0 = 1
    R0 = 0
    V0 = 0
    rstart = 3
    rstartsigma = 0.5
    days = 180
    #eta = np.random.normal(.03, genSigma(.03))
    eta = 0.03
    if simType == "NoVax":
	    eta = 0
    #rho = np.random.normal(.3, genSigma(.3))
    rho = .3
    #phi = np.random.normal(.3, genSigma(.3))
    phi = .3
    #chi = np.random.normal(.3, genSigma(.15))
    chi = .15
    #omega = np.random.normal(.2, genSigma(.2))
    omega = .2
    #psi = np.random.normal(.3, genSigma(.3))
    psi = .3
    #mu = 0
    mu = .001
    gamma = .35
    #gamma = np.random.normal(.35, genSigma(.35))
    kappa = .2
    #kappa = np.random.normal(.2, genSigma(.2))
    planeSize = 100
    # create the object
    test = ICUSpatialPeriodic(S0, E0, I0, R0, V0, rstart, rstartsigma, days, eta, rho, phi, chi, omega, psi, mu, gamma, kappa, planeSize, vaxStrat=typeVax[simType])
    test.initialize()
    test.run()
    df = test.toDataFrame()
    # save the dataframe as a CSV file
    df.to_csv(fileName)
    #print(df)

# main function
def main(args):
    if len(args) <= 1 :
        print("Need more arguments")
        return
    # where the out csv files should be stored.
    # change this variable depending on what type of vaccination strategy is being tested 
    filename = "../Outputs/" + sys.argv[2] + "/out_" + args[1] + ".csv"
    print("File: ", filename)

    
    runSims(filename, sys.argv[2])

    print("Finished Sim")


if __name__ == "__main__":
    main(sys.argv)
