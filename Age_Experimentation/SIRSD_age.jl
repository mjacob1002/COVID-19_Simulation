# SIRSD simple model
# assume well mixed population
g(x) = 1/ (1 - (3 * exp(x-65) / 4))
using Random, Plots
using Distributions
# mean age
μ = 40
# standard deviation of age
σ = 21
ages = Normal(μ, σ)
N = 100
I0 = 1
S0 = N - I0
R0 = 0
D0 = 0
# number of days
days = 31
# differential
dt = .1
# number of slots in array, number of random event
numOfPoints = convert(Int64, days/dt + 1)
# Parameters
β = 1.5 * dt
γ = .2 * dt
κ = .33 * dt
# determine if a random event occurs
function randEvent(p)
    if p == 0
        return false
    end
    x = rand()
    if 0 < x <= p
        return true
    else
        return false
    end
end
# determine the probability of infection and whether an infection occurs
function infect(β,i, n)
    prob = β * i / n
    x = randEvent(prob)
    return x
end
# determine whether someone dies or not
function PDeath(age)
    w0 = .8
    x = w0 * g(age)
    return randEvent(x)
end

function recovery(γ)
    return randEvent(γ)
end

function loseImmunity(λ)
    return randEvent(λ)
end

function initPop(startPop)
    S = Set(); I = Set(); R=Set(); D = Set()
    firstAge = rand(ages,1)
    push!(I, firstAge)
    susAges = rand(ages, startPop - 1)
    for i in 1:startPop-1
        push!(S, susAges[i])
    end
    return S, I, R, D
end

function stateChange(S, I, R, D, β, γ, κ, numPoint, pop, Sarray, Iarray, Rarray, Darray)
    # run all of the number of state changes required
    for i in 2:numPoint
        # create copies of sets to make keeping track of changes easier
        Scopy = deepcopy(S); Icopy = deepcopy(I); Rcopy = deepcopy(R)
        # for every susceptible in copy
        for j in Scopy
            # the current number of infected people
            currInfect = Iarray[i-1]
            # determine whether a person becomes infected
            x = infect(β,currInfect,pop)
            # if true, move them from S to I
            if x
                delete!(S, j)
                push!(I, j)
            end
        end
        # for every infected person in copy(j is really just the age of the person)
        for j in Icopy
            # determine if they die or not
            x = PDeath(j)
            # move sets if they die
            if x
                delete!(I,j)
                push!(D,j)
                # adjus the total population that is alive
                pop = pop - 1
            # if they don't die, check if they will recover
            else
                # if they do recover, update sets
                if recovery(γ)
                    delete!(I, j)
                    push!(R, j)
                end
            end
        end
        # run state changes on the recovered group
        for j in Rcopy
            x = loseImmunity(κ)
            if x
                delete!(R, j)
                push!(S, j)
            end
        end
        Sarray[i] = length(S)
        Iarray[i] = length(I)
        Rarray[i] = length(R)
        Darray[i] = length(D)
        S = Scopy; I=Icopy; R=Rcopy
    end
    return Sarray, Iarray, Rarray, Darray
end

S = zeros(numOfPoints)
S[1] = S0
I = zeros(numOfPoints)
I[1] = I0
R = zeros(numOfPoints)
R[1] = R0
D = zeros(numOfPoints)
D[1] = D0

Sset, Iset, Rset, Dset = initPop(N)
S, I, R, D = stateChange(Sset, Iset, Rset, Dset, β, γ, κ, numOfPoints, N, S, I, R, D)
