#!/usr/bin/python3
from datetime import datetime
import matplotlib.pyplot as plt
from Arrival import Poisson, Periodic
from Server import Server, ConstantRateServer, MarkovOnOff, Orchestra, MSF
import math
from ParameterOutOfBounds import ParameterOutOfBounds
from dvp_obj import *
import file_process


def box_plot(delays, Rates,scheduler="MSF"):
    print("in box plot")
    print(delays)
    print(len(delays))
    
    Pon=1
    dvpLS=[]
    delayLS=[]    
    delay2LS=[]    
    delay05LS=[]    
    LUC=17

    for interval in Rates:
        # arr=Poisson(1/interval,1)
        arr=Periodic(interval,1)
        if scheduler == "MSF":
            ser=MSF(Pon,LUC)
        if scheduler == "Orchestra":
            ser=Orchestra(Pon, LUC, 97, 397)
        if scheduler == "no-collision":
            ser=MarkovOnOff(Pon,LUC)
        # DELAY = opt_delay(arr, ser, prob=0.01)
        
        # print(f"bound on delay': {DELAY} {LUC}")
        DELAY1 = opt_delay(arr, ser, prob=0.01)
        DELAY2 = opt_delay(arr, ser, prob=0.02)
        DELAY05 = opt_delay(arr, ser, prob=0.005)
        delayLS.append(DELAY1*1000)
        delay2LS.append(DELAY2*1000)
        delay05LS.append(DELAY05*1000)

        # DVP = opt_dvp(arr, ser, T=1)
        # print(f"bound on delay's violation probability: {DVP}")
        # dvpLS.append(DVP)


    # plt.boxplot(delays, showmeans=True, whis = 99)
    plt.cla()  
    plt.rcParams["mathtext.fontset"] = "cm"
    plt.rcParams.update({'font.size': 15})
    plt.figure(figsize=(6.4,2))
    plt.violinplot(delays,positions=range(0,len(Rates)), showmeans=True, showextrema=False )

    print(delayLS)
    plt.plot(range(0,len(delayLS)), delay05LS, label=r"$\varepsilon$.=0.5%" )
    plt.plot(range(0,len(delayLS)), delayLS ,label=r"$\varepsilon$=1%")
    plt.plot(range(0,len(delayLS)), delay2LS, label=r"$\varepsilon$=2%" )

    ticks = [f"{1/x:.2f}" for x in Rates]
    plt.xticks(range(0,len(delayLS)), ticks) 
    plt.ylabel("Delay(ms)")
    plt.xlabel("Rate (pkt/s)")
    plt.ylim((0,1500))
    plt.legend(loc='upper center', 
    bbox_to_anchor=(0.5, 1.25),ncol=3)
    # plt.show()
    plt.savefig("Delay_Rate-"+scheduler+".pdf", format="pdf", bbox_inches="tight")

def iterate_files(InputNameEnding,rate,r=51):
    colors=['#d7b715', '#96d715', '#35d715', '#15d756', '#15d7b7', '#1596d7']
    dvp_avg_rungs=[]
    counter=0

    # print(InputNameEnding + str(i))
    Name="{}{}".format(InputNameEnding, rate)
    dvp, de = file_process.process_files("../contiki-ng/tools/cooja/",Name,T=1,range=range(1,r),UC=170)
    # print("dvp:")
    # print(dvp)
    dvp_avg_rungs.append(sum(dvp) / len(dvp) )
    # print("delays:")
    # print(de)    
    counter+=1
    return de

def run(name,scheduler,Rates,r):
    delays=[]
    for rate in Rates:
        customDelays=iterate_files(name, rate, r=r)
        # print(customDelays)
        delays.append(customDelays)
    box_plot(delays,Rates,scheduler)

if __name__ == '__main__' :
    Rates=[2, 1.75, 1.5, 1.25, 1, 0.75, 0.5, 0.25]
    # Pon_ls=[0.99, 0.95]
    # Pon_ls=[0.85]
    run("pair-custom_rate","no-collision",Rates,r=4)
    run("pair-msf_rate","MSF",Rates,r=4)
    run("pair-orch_rate","Orchestra",Rates,r=4)
    
    # plot_model_only()