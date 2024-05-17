#!/usr/bin/python3
from datetime import datetime
import matplotlib.pyplot as plt
from Arrival import Arrival, ExponentialDist, RateLatency, Periodic
from Server import Server, ConstantRateServer, MarkovOnOff, Orchestra, MSF

import math
from ParameterOutOfBounds import ParameterOutOfBounds
from dvp_obj import *
import file_process
import numpy as np 

def hist_plot(de,colors,i,OutputNameEnding,counter,xlim,bins):
    fig, ax = plt.subplots(figsize=(4, 2.5))
    plt.hist(de,bins=bins, color=colors[counter], density=True, cumulative=1, histtype='bar',label='$L_{SF}$='+str(i*10)+"ms")
    plt.axvline(x=10*i, color='b', linestyle=':', linewidth=2)
    # Ensure labels fit within the figure
    plt.tight_layout()

    plt.xlim(0,xlim)
    plt.xlabel("delay(ms)")
    plt.ylabel("% of packets")
    plt.legend()
    plt.savefig("SF"+str(i)+OutputNameEnding, format="pdf", bbox_inches="tight")
    plt.show()

# def dot_plot(de):
#     values, counts = np.unique(de, return_counts=True)

#     fig, ax = plt.subplots(figsize=(6, 3))
#     for value, count in zip(values, counts):
#         ax.plot([value]*count, list(range(count)), c='tab:blue', marker='o',
#                 ms=10, linestyle='')
#     for spine in ['top', 'right', 'left']:
#         ax.spines[spine].set_visible(False)
#     ax.yaxis.set_visible(False)
#     ax.set_ylim(-1, max(counts))
#     ax.set_xticks(range(int(min(values)), int(max(values)+1)))
#     ax.tick_params(axis='x', length=0, pad=8, labelsize=12)
#     ax.set_title('Hours of Sleep for Students', pad=30, fontsize=14)

#     plt.show()


def iterate_files(OutputNameEnding,InputNameEnding,UCs= [ 7, 23, 53, 97, 199],r=51):
    arr=Periodic(2,1)

    colors=['#d7b715', '#96d715', '#35d715', '#15d756', '#15d7b7', '#1596d7']
    BC=31
    EB=397
    dvp_avg_rungs=[]
    counter=0
    for i in UCs:
        print(InputNameEnding + str(i))
        dvp, de = file_process.process_files("../contiki-ng/tools/cooja/",InputNameEnding+str(i),T=1,range=range(1,r),UC=i)
        print("dvp:")
        print(dvp)
        dvp_avg_rungs.append(sum(dvp) / len(dvp) )
        print("delays:")
        print(de)
        if(i>100):
            x=10000
            b=150
        else:
            x=4000
            b=100
        hist_plot(de,colors,i,OutputNameEnding,counter, xlim=x,bins=b)
        # dot_plot(de)
        counter+=1
        
def plot_model_only():
    UCs= [ 7, 23, 53, 97, 199]
    # UCs= [ 7, 23]
    scheduler="Orchestra"
    # LUC=17
    delayLS=[]
    Pon=1
    arr=Periodic(2,1)
    for LUC in UCs:    
        if scheduler == "MSF":
            ser=MSF(Pon,LUC)
        if scheduler == "Orchestra":
            ser=Orchestra(Pon, LUC, 97, 397)
        if scheduler == "no-collision":
            ser=MarkovOnOff(Pon,LUC)
        
        # ser=ConstantRateServer(1*100/LUC)
        # print(f"service {ser.rho(1.0)}")
        DELAY = opt_delay(arr, ser, prob=0.01)
        delayLS.append(DELAY*1000)

    print(delayLS)    
    plt.plot(range(1,len(delayLS)+1), delayLS )
    ticks = [x for x in UCs]
    plt.xticks(range(1,len(delayLS)+1), ticks) 
    plt.ylabel("Delay(ms)")
    plt.xlabel("UC")
    plt.legend()
    plt.show()
    # plt.savefig("Delay_Pon"+scheduler+".pdf", format="pdf", bbox_inches="tight")


if __name__ == '__main__' :
    # iterate_files("_Delays_pair_MSF.pdf", "pair-msf", UCs=[ 7, 23, 53, 97], r=5)
    # iterate_files("_Delays_pair_Custom.pdf", "pair-custom", UCs=[ 7, 23, 53, 97], r=51)
    # iterate_files("_Delays_pair_Orchestra.pdf", "pair_orchestra",UCs=[ 7, 23, 53, 97], r=51)
    plot_model_only()
