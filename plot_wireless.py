from itertools import chain
#!/usr/bin/python3
from datetime import datetime
import matplotlib.pyplot as plt
from Arrival import Arrival, ExponentialDist, Periodic, Poisson
from Server import Server, ConstantRateServer, MarkovOnOff, Orchestra, MSF
import math
from ParameterOutOfBounds import ParameterOutOfBounds
from dvp_obj import *
import file_process



def box_plot(delays, Pon_ls,scheduler="MSF"):
    print("in box plot")
    print(delays)
    print(len(delays))
    
    dvpLS=[]
    delayLS=[]    
    delay2LS=[]    
    delay05LS=[]    
    LUC=17

    for Pon in Pon_ls:
        arr=Periodic(2,1)
        print(f"Pon{Pon}")
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

    violin_parts=plt.violinplot(delays,positions=range(0,len(Pon_ls)), showmeans=True, showextrema=False )

    # for pc in violin_parts['bodies']:
    #     pc.set_facecolor('black')
    #     pc.set_edgecolor('blue')

    plt.plot(range(0,len(delayLS)), delay05LS, label=r"$\varepsilon$.=0.5%" )
    plt.plot(range(0,len(delayLS)), delayLS ,label=r"$\varepsilon$=1%")
    plt.plot(range(0,len(delayLS)), delay2LS, label=r"$\varepsilon$=2%" )

    print(delayLS)
    ticks = [x for x in Pon_ls]
    plt.xticks(range(0,len(delayLS)), ticks) 
    plt.ylabel("Delay(ms)")
    plt.xlabel("PRR (%)")
    plt.ylim((0,3000))
    plt.legend(loc='upper center', 
    bbox_to_anchor=(0.5, 1.25),ncol=3)
    # plt.show()
    plt.savefig("Delay_PER-"+scheduler+".pdf", format="pdf", bbox_inches="tight")

def iterate_files(InputNameEnding,Pon,r=51):
    colors=['#d7b715', '#96d715', '#35d715', '#15d756', '#15d7b7', '#1596d7']
    dvp_avg_rungs=[]
    counter=0

    # print(InputNameEnding + str(i))
    Name="{}{:.2f}".format(InputNameEnding, Pon)
    # dvp, de = file_process.process_files("../contiki-ng/tools/cooja/",Name,T=1,range=chain(range(1,15),range(17,27),range(19,38)),UC=170)
    dvp, de = file_process.process_files("../contiki-ng/tools/cooja/",Name,T=1,range=range(1,r),UC=170)

    # print("dvp:")
    
    # print(dvp)
    dvp_avg_rungs.append(sum(dvp) / len(dvp) )
    # print("delays:")
    # print(de)    
    counter+=1
    return de


def plot_model_only():
    # Pon_ls=[1, 0.995, 0.98, 0.96, 0.932]
    Pon_ls=[0.85]
    scheduler="no-collision"
    LUC=7
    delayLS=[]
    delay2LS=[]
    delay05LS=[]

    for Pon in Pon_ls:
        arr=Periodic(2,100)
        # arr=Poisson(1/5,1)
        if scheduler == "MSF":
            ser=MSF(Pon,LUC)
        if scheduler == "Orchestra":
            ser=Orchestra(Pon, LUC, 97, 397)
        if scheduler == "no-collision":
            ser=MarkovOnOff(Pon,LUC)
        
        # ser=ConstantRateServer(1*100/LUC)
        print(f"service {ser.rho(1.0)}")
        DELAY = opt_delay(arr, ser, prob=0.01)
        delayLS.append(DELAY*1000)
        print("Nikolaus delay"+str(DELAY))
        print("------------")
        # DELAY = opt_delay(arr, ser, prob=0.02)
        # delay2LS.append(DELAY*1000)
        # DELAY = opt_delay(arr, ser, prob=0.005)
        # delay05LS.append(DELAY*1000)
        
        DELAY = opt_delay2(arr, ser, prob=0.01)
        delayLS.append(DELAY*1000)
        print("MGF delay"+str(DELAY))
    
    # plt.cla()  
    # plt.rcParams["mathtext.fontset"] = "cm"
    # plt.rcParams.update({'font.size': 15})
    
    # plt.plot(range(0,len(delayLS)), delay05LS, label=r"$\varepsilon$.=0.5%" )
    # plt.plot(range(0,len(delayLS)), delayLS ,label=r"$\varepsilon$=1%")
    # plt.plot(range(0,len(delayLS)), delay2LS, label=r"$\varepsilon$=2%" )

    print(delayLS)
    # ticks = [x for x in Pon_ls]
    # plt.xticks(range(1,len(delayLS)+1), ticks) 
    # plt.ylabel("Delay(ms)")
    # plt.xlabel("PER (%)")
    # plt.legend(loc='upper center', 
    # bbox_to_anchor=(0.5, 1.25),ncol=3)

    # plt.show()
    # plt.savefig("Delay_Pon"+scheduler+".pdf", format="pdf", bbox_inches="tight")

def run(name,scheduler, Pon_ls,r):
    delays=[]
    for Pon in Pon_ls:
        customDelays=iterate_files(name, Pon, r=r)
        # print(customDelays)
        delays.append(customDelays)
    box_plot(delays,[0.995, 0.98, 0.96, 0.932],scheduler)
    # box_plot(delays,[0.99, 0.95, 0.90, 0.85],scheduler)
    

if __name__ == '__main__' :
    Pon_ls=[0.99, 0.95, 0.90, 0.85]
    # Pon_ls=[0.99, 0.95]
    # Pon_ls=[0.85]
    # run("pair-custom_rloss","no-collision",Pon_ls,r=41)
    # run("pair-msf_rloss","MSF",Pon_ls,r=5)
    # run("pair-orch_rloss","Orchestra",Pon_ls,r=41)
    
    plot_model_only()