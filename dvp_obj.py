import numpy as np
import math
from Arrival import Arrival, ExponentialDist, RateLatency
from Server import Server, ConstantRateServer, MarkovOnOff
from ParameterOutOfBounds import ParameterOutOfBounds

def backlog(arr: Arrival, ser: Server, theta: float, prob_b: float, indep=True, p=1.0) -> float:
    """Implements stationary standard_bound method"""
    if prob_b < 0.0 or prob_b > 1.0:
        raise IllegalArgumentError(f"prob_b={prob_b} must be in (0,1)")

    if indep:
        p = 1.0
        q = 1.0
    else:
        q = get_q(p=p)

    stability_check(arr=arr, ser=ser, theta=theta, indep=indep, p=p, q=q)
    sigma_sum, rho_diff = get_sigma_rho(arr=arr, ser=ser, theta=theta, indep=indep, p=p, q=q)

    if arr.is_discrete():
        return sigma_sum - (log(prob_b * theta * (-rho_diff))) / theta
    else:
        tau_opt = 1 / (theta * ser.rho(theta=q * theta))
        log_part = math.log(prob_b * theta * tau_opt * (-rho_diff))
        return tau_opt * ser.rho(theta=q * theta) + sigma_sum - log_part / theta


def delay_prob(arr: Arrival, ser: Server, theta: float, T: int) -> float:
    """Implements stationary standard_bound method"""
    if arr.rho(theta) >= ser.rho(theta):
        print("arrival and service:" + str(arr.rho(theta)) + " " + str(ser.rho(theta)) )
        raise ParameterOutOfBounds("System is not stable")

    return math.exp(-theta * ser.rho(theta) * T) * math.exp(theta * (
        arr.sigma(theta) + ser.sigma(theta))) / (theta * (ser.rho(theta) - arr.rho(theta)))


def opt_dvp(arr: Arrival, ser: Server, T: int):
    OPTIMUM = 100000
    OPT_THETA = 0.0

    for THETA in np.arange(2.0, 10.0, 0.1):
    # for THETA in [1.0, 2.0]:
        try:
            CANDIDATE = delay_prob(arr=arr,
                                ser=ser,
                                theta=THETA, T=T)
        except ParameterOutOfBounds:
            CANDIDATE = 100000
        
        if CANDIDATE < OPTIMUM:
            OPTIMUM = CANDIDATE
            OPT_THETA = THETA
    return CANDIDATE


def delay(arr:Arrival, ser:Server, prob, theta ):
    if arr.rho(theta) >= ser.rho(theta):
        # print("arrival larger than service:" + str(arr.rho(theta)) + " " + str(ser.rho(theta)))
        raise ParameterOutOfBounds("System is not stable")

    rho_diff=  (ser.rho(theta) - arr.rho(theta))
    sigma_sum=arr.sigma(theta) + ser.sigma(theta)

    tmp = prob * theta * rho_diff    
    if tmp < 0:
        return np.inf
    top= math.log(tmp) - (theta * sigma_sum)
    return top/(-theta*ser.rho(theta))

    # tau_opt = 1 / (theta * ser.rho(theta=theta))
    # log_part = math.log(prob * theta * tau_opt * (-rho_diff))

    # delay = (tau_opt * ser.rho(theta=theta) + sigma_sum - log_part / theta) / ser.rho(theta=theta)
    # print(f"tau_opt {tau_opt} sigma_sum {sigma_sum} log_part {log_part}" )

    # return delay


def opt_delay(arr: Arrival, ser: Server, prob):
    print(f"ser {ser.rho(0.01)}")
    OPTIMUM = 10
    OPT_THETA = 0.0
    for THETA in np.arange(0.00000000000000000001, 10.0, 0.01):
        try:
            CANDIDATE = delay(arr=arr,
                                ser=ser,
                                prob=prob, theta=THETA)
            # print(f"Theta {THETA} delay {CANDIDATE} arr {arr.rho(THETA)} ser {ser.rho(THETA)}"   )

        except ParameterOutOfBounds:
            CANDIDATE = 10
        
        if CANDIDATE < OPTIMUM:
            OPTIMUM = CANDIDATE
            OPT_THETA = THETA
            # print(f"Theta {THETA} delay {CANDIDATE} arr {arr.rho(THETA)} ser {ser.rho(THETA)}" )
    print(f"OPTIMUM {OPTIMUM}") 
    print(f"OPT_THETA {OPT_THETA}") 

    return OPTIMUM


def opt_delay2(arr: Arrival, ser: Server, prob):
    
    OPTIMUM = np.inf
    OPT_THETA = 0.0

    for DELTA in np.arange(0.0001, 0.25, 0.01):
        Thetas=np.arange(0.00000000000000000001, 2.0, 0.01)
        # Thetas=np.append(Thetas,np.arange(2.0,20, 1))
        for THETA in Thetas:
            try:
                CANDIDATE = delay2(arr=arr,
                                    ser=ser,
                                    prob=prob, theta=THETA, delta=DELTA)
                # print(f"Theta {THETA} delay {CANDIDATE} arr {arr.rho(THETA)} ser {ser.rho(THETA)}"   )

            except ParameterOutOfBounds:
                CANDIDATE = np.inf
            
            if CANDIDATE < OPTIMUM:
                OPTIMUM = CANDIDATE
                OPT_THETA = THETA
                # print(f"OPT Theta {OPT_THETA} THETA {THETA} delay {CANDIDATE} arr {arr.rho(THETA)} ser {ser.rho(THETA)}" )
    print(OPTIMUM) 
    print(f"OPT_THETA {OPT_THETA}") 

    return OPTIMUM

def bias_s(ser:Server, epsilon, theta , delta):
    term2 = (1/theta)*(math.log(epsilon) + math.log(1-pow(math.e,-theta*delta)))
    bS=ser.sigma(theta) - term2
    return bS



def delay2(arr:Arrival, ser:Server, prob, theta , delta ):
    # delta=0.00000000001
    # probA=0
    if arr.rho(theta) >= ser.rho(theta):
        # print("arrival and service:" + str(arr.rho(theta)) + " " + str(ser.rho(theta)) )
        raise ParameterOutOfBounds("System is not stable")

    term2 = (1/theta)*(math.log(prob/2) + math.log(1-pow(math.e,-theta*delta)))
    bA=arr.sigma(theta) #- term2
    bS=bias_s(ser, prob, theta, delta)
    # if(probA==0):
    # bS=0
        # bA=arr.sigma(theta)   
    print(f"bA+bS {bA+bS} arr.sigma {arr.sigma(theta)} term2 {term2} bS {bS} ser.sigma(theta) {ser.sigma(theta)} ser.rho {ser.rho(theta)} ")
    print(f"math.log(prob/2) {math.log(prob/2)} math.log(1-pow(math.e,-theta*delta)) {math.log(1-pow(math.e,-theta*delta))}")
    delay = (bA + bS)/(ser.rho(theta) - delta)
    print(delay)
    # print(f"tau_opt {tau_opt} sigma_sum {sigma_sum} log_part {log_part}" )

    return delay



def epsilon_S(ser:Server, b_S):

    OPT_EPS = 1.0
    OPT_Delta = 0.0
    OPT_Theta = 0.0
    
    for DELTA in np.arange(0.001, 2.5, 0.1):
        Thetas=np.arange(0.000000000001, 2.0, 0.01)
        # Thetas=np.append(Thetas,np.arange(2.0,20, 1))
        for THETA in Thetas:
            eps = math.exp(THETA* ser.sigma()) / (1-math.exp(-THETA*DELTA)) * math.exp(-THETA* b_S)
            if (eps < OPT_EPS):
                OPT_EPS = eps
                OPT_Delta = DELTA
                OPT_Theta = THETA
    print(f"OPT_EPS {OPT_EPS} OPT_Theta {OPT_Theta} OPT_DELTA {OPT_Delta}")