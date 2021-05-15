using Plots
# size of population
N = 100
# effective transmission rate
β = 1.5
# initial susceptible population
S0 = 99
# initial infected population
I0 = N - S0
# initial recovered individuals
R0 = 0
# initial dead people
D0 = 0
# probability of leaving I -> R/D
γ = .2
# percent of those leaving I going to R; rest go to D
multiplier = .8
# probability of those going from R -> S
κ = .15
# number of days in simulation
days = 31
# differential
dt = 0.1
# size of the arrays
size = convert(Int64, days/dt + 1)
# initialize S, I, R, D arrays
S, I, R, D = zeros(size)
# put in initial values at t = 0
S[1] = S0
I[1] = I0
R[1] = R0
D[1] = D0
# pass in beta and the current position in array
function deriv(B, pos)
    # compute the amount of people going from S -> I
    x = B * S[pos] * I[pos] / N
    # people going from I -> R
    y = γ * multiplier * I[pos]
    # people going from I -> D
    z = γ * (1-multiplier) * I[pos]
    # people going from R to S
    w = κ * R[pos]
    return -x + w, x - y - z, y - w, z
end
function updateSIRSD(β)
    for i in 2:size
        f = deriv(β, i-1)
        S[i] = S[i-1] + f[1]*dt
        I[i] = I[i-1] + f[2]*dt
        R[i] = R[i-1] + f[3]*dt
        D[i] = D[i-1] + f[4]*dt
    end
end

updateSIRSD(β)
t = LinRange(0, days, size)
plot(t, I, label="Infected")
