import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import math

def randMovementAngle():
    delta_theta = np.random.uniform(0, 2*math.pi)
    return delta_theta

def randEvent(p: float):
    if p<=0:
        return False
    x = np.random.random()
    if 0 < x <= p:
        return True
    return False


class Person():
    def __init__(self, x, y, age, r, R, theta):
        # starting x coordinate
        self.x = x
        # starting y coordinate
        self.y = y
        # starting age
        self.age = age
        # starting spreading radius
        self.r = r
        # starting movement radius
        self.R = R
        # randomly generated starting angle
        self.theta = theta
        self.currTheta = theta
        self.isIncluded = False
        self.h = self.x - self.R * math.cos(theta)
        self.k = self.y - self.R * math.sin(theta)

def dist(p1: Person, p2: Person):
    return ((p1.x-p2.x)**2 + (p1.y-p2.y)**2)**0.5


# eta is P(S->V)
# rho is P(leave E)
# phi is P(E->L|leave E), 1-phi is E->I|leave E
# chi is P(L->ICU)
# omega is P(ICU->D)
# psi is P(ICU->R)
# mu is P(I->D)
# gamma is P(I->R)
# kappa is P(R -> S)

# if vaxStrat is 0, standard vax strat
# if vaxStrat=1, age based
# if vaxStrat = 2, movement radius based
# if vaxStrat = 3, spread radius based

# rstart is the mean of the spreading radius, rstartsigma, is the standard deviation of the spreading radius distribution
# muR is the movement radius mean, sigmaR is the standard deviation
class ICUSpatialPeriodic():
    def __init__(self, S0, E0, I0, R0, V0, rstart, rstartsigma, days,
    eta, rho, phi, chi, omega, psi, mu, gamma, kappa, planeSize, w0=1.0, alpha = 2.0, vaxStrat = 0):
        # represents the vaccination type
        self.vaxStrat = vaxStrat
        # the total population
        self.N = S0 + E0 + I0 + R0 + V0
        # initialize all of the arrays storing number of people in each compartment
        self.S, self.I, self.R = np.zeros(days+1), np.zeros(days+1), np.zeros(days+1)
        self.E, self.L, self.ICU = np.zeros(days+1), np.zeros(days+1), np.zeros(days+1)
        self.D, self.V = np.zeros(days+1), np.zeros(days+1)
        self.infectious, self.combine, self.additionalDeath = np.zeros(days+1), np.zeros(days+1), np.zeros(days+1)
        self.S[0], self.E[0], self.I[0], self.R[0], self.V[0] = S0, E0, I0, R0, V0
        self.D[0], self.L[0], self.ICU[0] = 0, 0, 0
        # create the data structures
        self.Scollect = []
        self.Ecollect = []
        self.Icollect = []
        self.Lcollect = []
        self.ICUcollect = []
        self.Rcollect = []
        self.Dcollect = []
        self.Vcollect = []
        # map the distribution values, sigma being std deviation and mu being mean
        self.rstart = rstart
        self.rstartsigma = rstartsigma
        self.muAges = 45.81
        self.sigmaAges = 15
        self.muR = 12
        self.sigmaR = 5
        # map the parameters
        # eta, psi are defined are the conditional probabilites
        self.eta, self.rho, self.phi, self.chi, self.omega, self.psi, self.mu, self.gamma, self.kappa = eta, rho, phi, chi, omega, psi, mu, gamma, kappa
        self.planeSize = planeSize
        self.w0 = w0
        self.alpha = alpha
        self.days = days

    # done before running the simulation
    def initialize(self):
        # create arrays for every person in the simulation
        ages = np.random.normal(self.muAges, self.sigmaAges, self.N)
        coordinateX = np.random.random(self.N) * self.planeSize
        coordinateY = np.random.random(self.N) * self.planeSize
        movementRadii = np.random.normal(self.muR, self.sigmaR, self.N)
        startingAngles = np.random.random(self.N) * 2 * math.pi
        spreadingRadius = np.random.normal(self.rstart, self.rstartsigma, self.N)
        for i in range(self.N):
            # S copy
            p1 = Person(coordinateX[i], coordinateY[i], ages[i], spreadingRadius[i],
                        movementRadii[i],
                        startingAngles[i])
            # I copy
            p2 = Person(coordinateX[i], coordinateY[i], ages[i], spreadingRadius[i],
                        movementRadii[i],
                        startingAngles[i])
            # R copy
            p3 = Person(coordinateX[i], coordinateY[i], ages[i], spreadingRadius[i],
                        movementRadii[i],
                        startingAngles[i])
            # D copy
            p4 = Person(coordinateX[i], coordinateY[i], ages[i], spreadingRadius[i],
                        movementRadii[i],
                        startingAngles[i])
            # Ecopy
            p5 = Person(coordinateX[i], coordinateY[i], ages[i], spreadingRadius[i],
                        movementRadii[i],
                        startingAngles[i])
            # Lcopy
            p6 = Person(coordinateX[i], coordinateY[i], ages[i], spreadingRadius[i],
                        movementRadii[i],
                        startingAngles[i])
            # ICU copy
            p7 = Person(coordinateX[i], coordinateY[i], ages[i], spreadingRadius[i],
                        movementRadii[i],
                        startingAngles[i])
            # Vaccine copy
            p8 = Person(coordinateX[i], coordinateY[i], ages[i], spreadingRadius[i],
                        movementRadii[i],
                        startingAngles[i])
            # Susceptible collect
            self.Scollect.append(p1)
            # Exposed collect
            self.Ecollect.append(p5)
            # Infected collected
            self.Icollect.append(p2)
            # Lag compartment collected
            self.Lcollect.append(p6)
            # Removed compartment collected
            self.Rcollect.append(p3)
            # ICU compartment collect
            self.ICUcollect.append(p7)
            # Death compartment collect
            self.Dcollect.append(p4)
            # Vaccinated compartment collect
            self.Vcollect.append(p8)
        for i in range(self.N):
            # print("Iterator:", i, " I[0]: ", self.I[0], "I[i].isIncluded: ", self.Icollect[i].isIncluded, "Condition:", i<self.I[0])
            if i < self.I[0]:
                self.Icollect[i].isIncluded = True
            elif i < self.I[0] + self.S[0]:
                self.Scollect[i].isIncluded = True
            elif i < self.I[0] + self.S[0] + self.V[0]:
                self.Vcollect[i].isIncluded = True
            else:
                self.Rcollect[i].isIncluded = True
            # print("Icollect[i].isIncluded:", self.Icollect[i].isIncluded)

    def adjustTheta(self, person: Person, delta: float):
        # adjust the current theta of the person object
        person.currTheta += delta
        # adjust the theoretical x  and y value
        x = person.h + person.R * math.cos(person.currTheta)
        if x < 0:
            x = 0
        elif x > self.planeSize:
            x = self.planeSize
        
        y = person.k + person.R * math.sin(person.currTheta)
        if y < 0:
            y = 0
        elif y > self.planeSize:
            y = self.planeSize
        
        person.x, person.y = x, y
    
    def move(self):
        #print('moving now')
        for i in range(self.N):
            # create random movement angle
            #print("Before: (", self.Scollect[i].x, self.Scollect[i].y, ")")
            angle = randMovementAngle()
            # only if the person isn't dead do you adjust D
            if self.Dcollect[i].isIncluded == False:
                self.adjustTheta(self.Dcollect[i], angle)
                # adjust the x and y coordinates of everyone
                self.adjustTheta(self.Scollect[i], angle)
                self.adjustTheta(self.Ecollect[i], angle)
                self.adjustTheta(self.Lcollect[i], angle)
                self.adjustTheta(self.Icollect[i], angle)
                self.adjustTheta(self.Rcollect[i], angle)
                self.adjustTheta(self.Vcollect[i], angle)
            #print("After: (", self.Scollect[i].x, self.Scollect[i].y, ")")
            

    # calculate infection probs given two Person objects and constants
    def infect(self, inf: Person, sus: Person):
        r0 = inf.r
        r = dist(inf, sus)
        if r >= r0:
            return 0
        w = self.w0 * (1-(r/r0)**self.alpha)
        return w
    
    #P(E->L|E->)
    def PICU(self, age: float):
        a = math.exp(-(age-65))
        p0 = 1.0
        return p0 / (1 + a)
    
    # P(V|S) based on age
    def PV(self, age):
        # bunch of sigmoid stuff
        a = math.exp(-(age-self.muAges-self.sigmaAges))
        # according to the equation obtained from the regression.py file
        p0 = self.eta / .16
        return p0 / (1+a)
    
    # P(S->V) based on R
    def PVR(self, R):
        a = math.exp(-(R-self.muR - self.sigmaR))
        p0 = .1
        return p0 / 1 + a
    # for spreading radius strategies
    def PV_spread_r(self, r):
        a = math.exp(-(r-self.rstart - self.rstartsigma))
        p0 = .1
        return p0 / 1 + a

    # leave S helper function
    # replace the eta
    def _leaveSHelp(self, w, sus: Person):
        if w == 0:
            return 0
        # generate a random number
        p = np.random.random()
        # if infected
        if 0 < p <= w:
            return 1
        # eta is currently defined as P(S->v|!(S->E)). May change later
        # if person is decided to become vaccinated
        
        # probability of getting vaccinated
        pv = 0
        # standard vaccination strategy
        if self.vaxStrat == 0:
            pv = self.eta
        # age based vaccination strategy
        elif self.vaxStrat == 1:
            pv = self.PV(sus.age)
        # radius based vaccination strategy
        elif self.vaxStrat == 2:
            pv = self.PVR(sus.R)
        # spreading readius based strategy
        else:
            pv = self.PV_spread_r(sus.rstart)
        
        if w < p <= w + pv * (1-w):
            return 2
        else:
            return 0
    
    # transfer from S
    def leaveS(self):
        # cycle through all of the person objects in Scollects
        transferStoE = set()
        transferStoV = set()
        # cycle through all of the susceptibles
        for i, person in enumerate(self.Scollect):
            # if the person isn't in Susceptible
            if not person.isIncluded:
                continue
            # for all the infecteds
            for j, inf in enumerate(self.Icollect):
                # if not in infected compartment, move on
                if not inf.isIncluded:
                    continue
                # generate infection probs and generate an event
                w = self.infect(inf, person)
                event = self._leaveSHelp(w, person)
                if event == 1:
                    transferStoE.add(i)
                    self.Scollect[i].isIncluded=False
                    # break out of infection loop bc can't get infected twice
                    break
                elif event == 2:
                    self.Scollect[i].isIncluded = False
                    transferStoV.add(i)
                    break
            # if the person left the S compartment, move on the next person
            if self.Scollect[i].isIncluded == False:
                continue
            for j, inf in enumerate(self.Lcollect):
                if not inf.isIncluded:
                    continue
                w = self.infect(inf, person)
                event = self._leaveSHelp(w, person)
                if event == 1:
                    transferStoE.add(i)
                    self.Scollect[i].isIncluded=False
                    break
                elif event == 2:
                    self.Scollect[i].isIncluded = False
                    transferStoV.add(i)
                    break
        return transferStoE, transferStoV

    # run state changes for those leaving the E compartment
    def leaveE(self):
        # keeps track of those going from I - > R
        transfersL = set()
        transfersI = set()
        for count, person in enumerate(self.Ecollect):
            # if the person isn't an exposed person
            if not person.isIncluded:
                continue
            # if the person is infected
            # test for leaving E
            leaveE = randEvent(self.rho)
            # if the person leaves E, test for whether they go to L or I
            if not leaveE:
                continue
            # remove them from exposed
            person.isIncluded = False
            # test whether they'll go to L or I using PICU
            # get the probability of going to L/ICU
            w = self.PICU(person.age)
            # generate an event
            eventICU = randEvent(w)
            # if the person is determined to go to the ICU
            if eventICU:
                transfersL.add(count)
            else:
                transfersI.add(count)
        # those who wil go from I -> R, but not done immediately because state change will be done on current R
        # and those who just transfered shouldn't be eligible to go immediately back to S
        return transfersL, transfersI
    
    # run state changes for those leaving L -> ICU
    def LtoICU(self):
        transfersICU = set()
        for count, person in enumerate(self.Lcollect):
            # if the person currently isn't in lag compartment, move onto the next
            if not person.isIncluded:
                continue
            # person is in lag compartment, so generate an event
            event = randEvent(self.chi)
            # if the person doesn't transfer to ICU, then don't do anything and check next person
            if not event:
                continue
            # the person does transfer to ICU
            # remove them from the Lcollect
            self.Lcollect[count].isIncluded = False
            # add the index to the set to be changed at the end
            transfersICU.add(count)
        return transfersICU
    
    def _leaveICUHelp(self):
        x = np.random.random()
        # determine if the number falls in range for ICU->D
        if 0 < x <= self.omega:
            return 1
        # use Bayes Rule to find conditional probability
        elif self.omega < x <= self.omega + (self.psi) * (1-self.omega):
            return 2
        return 0
        
    def leaveICU(self):
        transferICUtoD = set()
        transferICUtoR = set()
        for i, person in enumerate(self.ICUcollect):
            if person.isIncluded == False:
                continue
            event = self._leaveICUHelp()
            if event == 1:
                transferICUtoD.add(i)
                self.ICUcollect[i].isIncluded = False
            elif event == 2:
                transferICUtoR.add(i)
                self.ICUcollect[i].isIncluded = False
        return transferICUtoD, transferICUtoR
    

    def _leaveIHelp(self):
        x = np.random.random()
        if 0 < x <= self.mu:
            return 1
        elif self.mu < x <= self.mu + self.gamma * (1-self.mu):
            return 2
        return 0
    
    def leaveI(self):
        transferID = set()
        transferIR = set()
        for i, person in enumerate(self.Icollect):
            if not person.isIncluded:
                continue
            event = self._leaveIHelp()
            if event == 1:
                transferID.add(i)
                self.Icollect[i].isIncluded = False
            elif event == 2:
                transferIR.add(i)
                self.Icollect[i].isIncluded = False
        #print(type(transferID), " ", type(transferIR))
        return transferID, transferIR

    def leaveR(self):
        transferRS = set()
        for i, person in enumerate(self.Rcollect):
            if not person.isIncluded:
                continue
            event = randEvent(self.kappa)
            if event:
                self.Rcollect[i].isIncluded = False
                transferRS.add(i)
        return transferRS
    
    def assertionCheck(self):
        # number of trues in a given column
        for i in range(self.N):
            trueCount = 0
            if self.Scollect[i].isIncluded:
                trueCount += 1
            if self.Ecollect[i].isIncluded:
                trueCount += 1
            if self.Icollect[i].isIncluded:
                trueCount += 1
            if self.Lcollect[i].isIncluded:
                trueCount += 1
            if self.ICUcollect[i].isIncluded:
                trueCount += 1
            if self.Rcollect[i].isIncluded:
                trueCount += 1
            if self.Dcollect[i].isIncluded:
                trueCount+=1
            if self.Vcollect[i].isIncluded:
                trueCount +=1
            assert trueCount == 1
    
    def stateChanger(self, transferStoE, transferEtoL, transferEtoI, transferItoD
    , transferItoR, transferLtoICU, transferICUtoD, transferICUtoR, transferRtoS, transferStoV):
        for i in transferStoE:
            self.Scollect[i].isIncluded = False
            self.Ecollect[i].isIncluded = True
        for i in transferStoV:
            self.Scollect[i].isIncluded = False
            self.Vcollect[i].isIncluded = True
        for i in transferEtoL:
            self.Ecollect[i].isIncluded = False
            self.Lcollect[i].isIncluded = True
        for i in transferEtoI:
            self.Ecollect[i].isIncluded = False
            self.Icollect[i].isIncluded = True
        for i in transferLtoICU:
            self.Lcollect[i].isIncluded = False
            self.ICUcollect[i].isIncluded = True
        for i in transferICUtoD:
            self.ICUcollect[i].isIncluded = False
            self.Dcollect[i].isIncluded = True
        for i in transferICUtoR:
            self.ICUcollect[i].isIncluded = False
            self.Rcollect[i].isIncluded = True
        for i in transferItoD:
            self.Icollect[i].isIncluded = False
            self.Dcollect[i].isIncluded = True
        for i in transferItoR:
            self.Icollect[i].isIncluded = False
            self.Rcollect[i].isIncluded = True
        for i in transferRtoS:
            self.Rcollect[i].isIncluded = False
            self.Scollect[i].isIncluded = True

    def run(self):
        self.initialize()
        for i in range(1, self.days + 1):
            # run state changes from S
            transferStoE, transferStoV = self.leaveS()
            transferEtoL, transferEtoI = self.leaveE()
            transferLtoICU = self.LtoICU()
            transferICUtoD, transferICUtoR = self.leaveICU()
            transferItoD, transferItoR = self.leaveI()
            transferRtoS = self.leaveR()

            self.stateChanger(transferStoE, transferEtoL, transferEtoI, transferItoD, transferItoR, transferLtoICU, transferICUtoD, transferICUtoR, transferRtoS, transferStoV)

            # make sure everything is working properly
            self.assertionCheck()
            #print("I am just before move function")
            self.move()
            # adjust the values 
            self.S[i] += self.S[i-1] + len(transferRtoS) - len(transferStoE) - len(transferStoV)
            self.E[i] += self.E[i-1] + len(transferStoE) - len(transferEtoL) - len(transferEtoI)
            self.I[i] += self.I[i-1] + len(transferEtoI) - len(transferItoR) - len(transferItoD)
            self.L[i] += self.L[i-1] + len(transferEtoL) - len(transferLtoICU)
            self.ICU[i] += self.ICU[i-1] + len(transferLtoICU) - len(transferICUtoR) - len(transferICUtoD)
            self.R[i] += self.R[i-1] + len(transferItoR) + len(transferICUtoR) - len(transferRtoS)
            self.D[i] += self.D[i-1] + len(transferICUtoD) + len(transferItoD)
            self.V[i] += self.V[i-1] + len(transferStoV)

            assert self.S[i] + self.E[i] + self.L[i] + self.I[i] + self.ICU[i] + self.R[i] + self.D[i] + self.V[i] == self.N
        


    def toDataFrame(self):
        t = np.linspace(0, self.days, self.days+1)
        arr = np.stack([t, self.S, self.E, self.I, self.L, self.ICU, self.R, self.D, self.V], axis=1)
        df = pd.DataFrame(arr, columns=["Days", "Susceptible", "Exposed", "Infectious", "Lag", "ICU", "Recovered", "Dead", "Vaccinated"])
        return df
            


        





