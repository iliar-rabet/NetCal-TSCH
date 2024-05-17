#!/usr/bin/python3
from datetime import datetime
import matplotlib.pyplot as plt
from Arrival import Arrival, ExponentialDist, RateLatency
from Server import Server, ConstantRateServer, MarkovOnOff
import math
from ParameterOutOfBounds import ParameterOutOfBounds
import dvp_obj 
import file_process



if __name__ == '__main__' :
    # print(process_files("tools/cooja/A-","-1hop"))
    # print(process_files("tools/cooja/log/A/A-","-pair"))
    # print(process_files("tools/cooja/log/A/A-","-pair",T=3))
    # print(process_files("tools/cooja/log/A/A-","-pair",T=2))
    # print(process_files("tools/cooja/log/A/A-","-pair",T=1))
    # EBs=[251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397]
    
    arr=RateLatency(0.25)
    
    # UCs= [ 23, 53, 97, 199]
    # UCs= [ 23, 53]
    UCs= [ 97, 199]
    #UCs= [ 199]
    
    colors=['#d7b715', '#96d715', '#35d715', '#15d756', '#15d7b7', '#1596d7']
    BC=31
    EB=397
    dvps=[]
    # for UC in UCs:
        
    #     UC_Rate= 1 - 1/(UC*EB) - 1/(UC*BC) + 1/(BC*EB*UC)
    #     print(UC_Rate)
    #     PRR=1.0
    #     ser=MarkovOnOff(UC_Rate,PRR,100)
        
    #     DELAY_PROB = dvp_obj.opt_dvp(arr=arr, ser=ser, T=1)
    #     print(f"bound on delay's violation probability: {DELAY_PROB}")
    #     dvps.append(DELAY_PROB)

    dvp_avg_rungs=[]
    counter=0
    for i in UCs:
        # print("filename=" + "pair_EB"+str(i))
        dvp, de = file_process.process_files("../contiki-ng/tools/cooja/","pair_UC"+str(i),T=1,range=range(1,21),UC=i)
        print(dvp)
        dvp_avg_rungs.append(sum(dvp) / len(dvp) )
        print(de)
        plt.hist(de,bins=50, color=colors[counter],histtype='step',label='$L_{UC}^{SF}$='+str(i))
        plt.axvline(x=10*i, color='b', linestyle=':', linewidth=2)

        counter+=3
    plt.xlim(0,4000)
    plt.legend()
    plt.savefig("UC"+str(i)+"_Delays_pair.pdf", format="pdf", bbox_inches="tight")
    plt.show()

    # plt.ylim((0.0,0.1))
    # plt.xlabel("EB slotframe size")
    # plt.ylabel("Delay Violation Probability")
    # plt.legend()
    # plt.savefig("UC_Delays_pair.pdf", format="pdf", bbox_inches="tight")
    # plt.show()

    # for i in [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67]:
    #     print(process_files("tools/cooja/","pair_UC"+str(i),T=1,range=range(1,6))[0])